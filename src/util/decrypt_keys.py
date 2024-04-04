import os
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes

def load_private_key():
    # Adjust the path to your id_rsa file as necessary
    private_key_path = os.path.expanduser('~/.ssh/id_rsa')

    with open(private_key_path, 'rb') as key_file:
        # If your private key is encrypted, add the password argument to load_pem_private_key
        # e.g., password=b'my_passphrase'
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=None,  # Change this if your key is password-protected
            backend=default_backend()
        )

    return private_key

def decrypt_message(private_key, file_name):
    # Read the encrypted message from .gptsecret
    dir_path = os.path.dirname(os.path.realpath(__file__))  # Gets the directory where the script is located
    secret_file_path = os.path.join(dir_path, file_name)
    with open(secret_file_path, 'rb') as secret_file:
        encrypted_message = secret_file.read()

    # Decrypt the message
    decrypted = private_key.decrypt(
        encrypted_message,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    return decrypted.decode()

def decrypt_externally(file_name):
    private_key = load_private_key()
    return decrypt_message(private_key, file_name)

def main():
    private_key = load_private_key()
    file_name = input("Enter the name of the file to decrypt (Ex: .openai_secret): ")
    decrypted_message = decrypt_message(private_key, file_name)
    print("Decrypted message:", decrypted_message)

if __name__ == "__main__":
    main()
