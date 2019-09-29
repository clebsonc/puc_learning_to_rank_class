import numpy as np
from os import listdir
from IPython import embed
import string


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
        self.documents = set()
        self.frequency = len(0)
        pass
        # oveload operator in constructor


class BooleanModel(object):
    def __init__(self, documents: dict):
        self.doc = documents
        self.inverted_index = dict()

    def compute_inverted_index(self):
        for key, text in self.doc.items():
            text = text.split(" ")
            text = set(text)
            for term in text:
                try:
                    dummy = int(term)
                except ValueError:
                    if term in self.inverted_index:
                        self.inverted_index[term].add(key)
                    else:
                        self.inverted_index[term] = {key, }

    def subtract(self, term1, term2):
        valid_docs = set()
        res1 = self.inverted_index[term1]
        res2 = self.inverted_index[term2]
        valid_docs = res1.difference(res2)
        return valid_docs

    def add(self, term1, term2):
        valid_docs = set()
        res1 = self.inverted_index[term1]
        res2 = self.inverted_index[term2]
        valid_docs = res1.union(res2)
        return valid_docs

    def intersect(self, term1, term2):
        valid_docs = set()
        res1 = self.inverted_index[term1]
        res2 = self.inverted_index[term2]
        valid_docs = res1.intersection(res2)
        return valid_docs

    def query(self, processed_terms):
        """String in the format: AMDEUS and Jose or Pneu and Balburdio
        Arguments:
            processed_terms {[type]} -- [description]
        """
        processed_terms = [x.strip() for x in processed_terms.split(" ")]
        # [AMDEUS, and, Jose, or, Pneu, and, Balburdio]
        it1 = 0
        iop = it1 + 1
        it2 = it1 + 2
        valid_docs = set()
        while it2 < len(processed_terms):
            term1 = processed_terms[it1]
            operator = processed_terms[iop]
            term2 = processed_terms[it2]
            it1 += 4
            iop += it1 + 1
            it2 += it1 + 2
            if operator == 'and':
                if len(valid_docs):
                    valid_docs.intersection(self.intersect(term1, term2))
                else:
                    valid_docs = self.intersect(term1, term2)
            if operator == 'or':
                valid_docs.union(self.add(term1, term2))
            if operator == 'not':
                valid_docs.difference(self.subtract(term1, term2))
        return valid_docs


def main():
    data_reader = DataReader("./data/shakespeare/")
    documentos = data_reader.read()
    bm = BooleanModel(documents=documentos)
    bm.compute_inverted_index()
    res = bm.query("caesar and brutus")
    print(res)


if __name__ == "__main__":
    main()
