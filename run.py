
from app.db import get_known_corrects, get_random_word_lemma
from app.models import get_random_conversion
from app import create_app

app = create_app()

# def get_random():
#     # Get a random conversion
#     pos, wordform = get_random_conversion()

#     # Get a random word
#     word, lemma = get_random_word_lemma(pos)

#     known_corrects = get_known_corrects(pos, wordform, lemma)
#     return word, known_corrects

if __name__ == "__main__":
    # import cProfile
    # for _ in range(10):
        # print(get_random())
    # cProfile.run("for _ in range(100): get_random()", "get_random_2.prof")
    app.run(host="127.0.0.1", port=5000, debug=True)
