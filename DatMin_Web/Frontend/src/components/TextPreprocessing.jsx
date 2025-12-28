import React, { useMemo, useState } from 'react';
import { ChevronRight, ArrowLeft, CheckCircle, AlertCircle } from 'lucide-react';

export function TextPreprocessing({ selectedDoc, onBack }) {
  const [stemmingLimit, setStemmingLimit] = useState(100);

  // 1. Validasi Data
  if (!selectedDoc || !selectedDoc.preprocessing) {
    return (
      <div className="flex flex-col items-center justify-center py-20 bg-gray-50 rounded-xl border border-dashed border-gray-300">
        <div className="bg-gray-100 p-4 rounded-full mb-4">
          <AlertCircle className="w-8 h-8 text-gray-400" />
        </div>
        <p className="text-gray-500 font-medium">Data preprocessing tidak ditemukan.</p>
        <button onClick={onBack} className="mt-4 text-blue-600 hover:text-blue-700 hover:underline font-medium">
          Kembali ke hasil pencarian
        </button>
      </div>
    );
  }

  const p = selectedDoc.preprocessing;

  // 2. Mapping Data (SESUAI JSON SERVER)
  const originalText = p.original_text || "Teks asli tidak tersedia";
  const caseFoldedText = p.case_folding || "";
  const tokens = p.tokens || [];
  
  // Ambil langsung dari JSON, tidak perlu hitung manual
  const filteredTokens = p.filtered_tokens || [];
  const rawRemovedStopwords = p.removed_stopwords || [];
  const rawStemming = p.stemming || [];

  // 3. Logika Tampilan (useMemo)
  const { uniqueRemovedStopwords, stemmingPairs } = useMemo(() => {
    // A. Stopword: Ambil unik dari data server
    const uniqueRemoved = [...new Set(rawRemovedStopwords)];

    // B. Stemming: Mapping langsung dari array object server
    // Server sudah mengirim format: [{original: "...", stemmed: "..."}, ...]
    const pairs = rawStemming.map((item) => ({
      original: item.original,
      stemmed: item.stemmed,
      // Flag warna jika kata berubah
      isChanged: item.original !== item.stemmed 
    }));

    return { uniqueRemovedStopwords: uniqueRemoved, stemmingPairs: pairs };
  }, [rawRemovedStopwords, rawStemming]);

  return (
    <div className="space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-500 pb-12">
      
      {/* Header */}
      <div className="flex items-center justify-between sticky top-0 bg-white/80 backdrop-blur-sm z-20 py-4 border-b border-gray-100">
        <div>
          <h2 className="text-2xl font-bold text-gray-900 flex items-center gap-2">
            Pipeline Detail
            <span className="px-2 py-1 bg-blue-100 text-blue-700 text-xs rounded-full font-normal">
              {tokens.length} Token
            </span>
          </h2>
          <p className="text-gray-600 text-sm mt-1">
            File: <span className="font-semibold text-blue-600">{selectedDoc.documentName}</span>
          </p>
        </div>
        <button
          onClick={onBack}
          className="flex items-center gap-2 px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 transition-all hover:shadow-sm"
        >
          <ArrowLeft className="w-4 h-4" />
          Kembali
        </button>
      </div>

      {/* Step 1: Case Folding */}
      <SectionCard step="1" title="Case Folding" description="Mengubah semua huruf menjadi huruf kecil.">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <CodeBlock label="Teks Asli" content={originalText} />
          <CodeBlock label="Hasil Lowercase" content={caseFoldedText} isPrimary />
        </div>
      </SectionCard>

      {/* Step 2: Tokenizing */}
      <SectionCard step="2" title="Tokenizing" description={`Memecah kalimat menjadi ${tokens.length} token terpisah.`}>
        <div className="bg-white p-4 rounded-lg border border-gray-200 max-h-60 overflow-y-auto custom-scrollbar">
          <div className="flex flex-wrap gap-2">
            {tokens.slice(0, 200).map((token, idx) => (
              <span key={idx} className="px-2 py-1 bg-gray-100 text-gray-600 text-xs rounded border border-gray-200 font-mono">
                {token}
              </span>
            ))}
            {tokens.length > 200 && (
              <span className="px-2 py-1 text-gray-400 text-xs italic">
                ... (+{tokens.length - 200} lainnya)
              </span>
            )}
          </div>
        </div>
      </SectionCard>

      {/* Step 3: Filtering */}
      <SectionCard step="3" title="Filtering" description="Menghapus kata hubung (Stopwords) yang tidak bermakna.">
        <div className="space-y-6">
          {/* Stopwords Dibuang (Data dari server: removed_stopwords) */}
          <div className="bg-red-50/50 rounded-lg p-5 border border-red-100">
            <label className="block text-sm font-bold text-red-800 mb-3 flex items-center gap-2">
              <span className="w-2 h-2 rounded-full bg-red-500"></span>
              Stopwords Dibuang ({uniqueRemovedStopwords.length} unik)
            </label>
            <div className="flex flex-wrap gap-2 max-h-40 overflow-y-auto custom-scrollbar">
              {uniqueRemovedStopwords.length > 0 ? uniqueRemovedStopwords.map((word, idx) => (
                <span key={idx} className="px-2 py-0.5 bg-white text-red-600 text-xs rounded border border-red-200 line-through decoration-red-400 opacity-75">
                  {word}
                </span>
              )) : <span className="text-gray-400 text-sm italic">Tidak ada stopword yang dibuang.</span>}
            </div>
          </div>
          
          {/* Hasil (Data dari server: filtered_tokens) */}
          <div className="bg-green-50/50 rounded-lg p-5 border border-green-100">
             <label className="block text-sm font-bold text-green-800 mb-3 flex items-center gap-2">
              <CheckCircle className="w-4 h-4" />
              Hasil Bersih ({filteredTokens.length} kata)
            </label>
            <div className="flex flex-wrap gap-2 max-h-40 overflow-y-auto custom-scrollbar">
              {filteredTokens.length > 0 ? filteredTokens.slice(0, 100).map((token, idx) => (
                <span key={idx} className="px-2 py-1 bg-white text-green-700 text-xs rounded border border-green-200 font-medium">
                  {token}
                </span>
              )) : <span className="text-gray-400 text-sm italic">Tidak ada kata tersisa.</span>}
              
              {filteredTokens.length > 100 && (
                <span className="px-2 py-1 text-gray-500 text-xs italic">...dan lainnya</span>
              )}
            </div>
          </div>
        </div>
      </SectionCard>

      {/* Step 4: Stemming */}
      <SectionCard step="4" title="Stemming" description="Mengubah kata berimbuhan menjadi kata dasar.">
        <div className="overflow-hidden rounded-lg border border-gray-200">
          <div className="max-h-[500px] overflow-y-auto custom-scrollbar relative">
            <table className="w-full text-sm text-left">
              <thead className="bg-gray-50 text-gray-700 font-semibold sticky top-0 z-10 shadow-sm text-xs uppercase tracking-wider">
                <tr>
                  <th className="px-6 py-3 bg-gray-50">Kata Berimbuhan</th>
                  <th className="px-6 py-3 bg-gray-50 text-center w-12"></th>
                  <th className="px-6 py-3 bg-gray-50">Kata Dasar (Stem)</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-100 bg-white">
                {stemmingPairs.slice(0, stemmingLimit).map((item, idx) => (
                  <tr key={idx} className={`group transition-colors ${item.isChanged ? 'bg-blue-50/30 hover:bg-blue-50' : 'hover:bg-gray-50'}`}>
                    <td className={`px-6 py-2.5 font-medium ${item.isChanged ? 'text-gray-800' : 'text-gray-500'}`}>
                      {item.original}
                    </td>
                    <td className="px-6 py-2.5 text-center">
                      <ChevronRight className={`w-4 h-4 mx-auto ${item.isChanged ? 'text-blue-500' : 'text-gray-300'}`} />
                    </td>
                    <td className={`px-6 py-2.5 font-bold ${item.isChanged ? 'text-blue-700' : 'text-gray-400'}`}>
                      {item.stemmed}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
          {/* Load More Button jika data banyak */}
          {stemmingPairs.length > stemmingLimit && (
            <div className="p-3 bg-gray-50 border-t border-gray-200 text-center">
              <button 
                onClick={() => setStemmingLimit(prev => prev + 100)}
                className="text-xs font-medium text-blue-600 hover:text-blue-800 hover:underline"
              >
                Tampilkan {stemmingPairs.length - stemmingLimit} kata lagi...
              </button>
            </div>
          )}
        </div>
      </SectionCard>
    </div>
  );
}

// --- Sub-Components (Sama seperti sebelumnya) ---

function SectionCard({ step, title, description, children }) {
  return (
    <div className="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
      <div className="bg-gray-50 px-6 py-4 border-b border-gray-200 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 rounded-full bg-blue-600 text-white flex items-center justify-center font-bold shadow-sm text-sm">
            {step}
          </div>
          <div>
            <h3 className="text-lg font-bold text-gray-900 leading-tight">{title}</h3>
            <p className="text-xs text-gray-500 mt-0.5">{description}</p>
          </div>
        </div>
      </div>
      <div className="p-6">{children}</div>
    </div>
  );
}

function CodeBlock({ label, content, isPrimary = false }) {
  return (
    <div className="flex flex-col h-full">
      <label className={`block text-xs font-bold uppercase tracking-wider mb-2 ${isPrimary ? 'text-blue-700' : 'text-gray-600'}`}>
        {label}
      </label>
      <div className={`flex-1 p-4 rounded-lg border text-sm font-mono whitespace-pre-wrap max-h-48 overflow-y-auto custom-scrollbar
        ${isPrimary 
          ? 'bg-blue-50 border-blue-100 text-blue-900' 
          : 'bg-gray-50 border-gray-200 text-gray-600'
        }`}>
        {content.substring(0, 1000)}
        {content.length > 1000 && <span className="opacity-50">...</span>}
      </div>
    </div>
  );
}