class Storage:
    """store parsed wiktionary data into mongo

    Arguments:
        db (pymongo.database.Database)
    """

    COLLECTION_WIKTIONARY = "wiktionary"
    COLLECTION_WORDS = "words"
    COLLECTION_WORDS_ENCODED = "encodedWords"

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

    def get_wiktionary_words(self):
        words_collection = self._db[self.COLLECTION_WORDS]
        return words_collection.find()

    def store_encoded_wiktionary_words(self, encoded_words):
        words_collection = self._db[self.COLLECTION_WORDS_ENCODED]
        words_collection.insert_many(encoded_words)

    def get_export_encoded_words(self):
        words_collection = self._db[self.COLLECTION_WORDS_ENCODED]
        return words_collection.find(projection={"_id": 0})
