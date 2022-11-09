import rsa
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes


def load_private_key(user_name, user_password):
    try:
        f = open("myPrivateKey/" + user_name + ".pem", "rb")
        private_key = serialization.load_pem_private_key(
            f.read(),
            password=user_password.encode("utf-8")
        )
        return private_key
    except ValueError as e:
        print("Bad password")
        return None


def sign_message(message, private_key):
    signature = private_key.sign(
        message,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    return signature


def create_new_key(user_name, user_password):
    # print(user_password)
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )
    pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.BestAvailableEncryption(user_password.encode("utf-8"))
    )

    f = open("myPrivateKey/" + user_name + ".pem", "wb")
    f.write(pem)
    f.close()
    public_key = private_key.public_key()
    pub_key_bytes = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.PKCS1,
    )
    f = open("pubkeys/" + user_name, "wb")
    f.write(pub_key_bytes)
    f.close()
    return private_key
