import os
import re
from collections import Counter

import docx
import pdfplumber


# Fungsi membaca file TXT
def read_txt(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()


# Fungsi membaca file PDF
def read_pdf(file_path):
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + " "
    return text


# Fungsi membaca file DOCX
def read_docx(file_path):
    doc = docx.Document(file_path)
    text = "\n".join([para.text for para in doc.paragraphs])
    return text


# Fungsi membersihkan teks
def clean_text(text):
    text = text.lower()
    words = re.findall(r"[a-zA-Z0-9]+", text)
    return words


# Main program
def process_documents(folder_path):
    print(f"Nama path: {folder_path}\n")
    file_list = os.listdir(folder_path)

    for idx, filename in enumerate(file_list, start=1):
        file_path = os.path.join(folder_path, filename)
        ext = filename.split(".")[-1].lower()

        text = ""

        if ext == "txt":
            text = read_txt(file_path)
        elif ext == "pdf":
            text = read_pdf(file_path)
        elif ext == "docx":
            text = read_docx(file_path)
        else:
            print(f"(!!) Format file tidak didukung: {filename}")
            continue

        words = clean_text(text)
        frequencies = Counter(words)

        print(f"{idx}. {filename}")
        print("   Mengandung kata:")
        for word, count in frequencies.items():
            print(f"   {word} = {count}")
        print("\n")


# Cara menjalankan
if __name__ == "__main__":
    path = input("Masukkan path folder dokumen: ")
    process_documents(path)


