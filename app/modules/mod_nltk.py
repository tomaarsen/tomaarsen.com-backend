
__all__ = [
    "NLTK"
]
from .module import Module

from nltk.corpus import wordnet as wn
from nltk.stem import WordNetLemmatizer

# https://github.com/nltk/nltk


class NLTK(Module):

    # START OF NOUN
    # Conversions
    def noun_to_singular(self, term: str, *args, **kwargs) -> str:
        return wn.morphy(term, wn.NOUN)

    def noun_to_plural(self, term: str, *args, **kwargs) -> str:
        raise NotImplementedError()

    def noun_to_classical_plural(self, term: str, *args, **kwargs) -> str:
        raise NotImplementedError()

    # Checking
    def noun_is_singular(self, term: str, *args, **kwargs) -> bool:
        raise NotImplementedError()

    def noun_is_plural(self, term: str, *args, **kwargs) -> bool:
        raise NotImplementedError()
    # END OF NOUN

    # START OF VERB
    # Conversions
    def verb_to_singular(self, term: str, *args, **kwargs) -> str:
        raise NotImplementedError()

    def verb_to_plural(self, term: str, *args, **kwargs) -> str:
        return wn.morphy(term, wn.VERB)

    def verb_to_pret(self, term: str, *args, **kwargs) -> str:
        raise NotImplementedError()

    def verb_to_past_part(self, term: str, *args, **kwargs) -> str:
        raise NotImplementedError()

    def verb_to_pres_part(self, term: str, *args, **kwargs) -> str:
        raise NotImplementedError()

    # Checking
    def verb_is_singular(self, term: str, *args, **kwargs) -> bool:
        raise NotImplementedError()

    def verb_is_plural(self, term: str, *args, **kwargs) -> bool:
        raise NotImplementedError()

    def verb_is_pret(self, term: str, *args, **kwargs) -> str:
        raise NotImplementedError()

    def verb_is_past_part(self, term: str, *args, **kwargs) -> str:
        raise NotImplementedError()

    def verb_is_pres_part(self, term: str, *args, **kwargs) -> str:
        raise NotImplementedError()
    # END OF VERB

    # START OF ADJECTIVE
    # Conversions
    def adj_to_singular(self, term: str, *args, **kwargs) -> str:
        raise NotImplementedError()

    def adj_to_plural(self, term: str, *args, **kwargs) -> str:
        raise NotImplementedError()

    # Checking
    def adj_is_singular(self, term: str, *args, **kwargs) -> bool:
        raise NotImplementedError()

    def adj_is_plural(self, term: str, *args, **kwargs) -> bool:
        raise NotImplementedError()

    def adj_to_comparative(self, term: str, *args, **kwargs) -> str:
        raise NotImplementedError()

    def adj_to_superlative(self, term: str, *args, **kwargs) -> str:
        raise NotImplementedError()
    # END OF ADJECTIVE
