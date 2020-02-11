from nltk import word_tokenize
from nltk.corpus import stopwords


class InvertedIndex(object):
    def __init__(self, collection: dict):
        self.collection = collection
        self.inverted_index = dict()
        self.mapped_doc_id = dict()
        self.__build_mapped_doc_id()

    def __build_mapped_doc_id(self):
        id = 0
        for document in self.collection:
            self.mapped_doc_id[document] = id
            id += 1

    def compute_inverted_index(self):
        for document in self.collection:
            tokenized_text = set(word_tokenize(self.collection[document],
                                               language='english'))
            tokenized_text -= set(stopwords.words('english'))
            for token in tokenized_text:
                if token in self.inverted_index:
                    self.inverted_index[token].add(self.mapped_doc_id[document])
                else:
                    self.inverted_index[token] = {self.mapped_doc_id[document]}


if __name__ == "__main__":
    documents = {  # documentos que utilizei para testar o algoritmo
        "book1": "i did enact julius caesar i was killed i the capitol brutus killed me",
        "book2": "so let it be with caesar the noble brutus hath told you caesar was ambitious",
        "book3": ("full fathom five thy father lies of his bones are coral made those are pearls"
                  " that were his eyes nothing of him that doth fade but doth suffer a sea-change"
                  " into something rich and strange")
    }
    inv_index = InvertedIndex(documents)
    inv_index.compute_inverted_index()
    __import__('IPython').embed()
