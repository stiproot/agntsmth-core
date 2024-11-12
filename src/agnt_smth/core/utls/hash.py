import hashlib

def generate_sha256(content: str) -> str:
    sha256_hash = hashlib.sha256()
    sha256_hash.update(content.encode('utf-8'))
    return sha256_hash.hexdigest()
