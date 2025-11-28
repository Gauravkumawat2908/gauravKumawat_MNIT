Bajaj Health Datathon - AI Bill Extraction Pipeline
📖 Project Overview
This solution is an automated pipeline designed to extract structured line-item data from complex medical invoices. It solves the challenge of extracting messy, unstructured visual data into a clean JSON format while strictly avoiding double-counting and ensuring mathematical accuracy through a reconciliation layer.

🚀 Key Features
Multimodal AI Extraction: Uses Google Gemini 1.5 Pro to visually analyze document layout, ensuring columns (Rate, Quantity, Amount) are correctly identified even in distorted images.
Double-Counting Prevention: Advanced prompt engineering explicitly filters out summary rows (e.g., "Subtotal", "Tax", "Grand Total") to capture only transaction line items.
Mathematical Reconciliation: The API does not simply read the total from the page. Instead, it recalculates the sum of all extracted line items (reconciled_amount). This provides a validation layer—if the AI's math matches the bill's total, confidence is high.
Robust Error Handling: Automatic fallback logic handles API timeouts or model availability issues.
🛠️ Tech Stack
Language: Python 3.9+
Framework: FastAPI (High-performance, async)
Server: Uvicorn
AI Engine: Google Gemini 1.5 Pro (via google-generativeai SDK)
Deployment: Render (Cloud Hosting)
🔗 Live API Endpoint
The solution is deployed and live. You can test it using the endpoint below:

Base URL: https://<YOUR-RENDER-APP-NAME>.onrender.com Method: POST Endpoint: /extract-bill-data

📝 API Documentation
Request Format
Send a POST request with the URL of the bill image.

{
  "document": "[https://hackrx.blob.core.windows.net/assets/datathon-IIT/sample_2.png](https://hackrx.blob.core.windows.net/assets/datathon-IIT/sample_2.png)?..."
}
Response Format
The API returns a structured JSON matching the Datathon schema.

{
  "is_success": true,
  "data": {
    "pagewise_line_items": [
      {
        "page_no": "1",
        "bill_items": [
          {
            "item_name": "Livi 300mg Tab",
            "item_amount": 448.0,
            "item_rate": 32.0,
            "item_quantity": 14.0
          }
        ]
      }
    ],
    "total_item_count": 1,
    "reconciled_amount": 448.0
  }
}
reconciled_amount: This is the calculated sum of all extracted item_amount fields. It serves as a ground-truth check for the extraction accuracy.
💻 Local Setup & Installation
If you wish to run this pipeline locally, follow these steps:

1. Clone the Repository
git clone <your-repo-link>
cd <folder-name>
2. Install Dependencies
pip install -r requirements.txt
3. Configure Environment
Create a .env file in the root directory and add your Google Gemini API key:

GEMINI_API_KEY=AIzaSy...YourKeyHere
4. Run the Server
python main.py
The server will start at http://0.0.0.0:8000.

📂 Project Structure
├── main.py              # The core FastAPI application & AI logic
├── requirements.txt     # Python dependencies
├── render.yaml          # Configuration for Cloud Deployment
├── test_api.py          # Script to test the API locally
├── test_cloud.py        # Script to test the deployed API
├── .env                 # API Keys (Not uploaded to GitHub)
└── README.md            # Documentation
✅ Evaluation Criteria Checklist
[x] Accuracy: High-precision extraction using the "Pro" vision model.
[x] Reconciliation: Implemented Python-side summation logic.
[x] Double-Counting: Filtered via strict System Prompt instructions.
[x] Deployment: Successfully hosted on Render with a public endpoint.
