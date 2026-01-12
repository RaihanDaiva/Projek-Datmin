from flask import Flask, request, jsonify
from flask_cors import CORS
import os


from tokenizing import Tokenizer
from filtering import StopwordFilter
from indonesian_porter_stemmer import IndonesianPorterStemmer
from preprocessing_pipeline import PreprocessingPipeline
from vector_space_model import VectorSpaceModel  # TIDAK DIUBAH
from GVSM.gvsm import GVSMModel
from cache_utils import save_cache, load_cache

app = Flask(__name__)
CORS(app)

# UPLOAD_FOLDER = os.path.join(os.getcwd(), 'Projek/DatMin_Web/Backend/uploads')
UPLOAD_FOLDER = os.path.join('DatMin_Web/Backend/uploads')

# ======================
# INISIALISASI PIPELINE
# ======================
tokenizer = Tokenizer()
filtering = StopwordFilter()
stemmer = IndonesianPorterStemmer()


DOCUMENT_CACHE = None
TOKEN_CACHE = None
FILENAME_CACHE = None
CACHE_PATH = os.path.join('DatMin_Web/Backend', 'preprocessing_cache.pkl')
def get_uploads_state():
    """Return a tuple of (filenames, mtimes) for all .txt, .docx, .pdf in uploads."""
    state = []
    for file in sorted(os.listdir(UPLOAD_FOLDER)):
        ext = os.path.splitext(file)[1].lower()
        if ext in {'.txt', '.docx', '.pdf'}:
            path = os.path.join(UPLOAD_FOLDER, file)
            try:
                mtime = os.path.getmtime(path)
                state.append((file, mtime))
            except Exception:
                continue
    return state


def load_documents_cached():
    global DOCUMENT_CACHE, TOKEN_CACHE, FILENAME_CACHE

    uploads_state = get_uploads_state()
    cache = load_cache(CACHE_PATH)
    if cache:
        cached_state = cache.get('uploads_state')
        if cached_state == uploads_state:
            DOCUMENT_CACHE = cache['documents_raw']
            TOKEN_CACHE = cache['doc_tokens']
            FILENAME_CACHE = cache['file_names']
            return DOCUMENT_CACHE, TOKEN_CACHE, FILENAME_CACHE

    # If cache is missing or outdated, reload and reprocess
    documents_raw, file_names = load_documents()
    doc_tokens = pipeline.process_documents(documents_raw)

    DOCUMENT_CACHE = documents_raw
    TOKEN_CACHE = doc_tokens
    FILENAME_CACHE = file_names

    save_cache({
        'uploads_state': uploads_state,
        'documents_raw': documents_raw,
        'doc_tokens': doc_tokens,
        'file_names': file_names
    }, CACHE_PATH)

    return DOCUMENT_CACHE, TOKEN_CACHE, FILENAME_CACHE


pipeline = PreprocessingPipeline(
    tokenizer=tokenizer,
    stopword_filter=filtering,
    stemmer=stemmer
)

# ======================    
# LOAD DOKUMEN .TXT
# ======================
def load_documents():
    documents_raw = []
    file_names = []

    for file in sorted(os.listdir(UPLOAD_FOLDER)):
        path = os.path.join(UPLOAD_FOLDER, file)
        ext = os.path.splitext(file)[1].lower()
        if ext == ".txt":
            with open(path, "r", encoding="utf-8") as f:
                documents_raw.append(f.read())
                file_names.append(file)
        elif ext == ".docx":
            try:
                text = stemmer.read_docx_file(path)
                documents_raw.append(text)
                file_names.append(file)
            except Exception as e:
                print(f"Error reading DOCX {file}: {e}")
        elif ext == ".pdf":
            try:
                text = stemmer.read_pdf_file(path)
                documents_raw.append(text)
                file_names.append(file)
            except Exception as e:
                print(f"Error reading PDF {file}: {e}")

    return documents_raw, file_names


# ======================
# API: GET DOKUMEN SERVER
# ======================
@app.route('/documents')
def list_documents():
    files = []
    for fname in os.listdir(UPLOAD_FOLDER):
        fpath = os.path.join(UPLOAD_FOLDER, fname)
        if os.path.isfile(fpath):
            ext = os.path.splitext(fname)[1]
            files.append({
                "id": fname,
                "name": fname,
                "type": ext,
                "status": "Available"
            })
    return jsonify(files)

# ======================
# API: SEARCH QUERY (VSM)
# ======================
# @app.route("/search", methods=["POST"])
# def search():
#     data = request.get_json()
#     query = data.get("query", "").strip()

#     if not query:
#         return jsonify([])

#     # Load & preprocessing dokumen
#     documents_raw, file_names = load_documents()
#     doc_tokens = pipeline.process_documents(documents_raw)

#     # VSM
#     vsm = VectorSpaceModel(doc_tokens)

#     # Preprocess query
#     query_tokens = pipeline.process_query(query)
#     query_string = " ".join(query_tokens)

#     # Matching
#     results = vsm.match(query_string)

#     # Format output (untuk frontend)
#     response = []
#     for rank, (doc_id, score) in enumerate(results, start=1):
#         response.append({
#             "documentId": doc_id,
#             "documentName": file_names[doc_id],
#             "similarity": round(score * 100, 2),  # persen
#             "rank": rank,
#             "source": "server"
#         })

#     return jsonify(response)

@app.route("/search", methods=["POST"])
def search():
    # 1. Ambil data JSON dengan aman
    data = request.get_json()
    if not data or "query" not in data:
         return jsonify({"error": "Query is required"}), 400
         
    query = data["query"].strip()

    # 2. Cek jika query kosong
    if not query:
        return jsonify([])

    # 3. Load & preprocessing dokumen
    documents_raw, doc_tokens, file_names = load_documents_cached()
    
    # Pastikan file_names valid
    if not file_names:
        return jsonify({"error": "No documents found"}), 500

    # doc_tokens sudah di-cache di load_documents_cached

    # 4. VSM
    # Option 1
    # vsm = VectorSpaceModel(doc_tokens)

    # Option 2
    # lsi_model = LSIModel(documents_raw, k=2)

    # Option 3
    # print("===========> doc_tokens", doc_tokens)
    # print("===========> documents_raw", documents_raw)
    gvsm = GVSMModel(doc_tokens)


    # 5. Preprocess query
    query_tokens = pipeline.process_query(query)
    query_string = " ".join(query_tokens)
    query_string = query_string.lower().split() # Tokenize Query Input
    print("===============>  ", query_string)

    # 6. Matching
    # results = vsm.match(query_string)
    # results = lsi_model.match(query_string)
    results = gvsm.match(query_string)

    response = []

    # 7. Loop hasil
    # print(results)
    for rank, result in enumerate(results, start=1):
        doc_id = result["doc_id"]
        score = result["score"]
        if doc_id < 0 or doc_id >= len(documents_raw):
            continue

        doc_text = documents_raw[doc_id]
        
        # Jalankan preprocessing detail
        preprocessing_detail = pipeline.process_document_with_steps(doc_text)

        # Ambil nama file
        current_filename = file_names[doc_id] if doc_id < len(file_names) else "Unknown File"

        response.append({
            "doc_id": doc_id,
            "documentName": current_filename,
            "filename": current_filename,     
            "similarity": round(score * 100, 2),
            "rank": rank,
            "preprocessing": preprocessing_detail,
            
            # --- PERBAIKAN DI SINI ---
            # Menambahkan penanda bahwa ini adalah data dari server,
            # sehingga UI tidak menampilkan logo upload.
            "source": "server" 
            # -------------------------
        })

    return jsonify(response)


if __name__ == "__main__":
    app.run(debug=True)
