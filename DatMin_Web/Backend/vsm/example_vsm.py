import math

# ---------- Step 1: Example Documents ----------
# documents = [
#     "Information retrieval is the process of finding relevant documents",
#     "Vector space model represents documents as vectors",
#     "We use cosine similarity for ranking in vector space model",
#     "Retrieval and matching are core operations in IR systems"
# ]

documents = [
    ['simpul', 'ndidik', 'era', 'gital', 'rluk', 'imbang', 'manfaat', 'teknolog', 'mpertahank', 'nila', 'nila', 'mbelajar', 'tradisional', 'ndekat', 'tepat', 'teknolog', 'tjad', 'alat', 'powerful', 'ningkatk', 'kualitas', 'ndidik', 'nciptak', 'generas', 'siap', 'khadap', 'tantang', 'masa', 'dep'], 
    ['ndidik', 'mbelajar', 'era', 'gital', 'ndidik', 'rupak', 'aspek', 'fundamental', 'mbangun', 'sumber', 'daya', 'manusia', 'ndidik', 'masyarakat', 'ngembangk', 'ngetahu', 'ampil', 'sikap', 'rlu', 'khadap', 'baga', 'tantang', 'hidup', 'era', 'gital', 'pert', 'karang', 'mbelajar', 'kalam', 'transformas', 'signif', 'teknolog', 'informas', 'komunikas', 'kubah', 'cara', 'guru', 'kajar', 'siswa', 'ajar', 'mbelajar', 'batas', 'ruang', 'las', 'tradisional', 'laku', 'daring', 'mana', 'rkembang', 'teknolog', 'ndidik', 'bawa', 'dampak', 'positif', 'negatif', 'satu', 'sis', 'teknolog', 'mudahk', 'akses', 'hadap', 'baga', 'sumber', 'ajar', 'siswa', 'kakses', 'rpustaka', 'gital', 'kikut', 'kursus', 'online', 'kolaboras', 'lajar', 'baga', 'negara', 'sis', 'lain', 'gantung', 'teknolog', 'kurang', 'interaks', 'sosial', 'langsung', 'ampil', 'komunikas', 'interpersonal', 'ndidik', 'rlu', 'adaptas', 'rubah', 'kuasa', 'teknolog', 'mbelajar', 'ngintegrasik', 'tode', 'ngajar', 'efektif', 'latih', 'guru', 'lanjut', 'tjad', 'nting', 'mastik', 'kualitas', 'ndidik', 'tetap', 'jaga', 'simpul', 'ndidik', 'era', 'gital', 'rluk', 'imbang', 'manfaat', 'teknolog', 'mpertahank', 'nila', 'nila', 'mbelajar', 'tradisional', 'ndekat', 'tepat', 'teknolog', 'tjad', 'alat', 'powerful', 'ningkatk', 'kualitas', 'ndidik', 'nciptak', 'generas', 'siap', 'khadap', 'tantang', 'masa', 'dep']
]

# documents = [
#     ['simpul', 'ndidik', 'era', 'gital', 'rluk', 'imbang', 'manfaat', 'teknolog', 'mpertahank', 'nila', 'nila', 'mbelajar', 'tradisional', 'ndekat', 'tepat', 'teknolog', 'tjad', 'alat', 'powerful', 'ningkatk', 'kualitas', 'ndidik', 'nciptak', 'generas', 'siap', 'khadap', 'tantang', 'masa', 'dep'], 
#     ['ndidik', 'mbelajar', 'era', 'gital', 'ndidik', 'rupak', 'aspek', 'fundamental', 'mbangun', 'sumber', 'daya', 'manusia', 'ndidik', 'masyarakat', 'ngembangk', 'ngetahu', 'ampil', 'sikap', 'rlu', 'khadap', 'baga', 'tantang', 'hidup', 'era', 'gital', 'pert', 'karang', 'mbelajar', 'kalam', 'transformas', 'signif', 'teknolog', 'informas', 'komunikas', 'kubah', 'cara', 'guru', 'kajar', 'siswa', 'ajar', 'mbelajar', 'batas', 'ruang', 'las', 'tradisional', 'laku', 'daring', 'mana', 'rkembang', 'teknolog', 'ndidik', 'bawa', 'dampak', 'positif', 'negatif', 'satu', 'sis', 'teknolog', 'mudahk', 'akses', 'hadap', 'baga', 'sumber', 'ajar', 'siswa', 'kakses', 'rpustaka', 'gital', 'kikut', 'kursus', 'online', 'kolaboras', 'lajar', 'baga', 'negara', 'sis', 'lain', 'gantung', 'teknolog', 'kurang', 'interaks', 'sosial', 'langsung', 'ampil', 'komunikas', 'interpersonal', 'ndidik', 'rlu', 'adaptas', 'rubah', 'kuasa', 'teknolog', 'mbelajar', 'ngintegrasik', 'tode', 'ngajar', 'efektif', 'latih', 'guru', 'lanjut', 'tjad', 'nting', 'mastik', 'kualitas', 'ndidik', 'tetap', 'jaga', 'simpul', 'ndidik', 'era', 'gital', 'rluk', 'imbang', 'manfaat', 'teknolog', 'mpertahank', 'nila', 'nila', 'mbelajar', 'tradisional', 'ndekat', 'tepat', 'teknolog', 'tjad', 'alat', 'powerful', 'ningkatk', 'kualitas', 'ndidik', 'nciptak', 'generas', 'siap', 'khadap', 'tantang', 'masa', 'dep']
# ]

# ---------- Step 2: Preprocess (Tokenize + Normalize) ----------
def tokenize(text):
    # Lowercase & simple split on spaces
    return text.lower().split()

indexed_docs = []
for i, doc in enumerate(documents):
    # If it's a list of words, assume already tokenized
    if isinstance(doc, list):
        # Verify that each element is a string
        if not all(isinstance(token, str) for token in doc):
            raise ValueError(f"Document at index {i} contains non-string tokens")
        indexed_docs.append([token.lower() for token in doc])

    # If it's a string, tokenize it
    elif isinstance(doc, str):
        indexed_docs.append(tokenize(doc))

    else:
        raise ValueError(
            f"Document at index {i} must be a string or list of strings, got {type(doc)}"
        )

# indexed_docs = [tokenize(doc) for doc in documents]
print("\n<=========== Indexed/Tokenized Docs ============> START")
print(indexed_docs)
print("<=========== Indexed/Tokenized Docs ============> END\n")

# ---------- Step 3: Build Vocabulary ----------
vocab = sorted(set(term for doc in indexed_docs for term in doc))

# Map each term to an index
term_index = {term: i for i, term in enumerate(vocab)}

# ---------- Step 4: Build Document Vectors (TF) ----------
def vectorize(tokens):
    vec = [0] * len(vocab)
    for term in tokens:
        if term in term_index:
            vec[term_index[term]] += 1
    print("Vectorized", vec)
    return vec

doc_vectors = [vectorize(doc) for doc in indexed_docs]

# ---------- Step 5: Query ----------
query = "vector space retrieval"
# query = "Siswa Sosial Sumber"
q_tokens = tokenize(query)
query_vec = vectorize(q_tokens)

# ---------- Step 6: Cosine Similarity ----------
def cosine_similarity(v1, v2): # Similarity (Di, Q)
    dot = sum(x * y for x, y in zip(v1, v2))
    norm1 = math.sqrt(sum(x * x for x in v1))
    norm2 = math.sqrt(sum(y * y for y in v2))
    if norm1 == 0 or norm2 == 0:
        return 0.0
    return dot / (norm1 * norm2)

# Compute similarity scores
scores = [(i + 1, cosine_similarity(query_vec, doc_vectors[i])) 
          for i in range(len(doc_vectors))]

# Sort results by score descending
ranked = sorted(scores, key=lambda x: x[1], reverse=True)

# ---------- Step 7: Show Results ----------
print("Vocabulary:", vocab)
print("\nQuery Vector:", query_vec)
print("\nDocument Similarity Rankings:")
for doc_id, score in ranked:
    print(f"D{doc_id} (score: {score:.4f})")