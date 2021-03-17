
__all__ = [
    "Pattern"
]
from .module import Module

from pattern.en import pluralize, singularize, conjugate

# https://github.com/clips/pattern
class Pattern(Module):
    
    # START OF NOUN
    # Conversions
    def noun_to_singular(self, term: str, *args, **kwargs) -> str:
        return singularize(term)
        # return conjugate(term, "3sg")

    def noun_to_plural(self, term: str, *args, **kwargs) -> str:
        # return conjugate(term, "pl")
        return pluralize(term)

    def noun_to_classical_plural(self, term: str, *args, **kwargs) -> str:
        return pluralize(term, classical=True)

    # Checking
    def noun_is_singular(self, term: str, *args, **kwargs) -> bool:
        raise NotImplementedError()

    def noun_is_plural(self, term: str, *args, **kwargs) -> bool:
        raise NotImplementedError()
    # END OF NOUN

    # START OF VERB
    # Conversions
    def verb_to_singular(self, term: str, *args, **kwargs) -> str:
        # return singularize(term, pos="VB")
        return conjugate(term, "3sg")

    def verb_to_plural(self, term: str, *args, **kwargs) -> str:
        # return pluralize(term, pos="VB")
        return conjugate(term, "inf")

    def verb_to_pret(self, term: str, *args, **kwargs) -> str:
        return conjugate(term, "past")

    def verb_to_past_part(self, term: str, *args, **kwargs) -> str:
        return conjugate(term, "pastparticiple")

    def verb_to_pres_part(self, term: str, *args, **kwargs) -> str:
        return conjugate(term, "part")

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
    # END OF ADJECTIVE
