def install_libraries():
    print("Some or all of the required libraries are missing.")
    print("Please run 'python3 install.py' to install the necessary packages.")
    exit(1)

try:
    import rsa
    import pyfiglet
    from rich import print
    from termcolor import colored
    from OpenSSL import crypto
    import os 

    
except ImportError as e:
    install_libraries()

def generate_keys(bits, private_key_name, public_key_name):
    if bits < 2048:
        print("Warning: RSA key sizes below 2048 bits are not secure.")
        print("It is highly recommended to use at least 2048 bits.")
        response = input("Do you want to continue? (yes/no): ").lower()
        if response != 'yes':
            print("Key generation aborted.")
            return

    public_key, private_key = rsa.newkeys(bits)

    with open(f"{public_key_name}.pem", "wb") as public_file:
        public_file.write(public_key.save_pkcs1())

    with open(f"{private_key_name}.pem", "wb") as private_file:
        private_file.write(private_key.save_pkcs1())

    print("Keys generated successfully!")

def create_certificate(private_key_name, public_key_name, cert_filename):
    # Check if private key file exists
    private_key_path = f"{private_key_name}.pem"
    if not os.path.exists(private_key_path):
        print(f"Error: Private key file '{private_key_path}' not found.")
        return

    # Check if public key file exists
    public_key_path = f"{public_key_name}.pem"
    if not os.path.exists(public_key_path):
        print(f"Error: Public key file '{public_key_path}' not found.")
        return

    private_key = crypto.load_privatekey(crypto.FILETYPE_PEM, open(private_key_path).read())
    public_key = crypto.load_publickey(crypto.FILETYPE_PEM, open(public_key_path).read())

    cert = crypto.X509()
    cert.set_serial_number(1000)
    cert.gmtime_adj_notBefore(0)
    cert.gmtime_adj_notAfter(365 * 24 * 60 * 60)  # Valid for one year

    # Set issuer and subject based on the names of private and public keys
    issuer = crypto.X509Name()
    issuer.CN = private_key_name
    cert.set_issuer(issuer)

    subject = crypto.X509Name()
    subject.CN = public_key_name
    cert.set_subject(subject)

    cert.set_pubkey(public_key)
    cert.sign(private_key, 'sha256')

    with open(f"{cert_filename}.pem", "wb") as cert_file:
        cert_file.write(crypto.dump_certificate(crypto.FILETYPE_PEM, cert))

    print("Certificate created successfully!")


def encrypt(message, public_key):
    ciphertext = rsa.encrypt(message.encode(), public_key)
    return ciphertext

def decrypt(ciphertext, private_key):
    plaintext = rsa.decrypt(ciphertext, private_key).decode()
    return plaintext

def main():
    title = pyfiglet.figlet_format('RSAKEYGEN')
    print(f'[magenta]{title}[/magenta]')
    print("=======================_By pootinx_=======================")

    while True:
        print("\n[1] Generate keys (private and public)")
        print("[2] Encrypt")
        print("[3] Decrypt")
        print("[4] Create Certificate")
        print("[5] Exit")

        choice = input("Choose an option: ")

        if choice == '1':
            bits = int(input("Enter the number of bits for the key: "))
            private_key_name = input("Enter the name for the private key file: ")
            public_key_name = input("Enter the name for the public key file: ")
            generate_keys(bits, private_key_name, public_key_name)
            print("Keys generated successfully!")

        elif choice == '2':
            public_key_path = input("Enter the path to the public key file: ")
            message = input("Enter the message to encrypt: ")

            with open(public_key_path, "rb") as public_file:
                public_key = rsa.PublicKey.load_pkcs1(public_file.read())

            ciphertext = encrypt(message, public_key)
            print("Encrypted message:", ciphertext.hex())

        elif choice == '3':
            private_key_path = input("Enter the path to the private key file: ")
            ciphertext_hex = input("Enter the encrypted message in hexadecimal format: ")

            with open(private_key_path, "rb") as private_file:
                private_key = rsa.PrivateKey.load_pkcs1(private_file.read())

            ciphertext = bytes.fromhex(ciphertext_hex)
            plaintext = decrypt(ciphertext, private_key)
            print("Decrypted message:", plaintext)

        elif choice == '4':
            private_key_name = input("Enter the name of the private key file: ")
            public_key_name = input("Enter the name of the public key file: ")
            cert_filename = input("Enter the name for the certificate file: ")
            create_certificate(private_key_name, public_key_name, cert_filename)
            print("Certificate created successfully!")

        elif choice == '5':
            break

        else:
            print("Invalid choice. Please choose a valid option.")

if __name__ == "__main__":
    main()

