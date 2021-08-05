
from app.models import is_lemma_form
from .constants import POS, Wordform
import random
import json

with open("agid_json/agid.json") as f:
    agid = json.load(f)

def get_random_word_lemma(pos: str) -> str:
    """
    Randomly choose a known word from the mongoDB database for the given `pos`.
    Also return its lemma as the second parameter.
    """
    entries = agid[pos]["to_word"]
    lemma = random.choice(list(entries.keys()))
    word = random.choice(list(entries[lemma].values()))
    if isinstance(word, list):
        return random.choice(word), lemma
    return word, lemma

def get_known_corrects(pos: str, wordform: str, input_word: str):
    """
    Get list of known correct outputs of `input_word` with given `pos`, 
    converted to `wordform`.
    """
    try:
        lemma = agid[pos]["to_lemma"][input_word]
    except KeyError:
        return []

    # Check if we are converting to the lemma
    if is_lemma_form(pos, wordform):
        return [lemma]
    
    # Otherwise use the to_word database to potentially find a word
    # in the desired wordform
    entry = agid[pos]["to_word"][lemma]
    # If the desired wordform is in the entry, return the list of the results
    if wordform in entry:
        return entry[wordform]
    # If the desired wordform is past participle, and only "past" is in the entry, use that
    elif wordform == Wordform.PAST_PART and Wordform.PAST in entry:
        return entry[Wordform.PAST]
                
    return []
