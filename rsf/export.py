"""export stored encoded words

"""
import json
from . import config
from . import utils


def export(storage, path, pretty):
    """export stored encoded words

    Arguments:
        storage (rsf.storage.Storage)
        path (str)
        pretty (bool)
    """
    export_words = storage.get_export_encoded_words()
    indent = 2 if pretty else None
    with open(path, "w") as f:
        json.dump(list(export_words), f, indent=indent)


def main_export(config=config.ExportConfig):
    storage = utils.get_storage(config.MONGO)
    export(storage, config.PATH, config.PRETTY)
