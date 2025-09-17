from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 비밀번호 암호화
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

if __name__ == "__main__":
    print(get_password_hash("1234"))
