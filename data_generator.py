
from faker import Faker
import random, json, uuid
from datetime import datetime, timedelta

fake = Faker()

categories = ["Food", "Shopping", "Rent", "Salary", "Utilities", "Entertainment", "Travel", "Others"]

def generate_transactions(user_id, n=150):
    balance = random.randint(10000, 50000)
    transactions = []
    for _ in range(n):
        amount = random.randint(100, 5000)
        category = random.choice(categories)
        txn_type = random.choice(["Credit", "Debit"])
        if txn_type == "Debit":
            balance -= amount
        else:
            balance += amount

        transactions.append({
            "id": str(uuid.uuid4()),
            "userId": user_id,
            "date": (datetime.now() - timedelta(days=random.randint(1, 90))).strftime("%Y-%m-%d"),
            "description": fake.sentence(nb_words=4),
            "amount": amount,
            "type": txn_type,
            "category": category,
            "balance": balance
        })
    return transactions

if __name__ == "__main__":
    data = []
    for i in range(3):
        data.extend(generate_transactions(f"user_{i+1}"))
    with open("data/transactions.json", "w") as f:
        json.dump(data, f, indent=4)
    print("transactions.json generated successfully!")
