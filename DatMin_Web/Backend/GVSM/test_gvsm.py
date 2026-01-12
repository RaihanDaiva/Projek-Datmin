import math

# -----------------------------
# 1. Data
# -----------------------------
documents = [
    "Pendidikan dan Pembelajaran di Era Digital Pendidikan merupakan aspek fundamental dalam pembangunan sumber daya manusia. Melalui pendidikan, masyarakat dapat mengembangkan pengetahuan, keterampilan, dan sikap yang diperlukan untuk menghadapi berbagai tantangan kehidupan. Dalam era digital seperti sekarang ini, pembelajaran mengalami transformasi yang sangat signifikan. Teknologi informasi dan komunikasi telah mengubah cara guru mengajar dan siswa belajar. Pembelajaran tidak lagi terbatas pada ruang kelas tradisional, tetapi dapat dilakukan secara daring dari mana saja. Perkembangan teknologi pendidikan membawa dampak positif dan negatif. Di satu sisi, teknologi memudahkan akses terhadap berbagai sumber belajar. Siswa dapat mengakses perpustakaan digital, mengikuti kursus online, dan berkolaborasi dengan pelajar dari berbagai negara. Di sisi lain, ketergantungan pada teknologi dapat mengurangi interaksi sosial langsung dan keterampilan komunikasi interpersonal. Para pendidik perlu beradaptasi dengan perubahan ini. Mereka harus menguasai teknologi pembelajaran dan mengintegrasikannya dengan metode pengajaran yang efektif. Pelatihan guru secara berkelanjutan menjadi sangat penting untuk memastikan kualitas pendidikan tetap terjaga. Kesimpulannya, pendidikan di era digital memerlukan keseimbangan antara pemanfaatan teknologi dan mempertahankan nilai-nilai pembelajaran tradisional. Dengan pendekatan yang tepat, teknologi dapat menjadi alat yang powerful untuk meningkatkan kualitas pendidikan dan menciptakan generasi yang siap menghadapi tantangan masa depan.",
    "Pembelajaran Pendidikan Mandiri",
    "retrieval of information"
]

query = "pendidikan digital"

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
