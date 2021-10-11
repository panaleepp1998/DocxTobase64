import base64
import requests


<<<<<<< HEAD
def get_as_base64(url):

    return base64.b64encode(requests.get(url).content)

if __name__ == '__main__':
    urls="https://s.isanook.com/ca/0/ui/279/1396205/download20190701165129_1562561119.jpg"
    imageTobase64=get_as_base64(url=urls)
    print(imageTobase64)
=======
# def get_as_base64(url):

#     return base64.b64encode(requests.get(url).content)

# if __name__ == '__main__':
#     urls="https://s.isanook.com/ca/0/ui/279/1396205/download20190701165129_1562561119.jpg"
#     imageTobase64=get_as_base64(url=urls)
#     print(imageTobase64)
def get_as_base64(url): 
    return base64.b64encode(requests.get(url).content)

def urltob64(url):  
    res = get_as_base64(url)
    return{ 
            'base64': res,   
        }  
if __name__ == '__main__':
    urls="https://s.isanook.com/ca/0/ui/279/1396205/download20190701165129_1562561119.jpg"
    imageTobase64=get_as_base64(url=urls)
    print(imageTobase64)

>>>>>>> 03ed6f2b561a5b76c9517adf79b99f74993b2949
