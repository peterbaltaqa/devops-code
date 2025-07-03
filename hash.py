from hashlib import sha256


def hash(pw):
    return sha256(pw.encode('UTF-8')).hexdigest()