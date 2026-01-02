import math

# -----------------------------
# 1. Data
# -----------------------------
documents = [
    "information retrieval model",
    "generalized vector space model",
    "retrieval of information"
]

query = "retrieval of information"

# -----------------------------
# 2. Tokenization
# -----------------------------
def tokenize(text):
    return text.lower().split()

# -----------------------------
# 3. Vocabulary Construction
# -----------------------------
vocab = {}
for doc in documents:
    for term in tokenize(doc):
        if term not in vocab:
            vocab[term] = len(vocab)

V = len(vocab)

# -----------------------------
# 4. Term Frequency Vectors
# -----------------------------
def tf_vector(text, vocab):
    vec = [0] * len(vocab)
    for term in tokenize(text):
        vec[vocab[term]] += 1
    return vec

doc_vectors = [tf_vector(doc, vocab) for doc in documents]
query_vector = tf_vector(query, vocab)

# -----------------------------
# 5. Term–Term Similarity Matrix (Co-occurrence)
# -----------------------------
S = [[0] * V for _ in range(V)]

# Count co-occurrences
for doc in doc_vectors:
    terms = [i for i, f in enumerate(doc) if f > 0]
    for i in terms:
        for j in terms:
            S[i][j] += 1

# Normalize similarity matrix
for i in range(V):
    for j in range(V):
        if S[i][i] != 0 and S[j][j] != 0:
            S[i][j] /= math.sqrt(S[i][i] * S[j][j])

# -----------------------------
# 6. Basic Linear Algebra
# -----------------------------
def dot(a, b):
    return sum(a[i] * b[i] for i in range(len(a)))

def mat_vec_mul(M, v):
    result = [0] * len(v)
    for i in range(len(v)):
        for j in range(len(v)):
            result[i] += M[i][j] * v[j]
    return result

# -----------------------------
# 7. GVSM Similarity
# -----------------------------
def gvsm_similarity(d, q, S):
    Sq = mat_vec_mul(S, q)
    Sd = mat_vec_mul(S, d)

    numerator = dot(d, Sq)
    denominator = math.sqrt(dot(d, Sd)) * math.sqrt(dot(q, Sq))

    return numerator / denominator if denominator != 0 else 0

# -----------------------------
# 8. Retrieval
# -----------------------------
print("GVSM Retrieval Results:\n")

for i, d in enumerate(doc_vectors):
    score = gvsm_similarity(d, query_vector, S)
    print(f"Document {i+1}: {score:.4f}")

# -----------------------------
# 9. Debug (Optional)
# -----------------------------
print("\nVocabulary:")
for term, idx in vocab.items():
    print(f"{idx}: {term}")
