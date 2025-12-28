"""
COMPLETE INDONESIAN TEXT PREPROCESSING
(Tokenizing + Filtering + Stemming)
======================================================
Gabungan logika pembacaan file, pembersihan, stopword removal,
dan algoritma stemming Porter untuk Bahasa Indonesia.
"""

import os
import re
from collections import Counter
from pathlib import Path

# --- DEPENDENCY CHECK ---
try:
    from docx import Document
    DOCX_AVAILABLE = True
except ImportError:
    DOCX_AVAILABLE = False
    print("Warning: modul 'python-docx' tidak ditemukan. Fitur .docx non-aktif.")

try:
    import pdfplumber
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False
    print("Warning: modul 'pdfplumber' tidak ditemukan. Fitur .pdf non-aktif.")


# ==========================================
# 1. KELAS STEMMER (Logika Stemming)
# ==========================================
class IndonesianPorterStemmer:
    def __init__(self):
        # Definisi awalan (prefixes) - urutan sangat berpengaruh
        self.prefixes_rules = {
            'mempere': 4, 'memperi': 4, 'memper': 4, 'menter': 4, 'mempe': 4,
            'diper': 4, 'penge': 4, 'pember': 4, 'terpe': 4,
            'peng': 3, 'meng': 3, 'meny': 3, 'mem': 3, 'men': 3, 
            'ber': 3, 'ter': 3, 'per': 3,
            'me': 2, 'di': 2, 'ke': 2, 'pe': 2, 'se': 2,
        }
        
        self.suffixes = ['kanlah', 'anlah', 'ilah', 'kan', 'an', 'i']
        self.particles = ['lah', 'kah', 'tah', 'pun']
        self.possessives = ['nya', 'ku', 'mu']
        
        # Dictionary kata dasar (Cache sederhana agar tidak over-stemming)
        self.root_words = {
            'baca', 'tulis', 'ajar', 'kerja', 'lari', 'jalan',
            'tidur', 'bangun', 'duduk', 'berdiri', 'ambil',
            'hilang', 'sahabat', 'bahagia', 'cantik', 'ganteng',
            'makan', 'minum', 'sapu', 'nyanyi', 'main', 'hutan'
        }
        
        self.special_words = {
            'belajar': 'ajar', 'bekerja': 'kerja', 'berlari': 'lari',
            'berjalan': 'jalan', 'bernyanyi': 'nyanyi'
        }
    
    def stem(self, word):
        word = word.lower().strip()
        if len(word) <= 2: return word
        if word in self.special_words: return self.special_words[word]
        if word in self.root_words: return word
        
        original = word
        
        # 1. Hapus Partikel & Possessive (Tabel 1 & 2)
        word = self._remove_particles(word)
        word = self._remove_possessives(word)
        
        # 2. Hapus Suffix (Tabel 5) dengan Cek Kondisi Prefix
        # Di Porter Stemmer asli (Inggris), suffix biasanya dipotong duluan atau belakangan tergantung varian.
        # Namun algoritma Indonesia sering kali memotong suffix dulu sebelum prefix.
        word = self._remove_suffix(word, original) # Kirim kata original untuk cek prefix
        
        # 3. Hapus Prefix (Tabel 3 & 4)
        # Note: Kita lakukan loop agar bisa menangani prefix bertumpuk (First & Second order)
        previous = ""
        iteration = 0
        while previous != word and iteration < 3:
            previous = word
            word = self._remove_confix(word) # Opsional, aturan tambahan
            word = self._remove_prefix(word)
            iteration += 1
            
        if len(word) < 2 or not word.isalpha():
            return original
            
        return word

    # --- Helper Stemming Methods ---
    def _remove_particles(self, word):
        for p in self.particles:
            if word.endswith(p) and len(word) > len(p) + 2:
                return word[:-len(p)]
        return word

    def _remove_possessives(self, word):
        for p in self.possessives:
            if word.endswith(p) and len(word) > len(p) + 2:
                return word[:-len(p)]
        return word

    def _remove_confix(self, word):
        confixes = [('ber', 'an'), ('ke', 'an'), ('pe', 'an'), ('per', 'an'), ('me', 'an')]
        for p, s in confixes:
            if word.startswith(p) and word.endswith(s):
                return word[len(p):-len(s)]
        return word

    def _remove_suffix(self, word, original_word):
        """
        Hapus suffix sesuai Tabel 5 (dengan Additional Condition)
        """
        # Cek kondisi Suffix -kan
        if word.endswith('kan') and len(word) > 5:
            # Condition: Prefix NOT in {ke, peng}
            # Kita cek ke original word karena prefix belum dihapus saat ini
            if not (original_word.startswith('ke') or original_word.startswith('peng')):
                return word[:-3]

        # Cek kondisi Suffix -an
        if word.endswith('an') and len(word) > 4:
            # Condition: Prefix NOT in {di, meng, ter}
            if not (original_word.startswith('di') or 
                    original_word.startswith('meng') or 
                    original_word.startswith('ter')):
                return word[:-2]

        # Cek kondisi Suffix -i
        if word.endswith('i') and len(word) > 3:
            # Condition: Prefix NOT in {ber, ke, peng}
            if not (original_word.startswith('ber') or 
                    original_word.startswith('ke') or 
                    original_word.startswith('peng')):
                # Logika V|K...c1c1 (huruf sebelum 'i' bukan 'i' lagi)
                stem_candidate = word[:-1]
                if not stem_candidate.endswith('i'): 
                    return stem_candidate
                    
        return word

    def _remove_prefix(self, word):
        sorted_prefixes = sorted(self.prefixes_rules.items(), key=lambda x: len(x[0]), reverse=True)
        for prefix, _ in sorted_prefixes:
            if word.startswith(prefix):
                stem = word[len(prefix):]
                if prefix in ['mem', 'men', 'meng', 'meny']:
                    return self._restore_nasal(stem, prefix)
                return stem
        return word

    def _restore_nasal(self, stem, prefix):
        if not stem: return stem
        if prefix == 'mem' and stem[0] not in ['p', 'b', 'm']: return 'p' + stem
        if prefix == 'men' and stem[0] not in ['t', 'd', 'n']: return 't' + stem
        if prefix == 'meng': return 'k' + stem # Simplifikasi, bisa k/g/h
        if prefix == 'meny': return 's' + stem
        return stem


# ==========================================
# 2. KELAS PREPROCESSOR (Tokenizing & Filtering)
# ==========================================
class TextPreprocessor:
    def __init__(self):
        self.stemmer = IndonesianPorterStemmer()
        
        # List Stopwords Bahasa Indonesia (Filtering)
        # Anda bisa menambahkan kata lain ke dalam set ini
        self.stopwords = {
            'yang', 'di', 'ke', 'dari', 'dan', 'ini', 'itu', 'untuk', 
            'pada', 'adalah', 'sebagai', 'dengan', 'dalam', 'juga', 
            'saya', 'anda', 'dia', 'mereka', 'kita', 'kami', 'bisa', 
            'ada', 'tidak', 'saat', 'oleh', 'akan', 'atau', 'karena',
            'namun', 'tetapi', 'sedang', 'sudah', 'telah', 'bagi',
            'sebuah', 'seorang', 'para', 'serta', 'lalu', 'maka'
        }

    def clean_and_tokenize(self, text):
        """
        Membersihkan teks dan memecahnya menjadi token.
        Hanya mengambil huruf a-z.
        """
        text = text.lower()
        # Regex: Hanya ambil huruf alfabet, abaikan angka dan simbol
        tokens = re.findall(r"[a-z]+", text)
        return tokens

    def filter_tokens(self, tokens):
        """
        Menghapus stopword dari list token.
        """
        return [t for t in tokens if t not in self.stopwords and len(t) > 1]

    def stem_tokens(self, tokens):
        """
        Melakukan stemming pada setiap token.
        """
        return [self.stemmer.stem(t) for t in tokens]

    def process_pipeline(self, text):
        """
        Menjalankan seluruh proses: Tokenize -> Filter -> Stem
        Mengembalikan: (list_token_bersih, list_token_stem)
        """
        # 1. Tokenizing
        tokens = self.clean_and_tokenize(text)
        
        # 2. Filtering
        filtered_tokens = self.filter_tokens(tokens)
        
        # 3. Stemming
        stemmed_tokens = self.stem_tokens(filtered_tokens)
        
        return filtered_tokens, stemmed_tokens


# ==========================================
# 3. FUNGSI PEMBACAAN FILE
# ==========================================
def read_file_content(file_path):
    ext = file_path.split(".")[-1].lower()
    text = ""
    
    try:
        if ext == "txt":
            with open(file_path, "r", encoding="utf-8") as f:
                text = f.read()
                
        elif ext == "pdf" and PDF_AVAILABLE:
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    extracted = page.extract_text()
                    if extracted: text += extracted + " "
                    
        elif ext == "docx" and DOCX_AVAILABLE:
            doc = Document(file_path)
            text = "\n".join([para.text for para in doc.paragraphs])
            
        else:
            print(f"(!!) Format tidak didukung atau modul hilang: {ext}")
            
    except Exception as e:
        print(f"(!!) Error membaca file {file_path}: {e}")
        
    return text


# ==========================================
# 4. MAIN PROGRAM
# ==========================================
def main():
    folder_path = input("Masukkan path folder dokumen: ")
    
    if not os.path.exists(folder_path):
        print("Folder tidak ditemukan!")
        return

    preprocessor = TextPreprocessor()
    file_list = os.listdir(folder_path)

    print(f"\n{'='*60}")
    print(f"Mulai Memproses Dokumen di: {folder_path}")
    print(f"{'='*60}\n")

    for idx, filename in enumerate(file_list, start=1):
        file_path = os.path.join(folder_path, filename)
        
        # Skip jika folder
        if os.path.isdir(file_path): continue

        print(f"📄 {idx}. Memproses: {filename}...")
        
        # 1. Baca File
        raw_text = read_file_content(file_path)
        if not raw_text:
            print("   -> File kosong atau gagal dibaca.")
            continue

        # 2. Jalankan Pipeline (Tokenize -> Filter -> Stem)
        filtered, stemmed = preprocessor.process_pipeline(raw_text)
        
        # Hitung Frekuensi Kata Dasar (Stemmed)
        frequencies = Counter(stemmed)
        
        # Tampilkan Hasil
        print(f"   -> Ditemukan {len(filtered)} token setelah filtering.")
        print(f"   -> Ditemukan {len(frequencies)} kata unik setelah stemming.")
        print("   -> 5 Kata teratas (Top Words):")
        
        for word, count in frequencies.most_common(5):
            print(f"      - {word}: {count}")
        print("-" * 40)

if __name__ == "__main__":
    main()