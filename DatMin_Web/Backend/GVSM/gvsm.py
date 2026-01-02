import math


class GVSMModel:
    def __init__(self, documents):
        """
        documents: List[List[str]]
        Example:
        [
            ["cinta", "usus"],
            ["teknolog", "inovas", "ndidik"],
            ...
        ]
        """

        # -----------------------------
        # Validation
        # -----------------------------
        if not isinstance(documents, list):
            raise TypeError("documents must be a list of token lists")

        if len(documents) == 0:
            raise ValueError("documents cannot be empty")

        for doc in documents:
            if not isinstance(doc, list):
                raise TypeError("each document must be a list of tokens")
            if not all(isinstance(t, str) for t in doc):
                raise TypeError("each token must be a string")

        self.documents = documents

        # -----------------------------
        # Build Vocabulary
        # -----------------------------
        self.vocab = {}
        for doc in documents:
            for term in doc:
                if term not in self.vocab:
                    self.vocab[term] = len(self.vocab)

        self.V = len(self.vocab)

        # -----------------------------
        # Document TF Vectors
        # -----------------------------
        self.doc_vectors = [self._tf_vector(doc) for doc in documents]

        # -----------------------------
        # Term–Term Similarity Matrix
        # -----------------------------
        self.S = self._build_similarity_matrix()

    # -----------------------------
    # Internal Helpers
    # -----------------------------

    def _tf_vector(self, tokens):
        vec = [0] * self.V
        for term in tokens:
            if term in self.vocab:
                vec[self.vocab[term]] += 1
        return vec

    def _build_similarity_matrix(self):
        S = [[0] * self.V for _ in range(self.V)]

        # Co-occurrence counting
        for doc in self.doc_vectors:
            terms = [i for i, f in enumerate(doc) if f > 0]
            for i in terms:
                for j in terms:
                    S[i][j] += 1

        # Normalize
        for i in range(self.V):
            for j in range(self.V):
                if S[i][i] != 0 and S[j][j] != 0:
                    S[i][j] /= math.sqrt(S[i][i] * S[j][j])

        return S

    def _dot(self, a, b):
        return sum(a[i] * b[i] for i in range(len(a)))

    def _mat_vec_mul(self, M, v):
        result = [0] * len(v)
        for i in range(len(v)):
            for j in range(len(v)):
                result[i] += M[i][j] * v[j]
        return result

    def _gvsm_similarity(self, d, q):
        Sq = self._mat_vec_mul(self.S, q)
        Sd = self._mat_vec_mul(self.S, d)

        numerator = self._dot(d, Sq)
        denominator = math.sqrt(self._dot(d, Sd)) * math.sqrt(self._dot(q, Sq))

        return numerator / denominator if denominator != 0 else 0.0

    # -----------------------------
    # Public API (Flask-safe)
    # -----------------------------

    def match(self, query_tokens, top_n=None):
        """
        query_tokens: List[str]
        """
        if not isinstance(query_tokens, list):
            raise TypeError("query_tokens must be a list of strings")

        if not all(isinstance(t, str) for t in query_tokens):
            raise TypeError("query_tokens must contain only strings")

        q_vec = self._tf_vector(query_tokens)

        scores = []
        for i, d_vec in enumerate(self.doc_vectors):
            score = self._gvsm_similarity(d_vec, q_vec)
            scores.append((i, score))

        scores.sort(key=lambda x: -x[1])

        if top_n is not None:
            scores = scores[:top_n]

        return [
            {
                "doc_id": idx,
                "score": float(score),
                "document": self.documents[idx]
            }
            for idx, score in scores
        ]
