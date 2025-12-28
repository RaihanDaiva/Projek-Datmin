import { useState, useEffect } from 'react';
import { Search, TrendingUp, FileText, Database, Upload as UploadIcon } from 'lucide-react';

// Indonesian stopwords
const INDONESIAN_STOPWORDS = [
  'yang', 'dan', 'di', 'dari', 'ini', 'itu', 'untuk', 'pada', 'dengan', 
  'adalah', 'oleh', 'akan', 'telah', 'atau', 'ke', 'dalam', 'sebagai',
  'juga', 'dapat', 'ada', 'tidak', 'saya', 'kami', 'kita', 'seperti',
  'semua', 'antara', 'tersebut', 'setiap', 'saat', 'hanya'
];

// Simple Indonesian stemming
const stemWord = (word) => {
  let stemmed = word.replace(/^(me|mem|men|meng|meny|di|ke|ter|ber|be|pe|per|se)/, '');
  stemmed = stemmed.replace(/(kan|an|i|nya)$/, '');
  return stemmed || word;
};

// Preprocessing ini akan diganti dengan menggunakan Flask di backend
// Preprocessing function
const preprocessText = (text) => {
  // Case folding
  const lowercased = text.toLowerCase();
  
  // Tokenizing
  const tokens = lowercased
    .replace(/[^\w\s]/g, ' ')
    .split(/\s+/)
    .filter(t => t.length > 0);
  
  // Filtering (stopword removal)
  const filtered = tokens.filter(token => !INDONESIAN_STOPWORDS.includes(token));
  
  // Stemming
  const stemmed = filtered.map(token => stemWord(token));
  
  return stemmed;
};

// Calculate TF-IDF and Cosine Similarity
const calculateSimilarity = (query, documents, uploadedFiles) => {
  const queryTokens = preprocessText(query);
  
  if (queryTokens.length === 0) {
    return [];
  }
  
  // Preprocess all documents
  const docTokens = documents.map(doc => preprocessText(doc.content));
  const uploadedTokens = uploadedFiles.map(file => preprocessText(file.content));
  
  // Build vocabulary
  const vocabulary = new Set();
  queryTokens.forEach(token => vocabulary.add(token));
  docTokens.forEach(tokens => tokens.forEach(token => vocabulary.add(token)));
  uploadedTokens.forEach(tokens => tokens.forEach(token => vocabulary.add(token)));
  
  // Calculate IDF
  const idf = new Map();
  vocabulary.forEach(term => {
    const docsWithTerm = docTokens.filter(tokens => tokens.includes(term)).length;
    const uploadedWithTerm = uploadedTokens.filter(tokens => tokens.includes(term)).length;
    idf.set(term, Math.log((documents.length + uploadedFiles.length + 1) / (docsWithTerm + uploadedWithTerm + 1)) + 1);
  });
  
  // Calculate TF-IDF for query
  const queryTfidf = new Map();
  queryTokens.forEach(token => {
    const tf = queryTokens.filter(t => t === token).length / queryTokens.length;
    queryTfidf.set(token, tf * (idf.get(token) || 0));
  });
  
  // Calculate TF-IDF for documents and cosine similarity
  const results = documents.map((doc, idx) => {
    const tokens = docTokens[idx];
    const docTfidf = new Map();
    
    tokens.forEach(token => {
      const tf = tokens.filter(t => t === token).length / tokens.length;
      docTfidf.set(token, tf * (idf.get(token) || 0));
    });
    
    // Cosine similarity
    let dotProduct = 0;
    let queryMagnitude = 0;
    let docMagnitude = 0;
    
    vocabulary.forEach(term => {
      const queryVal = queryTfidf.get(term) || 0;
      const docVal = docTfidf.get(term) || 0;
      
      dotProduct += queryVal * docVal;
      queryMagnitude += queryVal * queryVal;
      docMagnitude += docVal * docVal;
    });
    
    const similarity = queryMagnitude > 0 && docMagnitude > 0
      ? (dotProduct / (Math.sqrt(queryMagnitude) * Math.sqrt(docMagnitude))) * 100
      : 0;
    
    return {
      documentId: doc.id,
      documentName: doc.name,
      similarity: similarity,
      rank: 0,
      source: 'server'
    };
  });
  
  // Calculate TF-IDF for uploaded files and cosine similarity
  const uploadedResults = uploadedFiles.map((file, idx) => {
    const tokens = uploadedTokens[idx];
    const fileTfidf = new Map();
    
    tokens.forEach(token => {
      const tf = tokens.filter(t => t === token).length / tokens.length;
      fileTfidf.set(token, tf * (idf.get(token) || 0));
    });
    
    // Cosine similarity
    let dotProduct = 0;
    let queryMagnitude = 0;
    let fileMagnitude = 0;
    
    vocabulary.forEach(term => {
      const queryVal = queryTfidf.get(term) || 0;
      const fileVal = fileTfidf.get(term) || 0;
      
      dotProduct += queryVal * fileVal;
      queryMagnitude += queryVal * queryVal;
      fileMagnitude += fileVal * fileVal;
    });
    
    const similarity = queryMagnitude > 0 && fileMagnitude > 0
      ? (dotProduct / (Math.sqrt(queryMagnitude) * Math.sqrt(fileMagnitude))) * 100
      : 0;
    
    return {
      documentId: file.id,
      documentName: file.name,
      similarity: similarity,
      rank: 0,
      source: 'uploaded'
    };
  });
  
  // Combine results
  const combinedResults = [...results, ...uploadedResults];
  
  // Sort by similarity and assign ranks
  combinedResults.sort((a, b) => b.similarity - a.similarity);
  combinedResults.forEach((result, idx) => {
    result.rank = idx + 1;
  });
  
  return combinedResults;
};

export function SimilaritySearch({ uploadedFiles }) {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);
  const [hasSearched, setHasSearched] = useState(false);
  const [isProcessing, setIsProcessing] = useState(false);
  const [serverDocuments, setServerDocuments] = useState([]);

  // Fetch server documents from backend
  useEffect(() => {
    fetch('http://localhost:5000/documents')
      .then(res => res.json())
      .then(data => setServerDocuments(data));
  }, []);

  const handleSearch = () => {
    if (query.trim()) {
      setIsProcessing(true);
      setTimeout(() => {
        // Pastikan dokumen server diambil dari state
        const similarityResults = calculateSimilarity(query, serverDocuments, uploadedFiles);
        setResults(similarityResults);
        setHasSearched(true);
        setIsProcessing(false);
      }, 500);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSearch();
    }
  };

  const getSimilarityColor = (similarity) => {
    if (similarity >= 50) return 'text-green-600';
    if (similarity >= 25) return 'text-yellow-600';
    return 'text-red-600';
  };

  const getSimilarityBgColor = (similarity) => {
    if (similarity >= 50) return 'bg-green-50';
    if (similarity >= 25) return 'bg-yellow-50';
    return 'bg-red-50';
  };

  const getRelevanceLabel = (similarity) => {
    if (similarity >= 50) return 'High';
    if (similarity >= 25) return 'Medium';
    return 'Low';
  };

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-gray-900 mb-2">Document Similarity Search</h2>
        <p className="text-gray-600">
          Enter your query text to search for similar documents from the server dataset using TF-IDF and Cosine Similarity.
        </p>
      </div>

      {/* Query Input */}
      <div className="bg-gray-50 rounded-lg p-6 border border-gray-200">
        <label className="block text-gray-900 mb-3">
          Query Text
        </label>
        <textarea
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder="Masukkan teks query untuk mencari dokumen yang mirip...&#10;Contoh: sistem temu kembali informasi, algoritma stemming porter, preprocessing teks"
          rows={4}
          className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none"
        />
        <div className="flex items-center justify-between mt-4">
          <div className="flex items-center gap-4">
            <p className="text-gray-500">
              Searching in: <span className="text-gray-700">{serverDocuments.length} server documents</span>
              {uploadedFiles.length > 0 && <span className="text-gray-700"> + {uploadedFiles.length} uploaded files</span>}
            </p>
          </div>
          <button
            onClick={handleSearch}
            disabled={!query.trim() || isProcessing}
            className="px-8 py-3 bg-blue-500 text-white rounded-lg hover:bg-blue-600 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors flex items-center gap-2"
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

      {/* Processing Pipeline Info */}
      <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
        <h4 className="text-blue-900 mb-2">Processing Pipeline</h4>
        <div className="flex flex-wrap gap-2">
          {['Case Folding', 'Tokenizing', 'Filtering', 'Indonesian Porter Stemming', 'TF-IDF Vectorization', 'Cosine Similarity'].map((step, idx) => (
            <span key={idx} className="px-3 py-1 bg-white text-blue-700 rounded-full border border-blue-200">
              {idx + 1}. {step}
            </span>
          ))}
        </div>
      </div>

      {/* Results */}
      {hasSearched && (
        <div>
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-gray-900">Similarity Results</h3>
            <span className="text-gray-600">
              {results.filter(r => r.similarity > 0).length} relevant documents found
            </span>
          </div>
          
          {results.filter(r => r.similarity > 0).length > 0 ? (
            <div className="space-y-4">
              {/* Results Table */}
              <div className="bg-white rounded-lg border border-gray-200 overflow-hidden">
                <table className="w-full">
                  <thead className="bg-gray-50">
                    <tr>
                      <th className="px-6 py-3 text-left text-gray-700">Rank</th>
                      <th className="px-6 py-3 text-left text-gray-700">Document Name</th>
                      <th className="px-6 py-3 text-left text-gray-700">Similarity Score (%)</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-gray-200">
                    {results.filter(r => r.similarity > 0).map((result) => (
                      <tr key={result.documentId} className="hover:bg-gray-50">
                        <td className="px-6 py-4">
                          <div className="flex items-center">
                            <div className={`w-8 h-8 rounded-full flex items-center justify-center ${
                              result.rank === 1 ? 'bg-yellow-100 text-yellow-700' :
                              result.rank === 2 ? 'bg-gray-100 text-gray-700' :
                              result.rank === 3 ? 'bg-orange-100 text-orange-700' :
                              'bg-gray-50 text-gray-600'
                            }`}>
                              {result.rank}
                            </div>
                          </div>
                        </td>
                        <td className="px-6 py-4">
                          <div className="flex items-center gap-2">
                            {result.source === 'server' ? (
                              <Database className="w-4 h-4 text-blue-500" />
                            ) : (
                              <UploadIcon className="w-4 h-4 text-green-500" />
                            )}
                            <span className="text-gray-900">{result.documentName}</span>
                            <span className={`text-xs px-2 py-0.5 rounded ${
                              result.source === 'server' 
                                ? 'bg-blue-100 text-blue-700' 
                                : 'bg-green-100 text-green-700'
                            }`}>
                              {result.source === 'server' ? 'Server' : 'Uploaded'}
                            </span>
                          </div>
                        </td>
                        <td className="px-6 py-4">
                          <div className="flex items-center gap-3">
                            <div className="flex-1 max-w-xs">
                              <div className="h-2 bg-gray-200 rounded-full overflow-hidden">
                                <div
                                  className={`h-full transition-all ${
                                    result.similarity >= 50 ? 'bg-green-500' :
                                    result.similarity >= 25 ? 'bg-yellow-500' :
                                    'bg-red-500'
                                  }`}
                                  style={{ width: `${result.similarity}%` }}
                                />
                              </div>
                            </div>
                            <span className={`min-w-[80px] ${getSimilarityColor(result.similarity)}`}>
                              {result.similarity.toFixed(2)}%
                            </span>
                            <span className={`px-3 py-1 rounded-full min-w-[80px] text-center ${getSimilarityBgColor(result.similarity)} ${getSimilarityColor(result.similarity)}`}>
                              {getRelevanceLabel(result.similarity)}
                            </span>
                          </div>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>

              {/* Visual Chart */}
              <div className="bg-white rounded-lg border border-gray-200 p-6">
                <h4 className="text-gray-900 mb-4">Similarity Score Distribution</h4>
                <div className="space-y-3">
                  {results.filter(r => r.similarity > 0).slice(0, 10).map((result) => (
                    <div key={result.documentId} className="space-y-1">
                      <div className="flex items-center justify-between">
                        <span className="text-gray-700">{result.documentName}</span>
                        <span className={getSimilarityColor(result.similarity)}>
                          {result.similarity.toFixed(2)}%
                        </span>
                      </div>
                      <div className="h-3 bg-gray-100 rounded-full overflow-hidden">
                        <div
                          className={`h-full transition-all ${
                            result.similarity >= 50 ? 'bg-green-500' :
                            result.similarity >= 25 ? 'bg-yellow-500' :
                            'bg-red-500'
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
              <p className="text-gray-500">Try adjusting your query with different keywords</p>
            </div>
          )}
        </div>
      )}

      {/* Info Card */}
      {!hasSearched && (
        <div className="bg-gray-50 border border-gray-200 rounded-lg p-6">
          <div className="flex items-start gap-4">
            <TrendingUp className="w-6 h-6 text-gray-400 flex-shrink-0 mt-1" />
            <div>
              <h4 className="text-gray-900 mb-2">How it works</h4>
              <p className="text-gray-600 mb-3">
                This system searches for similar documents from the server dataset using advanced text processing:
              </p>
              <ul className="space-y-1 text-gray-600">
                <li>• <strong>Preprocessing:</strong> Case folding, tokenizing, stopword removal, and Indonesian Porter stemming</li>
                <li>• <strong>Vectorization:</strong> TF-IDF (Term Frequency - Inverse Document Frequency) weighting</li>
                <li>• <strong>Similarity:</strong> Cosine similarity to measure document relevance (0-100%)</li>
              </ul>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
