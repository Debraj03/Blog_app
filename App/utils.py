from passlib.context import CryptContext

context=CryptContext(schemes=['bcrypt'],deprecated="auto")

def hash_password(password:str):
    hashed_password=context.hash(password)
    return hashed_password

def check_password(passwod:str,hashed_password:str):
    state=context.verify(passwod,hashed_password)
    return state