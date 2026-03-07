import hashlib

def generate_hash(data: str) -> str:
    return hashlib.sha256(data.encode()).hexdigest()

def verify_hash(data: str, stored_hash: str) -> bool:
    return generate_hash(data) == stored_hash