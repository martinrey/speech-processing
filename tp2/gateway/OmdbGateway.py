import requests


class OmdbGateway(object):
    def __init__(self, token='a908719f', url='http://www.omdbapi.com/'):
        self.url = url + '?apikey=' + token

    def movie(self, movie):
        uri = self.url + "?t=" + movie
        return requests.get(uri).json()
