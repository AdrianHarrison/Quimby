"""
seed.py

Seeding tools to randomize user input into viable key fields.
"""

class Seeder():

    def seed_fernet_key(self, seed: str, indexing: int) -> bytes:
        return ""

    def seed_scrypt_key(self, seed: str, indexing: int) -> bytes:
        return ""

    def fetch_fernet_key(self) -> bytes:
        return ""

    def fetch_scrypt_key(self) -> bytes:
        return ""