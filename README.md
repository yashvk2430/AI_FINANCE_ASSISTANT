
# AI-Powered Financial Data Assistant

This project builds an AI-powered assistant to **query and analyze financial transactions** using semantic search and embeddings.

---

## Features
- AI-generated dummy transaction data
- Embeddings using Sentence Transformers (`all-MiniLM-L6-v2`)
- FAISS vector database for similarity search
- REST API for natural language queries
- Example: “Show my top 5 food expenses in September”

---

##  Folder Structure
```
financial-data-assistant/
├── data/transactions.json
├── embeddings/vector_store.faiss
├── api/app.py
├── services/data_generator.py
├── services/embedding_service.py
└── README.md
```

---

##  Setup & Run

###  Install Dependencies
```bash
pip install flask faker sentence-transformers faiss-cpu numpy
```

###  Generate Data
```bash
python services/data_generator.py
```

###  Create Embeddings
```bash
python services/embedding_service.py
```

###  Run API
```bash
python api/app.py
```

---

##  Example Query
POST → `/search`  
```json
{ "query": "Show my top 5 food expenses in September" }
```

Response:
```json
[
  {"description": "UPI payment to Swiggy", "amount": 520, "category": "Food"},
  {"description": "Zomato order", "amount": 450, "category": "Food"}
]
```
### Example Query (Summary Report)
POST → `/search_report`
```json
{ "query": "Show my travel expenses last month", "top_n": 5 }
```
Response:
```json
[
{
  "transactions": [...],
  "report": "You spent ₹8,750 mostly on Travel and Food."
}
]
```


---

##  Optional Enhancements
- Add LLM summarizer (GPT-4/Llama-3)
- Add charts for category expenses
- Add date filters (e.g., “last 3 months”)

---

 Created for the **AI Financial Assistant Assignment**
