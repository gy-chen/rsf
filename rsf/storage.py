class Storage:
    """store parsed wiktionary data into mongo

    Arguments:
        db (pymongo.database.Database)
    """

    COLLECTION_WIKTIONARY = "wiktionary"
    COLLECTION_WORDS = "words"

    def __init__(self, db):
        self._db = db

    def store_wiktionary_pages(self, pages):
        wiktionary = self._db[self.COLLECTION_WIKTIONARY]
        for page in pages:
            wiktionary.insert_one(page)

    def store_wiktionary_words(self, words):
        words_collection = self._db[self.COLLECTION_WORDS]
        for word in words:
            words_collection.insert_one(word)
