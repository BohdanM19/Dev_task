import requests
import json


def append_to_json(_dict, path):
    with open(path, 'ab+') as f:
        f.seek(0, 2)  # Go to the end of file
        if f.tell() == 0:  # Check if file is empty
            f.write(json.dumps([_dict], indent=4).encode())  # If empty, write an array
        else:
            f.seek(-1, 2)
            f.truncate()  # Remove the last character, open the array
            f.write(' , '.encode())  # Write the separator
            f.write(json.dumps(_dict, indent=4).encode())  # Dump the dictionary
            f.write(']'.encode())  # Close the array


class Audit():
    def __init__(self, url):
        self.base_url = url
        self.client = requests.Session()
        self.client.headers.update({"accept": "*/*"})

    def do_request(self, url):
        req_url = self.base_url.format(url)
        with self.client.get(url=req_url) as resp:
            return resp

    @staticmethod
    def process_response(response, search_url):
        info = {"Search Url": search_url, 'Exist': True if response.status_code == 200 else False}
        return info


url = "https://webcache.googleusercontent.com/search?q=cache:{}"
search_url = "facebook.com"
task = Audit(url=url)
response = task.do_request(search_url)
data = task.process_response(response, search_url)
append_to_json(data, "info.json")
