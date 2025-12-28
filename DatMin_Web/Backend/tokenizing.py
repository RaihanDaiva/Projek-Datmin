import os
import re
from collections import Counter
from pathlib import Path
import docx
import pdfplumber


# Cara menggunakan class tokenizer

# ==========================================================
# from tokenizing import Tokenizer

# tokenizer = Tokenizer()

# tokens = tokenizer.process_file("data/dokumen1.txt")
# print(tokens)
# ==========================================================

class Tokenizer:
    """
    Tokenizer untuk preprocessing dokumen teks
    - Case folding
    - Tokenizing
    - Cleaning
    - Frequency counting
    """

    def __init__(self, remove_numbers=True, min_length=2):
        self.remove_numbers = remove_numbers
        self.min_length = min_length

    # =============================
    # FILE READER
    # =============================
    def read_txt(self, file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()

    def read_pdf(self, file_path):
        text = ""
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + " "
        return text

    def read_docx(self, file_path):
        doc = docx.Document(file_path)
        return "\n".join(p.text for p in doc.paragraphs)

    def read_file(self, file_path):
        ext = Path(file_path).suffix.lower()

        if ext == ".txt":
            return self.read_txt(file_path)
        elif ext == ".pdf":
            return self.read_pdf(file_path)
        elif ext == ".docx":
            return self.read_docx(file_path)
        else:
            raise ValueError("Format file tidak didukung")

    # =============================
    # TEXT PROCESSING
    # =============================
    def case_folding(self, text):
        return text.lower()

    def tokenize(self, text):
        if self.remove_numbers:
            tokens = re.findall(r"[a-z]+", text)
        else:
            tokens = re.findall(r"[a-z0-9]+", text)

        return [t for t in tokens if len(t) >= self.min_length]

    def process_text(self, text):
        text = self.case_folding(text)
        tokens = self.tokenize(text)
        return tokens

    # =============================
    # DOCUMENT PROCESSING
    # =============================
    def process_file(self, file_path):
        text = self.read_file(file_path)
        tokens = self.process_text(text)
        return tokens

    def process_folder(self, folder_path):
        results = {}

        files = os.listdir(folder_path)
        for file in files:
            path = os.path.join(folder_path, file)

            try:
                tokens = self.process_file(path)
                results[file] = Counter(tokens)
            except Exception as e:
                print(f"(!!) Skip {file}: {e}")

        return results

# tokenizer = Tokenizer()

# tokens = tokenizer.process_file("/home/han/Documents/Kuliah/S5/Data Mining/Tokenizing/test/contoh.txt")
# print(tokens)