from json import dumps, loads
import os.path
from datetime import datetime
import random
import string

class Credential:
    def __init__(self, date, username, password):
        self.date = date
        self.username = username
        self.password = password

    def to_dict(self):
        return {"date": self.date, "username": self.username, "password": self.password}

def random_password():
    random_source = string.ascii_letters + string.digits + string.punctuation
    password = ''
    # password = random.choice(string.ascii_lowercase)
    # password += random.choice(string.ascii_uppercase)
    # password += random.choice(string.digits)
    # password += random.choice(string.punctuation)

    for i in range(16):
        password += random.choice(random_source)

    password_list = list(password)
    random.SystemRandom().shuffle(password_list)
    password = ''.join(password_list)
    print(password)
    return password

def load_credentials():
    credentials_data = []
    if os.path.isfile("./credentials.json"):
        credentials_file = open("credentials.json", "r+")
        credentials_json = credentials_file.read()
        credentials_data = loads(credentials_json)
        
    credentials = []

    for credential in credentials_data:
        credentials.append(Credential(credential["date"], credential["username"], credential["password"]))

    if os.path.isfile("./credentials.json"):
        credentials_file.close()
    return credentials

def add_credential(date, username):
    credential_index = next((i for i, item in enumerate(credentials_list) if item.username == username), None)
    print(credential_index)
    if not credential_index:
        new_credential = Credential(date, username, random_password())
        credentials_list.append(new_credential)
    else:
        print("There is already a credential for that username! Try again")

def edit_credential(date, username):
    credential_index = next((i for i, item in enumerate(credentials_list) if item.username == username), None)
    print(credential_index)
    if credential_index:
        credentials_list[credential_index].password = random_password()
    else:
        print("There is no credential for that username! Try again")

def list_credentials():
    for credential in credentials_list:
        print("Credential => Username: {} Password: {} Date: {} ".format(credential.username, credential.password, credential.date))

def save_credentials(credentials):
    credentials_save_list = []
    for c in credentials:
        credentials_save_list.append(c.to_dict())
    credentials_file = open("credentials.json", "w+")
    credentials_file.write(dumps(credentials_save_list))
    credentials_file.close()

credentials_list = load_credentials()

print("Welcome to the credentials management tool!")

while True:
    print("Type 'create' to add a new credential")
    print("Type 'update' to update an existing credential")
    print("Type 'list' to show all credentials")
    print("Type 'quit' to quit the app")

    command = input('Type a command: ')
    # print(command)
    if command == 'quit':
        save_credentials(credentials_list)
        break

    if command == 'create':
        credential_username = input("Enter an username for the credential: ")
        now = datetime.now() # current date and time
        credential_date = now.strftime("%m/%d/%Y, %H:%M:%S")

        add_credential(credential_date, credential_username)

    if command == 'update':
        credential_username = input("Enter the username of the credential: ")
        now = datetime.now() # current date and time
        credential_date = now.strftime("%m/%d/%Y, %H:%M:%S")

        edit_credential(credential_date, credential_username)

    if command == 'history':
        list_credentials()
