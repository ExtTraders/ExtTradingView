from utils.encryption import SimpleEnDecrypt

class showEncryptAccessKey:
    def __init__(self):
        self.encrypt = None
        self.encrypt_access_key = None
        self.encrypt_secret_key = None
        

    def encryptCode(self, access_key: str, secret_key: str, encryption_key: str):
        self.encrypt = SimpleEnDecrypt(encryption_key)
        encrypt_access_key = self.encrypt.encrypt(access_key)
        encrypt_secret_key = self.encrypt.encrypt(secret_key)
        print(f"Encrypted Access Key: {encrypt_access_key}")
        print(f"Encrypted Secret Key: {encrypt_secret_key}")
        return encrypt_access_key, encrypt_secret_key


    def decrypt(self):
        # Placeholder for decryption logic
        return f"Decrypted({self.access_key})"