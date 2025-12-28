import { useState } from 'react';
import { DatasetBrowser } from './components/DatasetBrowser';
import { DocumentUpload } from './components/DocumentUpload';
import { TextPreprocessing } from './components/TextPreprocessing';
import { SimilaritySearch } from './components/SimilaritySearch';
import { Database, Upload, Layers, Search } from 'lucide-react';
import { SERVER_DOCUMENTS } from './data/mockDocuments';

export default function App() {
  const [activeTab, setActiveTab] = useState('dataset');
  const [uploadedFiles, setUploadedFiles] = useState([]);
  const [processedText, setProcessedText] = useState('');

  const tabs = [
    { id: 'dataset', label: 'Server Document Dataset', icon: Database },
    { id: 'upload', label: 'Upload Documents', icon: Upload },
    { id: 'preprocessing', label: 'Text Preprocessing', icon: Layers },
    { id: 'search', label: 'Document Similarity Search', icon: Search },
  ];

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-6 py-6">
          <h1 className="text-gray-900">Indonesian Document Retrieval System</h1>
          <p className="text-gray-600 mt-1">Document Upload, Preprocessing & Similarity Search</p>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-6 py-6">
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden">
          {/* Tab Navigation */}
          <div className="border-b border-gray-200">
            <nav className="flex">
              {tabs.map((tab) => {
                const Icon = tab.icon;
                return (
                  <button
                    key={tab.id}
                    onClick={() => setActiveTab(tab.id)}
                    className={`flex items-center gap-2 px-6 py-4 border-b-2 transition-colors ${
                      activeTab === tab.id
                        ? 'border-blue-500 text-blue-600'
                        : 'border-transparent text-gray-600 hover:text-gray-900 hover:border-gray-300'
                    }`}
                  >
                    <Icon className="w-5 h-5" />
                    {tab.label}
                  </button>
                );
              })}
            </nav>
          </div>

          {/* Tab Content */}
          <div className="p-8">
            {activeTab === 'dataset' && (
              <DatasetBrowser />
            )}
            {activeTab === 'upload' && (
              <DocumentUpload
                uploadedFiles={uploadedFiles}
                setUploadedFiles={setUploadedFiles}
                setProcessedText={setProcessedText}
                onComplete={() => setActiveTab('preprocessing')}
              />
            )}
            {activeTab === 'preprocessing' && (
              <TextPreprocessing
                processedText={processedText}
                uploadedFiles={uploadedFiles}
              />
            )}
            {activeTab === 'search' && (
              <SimilaritySearch
                documents={SERVER_DOCUMENTS}
                uploadedFiles={uploadedFiles}
              />
            )}
          </div>
        </div>
      </div>
    </div>
  );
}