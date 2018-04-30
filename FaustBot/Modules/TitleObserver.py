import html
import requests
import re
import urllib
from bs4 import BeautifulSoup

from FaustBot.Communication.Connection import Connection
from FaustBot.Modules.PrivMsgObserverPrototype import PrivMsgObserverPrototype


class TitleObserver(PrivMsgObserverPrototype):
    @staticmethod
    def cmd():
        return None

    @staticmethod
    def help():
        return None

    def update_on_priv_msg(self, data, connection: Connection):
        regex = "(?P<url>https?://[^\s]+)"
        url = re.search(regex, data['message'])
        if url is not None:
            url = url.group()
            print(url)
            try:
                headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'}
                url = url
                req = urllib.request.Request(url, None, headers)
                resource = BeautifulSoup(urllib.request.urlopen(req), "html.parser")
                title = self.getTitle(resource)
                print(title)
                title = title[:250]
                connection.send_back(title, data)
            except Exception as exc:
                print(exc)
                pass
            
    def getTitle(self, resource):
            title = resource.title.string
            title = html.unescape(title)
            title = title.replace('\n', ' ').replace('\r', '')
            title = title.replace("&lt;", "<")
            title = title.replace("&gt;", ">")
            title = title.replace("&amp;", "&")
            return title
