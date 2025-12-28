#!/usr/bin/env python3
"""
INDONESIAN STEMMER - File Processor
====================================

Script untuk memproses file txt, docx, dan pdf dengan Indonesian Porter Stemmer.

Penggunaan:
    python process_file.py <input_file> [output_file]

    atau...

    python process_file.py
    (nanti disuruh memasukkan nama file berserta ekstensinya pada lokasi root secara interaktif)
    
Contoh:
    python process_file.py dokumen.txt
    python process_file.py dokumen.docx hasil_stemmed.txt
    python process_file.py dokumen.pdf
"""

import sys
import os
from pathlib import Path
from indonesian_porter_stemmer import IndonesianPorterStemmer


def print_header():
    """Tampilkan header aplikasi"""
    print("=" * 70)
    print("🔤 INDONESIAN PORTER STEMMER - File Processor")
    print("=" * 70)
    print()


def print_statistics(original, stemmed):
    """Tampilkan statistik teks"""
    original_words = original.split()
    stemmed_words = stemmed.split()
    
    print("\n📊 Statistik:")
    print(f"   - Jumlah kata asli    : {len(original_words):,}")
    print(f"   - Jumlah kata stemmed : {len(stemmed_words):,}")
    print(f"   - Karakter asli       : {len(original):,}")
    print(f"   - Karakter stemmed    : {len(stemmed):,}")
    
    # Hitung unique words
    unique_original = len(set(original_words))
    unique_stemmed = len(set(stemmed_words))
    print(f"   - Unique kata asli    : {unique_original:,}")
    print(f"   - Unique kata stemmed : {unique_stemmed:,}")
    
    # Hitung reduksi
    if unique_original > 0:
        reduction = ((unique_original - unique_stemmed) / unique_original) * 100
        print(f"   - Reduksi unique kata : {reduction:.1f}%")


def preview_text(text, lines=5):
    """Tampilkan preview teks"""
    text_lines = text.strip().split('\n')
    preview_lines = text_lines[:lines]
    
    for line in preview_lines:
        if line.strip():
            print(f"   {line[:100]}")
    
    if len(text_lines) > lines:
        print(f"   ... ({len(text_lines) - lines} baris lagi)")


def process_file(input_file, output_file=None):
    """
    Proses file dengan stemmer
    
    Args:
        input_file (str): Path ke file input
        output_file (str): Path ke file output (optional)
    """
    print_header()
    
    # Validasi file input
    if not os.path.exists(input_file):
        print(f"❌ Error: File '{input_file}' tidak ditemukan!")
        return False
    
    # Inisialisasi stemmer
    stemmer = IndonesianPorterStemmer()
    
    try:
        # Proses file
        result = stemmer.stem_file(
            input_filepath=input_file,
            output_filepath=output_file,
            save_result=True
        )
        
        # Tampilkan preview
        print(f"\n📝 Preview Teks Asli (5 baris pertama):")
        preview_text(result['original'], lines=5)
        
        print(f"\n📝 Preview Teks Stemmed (5 baris pertama):")
        preview_text(result['stemmed'], lines=5)
        
        # Tampilkan statistik
        print_statistics(result['original'], result['stemmed'])
        
        print(f"\n✅ Proses selesai!")
        print(f"   File output: {result['output_file']}")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        return False


def interactive_mode():
    """Mode interaktif untuk memilih file"""
    print_header()
    print("Mode Interaktif\n")
    
    # Input file path
    print("Masukkan path ke file yang ingin diproses (sertakan ekstensinya juga):")
    print("(Format yang didukung: .txt, .docx, .pdf)")
    input_file = input("📁 Input file: ").strip()
    
    if not input_file:
        print("❌ Path file tidak boleh kosong!")
        return
    
    # Optional output file
    print("\nMasukkan path untuk file output (tekan Enter untuk default):")
    output_file = input("📁 Output file (optional): ").strip()
    
    if not output_file:
        output_file = None
    
    print()
    process_file(input_file, output_file)


def main():
    """Main function"""
    if len(sys.argv) < 2:
        # Jika tidak ada argument, jalankan mode interaktif
        interactive_mode()
    else:
        # Ambil argument dari command line
        input_file = sys.argv[1]
        output_file = sys.argv[2] if len(sys.argv) > 2 else None
        
        process_file(input_file, output_file)


if __name__ == "__main__":
    main()
