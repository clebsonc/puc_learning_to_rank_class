import numpy as np
from os import listdir
import string
from IPython import embed


class DataReader(object):
    """[summary]

    Arguments:
        object {[type]} -- [description]

    Returns:
        [type] -- [description]
    """
    def __init__(self, path: str):
        self.path = path

    def read(self) -> dict:
        file = [x for x in listdir(self.path)
                if x.endswith('.pdf.txt')]
        data = dict()
        for f in file:
            text = open('/'.join([self.path, f]), 'r')
            text = text.read()
            text = text.replace("\n", "").lower()
            for c in string.punctuation:
                text = text.replace(c, ' ')
            data[f] = text
        return data


class Term(object):
    def __init__(self, name):
        self.name = name
        self.frequency = 0

    def __str__(self):
        return self.name

    def __hash__(self):
        ## print(hash(str(self)))
        return hash(str(self))

    def __eq__(self, other):
        return self.name == other.name


class BooleanModel(object):
    def __init__(self, documents: dict):
        self.doc = documents
        self.inverted_index = dict()

    def __update_frequency(self):
        for key in self.inverted_index:
            key.frequency = len(self.inverted_index[key])

    def compute_inverted_index(self):
        for key, text in self.doc.items():
            text = text.split(" ")
            text = set(text)
            for term in text:
                term_object = Term(term)
                try:
                    dummy = int(term)
                except ValueError:
                    if term_object in self.inverted_index:
                        self.inverted_index[term_object].add(key)
                    else:
                        self.inverted_index[term_object] = {key, }
        self.__update_frequency()

    def subtract(self, term1, term2):
        valid_docs = set()
        res1 = self.inverted_index[Term(term1)]
        res2 = self.inverted_index[Term(term2)]
        valid_docs = res1.difference(res2)
        return valid_docs

    def add(self, term1, term2):
        valid_docs = set()
        res1 = self.inverted_index[Term(term1)]
        res2 = self.inverted_index[Term(term2)]
        valid_docs = res1.union(res2)
        return valid_docs

    def intersect(self, term1, term2):
        valid_docs = set()
        res1 = self.inverted_index[Term(term1)]
        res2 = self.inverted_index[Term(term2)]
        valid_docs = res1.intersection(res2)
        return valid_docs

    def retrieve_docs(self, processed_terms):
        """String in the format:
            * (caesar and brutus)
            * (caesar or brutus)
            * (caesar not brutus)
        Arguments:
            processed_terms {[type]} -- [description]
        """
        term1 = processed_terms[0]
        operator = processed_terms[1]
        term2 = processed_terms[2]
        valid_docs = set()
        if operator == 'and':
            valid_docs = self.intersect(term1, term2)
        elif operator == 'or':
            valid_docs = self.add(term1, term2)
        else:
            valid_docs = self.subtract(term1, term2)
        return valid_docs


def main():
    # data_reader = DataReader("./data/shakespeare/")
    documents = {  # documentos que utilizei para testar o algoritmo
        "doc1": "i did enact julius caesar i was killed i the capitol brutus killed me",
        "doc2": "so let it be with caesar the noble brutus hath told you caesar was ambitious",
        "doc3": ("full fathom five thy father lies of his bones are coral made those are pearls"
                 " that were his eyes nothing of him that doth fade but doth suffer a sea-change"
                 "into something rich and strange")
    }

    # documents = data_reader.read()
    bm = BooleanModel(documents=documents)
    bm.compute_inverted_index()
    res1 = bm.retrieve_docs(
        ("caesar", "or", "brutus"),
    )
    print(res1)

    res2 = bm.retrieve_docs(
        ("caesar", "and", "julius"),
    )
    print(res2)

    res3 = bm.retrieve_docs(
        ("bones", "not", "caesar"),
    )
    print(res3)


if __name__ == "__main__":
    main()
