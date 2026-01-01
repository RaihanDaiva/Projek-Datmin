import os
from tokenizing import Tokenizer
from filtering import StopwordFilter
from indonesian_porter_stemmer import IndonesianPorterStemmer
from preprocessing_pipeline import PreprocessingPipeline
from vector_space_model import VectorSpaceModel   # <- class VSM kamu (TIDAK DIUBAH)

# ======================
# INISIALISASI PIPELINE
# ======================
tokenizer = Tokenizer()
filtering = StopwordFilter()
stemmer = IndonesianPorterStemmer()

pipeline = PreprocessingPipeline(
    tokenizer=tokenizer,
    stopword_filter=filtering,
    stemmer=stemmer
)

# ======================
# BACA DOKUMEN .TXT
# ======================
folder_path = "./tes file"

documents_raw = []
file_names = []

for file in sorted(os.listdir(folder_path)):
    if file.endswith(".txt"):
        file_path = os.path.join(folder_path, file)
        with open(file_path, "r", encoding="utf-8") as f:
            documents_raw.append(f.read())
            file_names.append(file)

# ======================
# PREPROCESSING DOKUMEN
# ======================
doc_tokens = pipeline.process_documents(documents_raw)

print("\n=== HASIL PREPROCESSING DOKUMEN ===")
for i, tokens in enumerate(doc_tokens):
    print(f"D{i+1} ({file_names[i]}):")
    print(tokens)
    print("-" * 50)

# =====================================================
# VSM INPUT → HASIL PREPROCESSING (LIST OF LIST)
# =====================================================
vsm = VectorSpaceModel(doc_tokens)

# ======================
# QUERY USER
# ======================
query = input("\nMasukkan query: ")

# IMPORTANT:
# Query dipreprocess TERLEBIH DAHULU agar konsisten
query_tokens = pipeline.process_query(query)

# Ubah kembali ke string karena VSM.match()
# menerima QUERY berupa STRING
query_string = " ".join(query_tokens)

# ======================
# VSM MATCHING
# ======================
results = vsm.match(query_string)

# ======================
# OUTPUT RANKING
# ======================
print("\n=== HASIL VSM (Cosine Similarity) ===")
for doc_id, score in results:
    print(f"D{doc_id+1} ({file_names[doc_id]}): score = {score:.4f}")
