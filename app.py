from flask import Flask, request, jsonify
from sentence_transformers import SentenceTransformer
import faiss, numpy as np, json, os

app = Flask(__name__)
# Load model
print("Loading AI model and vector index...")
model = SentenceTransformer("all-MiniLM-L6-v2")

if not os.path.exists("embeddings/vector_store.faiss"):
    raise FileNotFoundError("vector_store.faiss not found. Run embedding_service.py first.")

index = faiss.read_index("embeddings/vector_store.faiss")

with open("embeddings/metadata.json") as f:
    transactions = json.load(f)

print("Model and data loaded successfully!")


#Default route
@app.route("/")
def home():
    return "AI Financial Assistant API is running! Use /search (POST) to query data."


#POST route for searching transactions
@app.route("/search", methods=["POST"])
def search():
    try:
        data = request.get_json(force=True)
        query = data.get("query", "")
        if not query:
            return jsonify({"error": "Please provide a 'query' in JSON body"}), 400
        query_vec = model.encode([query])
        D, I = index.search(np.array(query_vec).astype("float32"), k=5)
        results = [transactions[i] for i in I[0]]
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
#POST route for search and  summrize report
@app.route("/search_report", methods=["POST"])
def search_report():
    try:
        data = request.get_json(force=True)
        query = data.get("query", "")
        top_n = data.get("top_n", 5)  # optional, default top 5
        if not query:
            return jsonify({"error": "Please provide a 'query' in JSON body"}), 400
        query_vec = model.encode([query])
        D, I = index.search(np.array(query_vec).astype("float32"), k=top_n)
        results = [transactions[i] for i in I[0]]

        report_lines = []
        for t in results:
            report_lines.append(f"- {t['description']} – ₹{t['amount']} – {t['date']}")

        category_summary = {}
        total_expense = 0
        for t in results:
            if t["type"].lower() == "debit":
                total_expense += t["amount"]
                category_summary[t["category"]] = category_summary.get(t["category"], 0) + t["amount"]

        sorted_categories = sorted(category_summary.items(), key=lambda x: x[1], reverse=True)
        top_categories = ", ".join([cat for cat, amt in sorted_categories])

        summary_text = f"Most on {top_categories}, totaling ₹{total_expense}."

        final_report = "\n".join(report_lines) + "\n" + summary_text

        response = {
            "transactions": results,
            "report": final_report
        }

        return jsonify(response)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
