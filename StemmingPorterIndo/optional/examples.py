"""
CONTOH PENGGUNAAN INDONESIAN PORTER STEMMER
============================================

File ini berisi berbagai contoh penggunaan stemmer untuk
kasus-kasus yang berbeda.
"""

from indonesian_porter_stemmer import IndonesianPorterStemmer

def example_basic():
    """Contoh penggunaan dasar"""
    print("=" * 70)
    print("CONTOH 1: Penggunaan Dasar")
    print("=" * 70)
    
    stemmer = IndonesianPorterStemmer()
    
    words = ["membaca", "menulis", "berlari", "bekerja"]
    
    print("\nStem kata-kata sederhana:")
    for word in words:
        stem = stemmer.stem(word)
        print(f"  {word:15s} → {stem}")


def example_sentence():
    """Contoh stemming kalimat"""
    print("\n" + "=" * 70)
    print("CONTOH 2: Stemming Kalimat")
    print("=" * 70)
    
    stemmer = IndonesianPorterStemmer()
    
    sentences = [
        "Anak-anak sedang belajar membaca di perpustakaan",
        "Dia bekerja sebagai penulis untuk majalah terkenal",
        "Mereka berlari mengejar kebahagiaan yang sesungguhnya",
    ]
    
    print("\nHasil stemming:")
    for sentence in sentences:
        stemmed = stemmer.stem_sentence(sentence)
        print(f"\nOriginal : {sentence}")
        print(f"Stemmed  : {stemmed}")


def example_batch():
    """Contoh batch processing"""
    print("\n" + "=" * 70)
    print("CONTOH 3: Batch Processing")
    print("=" * 70)
    
    stemmer = IndonesianPorterStemmer()
    
    # Daftar kata untuk di-stem sekaligus
    words = [
        "pembelajaran", "pengajaran", "pendidikan",
        "pekerjaan", "pekerja", "bekerja",
        "kehidupan", "penghidupan", "hidup",
        "kebahagiaan", "membahagiakan", "bahagia"
    ]
    
    results = stemmer.batch_stem(words)
    
    print("\nHasil batch stemming:")
    print(f"{'Kata Asli':<20s} {'Kata Dasar':<15s}")
    print("-" * 35)
    for original, stemmed in results.items():
        print(f"{original:<20s} {stemmed:<15s}")


def example_affixes():
    """Contoh berbagai jenis imbuhan"""
    print("\n" + "=" * 70)
    print("CONTOH 4: Berbagai Jenis Imbuhan")
    print("=" * 70)
    
    stemmer = IndonesianPorterStemmer()
    
    # Kelompokkan berdasarkan jenis imbuhan
    test_groups = {
        "Prefix 'ber-'": ["belajar", "bekerja", "berlari", "berjalan"],
        "Prefix 'me-'": ["membaca", "menulis", "mengambil", "menyapu"],
        "Prefix 'pe-'": ["penulis", "pembaca", "pengajar", "penyanyi"],
        "Suffix '-an'": ["bacaan", "tulisan", "makanan", "minuman"],
        "Suffix '-kan'": ["bacakan", "tuliskan", "ambilkan", "berikan"],
        "Confix 'ke-an'": ["kehilangan", "kehidupan", "kebahagiaan", "kematian"],
    }
    
    for group_name, words in test_groups.items():
        print(f"\n{group_name}:")
        print("-" * 40)
        for word in words:
            stem = stemmer.stem(word)
            print(f"  {word:20s} → {stem}")


def example_text_processing():
    """Contoh pemrosesan teks panjang"""
    print("\n" + "=" * 70)
    print("CONTOH 5: Pemrosesan Teks Panjang")
    print("=" * 70)
    
    stemmer = IndonesianPorterStemmer()
    
    text = """
    Pendidikan merupakan kunci untuk membuka pintu kesuksesan.
    Dengan belajar, kita dapat mengembangkan pengetahuan dan keterampilan.
    Guru-guru yang berdedikasi mengajarkan ilmu kepada para pelajar.
    Mereka bekerja keras untuk membangun masa depan bangsa yang lebih baik.
    """
    
    print("\nTeks asli:")
    print(text.strip())
    
    print("\nHasil stemming:")
    stemmed = stemmer.stem_sentence(text.strip())
    print(stemmed)


def example_comparison():
    """Contoh perbandingan kata serupa"""
    print("\n" + "=" * 70)
    print("CONTOH 6: Perbandingan Kata Serupa")
    print("=" * 70)
    
    stemmer = IndonesianPorterStemmer()
    
    word_groups = [
        ["baca", "membaca", "bacaan", "pembaca", "dibaca", "bacalah"],
        ["tulis", "menulis", "tulisan", "penulis", "ditulis", "tuliskan"],
        ["kerja", "bekerja", "pekerjaan", "pekerja", "mengerjakan"],
        ["ajar", "belajar", "pelajaran", "pengajar", "mengajar"],
    ]
    
    print("\nKata-kata dengan root yang sama:")
    for group in word_groups:
        print(f"\nGrup kata:")
        for word in group:
            stem = stemmer.stem(word)
            print(f"  {word:20s} → {stem}")


def example_edge_cases():
    """Contoh kasus-kasus khusus"""
    print("\n" + "=" * 70)
    print("CONTOH 7: Kasus-kasus Khusus")
    print("=" * 70)
    
    stemmer = IndonesianPorterStemmer()
    
    edge_cases = [
        ("a", "Kata terlalu pendek"),
        ("di", "Kata pendek (2 huruf)"),
        ("aku", "Kata pendek (3 huruf)"),
        ("membacanya", "Kata dengan possessive"),
        ("bacalah", "Kata dengan partikel"),
        ("membacakanlah", "Kombinasi kompleks"),
        ("berbahagia", "Prefix ber- + kata sifat"),
        ("mempersatukan", "Prefix kompleks"),
    ]
    
    print("\nHasil stemming untuk kasus khusus:")
    for word, description in edge_cases:
        stem = stemmer.stem(word)
        print(f"  {word:20s} → {stem:15s} ({description})")


def main():
    """Jalankan semua contoh"""
    print("\n")
    print("🌟" * 35)
    print("   INDONESIAN PORTER STEMMER - EXAMPLES")
    print("🌟" * 35)
    
    # Jalankan semua contoh
    example_basic()
    example_sentence()
    example_batch()
    example_affixes()
    example_text_processing()
    example_comparison()
    example_edge_cases()
    
    print("\n" + "=" * 70)
    print("✅ Semua contoh selesai dijalankan!")
    print("=" * 70)
    print("\nTips:")
    print("- Stemmer bekerja paling baik untuk kata-kata umum")
    print("- Hasil mungkin tidak sempurna untuk kata-kata khusus")
    print("- Untuk production, pertimbangkan library Sastrawi")
    print("=" * 70)
    print()


if __name__ == "__main__":
    main()
