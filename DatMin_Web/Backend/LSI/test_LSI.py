import numpy as np
import math

np.set_printoptions(precision=4, suppress=True)

print("========== START DEBUG ==========\n")

# ------------------------
# 1) Basic Preprocessing
# ------------------------

documents = [
    "information retrieval is the science of searching",
    "latent semantic indexing finds hidden structure",
    "information retrieval with latent semantic analysis"
]

print("Documents:")
for i, d in enumerate(documents):
    print(f"Doc {i}: {d}")
print()

def tokenize(text):
    return text.lower().split()

tokenized_docs = [tokenize(d) for d in documents]

print("Tokenized Documents:")
for i, td in enumerate(tokenized_docs):
    print(f"Doc {i}: {td}")
print()

# build vocabulary
vocab = sorted({word for doc in tokenized_docs for word in doc})
word_index = {w: i for i, w in enumerate(vocab)}

print("Vocabulary:")
print(vocab)
print()

print("Word Index Mapping:")
for k, v in word_index.items():
    print(f"{k} -> {v}")
print()

# ------------------------
# 2) Compute TF Matrix
# ------------------------

tf = np.zeros((len(vocab), len(documents)))

for j, doc in enumerate(tokenized_docs):
    for term in doc:
        tf[word_index[term], j] += 1

print("TF Matrix (terms x documents):")
print(tf)
print()

# ------------------------
# 3) Compute IDF Vector
# ------------------------

def compute_idf(tf_matrix):
    n_docs = tf_matrix.shape[1]
    idf = np.zeros(tf_matrix.shape[0])
    for i in range(tf_matrix.shape[0]):
        df = np.count_nonzero(tf_matrix[i, :])
        idf[i] = math.log((n_docs + 1) / (df + 1)) + 1
    return idf

idf = compute_idf(tf)

print("IDF Vector:")
for term, idx in word_index.items():
    print(f"{term}: {idf[idx]:.4f}")
print()

# ------------------------
# 4) Build TF-IDF Matrix
# ------------------------

tfidf = tf * idf[:, None]

print("TF-IDF Matrix:")
print(tfidf)
print()

# ------------------------
# 5) Apply SVD (LSI)
# ------------------------

U, S, Vt = np.linalg.svd(tfidf, full_matrices=False)

print("U Matrix (Term-Concept):")
print(U)
print()

print("Singular Values:")
print(S)
print()

print("Vt Matrix (Concept-Document):")
print(Vt)
print()

# choose k components
k = 2
Uk = U[:, :k]
Sk = np.diag(S[:k])
Vtk = Vt[:k, :]

print(f"Reduced Uk (k={k}):")
print(Uk)
print()

print("Reduced Sk:")
print(Sk)
print()

print("Reduced Vtk:")
print(Vtk)
print()

# LSI document vectors
lsi_doc_vectors = Sk @ Vtk

print("LSI Document Vectors (k x documents):")
print(lsi_doc_vectors)
print()

# ------------------------
# 6) Query -> LSI
# ------------------------

query = "latent analysis retrieval"
print("Query:", query)

q_tokens = tokenize(query)
print("Query Tokens:", q_tokens)
print()

q_vec = np.zeros((len(vocab),))
for t in q_tokens:
    if t in word_index:
        q_vec[word_index[t]] += 1

print("Query Term Frequency Vector:")
print(q_vec)
print()

q_tfidf = q_vec * idf
print("Query TF-IDF Vector:")
print(q_tfidf)
print()

q_lsi = Uk.T @ q_tfidf

print("Query LSI Vector:")
print(q_lsi)
print()

# ------------------------
# 7) Cosine Similarity
# ------------------------

def cosine(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

scores = []
for di in range(lsi_doc_vectors.shape[1]):
    doc_vec = lsi_doc_vectors[:, di]
    sim = cosine(q_lsi, doc_vec)
    scores.append(sim)
    print(f"Cosine similarity (Query vs Doc {di}): {sim:.4f}")

print()

ranking = sorted(enumerate(scores), key=lambda x: -x[1])

print("Final Ranking:")
for idx, score in ranking:
    print(f"Doc {idx} (score={score:.4f}): {documents[idx]}")

print("\n=========== END DEBUG ===========")
