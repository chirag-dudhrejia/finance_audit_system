import hashlib

def generate_txn_hash(date, amount, description):
    raw = f"{date}-{amount}-{description}"
    return hashlib.sha256(raw.encode()).hexdigest()