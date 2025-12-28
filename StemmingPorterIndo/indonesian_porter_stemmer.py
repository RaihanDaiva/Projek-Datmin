"""
INDONESIAN PORTER STEMMER - Implementasi dari Scratch
======================================================

Algoritma stemming untuk Bahasa Indonesia yang diadaptasi dari Porter Stemmer.
Menggunakan aturan morfologi Bahasa Indonesia untuk menghapus imbuhan dan 
mendapatkan kata dasar.

Fitur:
- Menghapus prefix (awalan): me-, ber-, di-, ter-, ke-, pe-, dll
- Menghapus suffix (akhiran): -kan, -an, -i, -nya, dll
- Menghapus confix (kombinasi awalan-akhiran): ke-an, ber-an, dll
- Menangani nasalisasi (perubahan huruf karena prefix me-)
- Exception handling untuk kata-kata khusus
- Membaca input dari file: txt, docx, pdf

Author: Claude
Date: 2024
"""

import os
import re
from pathlib import Path

# Import untuk file processing
try:
    from docx import Document
    DOCX_AVAILABLE = True
except ImportError:
    DOCX_AVAILABLE = False

try:
    import PyPDF2
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False

class IndonesianPorterStemmer:
    """
    Implementasi Porter Stemmer untuk Bahasa Indonesia
    """
    
    def __init__(self):
        # Definisi awalan (prefixes) - diurutkan dari terpanjang
        self.prefixes_rules = {
            # Complex prefixes (harus dicek lebih dulu)
            'mempere': 4,
            'memperi': 4, 
            'memper': 4,
            'menter': 4,
            'mempe': 4,
            
            # Standard prefixes
            'diper': 4,
            'penge': 4,
            'pember': 4,
            'terpe': 4,
            
            # Common prefixes
            'peng': 3,
            'meng': 3,
            'meny': 3,
            'mem': 3,
            'men': 3,
            'ber': 3,
            'ter': 3,
            'per': 3,
            
            # Simple prefixes
            'me': 2,
            'di': 2,
            'ke': 2,
            'pe': 2,
            'se': 2,
        }
        
        # Definisi akhiran (suffixes)
        self.suffixes = ['kanlah', 'anlah', 'ilah', 'kan', 'an', 'i']
        
        # Partikel dan possessive
        self.particles = ['lah', 'kah', 'tah', 'pun']
        self.possessives = ['nya', 'ku', 'mu']
        
        # Kata dasar yang tidak perlu di-stem
        self.root_words = {
            'baca', 'tulis', 'ajar', 'kerja', 'lari', 'jalan',
            'tidur', 'bangun', 'duduk', 'berdiri', 'ambil',
            'hilang', 'sahabat', 'bahagia', 'cantik', 'ganteng'
        }
        
        # Pemetaan kata khusus (exceptions)
        self.special_words = {
            'belajar': 'ajar',
            'bekerja': 'kerja',
            'berlari': 'lari',
            'berjalan': 'jalan',
            'bernyanyi': 'nyanyi',
            'berbicara': 'bicara',
            'bertanya': 'tanya',
            'berkata': 'kata',
            'bertemu': 'temu',
            'berpisah': 'pisah',
        }
    
    def stem(self, word):
        """
        Fungsi utama untuk stemming
        
        Args:
            word (str): Kata yang akan di-stem
            
        Returns:
            str: Kata dasar (root word)
        """
        # Normalisasi: lowercase dan trim
        word = word.lower().strip()
        
        # Kata terlalu pendek
        if len(word) <= 2:
            return word
        
        # Cek kata khusus
        if word in self.special_words:
            return self.special_words[word]
        
        # Cek apakah sudah kata dasar
        if word in self.root_words:
            return word
        
        # Simpan kata asli untuk fallback
        original = word
        
        # Algoritma stemming bertahap
        # 1. Hapus partikel (-lah, -kah, -tah, -pun)
        word = self._remove_particles(word)
        
        # 2. Hapus possessive pronouns (-ku, -mu, -nya)
        word = self._remove_possessives(word)
        
        # 3. Proses stemming utama (loop sampai tidak ada perubahan)
        previous = ""
        max_iterations = 5
        iteration = 0
        
        while previous != word and iteration < max_iterations:
            previous = word
            
            # 3a. Coba hapus confix dulu (kombinasi prefix-suffix)
            word = self._remove_confix(word)
            
            # 3b. Hapus suffix
            word = self._remove_suffix(word)
            
            # 3c. Hapus prefix
            word = self._remove_prefix(word)
            
            iteration += 1
        
        # Validasi hasil akhir
        if len(word) < 2 or not word.isalpha():
            return original
        
        return word
    
    def _remove_particles(self, word):
        """Hapus partikel di akhir kata"""
        for particle in self.particles:
            if word.endswith(particle) and len(word) > len(particle) + 2:
                return word[:-len(particle)]
        return word
    
    def _remove_possessives(self, word):
        """Hapus possessive pronouns"""
        for poss in self.possessives:
            if word.endswith(poss) and len(word) > len(poss) + 2:
                return word[:-len(poss)]
        return word
    
    def _remove_confix(self, word):
        """
        Hapus kombinasi prefix-suffix (confix)
        Contoh: ke-an, ber-an, pe-an, per-an
        """
        confixes = [
            ('ber', 'an'),
            ('ke', 'an'),
            ('pe', 'an'),
            ('per', 'an'),
            ('me', 'an'),
        ]
        
        for prefix, suffix in confixes:
            if word.startswith(prefix) and word.endswith(suffix):
                stem = word[len(prefix):-len(suffix)]
                if len(stem) >= 2:
                    return stem
        
        return word
    
    def _remove_suffix(self, word):
        """Hapus suffix dengan prioritas dari yang terpanjang"""
        for suffix in self.suffixes:
            if word.endswith(suffix) and len(word) > len(suffix) + 2:
                stem = word[:-len(suffix)]
                if self._is_valid_stem(stem):
                    return stem
        return word
    
    def _remove_prefix(self, word):
        """
        Hapus prefix dengan penanganan nasalisasi
        """
        # Cek prefix dari yang terpanjang ke terpendek
        sorted_prefixes = sorted(self.prefixes_rules.items(), 
                                key=lambda x: len(x[0]), 
                                reverse=True)
        
        for prefix, min_stem_length in sorted_prefixes:
            if word.startswith(prefix):
                stem = word[len(prefix):]
                
                # Validasi panjang stem
                if len(stem) < min_stem_length:
                    continue
                
                # Handling khusus untuk prefix dengan nasalisasi
                if prefix in ['mem', 'men', 'meng', 'meny']:
                    restored = self._restore_nasal(stem, prefix)
                    if self._is_valid_stem(restored):
                        return restored
                
                if self._is_valid_stem(stem):
                    return stem
        
        return word
    
    def _restore_nasal(self, stem, prefix):
        """
        Kembalikan huruf yang hilang karena nasalisasi
        
        Aturan nasalisasi:
        - mem + p/f/v -> m (contoh: mem-potong -> memotong, p hilang)
        - men + t/d -> n (contoh: men-tulis -> menulis, t hilang)
        - meng + k/g/h -> ng (contoh: meng-ambil -> mengambil)
        - meny + s -> ny (contoh: meny-sapu -> menyapu, s hilang)
        """
        if prefix == 'mem':
            # Coba kembalikan p
            if stem and stem[0] not in ['p', 'b', 'm']:
                candidates = ['p' + stem, stem]
                for cand in candidates:
                    if cand in self.root_words or len(cand) >= 3:
                        return cand
        
        elif prefix == 'men':
            # Coba kembalikan t atau d
            if stem and stem[0] not in ['t', 'd', 'n']:
                candidates = ['t' + stem, stem]
                for cand in candidates:
                    if cand in self.root_words or len(cand) >= 3:
                        return cand
        
        elif prefix == 'meng':
            # Untuk meng-, huruf k/g/h bisa hilang
            if stem:
                candidates = ['k' + stem, stem]
                for cand in candidates:
                    if cand in self.root_words or len(cand) >= 3:
                        return cand
        
        elif prefix == 'meny':
            # Untuk meny-, huruf s hilang
            if stem and not stem.startswith('s'):
                candidates = ['s' + stem, stem]
                for cand in candidates:
                    if cand in self.root_words or len(cand) >= 3:
                        return cand
        
        return stem
    
    def _is_valid_stem(self, stem):
        """
        Validasi apakah stem valid
        """
        # Minimal 2 karakter
        if len(stem) < 2:
            return False
        
        # Harus alphabet
        if not stem.isalpha():
            return False
        
        # Jika ada di root words, pasti valid
        if stem in self.root_words:
            return True
        
        # Minimal harus ada vokal
        vowels = set('aiueo')
        if not any(c in vowels for c in stem):
            return False
        
        return True
    
    def stem_sentence(self, sentence):
        """
        Stem seluruh kalimat
        
        Args:
            sentence (str): Kalimat yang akan di-stem
            
        Returns:
            str: Kalimat hasil stemming
        """
        words = sentence.split()
        stemmed = [self.stem(word) for word in words]
        return ' '.join(stemmed)
    
    def batch_stem(self, words):
        """
        Stem multiple words sekaligus
        
        Args:
            words (list): List kata yang akan di-stem
            
        Returns:
            dict: Dictionary {original: stemmed}
        """
        return {word: self.stem(word) for word in words}
    
    def read_txt_file(self, filepath):
        """
        Membaca file txt
        
        Args:
            filepath (str): Path ke file txt
            
        Returns:
            str: Isi file
        """
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            raise FileNotFoundError(f"File tidak ditemukan: {filepath}")
        except Exception as e:
            raise Exception(f"Error membaca file txt: {str(e)}")
    
    def read_docx_file(self, filepath):
        """
        Membaca file docx
        
        Args:
            filepath (str): Path ke file docx
            
        Returns:
            str: Isi file
        """
        if not DOCX_AVAILABLE:
            raise ImportError("Library python-docx tidak tersedia. Install dengan: pip install python-docx")
        
        try:
            doc = Document(filepath)
            text = []
            for paragraph in doc.paragraphs:
                if paragraph.text.strip():
                    text.append(paragraph.text)
            return '\n'.join(text)
        except FileNotFoundError:
            raise FileNotFoundError(f"File tidak ditemukan: {filepath}")
        except Exception as e:
            raise Exception(f"Error membaca file docx: {str(e)}")
    
    def read_pdf_file(self, filepath):
        """
        Membaca file pdf
        
        Args:
            filepath (str): Path ke file pdf
            
        Returns:
            str: Isi file
        """
        if not PDF_AVAILABLE:
            raise ImportError("Library PyPDF2 tidak tersedia. Install dengan: pip install PyPDF2")
        
        try:
            text = []
            with open(filepath, 'rb') as f:
                pdf_reader = PyPDF2.PdfReader(f)
                for page in pdf_reader.pages:
                    page_text = page.extract_text()
                    if page_text.strip():
                        text.append(page_text)
            return '\n'.join(text)
        except FileNotFoundError:
            raise FileNotFoundError(f"File tidak ditemukan: {filepath}")
        except Exception as e:
            raise Exception(f"Error membaca file pdf: {str(e)}")
    
    def read_file(self, filepath):
        """
        Membaca file dengan auto-detect format (txt, docx, pdf)
        
        Args:
            filepath (str): Path ke file
            
        Returns:
            str: Isi file
        """
        filepath = Path(filepath)
        
        if not filepath.exists():
            raise FileNotFoundError(f"File tidak ditemukan: {filepath}")
        
        extension = filepath.suffix.lower()
        
        if extension == '.txt':
            return self.read_txt_file(str(filepath))
        elif extension == '.docx':
            return self.read_docx_file(str(filepath))
        elif extension == '.pdf':
            return self.read_pdf_file(str(filepath))
        else:
            raise ValueError(f"Format file tidak didukung: {extension}. Gunakan .txt, .docx, atau .pdf")
    
    def stem_file(self, input_filepath, output_filepath=None, save_result=True):
        """
        Membaca file, lakukan stemming, dan simpan hasilnya
        
        Args:
            input_filepath (str): Path ke file input (txt/docx/pdf)
            output_filepath (str): Path ke file output (optional)
            save_result (bool): Apakah menyimpan hasil ke file
            
        Returns:
            dict: Dictionary berisi original text dan stemmed text
        """
        # Baca file
        print(f"📄 Membaca file: {input_filepath}")
        original_text = self.read_file(input_filepath)
        
        # Lakukan stemming
        print(f"⚙️  Melakukan stemming...")
        stemmed_text = self.stem_sentence(original_text)
        
        # Simpan hasil jika diminta
        if save_result:
            if output_filepath is None:
                input_path = Path(input_filepath)
                output_filepath = input_path.parent / f"{input_path.stem}_stemmed.txt"
            
            with open(output_filepath, 'w', encoding='utf-8') as f:
                f.write(stemmed_text)
            print(f"✅ Hasil disimpan ke: {output_filepath}")
        
        return {
            'original': original_text,
            'stemmed': stemmed_text,
            'output_file': output_filepath if save_result else None
        }


def demo():
    """Demonstrasi penggunaan Indonesian Porter Stemmer"""
    
    stemmer = IndonesianPorterStemmer()
    
    print("=" * 70)
    print("INDONESIAN PORTER STEMMER - Implementasi dari Scratch")
    print("=" * 70)
    print()
    
    # Test 1: Kata dengan berbagai imbuhan
    print("📝 Test 1: Stemming Kata-kata dengan Berbagai Imbuhan")
    print("-" * 70)
    
    test_cases = [
        # Prefix 'ber-'
        ("belajar", "ajar"),
        ("bekerja", "kerja"),
        ("berlari", "lari"),
        ("berjalan", "jalan"),
        
        # Prefix 'me-' dan variannya
        ("membaca", "baca"),
        ("menulis", "tulis"),
        ("mengambil", "ambil"),
        ("menyapu", "sapu"),
        
        # Suffix '-kan', '-an', '-i'
        ("bacaan", "baca"),
        ("tulisan", "tulis"),
        ("makanan", "makan"),
        ("minuman", "minum"),
        
        # Kombinasi prefix + suffix
        ("pembelajaran", "ajar"),
        ("pekerjaan", "kerja"),
        ("kehidupan", "hidup"),
        ("kebahagiaan", "bahagia"),
        
        # Prefix 'pe-' dan variannya
        ("penulis", "tulis"),
        ("pembaca", "baca"),
        ("pengajar", "ajar"),
        ("penyanyi", "nyanyi"),
        
        # Kata dengan partikel
        ("bacalah", "baca"),
        ("tuliskanlah", "tulis"),
        ("ambilkan", "ambil"),
        
        # Kata dengan possessive
        ("bukunya", "buku"),
        ("rumahku", "rumah"),
        ("mobilmu", "mobil"),
    ]
    
    correct = 0
    total = len(test_cases)
    
    for word, expected in test_cases:
        result = stemmer.stem(word)
        status = "✓" if result == expected else "✗"
        print(f"{status} {word:20s} → {result:15s} (expected: {expected})")
        if result == expected:
            correct += 0
    
    accuracy = (correct / total) * 100
    print(f"\nAkurasi: {correct}/{total} ({accuracy:.1f}%)")
    
    # Test 2: Stemming kalimat
    print("\n" + "=" * 70)
    print("📝 Test 2: Stemming Kalimat Lengkap")
    print("-" * 70)
    
    sentences = [
        "Saya sedang membaca buku pelajaran di perpustakaan",
        "Mereka bekerja sama untuk membangun jembatan baru",
        "Penulis itu menuliskan cerita yang sangat menarik",
        "Kebahagiaan adalah kunci kehidupan yang bermakna",
        "Pelari itu berlari dengan cepat mengejar waktu"
    ]
    
    for sent in sentences:
        stemmed = stemmer.stem_sentence(sent)
        print(f"\nAsli    : {sent}")
        print(f"Stemmed : {stemmed}")
    
    # Test 3: Batch processing
    print("\n" + "=" * 70)
    print("📝 Test 3: Batch Stemming")
    print("-" * 70)
    
    words = ["pembelajaran", "pekerjaan", "kehidupan", "kebahagiaan", 
             "persahabatan", "perjuangan", "kemenangan"]
    
    results = stemmer.batch_stem(words)
    for original, stemmed in results.items():
        print(f"{original:20s} → {stemmed}")
    
    print("\n" + "=" * 70)
    print("✅ Demo selesai!")
    print("=" * 70)


if __name__ == "__main__":
    demo()
