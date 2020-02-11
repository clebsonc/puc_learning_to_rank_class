from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import os
import pathlib


class TextReader(object):
    def __init__(self, path: str):
        self.path: pathlib.Path = pathlib.Path(path)
        self.text_files: list = self.__find_text_files()
        self.documents: dict = dict()

    def __find_text_files(self):
        return sorted([x for x in os.listdir(self.path) if x.endswith(".txt")])

    def reader(self):
        for file_name in self.text_files:
            with self.path.joinpath(file_name).open(mode='r') as file:
                txt = ""
                for line in file:
                    txt += line
                txt = set(word_tokenize(txt))
                txt = txt - set(stopwords.words('english'))
            self.documents[file_name] = txt


if __name__ == "__main__":
    extractor = TextReader("./shakespeare/")
    extractor.reader()
    __import__('IPython').embed()    
