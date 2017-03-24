import uuid
import requests
from bs4 import BeautifulSoup
import re
import src.models.users.constants as ItemsConstants
from src.common.database import Database
from src.models.stores.store import Store

__author__ = 'alee'

class Item(object):
    def __init__(self, url, _id=None):
        self.url = url
        store = Store.find_by_url(url)
        name_item_tag = store.name_item_tag
        name_query = store.name_query
        tag_name = store.tag_name
        query = store.query
        self.name = self.load_name(name_item_tag, name_query)
        self.price = self.load_price(tag_name, query)
        self._id = uuid.uuid4().hex if _id is None else _id

    def __repr__(self):
        return "<Item {} with URL {}>".format(self.name, self.url)

    def load_name(self, tag_name, query):
        #Amazon <span id="priceblock_ourprice" class="a-size-medium a-color-price">$165.99</span>
        request = requests.get(self.url)
        content = request.content
        soup = BeautifulSoup(content, "html.parser")

        element = soup.find(tag_name,query)
        string_price = element.text.strip()

        pattern = re.compile("(.+)")
        match = pattern.search(string_price)

        return match.group()

    def load_price(self, tag_name, query):
        #Amazon <span id="priceblock_ourprice" class="a-size-medium a-color-price">$165.99</span>
        request = requests.get(self.url)
        content = request.content
        soup = BeautifulSoup(content, "html.parser")

        element = soup.find(tag_name,query)
        string_price = element.text.strip()

        pattern = re.compile("(\d+.\d+)")
        match = pattern.search(string_price)

        return match.group()

    def save_to_mongo(self):
        Database.insert(ItemsConstants.COLLECTION, self.json())

    def json(self):
        return {
            "name": self.name,
            "url": self.url,
            "_id":self._id
        }