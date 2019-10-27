import requests


class Audit():
    def __init__(self):
        self.base_url = "https://webcache.googleusercontent.com/search?q=cache:{}"
        self.client = requests.Session()
        self.client.headers.update({"accept": "*/*"})

    def do_request(self, url):
        req_url = self.base_url.format(url)
        with self.client.get(url=req_url) as resp:
            return resp

    @staticmethod
    def process_response(response, search_url):
        info = {"Search Url": search_url}
        info['Exist'] = True if response.status_code == 200 else False
        if response.code == 200:
            pass


a = Audit()
b = a.do_request("youtube.com")
a.process_response(b, "youtube")

