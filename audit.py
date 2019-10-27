import requests
import json


class BaseAudit():
    def __init__(self, url):
        self.base_url = url
        self.client = requests.Session()

    def do_request(self, url):
        req_url = self.base_url.format(url)
        with self.client.get(url=req_url) as resp:
            return resp


class Audit(BaseAudit):
    @staticmethod
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

    def __init__(self, url):
        self.base_url = url
        super().__init__(url)
        self.client.headers.update({"accept": "*/*"})


    @staticmethod
    def process_response(response, search_url):
        info = {"Search Url": search_url, 'Exist': True if response.status_code == 200 else False}
        return info


class AuditTask():
    def __init__(self, base_url):
        self.base_url = base_url
        self.audit = Audit(url=self.base_url)

    def search_url_in_cache(self, search_url):
        response = self.audit.do_request(search_url)
        data = self.audit.process_response(response, search_url)
        self.audit.append_to_json(data, "info.json")  # Write result to .json file


url = "https://webcache.googleusercontent.com/search?q=cache:{}"
search_url = "facebook.com"

task = AuditTask(base_url=url)
task.search_url_in_cache(search_url=search_url)
