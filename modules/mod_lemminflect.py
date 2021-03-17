__all__ = [
    "LemmInflect"
]
from .module import Module

from lemminflect import getInflection, getLemma

# https://github.com/bjascob/LemmInflect
class LemmInflect(Module):

    # START OF NOUN
    # Conversions
    def noun_to_singular(self, term: str, *args, **kwargs) -> str:
        return getLemma(term, upos="NOUN")[0]
        # return getInflection(term, tag="NN")[0]

    def noun_to_plural(self, term: str, *args, **kwargs) -> str:
        return getInflection(getLemma(term, upos="NOUN")[0], tag="NNS")[0]

    def noun_to_classical_plural(self, term: str, *args, **kwargs) -> str:
        return getInflection(getLemma(term, upos="NOUN")[0], tag="NNS")[-1]

    # Checking
    def noun_is_singular(self, term: str, *args, **kwargs) -> bool:
        raise NotImplementedError()

    def noun_is_plural(self, term: str, *args, **kwargs) -> bool:
        raise NotImplementedError()
    # END OF NOUN

    # START OF VERB
    # Conversions
    def verb_to_singular(self, term: str, *args, **kwargs) -> str:
        return getInflection(getLemma(term, upos="VERB")[0], tag="VBZ")[0]

    def verb_to_plural(self, term: str, *args, **kwargs) -> str:
        return getLemma(term, upos="VERB")[0]
        # return getInflection(term, tag="VB")[0]

    def verb_to_pret(self, term: str, *args, **kwargs) -> str:
        return getInflection(getLemma(term, upos="VERB")[0], tag="VBD")[0]

    def verb_to_past_part(self, term: str, *args, **kwargs) -> str:
        return getInflection(getLemma(term, upos="VERB")[0], tag="VBN")[0]

    def verb_to_pres_part(self, term: str, *args, **kwargs) -> str:
        return getInflection(getLemma(term, upos="VERB")[0], tag="VBG")[0]

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
