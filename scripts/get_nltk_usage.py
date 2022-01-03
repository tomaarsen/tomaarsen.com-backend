
from module_dependencies import Module
import pickle

module = Module("nltk", count="all", lazy=False)

with open("app/static/data/nltk_module.pickle", "wb") as f:
    pickle.dump(module, f)

# with open("nltk_module.pickle", "rb") as f:
#     module = pickle.load(f)

# params = module.plot(show=False)

# breakpoint()
