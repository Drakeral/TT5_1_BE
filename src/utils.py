import uuid
import hashlib
import os
import random

def generate_uuid():
    return str(uuid.uuid4())

def hash_new_password(password: str):

    salt = str(random.randint(100000, 9999999))
    pw_hash = hashlib.sha256(password.encode("utf-8")).hexdigest() + salt
    
    return salt, pw_hash

def is_correct_password(salt: bytes, password: str, pw_from_db):
    pw_hash = hashlib.sha256(password.encode("utf-8")).hexdigest()  + salt
    if pw_from_db == pw_hash:
        return True
    else:
        return False

    