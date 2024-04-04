import os
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes

def load_public_key():
    # Adjust the path to your id_rsa.pub file as necessary
    public_key_path = os.path.expanduser('~/.ssh/id_rsa.pub')

    with open(public_key_path, 'rb') as key_file:
        public_key = serialization.load_ssh_public_key(
            key_file.read(),
            backend=default_backend()
        )

    return public_key

def encrypt_and_save(message, public_key, filename):
    encrypted = public_key.encrypt(
        message.encode(),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    dir_path = os.path.dirname(os.path.realpath(__file__))  # Gets the directory where the script is located
    secret_file_path = os.path.join(dir_path, '.openai_secret')
    # Write the encrypted message to .gptsecret
    with open(secret_file_path, 'wb') as secret_file:
        secret_file.write(encrypted)

def encrypt_externally(message, file_name):
    pub = load_public_key()
    encrypt_and_save(message, pub, file_name)

def main():
    public_key = load_public_key()

    # Read a line of text from the console
    text_to_encrypt = input("Enter the text to encrypt: ")
    print('\n')
    file_name = input("Enter the name of the file to encrypt to (Ex: .openai_secret): ")
    # Encrypt the text and write it to .gptsecret
    encrypt_and_save(text_to_encrypt, public_key, file_name)
    print("The text has been encrypted and saved to " + file_name)

if __name__ == "__main__":
    main()
