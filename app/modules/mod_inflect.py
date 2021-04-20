
__all__ = [
    "Inflect"
]
from .module import Module

from inflect import engine

# https://github.com/jaraco/inflect


class Inflect(Module):

    # START OF NOUN
    # Conversions
    def noun_to_singular(self, term: str, *args, **kwargs) -> str:
        # May return False if noun is deemed already singular,
        # So then we return the deemed singular term
        output = engine().singular_noun(term)
        if output == False:
            return term
        return output

    def noun_to_plural(self, term: str, *args, **kwargs) -> str:
        return engine().plural_noun(term)

    def noun_to_classical_plural(self, term: str, *args, **kwargs) -> str:
        p = engine()
        p.classical(all=True)
        try:
            return p.plural_noun(term)
        finally:
            p.classical(all=False)

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
        return engine().plural_verb(term)

    def verb_to_pret(self, term: str, *args, **kwargs) -> str:
        raise NotImplementedError()

    def verb_to_past_part(self, term: str, *args, **kwargs) -> str:
        raise NotImplementedError()

    def verb_to_pres_part(self, term: str, *args, **kwargs) -> str:
        return engine().present_participle(term)

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
