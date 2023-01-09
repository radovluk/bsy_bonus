from my_token import MY_TOKEN
import requests
import time
import base64

class Controller:
    def __init__(self, gist_id, token, url):
        self.gist_id = gist_id
        self.token = token
        self.url = url
        self.headers = {"Authorization": "Bearer " + self.token}

    def check_for_updates(self):
        response = requests.get(self.url)

        if response.status_code == 200:
            comments = response.json()
            for comment in comments:
                print(comment['body'])
        else:
            print(response.json()['message'])

    def handle_message(self, msg):
        pass

    def post_message(self, msg):
        data = {"body": + msg}
        response = requests.post(self.url, headers=self.headers, json=data)

        if response.status_code == 201:
            print("Comment posted successfully!")
        else:
            print("Failed to post comment. Status code: " + response.status_code)


if __name__ == "__main__":
    GIST_ID = "b13a8ec03c698d771a70ce34595621d6"
    url = f"https://api.github.com/gists/{GIST_ID}/comments"

    controller = Controller(GIST_ID, MY_TOKEN, url)
    while True:
        controller.check_for_updates()
        time.sleep(10)