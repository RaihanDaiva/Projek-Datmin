import { FileText, File, Database } from 'lucide-react';
import { useEffect, useState } from 'react';

export function DatasetBrowser() {
  const [documents, setDocuments] = useState([]);

  useEffect(() => {
    fetch('http://localhost:5000/documents')
      .then(res => res.json())
      .then(data => setDocuments(data));
  }, []);

  const getFileIcon = (type) => {
    switch (type) {
      case '.pdf':
        return <File className="w-5 h-5 text-red-500" />;
      case '.docx':
        return <FileText className="w-5 h-5 text-blue-500" />;
      case '.txt':
        return <FileText className="w-5 h-5 text-gray-500" />;
      default:
        return <File className="w-5 h-5 text-gray-400" />;
    }
  };

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-gray-900 mb-2">Server Document Dataset</h2>
        <p className="text-gray-600">
          Displaying all documents stored in the server dataset directory. These documents are used as the search corpus for similarity analysis.
        </p>
      </div>

      {/* Info Card */}
      <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 flex items-start gap-3">
        <Database className="w-5 h-5 text-blue-600 mt-0.5 flex-shrink-0" />
        <div>
          <h4 className="text-blue-900 mb-1">Pre-stored Document Corpus</h4>
          <p className="text-blue-700">
            Documents are pre-stored on the server and used as the search corpus. 
            Use the "Document Similarity Search" tab to find similar documents from this dataset.
          </p>
        </div>
      </div>

      {/* Documents Table Section */}
      <div>
        <h3 className="text-gray-900 mb-4">Available Documents ({documents.length})</h3>
        
        {/* PERUBAHAN UTAMA DI SINI */}
        <div className="border border-gray-200 rounded-lg overflow-hidden flex flex-col">
          {/* Container Scrollable */}
          <div className="overflow-y-auto max-h-96 relative">
            <table className="w-full text-left border-collapse">
              {/* Header dibuat Sticky */}
              <thead className="bg-gray-50 sticky top-0 z-10 shadow-sm">
                <tr>
                  <th className="px-6 py-3 text-left text-gray-700 font-semibold bg-gray-50">Document Name</th>
                  <th className="px-6 py-3 text-left text-gray-700 font-semibold bg-gray-50">File Type</th>
                  <th className="px-6 py-3 text-left text-gray-700 font-semibold bg-gray-50">Status</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-200 bg-white">
                {documents.map((doc) => (
                  <tr key={doc.id} className="hover:bg-gray-50 transition-colors">
                    <td className="px-6 py-4">
                      <div className="flex items-center gap-3">
                        {getFileIcon(doc.type)}
                        <span className="text-gray-900 font-medium">{doc.name}</span>
                      </div>
                    </td>
                    <td className="px-6 py-4 text-gray-600">{doc.type}</td>
                    <td className="px-6 py-4">
                      <span className="px-3 py-1 bg-green-100 text-green-700 text-sm font-medium rounded-full">
                        {doc.status}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>

      {/* Statistics */}
      <div className="grid grid-cols-3 gap-4">
        <div className="bg-gray-50 rounded-lg p-4 border border-gray-200">
          <p className="text-gray-600 mb-1">Total Documents</p>
          <p className="text-gray-900 font-bold">{documents.length}</p>
        </div>
        <div className="bg-gray-50 rounded-lg p-4 border border-gray-200">
          <p className="text-gray-600 mb-1">File Types</p>
          <p className="text-gray-900 font-bold">{new Set(documents.map(d => d.type)).size}</p>
        </div>
        <div className="bg-gray-50 rounded-lg p-4 border border-gray-200">
          <p className="text-gray-600 mb-1">Status</p>
          <p className="text-gray-900 font-bold">All Available</p>
        </div>
      </div>
    </div>
  );
}