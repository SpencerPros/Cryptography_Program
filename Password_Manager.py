###
#
#Name: Spencer Prosniewski
#Program: Password_Manager
###


from cryptography.fernet import Fernet, InvalidToken

class PasswordManager:
    def __init__(self, key_file):
        # Initialize PasswordManager with a key file and an empty passwords dictionary
        self.key_file = key_file
        self.key = self.load_key()
        self.passwords = {}

    def load_key(self):
        # Load the encryption key from the specified file
        return open(self.key_file, 'rb').read()

    def encrypt_password(self, password, key):
        # Encrypt a password using the provided key
        cipher_suite = Fernet(key)
        encrypted_password = cipher_suite.encrypt(password.encode())
        return encrypted_password

    def decrypt_password(self, encrypted_password, key):
        try:
            # Decrypt an encrypted password using the provided key
            cipher_suite = Fernet(key)
            decrypted_bytes = cipher_suite.decrypt(encrypted_password)
            decrypted_password = decrypted_bytes.decode('utf-8')
            return decrypted_password
        except InvalidToken as e:
            # Handle InvalidToken exception when decryption fails
            print(f'InvalidToken error: {e}')
            return None

    def save_password(self, username, password):
        # Save an encrypted password for a given username
        encrypted_password = self.encrypt_password(password, self.key)
        self.passwords[username] = encrypted_password

    def retrieve_password(self, username):
        encrypted_password = self.passwords.get(username)
        if encrypted_password:
            # Print both the stored username and the encrypted password
            print(f"Stored Username: {username}, Encrypted Password: {encrypted_password}")
            
            decrypted_password = self.decrypt_password(encrypted_password, self.key)
            if decrypted_password:
                print(f"Decrypted Password: {decrypted_password}")
            else:
                print("Password decryption failed.")
        else:
            print("Password not found.")

# Example usage:
password_manager = PasswordManager('key.key')

while True:
    print("\n1. Add a new user")
    print("2. Retrieve password for a user")
    print("3. Exit")

    choice = input("Enter your choice (1-3): ")

    if choice == '1':
        # Get user input for username and password, then save the user
        username = input("Enter username: ")
        password = input("Enter password: ")
        password_manager.save_password(username, password)
        print("User added successfully!")

    elif choice == '2':
        # Get user input for the username to retrieve the password
        username = input("Enter username to retrieve password: ")
        password_manager.retrieve_password(username)

    elif choice == '3':
        # Exit the program
        print("Exiting program. Goodbye!")
        break

    else:
        # Handle invalid choice
        print("Invalid choice. Please enter a number between 1 and 3.")






