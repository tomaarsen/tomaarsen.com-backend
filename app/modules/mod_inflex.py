
from inflex import Noun, Verb, Adjective
__all__ = [
    "Inflex"
]
import os
import sys
from .module import Module

sys.path.insert(1, os.path.join(sys.path[0], '../..'))

# Lingua::EN::Inflex


class Inflex(Module):

    # START OF NOUN
    # Conversions
    def noun_to_singular(self, term: str, *args, **kwargs) -> str:
        return Noun(term).singular()

    def noun_to_plural(self, term: str, *args, **kwargs) -> str:
        return Noun(term).plural()

    def noun_to_classical_plural(self, term: str, *args, **kwargs) -> str:
        return Noun(term).classical().plural()

    # Checking
    def noun_is_singular(self, term: str, *args, **kwargs) -> bool:
        raise Noun(term).is_singular()

    def noun_is_plural(self, term: str, *args, **kwargs) -> bool:
        raise Noun(term).is_plural()
    # END OF NOUN

    # START OF VERB
    # Conversions
    def verb_to_singular(self, term: str, *args, **kwargs) -> str:
        return Verb(term).singular()

    def verb_to_plural(self, term: str, *args, **kwargs) -> str:
        return Verb(term).plural()

    def verb_to_pret(self, term: str, *args, **kwargs) -> str:
        return Verb(term).past()

    def verb_to_past_part(self, term: str, *args, **kwargs) -> str:
        return Verb(term).past_part()

    def verb_to_pres_part(self, term: str, *args, **kwargs) -> str:
        return Verb(term).pres_part()

    # Checking
    def verb_is_singular(self, term: str, *args, **kwargs) -> bool:
        return Verb(term).is_singular()

    def verb_is_plural(self, term: str, *args, **kwargs) -> bool:
        return Verb(term).is_plural()

    def verb_is_pret(self, term: str, *args, **kwargs) -> str:
        return Verb(term).is_past()

    def verb_is_past_part(self, term: str, *args, **kwargs) -> str:
        return Verb(term).is_past_part()

    def verb_is_pres_part(self, term: str, *args, **kwargs) -> str:
        return Verb(term).is_pres_part()
    # END OF VERB

    # START OF ADJECTIVE
    # Conversions
    def adj_to_singular(self, term: str, *args, **kwargs) -> str:
        return Adjective(term).singular()

    def adj_to_plural(self, term: str, *args, **kwargs) -> str:
        return Adjective(term).plural()

    # Checking
    def adj_is_singular(self, term: str, *args, **kwargs) -> bool:
        raise NotImplementedError()

    def adj_is_plural(self, term: str, *args, **kwargs) -> bool:
        raise NotImplementedError()

    # Custom
    def adj_to_comparative(self, term: str, *args, **kwargs) -> str:
        return Adjective(term).comparative(only_suffix=True)

    def adj_to_superlative(self, term: str, *args, **kwargs) -> str:
        return Adjective(term).superlative(only_suffix=True)
    # END OF ADJECTIVE
