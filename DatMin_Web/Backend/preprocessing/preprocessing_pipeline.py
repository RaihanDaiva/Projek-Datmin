# class PreprocessingPipeline:
#     """
#     Pipeline preprocessing untuk:
#     - Dokumen koleksi
#     - Query user
#     """

#     def __init__(self, tokenizer, stopword_filter, stemmer):
#         self.tokenizer = tokenizer
#         self.stopword_filter = stopword_filter
#         self.stemmer = stemmer

#     def process_document(self, text):
#         """
#         Preprocessing satu dokumen

#         Returns:
#             list: token hasil preprocessing
#         """
#         tokens = self.tokenizer.process_text(text)
#         tokens = self.stopword_filter.filter_tokens(tokens)
#         tokens = self.stemmer.stem_tokens(tokens)
#         return tokens

#     def process_documents(self, documents):
#         """
#         Preprocessing banyak dokumen

#         Args:
#             documents (list): list dokumen (string)

#         Returns:
#             list: list of list token
#         """
#         processed_docs = []

#         for doc in documents:
#             tokens = self.process_document(doc)
#             processed_docs.append(tokens)

#         return processed_docs

#     def process_query(self, query):
#         """
#         Preprocessing query user

#         Args:
#             query (str)

#         Returns:
#             list: token query
#         """
#         return self.process_document(query)

class PreprocessingPipeline:

    def __init__(self, tokenizer, stopword_filter, stemmer):
        self.tokenizer = tokenizer
        self.stopword_filter = stopword_filter
        self.stemmer = stemmer

    # ===============================
    # UNTUK VSM (list token saja)
    # ===============================
    def process_document(self, text):
        tokens = self.tokenizer.process_text(text.lower())
        tokens = self.stopword_filter.filter_tokens(tokens)
        tokens = self.stemmer.stem_tokens(tokens)
        return tokens

    def process_documents(self, documents):
        return [self.process_document(doc) for doc in documents]

    def process_query(self, query):
        return self.process_document(query)

    # ===============================
    # UNTUK DETAIL PREPROCESSING UI
    # ===============================
    def process_document_with_steps(self, text):
        case_folding = text.lower()

        tokens = self.tokenizer.process_text(case_folding)

        filtered_tokens, removed_stopwords = \
            self.stopword_filter.filter_with_removed(tokens)

        stemmed = self.stemmer.stem_tokens(filtered_tokens)

        return {
            "original_text": text,
            "case_folding": case_folding,
            "tokens": tokens,
            "removed_stopwords": removed_stopwords,
            "filtered_tokens": filtered_tokens,
            "stemming": [
                {
                    "original": filtered_tokens[i],
                    "stemmed": stemmed[i]
                }
                for i in range(len(filtered_tokens))
            ]
        }

