from langchain_community.retrievers import BM25Retriever
import joblib
from pathlib import Path

class BM25:
    """
    langchain_community.retrievers.BM25Retriever wrapper that resolves creation via
    documents or index and enables retrieving documents.

    Parameters
    ----------
    retriever : langchain_community.retrievers.BM25Retriever
        BM25 retriever by LangChain.

    Attributes
    ----------
    processed_data : ndarray
        The data after applying the transformations.
    history : list of str
        A log of all operations performed on the instance.

    See Also
    --------
    DataCleaner : A class for pre-processing raw strings.

    Examples
    --------
    >>> retriever = BM25Retriever.from_documents(
            docs,
            k=k,
            preprocess_func=func,
        )
    >>> bm25 = BM25(retriever)
    """
    INDEX_FILENAME = "bm25_index.joblib"

    def __init__(self, retriever):
        """
        Construct the BM25 instance. See docstring above for class details.
        """
        self.retriever = retriever
    
    @staticmethod
    def dump_index(retriever, dir_path):
        """
        Dump the created BM25Retriever index.

        Parameters
        ----------
        retriever : langchain_community.retrievers.BM25Retriever
            (Built) BM25 retriever by LangChain.
        dir_path : pathlib.Path
            directory path for saving the index.

        Returns
        -------
        list of str
            the path to where the index is saved.
        """
        dir_path.mkdir(parents=True, exist_ok=True)
        return joblib.dump(retriever, dir_path / BM25.INDEX_FILENAME)

    @classmethod
    def from_documents(cls, docs, k, func, save_path=None):
        """
        Created a BM25 instance from the given documents and configuration.
        Dump the index in the given path.

        Parameters
        ----------
        docs : langchain_core.documents.Document
            documents used for constructing BM25Retriever.
        k : int
            number of documents to retrieve.
        func : function
            function that preprocesses text prior to vectorization.
        save_path : string
            where the created BM25Retriever index is saved to.

        Returns
        -------
        BM25
            an instance of this class.
        """
        retriever = BM25Retriever.from_documents(
            docs,
            k=k,
            preprocess_func=func,
        )
        if save_path is not None:
            cls.dump_index(retriever, save_path)
        return cls(retriever)

    @classmethod
    def from_index(cls, index_path):
        """
        Created a BM25 instance from the given BM25Retriever index path.

        Parameters
        ----------
        index_path : pathlib.Path
            path to the saved BM25Retriever index.

        Returns
        -------
        BM25
            an instance of this class.
        """
        if index_path.is_dir():
            index_path = index_path / cls.INDEX_FILENAME
        retriever = joblib.load(index_path)
        return cls(retriever)
    
    @classmethod
    def from_index_or_documents(cls, docs, k, func, index_path):
        """
        Create a BM25 instance from the given BM25Retriever index path, if the path exists.
        Otherwise, create a BM25 instance from the given documents and configuration, and then
        dump the index in the given path. 

        Parameters
        ----------
        docs : langchain_core.documents.Document
            documents used for constructing BM25Retriever.
        k : int
            number of documents to retrieve.
        func : function
            function that preprocesses text prior to vectorization.
        index_path : string
            where the created BM25Retriever index is retrieved from or saved to.

        Returns
        -------
        BM25
            an instance of this class.
        """
        if index_path.exists():
            return cls.from_index(index_path)

        return cls.from_documents(docs, k, func, save_path=index_path)
            
    def retrieve(self, query):
        """
        Retrieve the pre-specifed top k documents that best match the given query.

        Parameters
        ----------
        query : string
            user-given query.

        Returns
        -------
        list of `Document`.
            top k documents relevant to the query.
        """
        return self.retriever.invoke(query)
    
    def retrieve_with_scores(self, query, k=5):
        """
        Retrieve a list of dictionary; each contains a pre-specifed top k document
        that best match the given query with scores, and the corresponding matching score.

        Parameters
        ----------
        query : string
            user-given query.
        k : int
            number of documents

        Returns
        -------
        list of dict
            Top k highest scored documents and their respective scores.
        """
        # Asked GitHub Copilot how to retrieve the top 5 results with scores.
        query_tokens = self.retriever.preprocess_func(query)
        scores = self.retriever.vectorizer.get_scores(query_tokens)
        docs = self.retriever.docs
        # Find the index of the top k highest scores
        top_idx = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:k]
        # Return a list of documents with corresponding scores
        return [
            {"doc": docs[i], "score": float(scores[i])}
            for i in top_idx
        ]