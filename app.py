import requests
from lxml import etree
import hashlib
import time

class Donation:
    def __init__(self, message, author, amount):
        self.message = message
        self.author = author
        self.amount = amount

    def __str__(self):
        return f'Message: {self.message}\nAuthor: {self.author}\nAmount: {self.amount}'

    def display_message(self):
        if self.message.startswith('['):
            return self.message.split(']', 1)[1]
        else:
            return self.message

    def display_amount(self):
        if self.amount is None:
            return 'Anonymous'
        return self.amount.replace(' ', '').split('K')[0]

    def display_author(self):
        if self.message.startswith('['):
            return self.message.split(']', 1)[0][1:]
        else:
            return 'Anonymous'

url = 'https://www.darujme.cz/projekt/1204937'
auth_key = '923847293847923847238947'
donation_history = []

while True:
    donations = []
    tree = etree.HTML(requests.get(url).text)
    messages = tree.xpath('//div[@class=\'bubble-content\']/p')
    meta = tree.xpath('//div[@class=\'pledgeComment-meta\']')

    for i, value in enumerate(messages):
        message = value.text.strip()
        author = meta[i].find('div[@class=\'pledgeComment-author\']').text.strip()
        amount_element = meta[i].find('div[@class=\'pledgeComment-amount\']')
        if amount_element is not None:
            amount = amount_element.text.strip()
        else:
            amount = None
        donation = Donation(message, author, amount)
        donation_info =  f'{donation.message}{donation.author}{donation.amount}'.encode('utf-8')
        donation_hash = hashlib.sha1(donation_info).hexdigest()
        if donation_hash not in donation_history:
            donations.append(donation)
            donation_history.append(donation_hash)

    for d in donations:
        params = {
            'key': auth_key,
            'message': d.display_message(),
            'author': d.display_author(),
            'amount': d.display_amount()
        }
        try:
            r = requests.get(f'http://31.31.76.93:9090/nodecg-czskm/darujme', params)
        except:
            print('Connection error')

    time.sleep(30)