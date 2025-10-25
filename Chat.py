import socket
import sys
import os
from dotenv import load_dotenv

try:
    from DES_Chat import des_encrypt, des_decrypt, bits_to_hex, hex_to_bits
except ImportError:
    print("Error: DES.py not found.")
    print("Please make sure DES.py is in the same directory as Chat.py")
    sys.exit(1)

try:
    load_dotenv()
except ModuleNotFoundError:
    print("Error: 'dotenv' module not found.")
    print("Please install it by running: pip install python-dotenv")
    sys.exit(1)
except FileNotFoundError:
    print("Error: .env file not found.")
    print("Please create a .env file with LHOST, RHOST, and PORT.")
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

def sender_mode(key):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(5)
            print(f"Attempting to connect to {RHOST}:{PORT}...")
            s.connect((RHOST, PORT))
            print("Connection successful!")
            
            s.settimeout(None)

            plaintext = input("Enter message: ")
            
            encrypted_bits = des_encrypt(plaintext, key)
            encrypted_hex = bits_to_hex(encrypted_bits)
            
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

def receiver_mode(key):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            
            s.bind((LHOST, PORT))
            s.listen()
            print(f"Server is listening on {LHOST}:{PORT}...")
            print("Waiting for a connection...")
            
            conn, addr = s.accept()
            
            with conn:
                print(f"Connected by {addr}")
                print("Waiting for one message...")
                
                data = conn.recv(4096)
                if data:
                    encrypted_hex = data.decode('utf-8').strip()
                    
                    try:
                        encrypted_bits = hex_to_bits(encrypted_hex)
                        decrypted_text = des_decrypt(encrypted_bits, key)
                        print(f"Received message: {decrypted_text}")
                    except Exception as e:
                        print(f"--- Error decrypting message ---")
                        print(f"Error: {e}. Was the key correct?")
                        print(f"Raw data received: {encrypted_hex}")
                        print(f"---------------------------------")
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
    print("--- DES Encrypted 'Walkie-Talkie' Chat ---")
    
    key = get_key()
    
    while True:
        print("Choose your role for this turn:")
        print("1. Sender (Send one message)")
        print("2. Receiver (Receive one message)")
        print("3. Quit")
        
        choice = input("Enter choice (1, 2, or 3): ")
            
        if choice == '1':
            print("\nStarting in Sender mode...")
            sender_mode(key)
        elif choice == '2':
            print("\nStarting in Receiver mode...")
            receiver_mode(key)
        elif choice == '3':
            print("Exiting chat. Goodbye!")
            break 
        else:
            print("Invalid input. Please enter 1, 2, or 3.\n")

if __name__ == "__main__":
    main()

