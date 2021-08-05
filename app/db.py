
import pymongo

# Initialize MongoDB database
client = pymongo.MongoClient("localhost:27017")

# Check whether MongoDB can be used.
try:
    # The ismaster command is cheap and does not require auth.
    client.admin.command('ismaster')
    from .db_mongo import get_random_word_lemma, get_known_corrects
except pymongo.errors.ConnectionFailure:
    from .db_json import get_random_word_lemma, get_known_corrects
