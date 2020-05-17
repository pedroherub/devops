from json import dumps, loads
import os.path
from datetime import datetime
import subprocess

class Backup:
    def __init__(self, date, name, scope):
        self.date = date
        self.name = name
        self.scope = scope

    def to_dict(self):
        return {"date": self.date, "name": self.name, "scope": self.scope}

def load_backups():
    backups_data = []
    if os.path.isfile("./backups.json"):
        backups_file = open("backups.json", "r+")
        backups_json = backups_file.read()
        backups_data = loads(backups_json)
        
    backups = []

    for backup in backups_data:
        backups.append(Backup(backup["date"], backup["name"], backup["scope"]))

    if os.path.isfile("./backups.json"):
        backups_file.close()
    return backups

def add_backup(date, name, scope):
    new_backup = Backup(date, name, scope)
    backups_list.append(new_backup)

def list_backups():
    for backup in backups_list:
        print("Backup ({}): Date: {} Scope: {}".format(backup.name, backup.date, backup.scope))

def save_backups(backups):
    backups_save_list = []
    for b in backups:
        backups_save_list.append(b.to_dict())
    backups_file = open("backups.json", "w+")
    backups_file.write(dumps(backups_save_list))
    backups_file.close()

backups_list = load_backups()

print("Welcome to the backup management tool!")

while True:
    print("Type 'home' to backup home folder")
    print("Type 'full' to backup full system")
    print("Type 'history' to show all backups")
    print("Type 'quit' to quit the app")

    command = input('Type a command: ')
    # print(command)
    if command == 'quit':
        save_backups(backups_list)
        break

    if command == 'home' or command == 'full':
        backup_name = input("Enter a name for the backup: ")
        backup_scope = command
        now = datetime.now() # current date and time
        backup_date = now.strftime("%m/%d/%Y, %H:%M:%S")

        if command == 'home':
            subprocess.call(['rsync', '-avzh', '/home/pedroherub/dev/ka107', '/home/pedroherub/Downloads/backups/'])
        elif command == 'full':
            subprocess.call(['sudo', 'rsync', '-aAXv', '/', '--exclude={"/dev/*","/proc/*","/sys/*","/tmp/*","/run/*","/mnt/*","/media/*","/lost+found"}', '/mnt'])

        add_backup(backup_date, backup_name, backup_scope)

    if command == 'history':
        list_backups()
