import numpy as np
from IPython import embed
import pandas as pd

class Similarity(object):
  """[summary]
  
  Arguments:
      object {[type]} -- [description]
  """
  def __init__(self):
    pass
  
  def cosine_similarity(self, d1: list, d2: list) -> dict:
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
      
  def tf_doc(self, doc: str):
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

  def tf_query(self):
    pass

  def idf(self):
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
    idf_values = self.idf()
    docs_tf = dict()
    for key in self.docs:
      docs_tf[key] = self.tf_doc(key)
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
  
  
  rank = TFIDF(docs=docs)
  result_tfidf = rank.tf_idf()
  print(result_tfidf)
  print(pd.DataFrame(result_tfidf))
  # result_tf = rank.tf_doc("doc1")
  # result_idf = rank.idf()
  # print(result_idf)
  
  # a = [1, 2, 3, 4, 5]
  # b = [1, 2, 5, 7, 8]
  # sim = Similarity()
  # result = sim.cosine_similarity(a, b)
  # print(result)

  
if __name__ == "__main__":
    main()
