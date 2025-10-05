
from sentence_transformers import SentenceTransformer
import json, numpy as np
import faiss, os

os.makedirs("embeddings", exist_ok=True)

model = SentenceTransformer("all-MiniLM-L6-v2")

with open("data/transactions.json") as f:
    transactions = json.load(f)

texts = [
    f"{t['type']} of ₹{t['amount']} on {t['date']} for {t['description']} under {t['category']} category."
    for t in transactions
]

embeddings = model.encode(texts)

dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(np.array(embeddings).astype("float32"))
faiss.write_index(index, "embeddings/vector_store.faiss")

with open("embeddings/metadata.json", "w") as f:
    json.dump(transactions, f, indent=4)

print("Embeddings and FAISS index created successfully!")
