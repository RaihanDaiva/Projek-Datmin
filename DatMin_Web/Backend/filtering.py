# Cara menggunakan filtering stopword

# ==========================================================
# from filtering import StopwordFilter

# tokens = [
#     'pendidikan', 'dan', 'pembelajaran', 'di', 'era', 'digital',
#     'pendidikan', 'merupakan', 'aspek', 'fundamental', 'dalam'
# ]

# filtering = StopwordFilter()
# filtered_tokens = filtering.filter_tokens(tokens)

# print(filtered_tokens)
# ==========================================================


class StopwordFilter:
    """
    Stopword Filtering untuk Bahasa Indonesia (OOP)
    -----------------------------------------------
    Menghapus kata-kata umum (stopwords) yang tidak
    memiliki makna penting dalam proses temu balik.
    """

    def __init__(self, custom_stopwords=None):
        # Stopword dasar Bahasa Indonesia
        self.stopwords = set([
            'dan', 'di', 'ke', 'dari', 'yang', 'untuk', 'dengan',
            'pada', 'dalam', 'oleh', 'sebagai', 'adalah', 'itu',
            'ini', 'atau', 'juga', 'tidak', 'lagi', 'sudah',
            'akan', 'telah', 'dapat', 'harus', 'sangat',
            'lebih', 'antara', 'para', 'secara', 'agar',
            'karena', 'hingga', 'maka', 'namun', 'tetapi',
            'sehingga', 'yaitu', 'yakni', 'guna', 'melalui',
            'saja', 'pun', 'lah', 'nya', 'ku', 'mu',
            'mereka', 'kita', 'kami', 'saya', 'anda'
        ])

        # Tambah stopword custom jika ada
        if custom_stopwords:
            self.stopwords.update(custom_stopwords)

    def filter_tokens(self, tokens):
        """
        Menghapus stopword dari token list

        Args:
            tokens (list): List token hasil tokenizing

        Returns:
            list: Token tanpa stopword
        """
        return [token for token in tokens if token not in self.stopwords]

    def filter_and_count(self, tokens):
        """
        Filtering + hitung frekuensi

        Args:
            tokens (list): Token hasil tokenizing

        Returns:
            dict: {kata: frekuensi}
        """
        filtered = self.filter_tokens(tokens)
        freq = {}

        for token in filtered:
            freq[token] = freq.get(token, 0) + 1

        return freq
    
    def filter_with_removed(self, tokens):
        filtered = []
        removed = []

        for t in tokens:
            if t in self.stopwords:
                removed.append(t)
            else:
                filtered.append(t)

        return filtered, removed
