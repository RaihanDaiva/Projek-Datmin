import math

class VectorSpaceModel:
    def __init__(self, documents):
        """
        Docstring for __init__
        
        :param self: Description
        ====================================>
        :param documents: Should be an array data type. Example:
        documents = [
        "Information retrieval is the process of finding relevant documents",
        "Vector space model represents documents as vectors",
        "We use cosine similarity for ranking in vector space model",
        "Retrieval and matching are core operations in IR systems"
        ]
        Each elements on the array is a String of text 
        """
        self.documents = documents
        self.indexed_docs = self._prepare_docs(documents)

        self.vocab = sorted(set(term for doc in self.indexed_docs for term in doc))
        self.term_index = {term: i for i, term in enumerate(self.vocab)}
        
        self.doc_vectors = [self.vectorize(doc) for doc in self.indexed_docs]

    def _prepare_docs(self, docs):
        """
        Convert raw strings to token lists, or validate already tokenized docs.
        """
        processed = []
        for i, doc in enumerate(docs):
            # If it's a list of words, assume already tokenized
            if isinstance(doc, list):
                # Verify that each element is a string
                if not all(isinstance(token, str) for token in doc):
                    raise ValueError(f"Document at index {i} contains non-string tokens")
                processed.append([token.lower() for token in doc])

            # If it's a string, tokenize it
            elif isinstance(doc, str):
                processed.append(self.tokenize(doc))

            else:
                raise ValueError(
                    f"Document at index {i} must be a string or list of strings, got {type(doc)}"
                )

        return processed

    def tokenize(self, text):
        return text.lower().split()

    def vectorize(self, tokens):
        vec = [0] * len(self.vocab)
        for term in tokens:
            if term in self.term_index:
                vec[self.term_index[term]] += 1 
        return vec

    def cosine_similarity(self, v1, v2):
        dot = sum(x * y for x, y in zip(v1, v2))
        norm1 = math.sqrt(sum(x * x for x in v1))
        norm2 = math.sqrt(sum(y * y for y in v2))
        if norm1 == 0 or norm2 == 0:
            return 0.0
        return dot / (norm1 * norm2)

    def match(self, query):
        # Tokenize & vectorize the query
        query_tokens = self.tokenize(query)
        query_vec = self.vectorize(query_tokens)
        
        # Compute similarity with each document
        scores = [
            (i, self.cosine_similarity(query_vec, self.doc_vectors[i]))
            for i in range(len(self.doc_vectors))
        ]
        # Sort by descending similarity
        ranked = sorted(scores, key=lambda x: x[1], reverse=True)
        return ranked
