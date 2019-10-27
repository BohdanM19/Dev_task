import requests


class Audit():
    def __init__(self):
        self.base_url = "https://webcache.googleusercontent.com/search?q=cache:{}"
        self.client = requests.Session()
        self.client.headers.update({"accept": "*/*"})

    def do_request(self, url):
        req_url = self.base_url.format(url)
        with self.client.get(url=req_url) as response:
            text = response.text


a = Audit()
a.do_request("http://twitdfgdfgch.tv")
