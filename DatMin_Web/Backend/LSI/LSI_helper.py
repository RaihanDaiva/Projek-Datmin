import numpy as np
import math


class LSIModel:
    def __init__(self, documents, k=2):
        """
        Build LSI model from documents
        """
        self.documents = documents
        self.k = k

        # preprocessing
        self.tokenized_docs = [self._tokenize(d) for d in documents]
        self.vocab = sorted({w for doc in self.tokenized_docs for w in doc})
        self.word_index = {w: i for i, w in enumerate(self.vocab)}

        # build model
        self.tf = self._compute_tf()
        self.idf = self._compute_idf(self.tf)
        self.tfidf = self.tf * self.idf[:, None]

        self._compute_lsi()

    # ------------------------
    # Internal helpers
    # ------------------------

    def _tokenize(self, text):
        return text.lower().split()

    def _compute_tf(self):
        tf = np.zeros((len(self.vocab), len(self.documents)))
        for j, doc in enumerate(self.tokenized_docs):
            for term in doc:
                tf[self.word_index[term], j] += 1
        return tf

    def _compute_idf(self, tf_matrix):
        n_docs = tf_matrix.shape[1]
        idf = np.zeros(tf_matrix.shape[0])
        for i in range(tf_matrix.shape[0]):
            df = np.count_nonzero(tf_matrix[i, :])
            idf[i] = math.log((n_docs + 1) / (df + 1)) + 1
        return idf

    def _compute_lsi(self):
        U, S, Vt = np.linalg.svd(self.tfidf, full_matrices=False)

        self.Uk = U[:, :self.k]
        self.Sk = np.diag(S[:self.k])
        self.Vtk = Vt[:self.k, :]

        # document vectors in LSI space
        self.doc_vectors = self.Sk @ self.Vtk

    def _cosine(self, a, b):
        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

    # ------------------------
    # Public API (used by Flask)
    # ------------------------

    def match(self, query, top_n=None):
        """
        Match a query against indexed documents
        """
        q_tokens = self._tokenize(query)
        q_vec = np.zeros(len(self.vocab))

        for t in q_tokens:
            if t in self.word_index:
                q_vec[self.word_index[t]] += 1

        q_tfidf = q_vec * self.idf
        q_lsi = self.Uk.T @ q_tfidf

        print("q_vec:", q_vec)
        print("q_tfidf:", q_tfidf)
        print("q_lsi:", q_lsi)
        print("||q_lsi||:", np.linalg.norm(q_lsi))

        scores = []
        print("====> self.doc_vectors.shape: ", self.doc_vectors)
        for i in range(self.doc_vectors.shape[1]):
            score = self._cosine(q_lsi, self.doc_vectors[:, i])
            scores.append((i, score))

        scores.sort(key=lambda x: -x[1])

        if top_n:
            scores = scores[:top_n]
        
        print(" ===> Score: ", scores)

        return [
            {
                "doc_id": idx,
                "score": score,
                "document": self.documents[idx]
            }
            for idx, score in scores
        ]
