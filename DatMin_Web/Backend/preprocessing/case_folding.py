import re

# Cara menggunakan case folding

# ==========================================================
# from case_folding import CaseFolding

# cf = CaseFolding()

# filtered_tokens = [
#     'Pendidikan', 'Pembelajaran', 'Digital', 'Teknologi'
# ]

# result = cf.process_tokens(filtered_tokens)

# print(result)
# ==========================================================

class CaseFolding:
    """
    Case Folding (OOP)
    ------------------
    Mengubah teks menjadi lowercase dan
    membersihkan karakter non-alfanumerik
    """

    def __init__(self, keep_number=True):
        """
        Args:
            keep_number (bool): 
                True  -> angka dipertahankan
                False -> angka dihapus
        """
        self.keep_number = keep_number

    def process_text(self, text):
        """
        Case folding untuk teks mentah (string)

        Args:
            text (str): teks asli

        Returns:
            str: teks hasil case folding
        """
        # Lowercase
        text = text.lower()

        # Hapus karakter non-alfanumerik
        if self.keep_number:
            text = re.sub(r'[^a-z0-9\s]', ' ', text)
        else:
            text = re.sub(r'[^a-z\s]', ' ', text)

        # Hapus spasi berlebih
        text = re.sub(r'\s+', ' ', text).strip()

        return text

    def process_tokens(self, tokens):
        """
        Case folding untuk list token

        Args:
            tokens (list): token hasil tokenizing

        Returns:
            list: token lowercase
        """
        return [token.lower() for token in tokens]