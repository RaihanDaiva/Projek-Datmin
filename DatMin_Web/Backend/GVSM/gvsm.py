import numpy as np
import scipy.sparse as sp
from scipy.sparse import csr_matrix, diags

class GVSMModel:
    def __init__(self, documents):
        """
        Versi Optimized menggunakan Sparse Matrix untuk kecepatan tinggi.
        """
        # 1. Validation
        if not isinstance(documents, list) or len(documents) == 0:
            raise ValueError("Documents must be a non-empty list of token lists")
        
        self.documents = documents

        # 2. Build Vocabulary
        self.vocab = {}
        for doc in documents:
            for term in doc:
                if term not in self.vocab:
                    self.vocab[term] = len(self.vocab)
        
        self.V = len(self.vocab)
        self.doc_count = len(documents)

        # -----------------------------
        # 3. Build Document TF Matrix (Sparse)
        # -----------------------------
        # Kita gunakan lil_matrix untuk construct, lalu convert ke csr_matrix untuk math cepat
        print(f"Building TF Matrix for {self.doc_count} docs and {self.V} terms...")
        
        # Cara cepat buat sparse matrix: kumpulkan row, col, data
        rows, cols, data = [], [], []
        for doc_idx, doc in enumerate(documents):
            # Hitung frekuensi lokal dulu agar hemat loop
            term_counts = {}
            for term in doc:
                if term in self.vocab:
                    tid = self.vocab[term]
                    term_counts[tid] = term_counts.get(tid, 0) + 1
            
            for tid, count in term_counts.items():
                rows.append(doc_idx)
                cols.append(tid)
                data.append(float(count))

        # Matriks TF (N x V) dalam format Sparse CSR
        self.doc_vectors = csr_matrix((data, (rows, cols)), shape=(self.doc_count, self.V))

        # -----------------------------
        # 4. Term-Term Similarity Matrix (Sparse / Optimized)
        # -----------------------------
        print("Building Similarity Matrix...")
        self.S = self._build_similarity_matrix_optimized()

        # -----------------------------
        # 5. Pre-compute Transformed Docs
        # -----------------------------
        print("Transforming Documents...")
        # Formula: transformed_d = d @ S
        # Operasi Sparse @ Dense jauh lebih cepat daripada Dense @ Dense
        self.transformed_docs = self.doc_vectors @ self.S

        # -----------------------------
        # 6. Pre-compute Document Norms
        # -----------------------------
        # Denom = sqrt(d . transformed_d)
        # Kita bisa hitung ini dengan sangat cepat menggunakan perkalian element-wise
        # Namun karena self.transformed_docs mungkin dense, kita hati-hati memorynya
        
        # Convert doc_vectors ke dense sementara hanya untuk hitungan dot product baris
        # Atau lebih hemat memori: (A * B).sum(axis=1)
        # A adalah sparse, B adalah dense.
        
        # Dot product baris per baris: sum(doc_vec[i] * transformed_docs[i])
        # Karena doc_vectors sparse, kita iterasi manual atau gunakan multiply
        # Cara paling efisien di numpy/scipy:
        
        # Kita gunakan teknik Einstein Summation tapi hati-hati dengan sparse
        # Solusi: result_i = sum_j (D_ij * T_ij)
        # Karena D sparse, kita hanya kalikan indeks yang non-zero.
        
        # Paling cepat & aman memori:
        # self.transformed_docs adalah Dense array (numpy)
        # self.doc_vectors adalah Sparse
        
        # Kita lakukan element-wise multiplication. Scipy akan otomatis broadcast sparse ke dense
        product = self.doc_vectors.multiply(self.transformed_docs) 
        doc_dot_transformed = product.sum(axis=1).A1 # .A1 convert matrix to 1D array
        
        self.doc_norms = np.sqrt(np.maximum(doc_dot_transformed, 0.0))

        print("Initialization Complete.")

    def _build_similarity_matrix_optimized(self):
        """
        Versi Super Cepat menggunakan Aljabar Linear Sparse
        """
        # 1. Binary Matrix (N x V)
        # Copy struktur dari doc_vectors tapi semua data jadi 1.0
        bin_matrix = self.doc_vectors.copy()
        bin_matrix.data[:] = 1.0 

        # 2. Co-occurrence calculation: C = B.T @ B
        # Scipy sangat cepat melakukan ini (Sparse Matrix Multiplication)
        # Hasilnya C adalah matriks (V x V) yang mungkin agak dense tapi tetap sparse
        C = bin_matrix.T @ bin_matrix

        # 3. Normalization (Cosine Similarity)
        # S_ij = C_ij / (sqrt(C_ii) * sqrt(C_jj))
        # Kita gunakan teknik Matriks Diagonal untuk menghindar loop dan outer product raksasa
        
        # Ambil diagonal (C_ii)
        diag_val = C.diagonal()
        
        # Hitung faktor pengali invers: 1 / sqrt(C_ii)
        # Hati-hati pembagian nol
        with np.errstate(divide='ignore'):
            inv_sqrt_diag = 1.0 / np.sqrt(diag_val)
        inv_sqrt_diag[np.isinf(inv_sqrt_diag)] = 0.0
        
        # Buat matriks diagonal sparse dari faktor tersebut
        # D_inv = diag(1/sqrt(C_ii))
        D_inv = diags(inv_sqrt_diag)

        # Rumus Aljabar Linear: S = D_inv @ C @ D_inv
        # Ini secara matematis SAMA dengan membagi setiap elemen dengan norma baris & kolom
        # Tapi jauh lebih cepat
        S = D_inv @ C @ D_inv

        # Kembalikan sebagai dense matrix jika V < 10.000 agar akses query cepat
        # Jika V sangat besar (>20.000), sebaiknya tetap sparse. 
        # Untuk 500 dokumen, V mungkin sekitar 5000-10000. Dense masih aman (sekitar 200MB RAM).
        # Tapi mari kita lihat. Jika kita return sparse, query logic harus siap sparse.
        # Untuk keamanan memori maksimum, kita biarkan sparse (CSR).
        
        return S # Ini sekarang Sparse CSR Matrix

    def match(self, query_tokens, top_n=5, candidate_ids=None):
        # 1. Vectorize Query (V,) -> Sparse
        q_vec = np.zeros(self.V, dtype=np.float32)
        valid = False
        for term in query_tokens:
            if term in self.vocab:
                q_vec[self.vocab[term]] += 1.0
                valid = True
        
        if not valid:
            return []
            
        # Convert query ke sparse row vector (1 x V) agar konsisten
        q_vec_sparse = csr_matrix(q_vec)

        # 2. Calculate Transformed Query: Sq = q @ S
        # Karena S simetris, q @ S == S @ q.T
        # Sparse @ Sparse -> Sparse
        Sq = q_vec_sparse @ self.S 
        
        # Convert Sq ke Dense array (1D) untuk perhitungan dot product mudah
        Sq_dense = Sq.toarray().flatten()
        q_vec_dense = q_vec # ini sudah dense

        # 3. Calculate Query Denominator
        q_dot_Sq = np.dot(q_vec_dense, Sq_dense)
        if q_dot_Sq <= 0:
            return []
        denom_q = np.sqrt(q_dot_Sq)

        # 4. Filter Candidates & Numerators
        # transformed_docs (N x V) dot Sq (V,)
        # Numerator = d_trans . Sq_trans
        # Rumus GVSM: d . (S . q) = (d . S) . q = transformed_d . q
        # TAPI tunggu, rumus similarity adalah Cosine(d_trans, q_trans)
        # Numerator = transformed_d . transformed_q ?? TIDAK.
        # GVSM standard: Sim(d, q) = (d^T S q) / (norm...)
        # Kita sudah punya `transformed_docs` = d^T S.
        # Jadi Numerator = transformed_docs @ q
        
        if candidate_ids is not None:
            indices = list(candidate_ids)
            # Slicing numpy array
            target_docs = self.transformed_docs[indices] 
            target_norms = self.doc_norms[indices]
            mapping_back = indices
        else:
            target_docs = self.transformed_docs
            target_norms = self.doc_norms
            mapping_back = range(self.doc_count)

        # Hitung Numerator: (N x V) @ (V,)
        numerators = target_docs @ q_vec_dense

        # 6. Final Scores
        denominators = target_norms * denom_q
        
        with np.errstate(divide='ignore', invalid='ignore'):
            scores = numerators / denominators
            scores = np.nan_to_num(scores)

        # 7. Formatting
        results = []
        for i, score in enumerate(scores):
            final_score = min(float(score), 1.0)
            if final_score > 0.0001: # Filter skor 0 atau sangat kecil
                results.append((mapping_back[i], final_score))

        results.sort(key=lambda x: -x[1])
        if top_n:
            results = results[:top_n]

        return [
            {"doc_id": idx, "score": sc, "document": self.documents[idx]}
            for idx, sc in results
        ]

# --- TEST ---
if __name__ == "__main__":
    # Buat dummy data agak banyak untuk tes performa
    docs = [
        ["saya", "suka", "makan", "nasi", "goreng"],
        ["teknologi", "adalah", "masa", "depan", "bangsa"],
        ["saya", "belajar", "python", "numpy", "scipy"],
        ["makan", "malam", "bersama", "keluarga"],
    ] * 125 # Duplicate sampai 500 dokumen
    
    import time
    start = time.time()
    model = GVSMModel(docs)
    print(f"Build Time: {time.time() - start:.4f} seconds")
    
    start = time.time()
    res = model.match(["makan", "nasi"], top_n=3)
    print(f"Query Time: {time.time() - start:.4f} seconds")
    
    for r in res:
        print(f"Doc {r['doc_id']} Score: {r['score']:.4f}")