import requests
import string
import random
from db import DB
from spellchecker import SpellChecker
from unidecode import unidecode


class Bot:

    # initialize url for commands, database object, and a minimum update offset
    def __init__(self, api_token, database_file):
        self._base_url = 'https://api.telegram.org/bot' + str(api_token)
        self.database = DB(database_file)
        self.min_update = 0

        self.videos = ['https://youtu.be/7Dqgr0wNyPo', 'https://youtu.be/p7FCgw_GlWc', 'https://youtu.be/PsO6ZnUZI0g',
                       'https://youtu.be/6CHs4x2uqcQ', 'https://youtu.be/E58qLXBfLrs', 'https://youtu.be/L53gjP-TtGE',
                       'https://youtu.be/IxGvm6btP1A', 'https://youtu.be/Bm5iA4Zupek', ]
        self.interviews = ['https://youtu.be/zxwfDlhJIpw','https://youtu.be/IeA7lvC1ego','https://youtu.be/zOHhaMvk-XM',
                           'https://youtu.be/Jbgkk1eVHaM','https://youtu.be/PmZjaYdS3fA','https://youtu.be/QdDYjNImN4w']

    # gets updates from bot and responds to user
    def run(self):
        updates = self.get_updates()
        for x in updates:
            self.min_update = x['update_id']
            self.respond(x)

    # respond to a specific message from a single user
    def respond(self, update):
        user_id = update['message']['from']['id']
        message = update['message']['text']
        print("Received message from ", user_id)
        response = self.generate_response(message)
        self.send_message(user_id, response)
        print("Sent response to", user_id)

    # retrieve updates from a specific offset (which eliminates old updates)
    def get_updates(self):
        url = self._base_url + '/getupdates'
        url += '?offset=' + str(self.min_update+1)  # add offset so updates don't repeat
        results = requests.get(url)
        data = results.json()
        return data['result']

    # sends a response to a specific user
    def send_message(self, userid, message):
        message.replace(' ', '%20')
        url = self._base_url + '/sendMessage?'
        url = url + 'chat_id=' + str(userid) + '&'
        url = url + 'text=' + message + ''
        results = requests.get(url)
        return results

    # generate a response based on message
    def generate_response(self, message: str):
        if message == '/start':
            return "Wassup y'all it's Kanye. You can honestly ask me anything, your question doesn't really determine " \
                   "a response or not. You can play any song from my best studio album by saying play with the song title. " \
                   "Other than that, ask me a question!"
        if message == '/touch':
            return "If you would like to get in touch with me, Kanye West, please contact my manager... ME!"
        if message == '/talk':
            return random.choice(self.interviews)
        if message == '/watch':
            return random.choice(self.videos)
        if message == '/play':
            return "open.spotify.com/artist/5K4W6rqBFWDnAN6FQUkS6x"
        if message == 'play':
            return "I said from my best album, or are you not a true fan? Don't worry, haters are fans too."
        message = unidecode(message)
        message = correct_spelling(message)
        message = make_bare_string(message)
        responses = self.database.select_all('Responses')
        response = search_database_for_response(message, responses)
        if response != '':
            return response
        else:
            return 'You ain\'t got the answers sway'


# loop through a string and correct spelling of words
def correct_spelling(text: str):
    spell = SpellChecker()
    spell.word_frequency.load_words(['jayz', 'ninjas'])  # add words to not be flagged
    words = text.split()
    unknown = spell.unknown(words)
    for x in unknown:
        text = text.replace(x, spell.correction(x))
    return text


# make a string lowercase, remove whitespace and punctuation
def make_bare_string(text: str):
    text = text.lower()
    text = text.strip()
    exclude = list(string.punctuation)
    for x in exclude:
        if text.find(x) >= 0:
            text = text.replace(x, '')
    return text


# loop through database responses and try to find a response
def search_database_for_response(message, responses):
    found = list()
    for x in responses:
        if message.find(x[0]) >= 0:
            found.append(x)
    if len(found) == 0:
        return ''
    index_of_max_priority = 0
    max_priority = 0
    for i in range(len(found)):
        if found[i][2] > max_priority:
            index_of_max_priority = i
            max_priority = found[i][2]
    return found[index_of_max_priority][1]
