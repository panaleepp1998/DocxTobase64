
import base64
import requests
 
def get_as_base64(url): 
    return base64.b64encode(requests.get(url).content)
 
if __name__ == '__main__':
    endpoint = "https://i.stack.imgur.com/N4TSy.jpg"
    res = get_as_base64(url=endpoint) 
    print(res)