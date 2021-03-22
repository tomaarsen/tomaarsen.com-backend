
from app.models import is_lemma_form
from .constants import POS, Wordform
import random
import pymongo

# Initialize MongoDB database
client = pymongo.MongoClient("localhost:27017")
db = client["AGID"]


def get_random_word(pos: str) -> str:
    """
    Randomly choose a known word from the mongoDB database for the given `pos`.
    """
    word_entry = db[f"{pos.upper()}_to_word"].aggregate(
        [{"$sample": {"size": 1}}]).next()
    word = random.choice(list(word_entry.values()))
    if isinstance(word, list):
        return word[0]
    return word


def get_known_corrects(pos: str, wordform: str, input_word: str):
    """
    Get list of known correct outputs of `input_word` with given `pos`, 
    converted to `wordform`.
    """
    if pos != POS.A:
        lemma_entry = db[f"{pos.upper()}_to_lemma"].find_one({"_id": input_word})
        if lemma_entry:
            lemma = lemma_entry["lemma"]

            # Check if we are converting to the lemma
            if is_lemma_form(pos, wordform):
                return [lemma]
            else:
                # Otherwise use the to_word database to potentially find a word
                # in the desired wordform
                word_entry = db[f"{pos.upper()}_to_word"].find_one({"_id": lemma})
                # If the desired wordform is in the entry, return the list of the results
                if wordform in word_entry:
                    return list(word_entry[wordform])
                # If the desired wordform is past participle, and only "past" is in the entry, use that
                elif wordform == Wordform.PAST_PART and Wordform.PAST in word_entry:
                    return list(word_entry[Wordform.PAST])
                
    return []
