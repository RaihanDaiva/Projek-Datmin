from flask import Flask, request, jsonify
from flask_cors import CORS
import os

from tokenizing import Tokenizer
from filtering import StopwordFilter
from indonesian_porter_stemmer import IndonesianPorterStemmer
from preprocessing_pipeline import PreprocessingPipeline
from vector_space_model import VectorSpaceModel  # TIDAK DIUBAH

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = os.path.join(os.getcwd(), 'Projek/DatMin_Web/Backend/uploads')

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
@app.route("/search", methods=["POST"])
def search():
    data = request.get_json()
    query = data.get("query", "").strip()

    if not query:
        return jsonify([])

    # Load & preprocessing dokumen
    documents_raw, file_names = load_documents()
    doc_tokens = pipeline.process_documents(documents_raw)

    # VSM
    vsm = VectorSpaceModel(doc_tokens)

    # Preprocess query
    query_tokens = pipeline.process_query(query)
    query_string = " ".join(query_tokens)

    # Matching
    results = vsm.match(query_string)

    # Format output (untuk frontend)
    response = []
    for rank, (doc_id, score) in enumerate(results, start=1):
        response.append({
            "documentId": doc_id,
            "documentName": file_names[doc_id],
            "similarity": round(score * 100, 2),  # persen
            "rank": rank,
            "source": "server"
        })

    return jsonify(response)

# @app.route("/search", methods=["POST"])
# def search():
#     query = request.json["query"]

#     # preprocess query
#     query_tokens = pipeline.process_query(query)
#     query_string = " ".join(query_tokens)

#     # VSM
#     results = vsm.match(query_string)

#     response = []

#     for doc_id, score in results:
#         doc_text = documents_raw[doc_id]

#         preprocessing_detail = pipeline.process_document_with_steps(doc_text)

#         response.append({
#             "doc_id": doc_id,
#             "filename": file_names[doc_id],
#             "similarity": round(score * 100, 2),
#             "preprocessing": preprocessing_detail
#         })

#     return jsonify(response)


if __name__ == "__main__":
    app.run(debug=True)
