import numpy as np
from IPython import embed
import pandas as pd


class Similarity(object):
    """[summary]

    Arguments:
        object {[type]} -- [description]
    """
    def __init__(self, docs, query):
        self.docs = docs
        self.query = query

    def compute_similarity_query_documents(self):
        rank = TFIDF(docs=self.docs)
        result_tfidf_docs = rank.tf_idf()
        result_tfidf_query = rank.tf_idf_query(self.query)
        df = pd.DataFrame(result_tfidf_docs)
        df.loc[result_tfidf_query.keys(), 'query'] = list(result_tfidf_query.values())
        df = df.fillna(0)
        relevance = dict()
        for col in set(df.columns) - {'query'}:
            relevance[f'query -- doc: {col}'] = self.__cosine_similarity(
                df.loc[:, col], df.loc[:, 'query']
            )
        relevance = pd.Series(relevance).sort_values(ascending=False)
        return relevance

    def __cosine_similarity(self, d1: list, d2: list) -> dict:
        """
        [summary]
        """
        d1 = np.asarray(d1)
        d2 = np.asarray(d2)
        magn_d1 = np.sqrt(np.sum(d1 ** 2))
        magn_d2 = np.sqrt(np.sum(d2 ** 2))
        denominador = magn_d1 * magn_d2
        numerador = np.sum(d1 * d2)
        sim = numerador / denominador
        return sim


class TFIDF(object):
    def __init__(self, docs: dict):
        self.docs = docs
        self.__bag_of_words()

    def __bag_of_words(self):
        for key, value in self.docs.items():
            value = value.split(" ")
            self.docs[key] = value

    def __tf_doc(self, doc: str):
        term_frequency = dict()
        terms = self.docs[doc]
        for key in terms:
            if key in term_frequency:
                term_frequency[key] += 1
            else:
                term_frequency[key] = 1
        len_doc = len(terms)
        for key in terms:
            term_frequency[key] /= len_doc
        return term_frequency

    def __get_qtd_docs_with_term(self, term: str) -> int:
        qtd = 0
        for key, values in self.docs.items():
            if term in values:
                qtd += 1
        return qtd

    def tf_idf_query(self, query: str):
        """[summary]

        Arguments:
            query {str} -- [description]
        """
        query = query.split(" ")
        # compute the term frequêncy for the query related to the docs.
        tf_query = dict()
        for w in query:
            tf_query[w] = self.__get_qtd_docs_with_term(w)
        for key in tf_query:
            tf_query[key] /= len(self.docs)
        # compute the idf of query:
        idf_query = dict()
        for term in query:
            idf_query[term] = np.log10(len(self.docs) / self.__get_qtd_docs_with_term(term))
        tf_idf = dict()
        for term in query:
            tf_idf[term] = tf_query[term] * idf_query[term]
        return tf_idf

    def __idf(self):
        """ IDF = log_b(N/dft)
        """
        N = len(self.docs)
        terms_idf = dict()
        for key, value in self.docs.items():
            set_value = set(value)
            for v_key in set_value:
                if v_key in terms_idf:
                    terms_idf[v_key] += 1
                else:
                    terms_idf[v_key] = 1

        for key, value in terms_idf.items():
            terms_idf[key] = np.log10(N / value)
        return terms_idf

    def tf_idf(self):
        idf_values = self.__idf()
        docs_tf = dict()
        for key in self.docs:
            docs_tf[key] = self.__tf_doc(key)
        for key, value in docs_tf.items():
            for term, scalar in value.items():
                idf_term = idf_values[term]
                docs_tf[key][term] = scalar * idf_term
        return docs_tf


def main():
    docs = {
        "doc1": "five times new york times won a prize",
        "doc2": "new york times is great",
        "doc3": "los angeles times is new"
    }
    query = "times great"
    sim = Similarity(docs=docs, query=query)
    result = sim.compute_similarity_query_documents()
    print(result)


if __name__ == "__main__":
    main()
