import requests
from config import MESSEGE_URL, HEADERS_AUTH



class Message:
    def __init__(self, text, user):
        self.text = text
        self.user = user

    #check api methods https://crm.pachca.com/dev/getting-started/about/
    async def send_answer(self, response=None):
        answer = {
        "message": {
            "entity_type": "user",
            "entity_id": self.user,
            "content": response
        }
        }
        requests.post(MESSEGE_URL, headers=HEADERS_AUTH, json=answer)