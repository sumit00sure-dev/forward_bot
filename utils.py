import hashlib

def file_hash(file):
    return hashlib.md5(file).hexdigest()

def rename_file(name):
    return f"Professor_{name}"