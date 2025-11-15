import socket
import sys
import os
from dotenv import load_dotenv
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes

try:
    from DES_Chat import des_encrypt, des_decrypt, bits_to_hex, hex_to_bits
except ImportError:
    print("Error: DES_Chat.py not found.")
    sys.exit(1)

try:
    load_dotenv()
except ModuleNotFoundError:
    print("Error: 'dotenv' module not found.")
    sys.exit(1)
except FileNotFoundError:
    print("Error: .env file not found.")
    sys.exit(1)


LHOST = os.getenv("LHOST")
RHOST = os.getenv("RHOST")
PORT = int(os.getenv("PORT", 8080))

def get_key():
    key = ""
    while len(key) != 8:
        key = input("Enter your 8-character secret key: ")
        if len(key) != 8:
            print("Error: The key must be exactly 8 characters long. Please try again.")
    return key

def sender_mode():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(10) # Increased timeout for key exchange
            print(f"Attempting to connect to {RHOST}:{PORT}...")
            s.connect((RHOST, PORT))
            print("Connection successful!")
            s.settimeout(None)

            # 1. Receive the receiver's public key
            print("Receiving public key from receiver...")
            public_pem = s.recv(4096) # Adjust buffer size
            if not public_pem:
                print("Receiver disconnected before sending public key.")
                return

            # 2. Load the public key
            public_key = serialization.load_pem_public_key(public_pem)
            print("Public key received.")

            # 3. Generate a random 8-byte (64-bit) DES key
            des_key_bytes = os.urandom(8)
            
            # The DES key must be a string for your existing code
            # We use 'latin-1' to map bytes 0-255 directly to a string
            key = des_key_bytes.decode('latin-1')
            print("Generated random 8-byte DES key.")

            # 4. Encrypt the DES key with the public key
            print("Encrypting DES key for secure transport...")
            encrypted_des_key = public_key.encrypt(
                des_key_bytes,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )

            # 5. Send the encrypted DES key to the receiver
            s.sendall(encrypted_des_key)
            print("Secure DES key sent.")

            # 6. Now, proceed with the original chat logic
            print("======================================================")
            plaintext = input("Enter message: ")
            print("======================================================")
            
            # Use the new, randomly generated key!
            encrypted_bits = des_encrypt(plaintext, key) 
            encrypted_hex = bits_to_hex(encrypted_bits)

            print("======================================================")
            print(f"Encrypted message (hex): {encrypted_hex}")
            print("======================================================")
            
            s.sendall(encrypted_hex.encode('utf-8'))
            print("Message sent. Disconnecting.")

    except socket.timeout:
        print(f"Error: Connection timed out. Is the receiver listening on {RHOST}:{PORT}?")
    except ConnectionRefusedError:
        print(f"Error: Connection refused. Is the receiver running on {RHOST}:{PORT}?")
    except Exception as e:
        print(f"An error occurred in sender mode: {e}")
    finally:
        print("Returning to menu...\n")

def receiver_mode(): # No longer needs 'key' as an argument
    try:
        # 1. Generate RSA private and public keys
        print("Generating RSA key pair (this may take a moment)...")
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
        )
        public_key = private_key.public_key()

        # 2. Serialize the public key to send it
        public_pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((LHOST, PORT))
            s.listen()
            print(f"Server is listening on {LHOST}:{PORT}...")
            print("Waiting for a connection...")
            
            conn, addr = s.accept()
            
            with conn:
                print(f"Connected by {addr}")

                # 3. Send the public key to the sender
                print("Sending public key to sender...")
                conn.sendall(public_pem)

                # 4. Receive the encrypted DES key from the sender
                print("Waiting for encrypted DES key...")
                encrypted_des_key = conn.recv(1024) # Adjust buffer size if needed
                if not encrypted_des_key:
                    print("Sender disconnected before sending DES key.")
                    return

                # 5. Decrypt the DES key with the private key
                print("Decrypting DES key...")
                des_key_bytes = private_key.decrypt(
                    encrypted_des_key,
                    padding.OAEP(
                        mgf=padding.MGF1(algorithm=hashes.SHA256()),
                        algorithm=hashes.SHA256(),
                        label=None
                    )
                )
                
                # The DES key must be a string for your existing code
                # We use 'latin-1' to map bytes 0-255 directly to a string
                key = des_key_bytes.decode('latin-1') 
                print("Secure DES key established.")

                # 6. Proceed to receive the actual message
                print("Waiting for one message...")
                data = conn.recv(4096)
                if data:
                    encrypted_hex = data.decode('utf-8').strip()
                    print("======================================================")
                    print(f"Encrypted message (hex) received: {encrypted_hex}")
                    
                    try:
                        encrypted_bits = hex_to_bits(encrypted_hex)
                        # Use the new, securely received key!
                        decrypted_text = des_decrypt(encrypted_bits, key) 
                        print(f"Received message: {decrypted_text}")
                    except Exception as e:
                        print(f"--- Error decrypting message ---")
                        print(f"Error: {e}. Key exchange might have failed.")
                        print(f"Raw data received: {encrypted_hex}")
                        print(f"---------------------------------")
                    print("======================================================")
                else:
                    print("Client disconnected before sending data.")

            print("Message received. Closing connection.")

    except OSError as e:
        if e.errno == 98: 
            print(f"Error: Address {LHOST}:{PORT} is already in use.")
            print("This usually means another process (or your partner) is already listening.")
        else:
            print(f"An error occurred in receiver mode: {e}")
    except Exception as e:
        print(f"An error occurred in receiver mode: {e}")
    finally:
        print("Returning to menu...\n")


def main():    
    # key = get_key()
    
    while True:
        print("Choose your role for this turn:")
        print("1. Sender (Send one message)")
        print("2. Receiver (Receive one message)")
        print("3. Quit")
        
        choice = input("Enter choice (1, 2, or 3): ")
            
        if choice == '1':
            print("\nStarting in Sender mode...")
            sender_mode()
        elif choice == '2':
            print("\nStarting in Receiver mode...")
            receiver_mode()
        elif choice == '3':
            print("Exiting chat. Goodbye!")
            break 
        else:
            print("Invalid input. Please enter 1, 2, or 3.\n")

if __name__ == "__main__":
    main()

