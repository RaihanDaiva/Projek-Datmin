// Mock Indonesian documents stored on server
export const SERVER_DOCUMENTS = [
  {
    id: 'doc1',
    name: 'Sistem Temu Kembali Informasi.txt',
    type: '.txt',
    status: 'Available',
    content: 'Sistem temu kembali informasi adalah sistem yang digunakan untuk menemukan dokumen yang relevan dengan kebutuhan pengguna. Sistem ini menggunakan berbagai teknik pemrosesan teks seperti tokenisasi, filtering, dan stemming untuk menghasilkan representasi dokumen yang optimal.'
  },
  {
    id: 'doc2',
    name: 'Algoritma Stemming Porter.txt',
    type: '.txt',
    status: 'Available',
    content: 'Algoritma Porter untuk bahasa Indonesia adalah metode stemming yang mengubah kata berimbuhan menjadi kata dasar. Proses stemming meliputi penghapusan awalan seperti me, di, ke, ter, ber dan akhiran seperti kan, an, i. Algoritma ini penting dalam preprocessing teks bahasa Indonesia.'
  },
  {
    id: 'doc3',
    name: 'Preprocessing Teks.pdf',
    type: '.pdf',
    status: 'Available',
    content: 'Preprocessing teks merupakan tahapan penting dalam pengolahan dokumen. Tahapan preprocessing meliputi case folding untuk mengubah semua huruf menjadi huruf kecil, tokenizing untuk memecah teks menjadi token, filtering untuk menghapus stopword, dan stemming untuk mengubah kata ke bentuk dasar.'
  },
  {
    id: 'doc4',
    name: 'Cosine Similarity.docx',
    type: '.docx',
    status: 'Available',
    content: 'Cosine similarity adalah metode untuk mengukur kemiripan antara dua dokumen berdasarkan sudut antara vektor representasi dokumen. Metode ini banyak digunakan dalam sistem temu kembali informasi dan information retrieval. Nilai cosine similarity berkisar antara 0 hingga 1, dimana 1 menunjukkan dokumen identik.'
  },
  {
    id: 'doc5',
    name: 'TF-IDF Weighting.txt',
    type: '.txt',
    status: 'Available',
    content: 'TF-IDF adalah singkatan dari Term Frequency - Inverse Document Frequency. Metode ini digunakan untuk memberikan bobot pada setiap kata dalam dokumen. Term frequency menghitung frekuensi kemunculan kata, sedangkan inverse document frequency mengukur seberapa penting kata tersebut di seluruh koleksi dokumen.'
  },
  {
    id: 'doc6',
    name: 'Stopword Removal.pdf',
    type: '.pdf',
    status: 'Available',
    content: 'Stopword adalah kata-kata yang sering muncul dalam teks namun tidak memiliki makna penting seperti yang, dan, di, dari, untuk, adalah, dengan. Proses stopword removal bertujuan untuk menghilangkan kata-kata tersebut agar fokus pada kata-kata yang lebih bermakna dalam analisis dokumen.'
  },
  {
    id: 'doc7',
    name: 'Natural Language Processing.txt',
    type: '.txt',
    status: 'Available',
    content: 'Natural Language Processing atau NLP adalah bidang yang mempelajari interaksi antara komputer dan bahasa manusia. Aplikasi NLP meliputi text mining, sentiment analysis, machine translation, dan question answering. Pemrosesan bahasa alami memerlukan pemahaman struktur bahasa dan semantik.'
  },
  {
    id: 'doc8',
    name: 'Tokenisasi Bahasa Indonesia.docx',
    type: '.docx',
    status: 'Available',
    content: 'Tokenisasi adalah proses memecah teks menjadi unit-unit yang lebih kecil yang disebut token. Dalam bahasa Indonesia, tokenisasi umumnya dilakukan berdasarkan spasi dan tanda baca. Token dapat berupa kata, angka, atau simbol. Tokenisasi merupakan langkah awal dalam preprocessing teks.'
  },
  {
    id: 'doc9',
    name: 'Information Retrieval System.pdf',
    type: '.pdf',
    status: 'Available',
    content: 'Information retrieval system adalah sistem yang dirancang untuk mengambil informasi yang relevan dari kumpulan dokumen besar. Sistem ini menggunakan query dari pengguna untuk mencari dan merangking dokumen berdasarkan relevansi. Evaluasi sistem IR menggunakan metrik seperti precision dan recall.'
  },
  {
    id: 'doc10',
    name: 'Text Similarity Measures.txt',
    type: '.txt',
    status: 'Available',
    content: 'Pengukuran kemiripan teks dapat dilakukan dengan berbagai metode seperti jaccard similarity, dice coefficient, dan cosine similarity. Setiap metode memiliki karakteristik dan keunggulan masing-masing. Pemilihan metode tergantung pada jenis data dan kebutuhan aplikasi yang dikembangkan.'
  }
];
