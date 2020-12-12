import requests

class CatFacts:
    def __init__(self):
        self.text = None
        self.synced = False

    def sync(self):
        response = requests.get('https://cat-fact.herokuapp.com/facts')
        if response.status_code != 200:
            raise Exception('Server Unavailable')

        json = response.json()

        self.text = json[0]['text']
        self.synced = True

        return self
