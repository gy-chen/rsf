import string
from pymongo import MongoClient
from .storage import Storage
from .config import MongoConfig


def get_db(config=MongoConfig):
    return MongoClient(host=config.HOST, port=config.PORT)[config.DB]


def get_storage(config=MongoConfig):
    db = get_db(config)
    return Storage(db)


def filter_strip(words):
    for word in words:
        yield word.strip()


def filter_exclude_empty(words):
    for word in words:
        if not word:
            continue
        yield word


def filter_exclude_punctuation(words):
    for word in words:
        if any(p in word for p in string.punctuation):
            continue
        yield word
