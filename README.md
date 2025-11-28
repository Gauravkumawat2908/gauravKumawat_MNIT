# 📖 Bajaj Health Datathon – AI Bill Extraction Pipeline

## 🧩 Project Overview
This project implements an **automated AI-powered pipeline** that extracts **structured line-item data** from complex medical invoices.  
It converts messy, unstructured visual data into **clean JSON outputs** while ensuring:

- Zero double-counting  
- Column-wise accuracy  
- Mathematical consistency through reconciliation

---

## 🚀 Key Features

### 🔍 **Multimodal AI Extraction**
- Uses **Google Gemini 1.5 Pro** to analyze bill layouts.
- Correctly detects columns like **Rate, Quantity, Amount** even in distorted or blurry images.

### ➗ **Double-Counting Prevention**
- Smart prompt engineering filters out summary rows:  
  **Subtotal, Discount, Tax, Grand Total**, etc.

### ✔️ **Mathematical Reconciliation**
- The pipeline **recalculates** the final amount instead of trusting the printed total.
- Returns `reconciled_amount` (sum of all extracted line items).

### 🛡️ **Robust Error Handling**
- Automatic fallback logic for API timeouts or model unavailability.

---

## 🛠️ Tech Stack

| Component | Technology |
|----------|------------|
| **Language** | Python 3.9+ |
| **Framework** | FastAPI |
| **Server** | Uvicorn |
| **AI Engine** | Google Gemini 1.5 Pro |
| **Deployment** | Render Cloud Hosting |

---

## 🔗 Live API Endpoint

The API is deployed and live.

Base URL: https://gaurav-kumawat-mnit.vercel.app/
Method: POST
Endpoint: /extract-bill-data


---

## 📝 API Documentation

### 📤 **Request Format**
Send a POST request with the bill image URL:

```json
{
  "document": "https://hackrx.blob.core.windows.net/assets/datathon-IIT/sample_2.png?..."
}

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
```

reconciled_amount = Sum of all extracted item amounts.

---

## 💻 Local Setup & Installation
# 1️⃣ Clone the Repository

``` bash
git clone https://github.com/Gauravkumawat2908/gauravKumawat_MNIT
```
---

# 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```
---

# 3️⃣ Configure Your Environment

Create a .env file:

``` ini
GEMINI_API_KEY=AIzaSy...YourKeyHere
```
# 4️⃣ Run the Server

```bash
python main.py
```
# 📂 Project Structure

``` bash

├── main.py            # FastAPI application + AI extraction logic
├── requirements.txt   # Python dependencies
├── render.yaml        # Render cloud deployment config
├── test_api.py        # Local API testing
├── test_cloud.py      # Tests for deployed endpoint
├── .env               # Env variables (ignored in Git)
└── README.md          # Documentation
```


