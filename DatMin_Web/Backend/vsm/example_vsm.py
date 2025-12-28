import math

# ---------- Step 1: Example Documents ----------
documents = [
    "Information retrieval is the process of finding relevant documents",
    "Vector space model represents documents as vectors",
    "We use cosine similarity for ranking in vector space model",
    "Retrieval and matching are core operations in IR systems"
]

# ---------- Step 2: Preprocess (Tokenize + Normalize) ----------
def tokenize(text):
    # Lowercase & simple split on spaces
    return text.lower().split()

indexed_docs = [tokenize(doc) for doc in documents]
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
