import socket
import sys
import os
from dotenv import load_dotenv

from DES_Chat import des_encrypt, des_decrypt, bits_to_hex, hex_to_bits

load_dotenv()
LHOST = os.getenv("LHOST")
RHOST = os.getenv("RHOST")
PORT = int(os.getenv("PORT", 8080))

def get_key():
    """Prompts user for a valid 8-character DES key."""
    key = ""
    while len(key) != 8:
        key = input("Enter your 8-character secret key: ")
        if len(key) != 8:
            print("Error: The key must be exactly 8 characters long. Please try again.")
    return key

def sender_mode(key):
    """Runs the client (sender) side of the chat."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            print(f"Attempting to connect to {RHOST}:{PORT}...")
            s.connect((RHOST, PORT))
            print("Connection successful! Type 'exit' to quit.")
            
            while True:
                plaintext = input("Enter message: ")
                if plaintext.lower() == 'exit':
                    break
                
                # Encrypt the message
                encrypted_bits = des_encrypt(plaintext, key)
                encrypted_hex = bits_to_hex(encrypted_bits)
                
                # Send the encrypted hex string, encoded as bytes
                s.sendall(encrypted_hex.encode('utf-8'))
                
    except ConnectionRefusedError:
        print(f"Error: Connection refused. Is the receiver running on {RHOST}:{PORT}?")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        print("Sender shutting down.")

def receiver_mode(key):
    """Runs the server (receiver) side of the chat."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # This allows you to re-run the server quickly
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        s.bind((LHOST, PORT))
        s.listen()
        print(f"Server is listening on {LHOST}:{PORT}...")
        
        # Wait for a connection
        conn, addr = s.accept()
        
        with conn:
            print(f"Connected by {addr}")
            print("Waiting for messages...")
            
            while True:
                # Receive data from the sender (up to 4096 bytes)
                data = conn.recv(4096)
                if not data:
                    # If data is empty, the client has disconnected
                    print("Client disconnected.")
                    break
                
                # Decode the bytes back into a hex string
                encrypted_hex = data.decode('utf-8')
                
                # Convert hex to bits, then decrypt
                try:
                    encrypted_bits = hex_to_bits(encrypted_hex)
                    decrypted_text = des_decrypt(encrypted_bits, key)
                    print(f"Received message: {decrypted_text}")
                except Exception as e:
                    print(f"Error decrypting message: {e}. Was the key correct?")
                    print(f"Raw data received: {encrypted_hex}")

    print("Receiver shutting down.")

def main():
    print("Choose mode: sender or receiver")
    print("1. Sender \n2. Receiver")
    mode=int(input("Enter choice (1 or 2): "))
    if mode==1:
        mode = 'sender'
    elif mode==2:
        mode = 'receiver'
    else:
        print("Invalid choice. Exiting.")
        sys.exit(1)

    key = get_key()
    
    if mode == 'sender':
        sender_mode(key)
    elif mode == 'receiver':
        receiver_mode(key)

if __name__ == "__main__":
    main()
