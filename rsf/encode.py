"""give stored words a id for latter processing

"""
from . import config
from . import utils


def encode(storage):
    """give stored words a id and store result back to storage

    Argumnets:
        storage (rsf.storage.Storage): expect storage stored words collection
    """
    words = list(storage.get_wiktionary_words())
    all_words = _get_all_words(words)
    word_id = _encode_id(all_words)
    lookup = _build_word_lookup(words)

    def encoded_words():
        for w in all_words:
            word = lookup.get(w, {})
            word["id"] = word_id[w]
            word["name"] = w
            related = []
            for r in word.get("related", []):
                related.append(word_id[r])
            word["related"] = related
            yield word

    storage.store_encoded_wiktionary_words(encoded_words())


def _get_all_words(words):
    all_words = []
    for word in words:
        all_words.append(word["word"])
        all_words.extend(word["related"])
    all_words = sorted(set(all_words))
    return all_words


def _encode_id(all_words):
    word_id = {}
    current_id = 1

    for word in all_words:
        word_id[word] = current_id
        current_id += 1
    return word_id


def _build_word_lookup(words):
    lookup = {}

    for word in words:
        lookup[word["word"]] = word

    return lookup


def main_encode(config=config.EncodeConfig):
    storage = utils.get_storage(config.MONGO)
    encode(storage)
