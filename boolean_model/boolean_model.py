import numpy as np
import pandas as pd
from os import listdir
from IPython import embed
import re


class DataReader(object):
    def __init__(self, path_to_files: str):
        self.path_to_files = path_to_files

    def read_data(self) -> dict:
        """ Read all data collection in memory.
        Returns:
            dict -- Dicitionary containing the documents.
        """
        files = [x for x in listdir(self.path_to_files) if x.endswith('.pdf.txt')]
        data = dict()
        for file_name in files:
            file_data = open('/'.join([self.path_to_files, file_name]), 'r')
            file_data = file_data.read()
            file_data = file_data.replace(r'\r\n', ' ').lower().replace("\n", ' ')
            file_name = file_name.replace('.pdf.txt', '').lower().replace("_ entire play", '')
            data[file_name] = file_data
        return data


class Grepping(object):
    def __init__(self):
        pass

    def retrieve(self, documents: dict, contains: set, not_contains: set):
        """[summary]

        Arguments:
            documents {dict} -- [description]
            contains {set} -- [description]
            not_contains {set} -- [description]
        """
        valid_documents = set()
        for key, text in documents.items():
            for word in contains:
                if word in text:
                    valid_documents.add(key)

        # remove documents with not acceptable words
        result = valid_documents.copy()
        for key in valid_documents:
            for word in not_contains:
                if word in documents[key]:
                    try:
                        result.remove(key)
                    except KeyError:
                        pass
        return result


class BooleanModel(object):
    def __init__(self, documents):
        self.documents = documents
        self.incidence_matrix = self.build_incidence_matrix

    def __get_unique_terms(self):
        terms = set()
        for k, text in self.documents.items():
            for t in text.split(' '):
                terms.add(t)
        return terms

    def __get_document_terms(self, docId):
        terms = set(self.documents[docId].split(" "))
        return terms

    def build_incidence_matrix(self):
        header = list(self.documents.keys())
        index = self.__get_unique_terms()
        incidence_matrix = pd.DataFrame(columns=header, index=index)
        incidence_matrix = incidence_matrix.fillna(0)
        for doc in header:
            terms = self.__get_document_terms(doc)
            incidence_matrix.loc[terms, doc] = 1
        return incidence_matrix


def main():
    data = DataReader('./shakespeare/')
    documents = data.read_data()

    # print(Grepping().retrieve(documents=documents, contains={'brutus'}, not_contains={}))
    bm = BooleanModel(documents=documents)
    incidence_matrix = bm.build_incidence_matrix()
    embed()
    


if __name__ == "__main__":
    main()
