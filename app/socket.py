from .modules import (Inflect,
                     Inflection,
                     Inflector,
                     Inflexion,
                     LemmInflect,
                     NLTK,
                     Pattern,
                     PyInflect,
                     TextBlob,
                     Module
                     )
import pymongo
import random
import time

from flask_socketio import Namespace, emit

from .db import db, get_known_corrects, get_random_word
from .models import get_random_conversion, get_supported_modules

class InflexionNamespace(Namespace):

    def on_connect(self):
        # TODO: Replace this with logging
        emit('after connect', {'data': 'Lets dance'})

    def on_random(self, json):
        """
        Called whenever Client wants a random word, wordform and POS, 
        and then get the output for that.
        """
        # Get a random conversion
        pos, wordform = get_random_conversion()

        # Emit the list of modules that support the randomly chosen conversion
        self.on_input_modules({**json, **{
            "pos": pos,
            "wordform": wordform
        }})
        
        # Get a random word
        word = get_random_word(pos)

        # Emit the randomly generated data to the Client
        emit("conversion", {
            "pos": pos,
            "wordform": wordform,
            "word": word
        })

        # Send output for this conversion to Client
        self.on_input({**json, **{
            "pos": pos,
            "wordform": wordform,
            "word": word
        }})

    def on_input(self, json):
        """
        Called whenever Client wants to get the output of the currently visible
        modules, with the given input
        """
        # Get request parameters
        pos = json["pos"]
        wordform = json["wordform"]
        word = json["word"]
        show_competitors = json["show_competitors"]

        # Optionally emit list of known correct outputs
        correct_list = get_known_corrects(pos, wordform, word)
        if correct_list:
            emit("correct", {
                "output": correct_list
            })

        # Emit the output of each module that supports the desired conversion
        modules = get_supported_modules(pos, wordform, show_competitors)
        for module in modules:
            output = module().run(pos, wordform, word)
            emit("output", {
                "module": module.get_name(),
                "output": output
            })

    def on_input_modules(self, json):
        """
        Called whenever Client updates POS or Wordform, and we want to update
        which modules they are shown
        """
        # Get request parameters
        pos = json["pos"]
        wordform = json["wordform"]
        show_competitors = json["show_competitors"]

        # Emit the list of modules that support the desired conversion
        modules = get_supported_modules(pos, wordform, show_competitors)
        emit("output_modules", {
            "modules": [module.get_name() for module in modules]
        })
