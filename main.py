import os
import uvicorn
import requests
import json
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional
import google.generativeai as genai
from dotenv import load_dotenv
from PIL import Image
from io import BytesIO

# Load environment variables
load_dotenv()

# Configure Gemini
# NOTE: You need a generic Google AI Studio Key.
# Set this in your environment or .env file as GEMINI_API_KEY
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

app = FastAPI(title="Bajaj Health Datathon - Bill Extractor")

# --- ADD THIS NEW ROUTE ---
@app.get("/")
def home():
    return {"message": "Bajaj Health API is Live!", "status": "Running"}
# ---------------------------
# --- Pydantic Models for Input/Output ---

class DocumentRequest(BaseModel):
    document: str = Field(..., description="URL of the bill image/PDF")

class BillItem(BaseModel):
    item_name: str
    item_amount: float
    item_rate: Optional[float] = 0.0
    item_quantity: Optional[float] = 1.0

class PageLineItems(BaseModel):
    page_no: str
    bill_items: List[BillItem]

class ExtractionData(BaseModel):
    pagewise_line_items: List[PageLineItems]
    total_item_count: int
    reconciled_amount: float

class APIResponse(BaseModel):
    is_success: bool
    data: Optional[ExtractionData] = None
    error: Optional[str] = None

# --- Helper Functions ---

def download_image(url: str):
    """Downloads image from URL and converts to PIL Image."""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        image_data = BytesIO(response.content)
        img = Image.open(image_data)
        return img
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to download image: {str(e)}")

def get_gemini_extraction(image):
    """Sends image to Gemini 1.5 Flash for structured extraction."""
    
    # We use Gemini 1.5 Flash for speed and efficiency
    model = genai.GenerativeModel('gemini-2.5-pro')

    # Strict prompt to force specific JSON structure and handling logic
    prompt = """
    You are an expert OCR and financial data extraction system. 
    Analyze the provided invoice image.
    
    Your goal is to extract line items accurately.
    
    RULES:
    1. Extract the 'item_name', 'item_amount' (total for that line), 'item_rate' (unit price), and 'item_quantity'.
    2. If quantity is missing, assume 1. If rate is missing, infer it from amount/quantity.
    3. IMPORTANT: Do NOT include lines that are 'Subtotal', 'Tax', 'GST', 'Discount', or 'Grand Total' in the line items list. Only extract actual products or services.
    4. Ignore page numbers or footer text.
    5. Return the data in valid JSON format matching this structure exactly:
    
    {
      "pagewise_line_items": [
        {
          "page_no": "1",
          "bill_items": [
             { "item_name": "string", "item_amount": float, "item_rate": float, "item_quantity": float }
          ]
        }
      ]
    }
    """

    try:
        # Set response_mime_type to json for deterministic output
        response = model.generate_content(
            [prompt, image],
            generation_config=genai.GenerationConfig(
                response_mime_type="application/json",
                temperature=0.1 # Low temp for factual accuracy
            )
        )
        return json.loads(response.text)
    except Exception as e:
        print(f"LLM Error: {e}")
        raise HTTPException(status_code=500, detail="Failed to process image with AI model.")

# --- API Endpoints ---

@app.post("/extract-bill-data", response_model=APIResponse)
async def extract_bill_data(request: DocumentRequest):
    """
    Main endpoint to process bill URL and return structured data.
    """
    try:
        # 1. Download Image
        image = download_image(request.document)
        
        # 2. Extract Data using LLM
        raw_data = get_gemini_extraction(image)
        
        # 3. Post-Processing & Reconciliation Logic
        # We define reconciliation as: The sum of all individual extracted line items.
        # This ensures the 'Total' isn't just OCR'd from the bottom (which might be wrong),
        # but is mathematically derived from the extracted components.
        
        all_items = []
        pagewise_items = []
        
        # Parse LLM response into our Pydantic structure
        for page in raw_data.get("pagewise_line_items", []):
            p_items = []
            for item in page.get("bill_items", []):
                # Sanitize data
                validated_item = BillItem(
                    item_name=item.get("item_name", "Unknown"),
                    item_amount=float(item.get("item_amount", 0)),
                    item_rate=float(item.get("item_rate", 0)),
                    item_quantity=float(item.get("item_quantity", 1))
                )
                p_items.append(validated_item)
                all_items.append(validated_item)
            
            pagewise_items.append(PageLineItems(
                page_no=str(page.get("page_no", "1")),
                bill_items=p_items
            ))

        # Calculate Totals
        total_count = len(all_items)
        
        # Mathematical Reconciliation: Sum of all item amounts
        calculated_total = sum(item.item_amount for item in all_items)
        
        # Round to 2 decimal places
        calculated_total = round(calculated_total, 2)

        # 4. Construct Final Response
        response_data = ExtractionData(
            pagewise_line_items=pagewise_items,
            total_item_count=total_count,
            reconciled_amount=calculated_total
        )

        return APIResponse(is_success=True, data=response_data)

    except HTTPException as he:
        return APIResponse(is_success=False, error=he.detail)
    except Exception as e:
        return APIResponse(is_success=False, error=str(e))

if __name__ == "__main__":

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
