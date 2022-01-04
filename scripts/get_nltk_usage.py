
from module_dependencies import Module
import pickle
import json

# module = Module("nltk", count="all", lazy=False)

# with open("app/static/data/nltk_module.pickle", "wb") as f:
#     pickle.dump(module, f)

with open("app/static/data/nltk_module.pickle", "rb") as f:
    module = pickle.load(f)

print(module.n_uses())

usage = module.usage(cumulative=True)
with open("app/static/data/nltk_usage.json", "w") as f:
    json.dump(usage, f)

# params = module.plot(show=False, transparant=True)

# breakpoint()
