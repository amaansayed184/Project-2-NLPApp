"""Local accounts with salted password hashes and legacy migration."""
import hashlib
import hmac
import json
import os
from pathlib import Path
import re
import tempfile


class Database:
    def __init__(self, path=None):
        self.path = Path(path) if path else Path(__file__).resolve().parent / "db.json"

    def _read(self):
        if not self.path.exists():
            return {}
        try:
            data = json.loads(self.path.read_text(encoding="utf-8"))
            if not isinstance(data, dict):
                raise ValueError("Invalid account database.")
            return data
        except (json.JSONDecodeError, UnicodeDecodeError) as exc:
            raise ValueError("The account database is damaged. Restore db.json from a backup.") from exc

    def _write(self, data):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        handle, name = tempfile.mkstemp(dir=self.path.parent, prefix=".accounts-", suffix=".tmp")
        try:
            with os.fdopen(handle, "w", encoding="utf-8") as stream:
                json.dump(data, stream, indent=2)
            os.replace(name, self.path)
        finally:
            if os.path.exists(name):
                os.unlink(name)

    @staticmethod
    def _record(name, password):
        salt = os.urandom(16).hex()
        digest = hashlib.pbkdf2_hmac("sha256", password.encode(), bytes.fromhex(salt), 600000).hex()
        return {"name": name, "salt": salt, "password_hash": digest, "iterations": 600000}

    def migrate_legacy(self):
        data = self._read()
        changed = False
        for email, record in list(data.items()):
            if isinstance(record, list) and len(record) == 2:
                data[email] = self._record(record[0], record[1])
                changed = True
        if changed:
            self._write(data)

    def add_data(self, name, email, password):
        name, email = name.strip(), email.strip().casefold()
        if not name or not re.fullmatch(r"[^\s@]+@[^\s@]+\.[^\s@]+", email):
            raise ValueError("Enter your name and a valid email address.")
        if len(password) < 8:
            raise ValueError("Use a password with at least 8 characters.")
        data = self._read()
        if any(key.casefold() == email for key in data):
            return False
        data[email] = self._record(name, password)
        self._write(data)
        return True

    def search(self, email, password):
        self.migrate_legacy()
        email = email.strip().casefold()
        record = next((v for k, v in self._read().items() if k.casefold() == email), None)
        if not record:
            return False
        digest = hashlib.pbkdf2_hmac("sha256", password.encode(), bytes.fromhex(record["salt"]), record["iterations"]).hex()
        return hmac.compare_digest(record["password_hash"], digest)
