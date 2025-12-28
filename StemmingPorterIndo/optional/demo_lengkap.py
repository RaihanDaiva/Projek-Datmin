"""
DEMO LENGKAP - Indonesian Porter Stemmer
=========================================

Script ini mendemonstrasikan SEMUA fitur stemmer termasuk:
1. Stemming kata tunggal
2. Stemming kalimat
3. Batch processing
4. File processing (TXT, DOCX, PDF)
5. Analisis statistik
"""

from indonesian_porter_stemmer import IndonesianPorterStemmer
from collections import Counter
import os


def demo_header(title):
    """Print header untuk setiap demo section"""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


def demo_basic_stemming():
    """Demo 1: Stemming dasar"""
    demo_header("DEMO 1: Stemming Dasar")
    
    stemmer = IndonesianPorterStemmer()
    
    test_words = [
        "membaca", "menulis", "berlari", "bekerja",
        "pembelajaran", "pekerjaan", "kehidupan", "kebahagiaan"
    ]
    
    print("\nStemming kata-kata:")
    for word in test_words:
        stem = stemmer.stem(word)
        print(f"  {word:20s} → {stem}")


def demo_sentence_stemming():
    """Demo 2: Stemming kalimat"""
    demo_header("DEMO 2: Stemming Kalimat")
    
    stemmer = IndonesianPorterStemmer()
    
    sentences = [
        "Pendidikan adalah kunci kesuksesan masa depan",
        "Mereka bekerja keras untuk mencapai impian",
        "Teknologi mengubah cara kita belajar dan bekerja"
    ]
    
    print("\nHasil stemming kalimat:")
    for i, sentence in enumerate(sentences, 1):
        stemmed = stemmer.stem_sentence(sentence)
        print(f"\n{i}. Original : {sentence}")
        print(f"   Stemmed  : {stemmed}")


def demo_batch_processing():
    """Demo 3: Batch processing"""
    demo_header("DEMO 3: Batch Processing")
    
    stemmer = IndonesianPorterStemmer()
    
    # Simulasi processing banyak dokumen
    documents = {
        "Dokumen 1": "Pembelajaran aktif meningkatkan pemahaman siswa",
        "Dokumen 2": "Teknologi membantu proses pembelajaran modern",
        "Dokumen 3": "Guru mengajarkan materi dengan metode inovatif"
    }
    
    print("\nProses multiple dokumen:")
    all_stems = []
    
    for doc_name, text in documents.items():
        stemmed = stemmer.stem_sentence(text)
        print(f"\n{doc_name}:")
        print(f"  Original: {text}")
        print(f"  Stemmed : {stemmed}")
        all_stems.extend(stemmed.split())
    
    # Analisis kata paling sering
    print("\n\nKata yang paling sering muncul setelah stemming:")
    freq = Counter(all_stems)
    for word, count in freq.most_common(5):
        print(f"  {word}: {count}x")


def demo_file_processing():
    """Demo 4: File processing"""
    demo_header("DEMO 4: File Processing (TXT, DOCX, PDF)")
    
    stemmer = IndonesianPorterStemmer()
    
    # Cek file yang tersedia
    test_files = ['contoh_dokumen.txt', 'contoh_dokumen.docx', 'contoh_dokumen.pdf']
    available_files = [f for f in test_files if os.path.exists(f)]
    
    if not available_files:
        print("\n⚠️  File contoh tidak ditemukan!")
        print("   Buat file contoh terlebih dahulu atau gunakan file sendiri.")
        return
    
    print(f"\n📁 File yang tersedia: {', '.join(available_files)}\n")
    
    for filepath in available_files:
        print(f"\nMemproses: {filepath}")
        print("-" * 50)
        
        try:
            # Baca file
            text = stemmer.read_file(filepath)
            
            # Stem text
            stemmed = stemmer.stem_sentence(text)
            
            # Statistik
            original_words = text.split()
            stemmed_words = stemmed.split()
            
            print(f"✅ Berhasil!")
            print(f"   - Kata original: {len(original_words)}")
            print(f"   - Kata stemmed: {len(stemmed_words)}")
            print(f"   - Unique original: {len(set(original_words))}")
            print(f"   - Unique stemmed: {len(set(stemmed_words))}")
            
            # Preview
            preview = ' '.join(stemmed.split()[:15])
            print(f"   - Preview: {preview}...")
            
        except Exception as e:
            print(f"❌ Error: {str(e)}")


def demo_advanced_analysis():
    """Demo 5: Analisis lanjutan"""
    demo_header("DEMO 5: Analisis Lanjutan")
    
    stemmer = IndonesianPorterStemmer()
    
    # Contoh teks panjang
    text = """
    Teknologi pendidikan telah mengubah paradigma pembelajaran modern.
    Berbagai inovasi teknologi memungkinkan siswa untuk belajar secara mandiri
    dan mengakses berbagai sumber belajar dari seluruh dunia. Guru juga
    dimudahkan dalam menyampaikan materi dan mengevaluasi hasil belajar.
    Namun, tantangan tetap ada dalam hal infrastruktur dan kompetensi digital.
    """
    
    print("\nAnalisis dokumen:")
    print("-" * 50)
    
    # Stem
    stemmed = stemmer.stem_sentence(text)
    
    # Hitung statistik
    original_words = text.split()
    stemmed_words = stemmed.split()
    
    print(f"\n📊 Statistik Lengkap:")
    print(f"   Total kata        : {len(original_words)}")
    print(f"   Unique original   : {len(set(original_words))}")
    print(f"   Unique stemmed    : {len(set(stemmed_words))}")
    
    reduction = ((len(set(original_words)) - len(set(stemmed_words))) / 
                 len(set(original_words)) * 100)
    print(f"   Reduksi vocabulary: {reduction:.1f}%")
    
    # Kata paling sering
    print(f"\n🔝 Top 10 kata setelah stemming:")
    freq = Counter(stemmed_words)
    for i, (word, count) in enumerate(freq.most_common(10), 1):
        print(f"   {i:2d}. {word:15s} ({count}x)")
    
    # Kata-kata unik yang hilang setelah stemming
    original_unique = set(w.lower() for w in original_words)
    stemmed_unique = set(stemmed_words)
    
    print(f"\n📉 Contoh kata yang di-reduce:")
    examples = [
        ("pembelajaran", stemmer.stem("pembelajaran")),
        ("teknologi", stemmer.stem("teknologi")),
        ("memungkinkan", stemmer.stem("memungkinkan")),
        ("dimudahkan", stemmer.stem("dimudahkan")),
        ("mengevaluasi", stemmer.stem("mengevaluasi")),
    ]
    
    for original, stemmed in examples:
        print(f"   {original:20s} → {stemmed}")


def demo_comparison():
    """Demo 6: Perbandingan dokumen"""
    demo_header("DEMO 6: Perbandingan Similarity Dokumen")
    
    stemmer = IndonesianPorterStemmer()
    
    doc1 = "Pendidikan digital mengubah cara siswa belajar dan berkembang"
    doc2 = "Teknologi pendidikan membantu pelajar dalam pembelajaran modern"
    doc3 = "Makanan sehat penting untuk kesehatan tubuh dan pikiran"
    
    # Stem semua dokumen
    stem1 = set(stemmer.stem_sentence(doc1).split())
    stem2 = set(stemmer.stem_sentence(doc2).split())
    stem3 = set(stemmer.stem_sentence(doc3).split())
    
    # Hitung Jaccard similarity
    def jaccard_similarity(set1, set2):
        intersection = len(set1 & set2)
        union = len(set1 | set2)
        return intersection / union if union > 0 else 0
    
    print("\nDokumen yang dibandingkan:")
    print(f"\nDok 1: {doc1}")
    print(f"Dok 2: {doc2}")
    print(f"Dok 3: {doc3}")
    
    print("\n\n🔍 Hasil Similarity (Jaccard):")
    sim_12 = jaccard_similarity(stem1, stem2)
    sim_13 = jaccard_similarity(stem1, stem3)
    sim_23 = jaccard_similarity(stem2, stem3)
    
    print(f"   Dok 1 vs Dok 2: {sim_12:.2%} (topik sama: pendidikan)")
    print(f"   Dok 1 vs Dok 3: {sim_13:.2%} (topik beda)")
    print(f"   Dok 2 vs Dok 3: {sim_23:.2%} (topik beda)")
    
    print("\n💡 Insight: Dokumen dengan topik serupa memiliki similarity lebih tinggi")


def main():
    """Jalankan semua demo"""
    print("\n")
    print("🌟" * 35)
    print("      INDONESIAN PORTER STEMMER - DEMO LENGKAP")
    print("🌟" * 35)
    print("\nDemo ini menunjukkan semua fitur stemmer untuk tugas Anda")
    print("Algoritma stemming dibuat DARI SCRATCH tanpa library ML/NLP!")
    
    # Jalankan semua demo
    demo_basic_stemming()
    demo_sentence_stemming()
    demo_batch_processing()
    demo_file_processing()
    demo_advanced_analysis()
    demo_comparison()
    
    # Summary
    print("\n" + "=" * 70)
    print("  ✅ DEMO SELESAI")
    print("=" * 70)
    print("\n📚 Yang telah didemonstrasikan:")
    print("   1. ✅ Stemming kata tunggal")
    print("   2. ✅ Stemming kalimat")
    print("   3. ✅ Batch processing")
    print("   4. ✅ File processing (TXT, DOCX, PDF)")
    print("   5. ✅ Analisis statistik")
    print("   6. ✅ Document similarity")
    print("\n💡 Untuk tugas:")
    print("   - Algoritma stemming: DARI SCRATCH ✅")
    print("   - Support file format: TXT, DOCX, PDF ✅")
    print("   - Dokumentasi lengkap tersedia ✅")
    print("\n🚀 Siap untuk digunakan!")
    print("=" * 70)
    print()


if __name__ == "__main__":
    main()
