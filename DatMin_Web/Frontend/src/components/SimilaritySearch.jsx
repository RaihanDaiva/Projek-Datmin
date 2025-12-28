import { useState, useEffect } from "react";
import {
  Search,
  TrendingUp,
  FileText,
  Database,
  Upload as UploadIcon,
  Eye, // Import Icon Mata untuk tombol detail
} from "lucide-react";

// Asumsi: Anda mengimpor komponen TextPreprocessing dari file lain
// Jika dalam satu file, pastikan fungsi TextPreprocessing ada di atas SimilaritySearch
import { TextPreprocessing } from "./TextPreprocessing";

// ... (Bagian stopwords, stemWord, preprocessText, calculateSimilarity biarkan saja seperti sebelumnya) ...

export function SimilaritySearch({ uploadedFiles }) {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState([]);
  const [hasSearched, setHasSearched] = useState(false);
  const [isProcessing, setIsProcessing] = useState(false);
  const [serverDocuments, setServerDocuments] = useState([]);

  // 1. STATE BARU: Untuk menyimpan dokumen yang dipilih
  const [selectedDoc, setSelectedDoc] = useState(null);

  useEffect(() => {
    fetch("http://localhost:5000/documents")
      .then((res) => res.json())
      .then((data) => setServerDocuments(data));
  }, []);

  const handleSearch = async () => {
    if (!query.trim()) return;

    setIsProcessing(true);
    // Reset selection ketika search baru dilakukan
    setSelectedDoc(null);

    try {
      const res = await fetch("http://localhost:5000/search", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query }),
      });

      const data = await res.json();
      setResults(data);
      setHasSearched(true);
    } catch (error) {
      console.error("Error searching:", error);
    } finally {
      setIsProcessing(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSearch();
    }
  };

  // ... (Helper functions: getSimilarityColor, dll biarkan sama) ...
  const getSimilarityColor = (similarity) => {
    if (similarity >= 50) return "text-green-600";
    if (similarity >= 25) return "text-yellow-600";
    return "text-red-600";
  };

  const getSimilarityBgColor = (similarity) => {
    if (similarity >= 50) return "bg-green-50";
    if (similarity >= 25) return "bg-yellow-50";
    return "bg-red-50";
  };

  const getRelevanceLabel = (similarity) => {
    if (similarity >= 50) return "High";
    if (similarity >= 25) return "Medium";
    return "Low";
  };

  // 2. LOGIKA SWITCH VIEW
  // Jika ada dokumen yang dipilih, tampilkan halaman Detail TextPreprocessing
  if (selectedDoc) {
    return (
      <TextPreprocessing
        selectedDoc={selectedDoc}
        onBack={() => setSelectedDoc(null)}
      />
    );
  }

  // Jika tidak, tampilkan halaman Search (UI Asli)
  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-gray-900 mb-2">Document Similarity Search</h2>
        <p className="text-gray-600">
          Enter your query text to search for similar documents from the server
          dataset.
        </p>
      </div>

      {/* Query Input Section (Sama seperti sebelumnya) */}
      <div className="bg-gray-50 rounded-lg p-6 border border-gray-200">
        <label className="block text-gray-900 mb-3">Query Text</label>
        <textarea
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder="Masukkan teks query..."
          rows={4}
          className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none"
        />
        <div className="flex items-center justify-between mt-4">
          <div className="flex items-center gap-4">{/* Info text... */}</div>
          <button
            onClick={handleSearch}
            disabled={!query.trim() || isProcessing}
            className="px-8 py-3 bg-blue-500 text-white rounded-lg hover:bg-blue-600 disabled:bg-gray-300 transition-colors flex items-center gap-2"
          >
            {isProcessing ? (
              <>
                <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin" />
                Processing...
              </>
            ) : (
              <>
                <Search className="w-5 h-5" />
                Search Similar Documents
              </>
            )}
          </button>
        </div>
      </div>

      {/* Results Section */}
      {hasSearched && (
        <div>
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-gray-900">Similarity Results</h3>
            <span className="text-gray-600">
              {results.filter((r) => r.similarity > 0).length} relevant
              documents found
            </span>
          </div>

          {results.filter((r) => r.similarity > 0).length > 0 ? (
            <div className="space-y-4">
              {/* 3. MODIFIKASI TABEL HASIL */}
              <div className="bg-white rounded-lg border border-gray-200 overflow-hidden">
                <table className="w-full">
                  <thead className="bg-gray-50">
                    <tr>
                      <th className="px-6 py-3 text-left text-gray-700">
                        Rank
                      </th>
                      <th className="px-6 py-3 text-left text-gray-700">
                        Document Name
                      </th>
                      <th className="px-6 py-3 text-left text-gray-700">
                        Similarity Score (%)
                      </th>
                      {/* Tambah Header Kolom Action */}
                      <th className="px-6 py-3 text-center text-gray-700">
                        Action
                      </th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-gray-200">
                    {results
                      .filter((r) => r.similarity > 0)
                      // UBAH BARIS INI: Tambahkan parameter 'index'
                      .map((result, index) => (
                        <tr
                          // UBAH BARIS INI: Gunakan 'index' sebagai key, atau kombinasi agar lebih unik
                          key={`${result.source}-${index}`}
                          className="hover:bg-gray-50 transition-colors"
                        >
                          <td className="px-6 py-4">
                            <div className="flex items-center">
                              <div
                                className={`w-8 h-8 rounded-full flex items-center justify-center ${
                                  result.rank === 1
                                    ? "bg-yellow-100 text-yellow-700"
                                    : result.rank === 2
                                    ? "bg-gray-100 text-gray-700"
                                    : result.rank === 3
                                    ? "bg-orange-100 text-orange-700"
                                    : "bg-gray-50 text-gray-600"
                                }`}
                              >
                                {result.rank}
                              </div>
                            </div>
                          </td>
                          <td className="px-6 py-4">
                            <div className="flex items-center gap-2">
                              {result.source === "server" ? (
                                <Database className="w-4 h-4 text-blue-500" />
                              ) : (
                                <UploadIcon className="w-4 h-4 text-green-500" />
                              )}
                              <span className="text-gray-900 font-medium">
                                {result.documentName}
                              </span>
                            </div>
                          </td>
                          <td className="px-6 py-4">
                            <div className="flex items-center gap-3">
                              <div className="flex-1 max-w-xs">
                                <div className="h-2 bg-gray-200 rounded-full overflow-hidden">
                                  <div
                                    className={`h-full transition-all ${
                                      result.similarity >= 50
                                        ? "bg-green-500"
                                        : result.similarity >= 25
                                        ? "bg-yellow-500"
                                        : "bg-red-500"
                                    }`}
                                    style={{ width: `${result.similarity}%` }}
                                  />
                                </div>
                              </div>
                              <span
                                className={`min-w-[50px] font-semibold ${getSimilarityColor(
                                  result.similarity
                                )}`}
                              >
                                {result.similarity.toFixed(2)}%
                              </span>
                            </div>
                          </td>

                          {/* Tambah Tombol Detail */}
                          <td className="px-6 py-4 text-center">
                            <button
                              onClick={() => setSelectedDoc(result)}
                              className="inline-flex items-center gap-1.5 px-3 py-1.5 bg-white border border-blue-200 text-blue-600 rounded-md hover:bg-blue-50 hover:border-blue-300 transition-all text-sm font-medium shadow-sm"
                              title="Lihat detail preprocessing"
                            >
                              <Eye className="w-4 h-4" />
                              Detail
                            </button>
                          </td>
                        </tr>
                      ))}
                  </tbody>
                </table>
              </div>

              {/* Visual Chart Section (Biarkan sama) */}
              {/* Visual Chart Section */}
              <div className="bg-white rounded-lg border border-gray-200 p-6">
                <h4 className="text-gray-900 mb-4">
                  Similarity Score Distribution
                </h4>
                <div className="space-y-3">
                  {results
                    .filter((r) => r.similarity > 0)
                    .slice(0, 10)
                    // PERUBAHAN 1: Tambahkan parameter 'index' di sini
                    .map((result, index) => (
                      <div
                        // PERUBAHAN 2: Gunakan index sebagai key agar unik
                        key={`chart-${index}`}
                        className="space-y-1"
                      >
                        <div className="flex items-center justify-between">
                          <span className="text-gray-700">
                            {result.documentName}
                          </span>
                          <span
                            className={getSimilarityColor(result.similarity)}
                          >
                            {result.similarity.toFixed(2)}%
                          </span>
                        </div>
                        <div className="h-3 bg-gray-100 rounded-full overflow-hidden">
                          <div
                            className={`h-full transition-all ${
                              result.similarity >= 50
                                ? "bg-green-500"
                                : result.similarity >= 25
                                ? "bg-yellow-500"
                                : "bg-red-500"
                            }`}
                            style={{ width: `${result.similarity}%` }}
                          />
                        </div>
                      </div>
                    ))}
                </div>
              </div>
            </div>
          ) : (
            <div className="text-center py-12 bg-gray-50 rounded-lg border border-gray-200">
              <Search className="w-12 h-12 text-gray-400 mx-auto mb-3" />
              <p className="text-gray-600 mb-1">No similar documents found</p>
              <p className="text-gray-500">
                Try adjusting your query with different keywords
              </p>
            </div>
          )}
        </div>
      )}

      {/* Info Card (Biarkan sama) */}
      {!hasSearched && (
        <div className="bg-gray-50 border border-gray-200 rounded-lg p-6">
          {/* ... isi info card ... */}
          <div className="flex items-start gap-4">
            <TrendingUp className="w-6 h-6 text-gray-400 flex-shrink-0 mt-1" />
            <div>
              <h4 className="text-gray-900 mb-2">How it works</h4>
              {/* ... */}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
