import os
import dotenv

dotenv.load_dotenv()


class MongoConfig:
    HOST = os.getenv("RSF_MONGO_HOST", "127.0.0.1")
    PORT = int(os.getenv("RSF_MONGO_PORT", 27017))
    DB = os.getenv("RSF_MONGO_DB", "rsf")


class ConvertConfig:
    MONGO = MongoConfig
    WIKTIONARY_XML_PATH = os.getenv("RSF_WIKTIONARY_XML_PATH")


class EncodeConfig:
    MONGO = MongoConfig
