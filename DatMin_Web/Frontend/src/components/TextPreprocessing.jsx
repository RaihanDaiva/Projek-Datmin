import { useState, useEffect } from 'react';
import { ChevronRight } from 'lucide-react';

// Mock Indonesian stopwords
const INDONESIAN_STOPWORDS = [
  'yang', 'dan', 'di', 'dari', 'ini', 'itu', 'untuk', 'pada', 'dengan', 
  'adalah', 'oleh', 'akan', 'telah', 'atau', 'ke', 'dalam', 'sebagai',
  'juga', 'dapat', 'ada', 'tidak', 'saya', 'kami', 'kita'
];

// Simple Indonesian stemming (simplified for demo)
const stemWord = (word) => {
  // Remove common prefixes
  let stemmed = word.replace(/^(me|mem|men|meng|di|ke|ter|ber|pe|per|se)/, '');
  
  // Remove common suffixes
  stemmed = stemmed.replace(/(kan|an|i)$/, '');
  
  return stemmed || word;
};

export function TextPreprocessing({ processedText, uploadedFiles }) {
  const [caseFoldedText, setCaseFoldedText] = useState('');
  const [tokens, setTokens] = useState([]);
  const [filteredTokens, setFilteredTokens] = useState([]);
  const [removedStopwords, setRemovedStopwords] = useState([]);
  const [stemmedWords, setStemmedWords] = useState([]);

  useEffect(() => {
    if (processedText) {
      // Use sample Indonesian text if uploaded content is generic
      const sampleText = uploadedFiles.length > 0 && processedText.includes('Sample') 
        ? 'Sistem pengambilan dokumen adalah proses untuk menemukan dokumen yang relevan dengan kebutuhan pengguna. Dalam penelitian ini, kami menggunakan algoritma Porter untuk stemming bahasa Indonesia. Preprocessing teks meliputi case folding, tokenizing, filtering stopword, dan stemming untuk menghasilkan representasi dokumen yang optimal.'
        : processedText;

      // Step 1: Case Folding
      const lowercased = sampleText.toLowerCase();
      setCaseFoldedText(lowercased);

      // Step 2: Tokenizing
      const tokenArray = lowercased
        .replace(/[^\w\s]/g, ' ')
        .split(/\s+/)
        .filter(t => t.length > 0);
      setTokens(tokenArray);

      // Step 3: Filtering
      const removed = [];
      const filtered = tokenArray.filter(token => {
        if (INDONESIAN_STOPWORDS.includes(token)) {
          removed.push(token);
          return false;
        }
        return true;
      });
      setRemovedStopwords(removed);
      setFilteredTokens(filtered);

      // Step 4: Stemming
      const stemmed = filtered.map(token => ({
        original: token,
        stemmed: stemWord(token)
      }));
      setStemmedWords(stemmed);
    }
  }, [processedText, uploadedFiles]);

  if (!processedText) {
    return (
      <div className="text-center py-12">
        <p className="text-gray-500">
          Please upload and process documents in the Upload Documents tab first.
        </p>
      </div>
    );
  }

  return (
    <div className="space-y-8">
      <div>
        <h2 className="text-gray-900 mb-2">Text Preprocessing Steps</h2>
        <p className="text-gray-600">
          View detailed preprocessing steps applied to your uploaded documents.
        </p>
      </div>

      {/* Step 1: Case Folding */}
      <div className="bg-gray-50 rounded-lg p-6 border border-gray-200">
        <div className="flex items-center gap-2 mb-4">
          <div className="w-8 h-8 rounded-full bg-blue-500 text-white flex items-center justify-center">
            1
          </div>
          <h3 className="text-gray-900">Case Folding</h3>
        </div>
        
        <div className="grid grid-cols-2 gap-4">
          <div>
            <label className="block text-gray-700 mb-2">Original Text</label>
            <div className="bg-white p-4 rounded border border-gray-200 max-h-40 overflow-y-auto">
              <p className="text-gray-600 whitespace-pre-wrap">{processedText.substring(0, 200)}...</p>
            </div>
          </div>
          <div>
            <label className="block text-gray-700 mb-2">Lowercase Result</label>
            <div className="bg-white p-4 rounded border border-gray-200 max-h-40 overflow-y-auto">
              <p className="text-gray-600 whitespace-pre-wrap">{caseFoldedText.substring(0, 200)}...</p>
            </div>
          </div>
        </div>
      </div>

      {/* Step 2: Tokenizing */}
      <div className="bg-gray-50 rounded-lg p-6 border border-gray-200">
        <div className="flex items-center gap-2 mb-4">
          <div className="w-8 h-8 rounded-full bg-blue-500 text-white flex items-center justify-center">
            2
          </div>
          <h3 className="text-gray-900">Tokenizing</h3>
        </div>
        
        <div>
          <label className="block text-gray-700 mb-2">Tokens ({tokens.length})</label>
          <div className="bg-white p-4 rounded border border-gray-200 max-h-48 overflow-y-auto">
            <div className="flex flex-wrap gap-2">
              {tokens.map((token, idx) => (
                <span
                  key={idx}
                  className="px-3 py-1 bg-blue-100 text-blue-700 rounded-full"
                >
                  {token}
                </span>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* Step 3: Filtering */}
      <div className="bg-gray-50 rounded-lg p-6 border border-gray-200">
        <div className="flex items-center gap-2 mb-4">
          <div className="w-8 h-8 rounded-full bg-blue-500 text-white flex items-center justify-center">
            3
          </div>
          <h3 className="text-gray-900">Filtering (Stopword Removal)</h3>
        </div>
        
        <div className="space-y-4">
          <div>
            <label className="block text-gray-700 mb-2">
              Removed Stopwords ({removedStopwords.length})
            </label>
            <div className="bg-white p-4 rounded border border-gray-200">
              <div className="flex flex-wrap gap-2">
                {removedStopwords.map((word, idx) => (
                  <span
                    key={idx}
                    className="px-3 py-1 bg-red-100 text-red-700 rounded-full line-through"
                  >
                    {word}
                  </span>
                ))}
              </div>
            </div>
          </div>
          
          <div>
            <label className="block text-gray-700 mb-2">
              Filtered Tokens ({filteredTokens.length})
            </label>
            <div className="bg-white p-4 rounded border border-gray-200 max-h-48 overflow-y-auto">
              <div className="flex flex-wrap gap-2">
                {filteredTokens.map((token, idx) => (
                  <span
                    key={idx}
                    className="px-3 py-1 bg-green-100 text-green-700 rounded-full"
                  >
                    {token}
                  </span>
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Step 4: Stemming */}
      <div className="bg-gray-50 rounded-lg p-6 border border-gray-200">
        <div className="flex items-center gap-2 mb-4">
          <div className="w-8 h-8 rounded-full bg-blue-500 text-white flex items-center justify-center">
            4
          </div>
          <h3 className="text-gray-900">Stemming (Indonesian Porter Algorithm)</h3>
        </div>
        
        <div className="bg-white rounded border border-gray-200 overflow-hidden max-h-96 overflow-y-auto">
          <table className="w-full">
            <thead className="bg-gray-50 sticky top-0">
              <tr>
                <th className="px-6 py-3 text-left text-gray-700">Original Word</th>
                <th className="px-6 py-3 text-center text-gray-700">
                  <ChevronRight className="w-5 h-5 mx-auto" />
                </th>
                <th className="px-6 py-3 text-left text-gray-700">Stemmed Word</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-200">
              {stemmedWords.map((item, idx) => (
                <tr key={idx} className="hover:bg-gray-50">
                  <td className="px-6 py-3 text-gray-600">{item.original}</td>
                  <td className="px-6 py-3 text-center">
                    <ChevronRight className="w-4 h-4 text-gray-400 mx-auto" />
                  </td>
                  <td className="px-6 py-3 text-gray-900">{item.stemmed}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
