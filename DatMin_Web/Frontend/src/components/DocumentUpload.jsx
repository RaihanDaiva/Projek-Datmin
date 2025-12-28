import { useState } from 'react';
import { Upload, FileText, File, CheckCircle, AlertCircle } from 'lucide-react';

export function DocumentUpload({ 
  uploadedFiles, 
  setUploadedFiles, 
  setProcessedText,
  onComplete 
}) {
  const [isDragging, setIsDragging] = useState(false);

  const handleDragOver = (e) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = () => {
    setIsDragging(false);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setIsDragging(false);
    
    const files = Array.from(e.dataTransfer.files);
    processFiles(files);
  };

  const handleFileInput = (e) => {
    if (e.target.files) {
      const files = Array.from(e.target.files);
      processFiles(files);
    }
  };

  const processFiles = (files) => {
    const validExtensions = ['.txt', '.docx', '.pdf'];
    
    files.forEach((file) => {
      const ext = '.' + file.name.split('.').pop()?.toLowerCase();
      const isValid = validExtensions.includes(ext);
      
      const reader = new FileReader();
      reader.onload = (e) => {
        const content = e.target?.result;
        
        const newFile = {
          id: Math.random().toString(36).substr(2, 9),
          name: file.name,
          type: ext,
          status: isValid ? 'Ready' : 'Invalid Format',
          content: content || 'Sample Indonesian text content for processing...'
        };
        
        setUploadedFiles([...uploadedFiles, newFile]);
      };
      
      reader.readAsText(file);
    });
  };

  const handleProcess = () => {
    if (uploadedFiles.length > 0) {
      const allContent = uploadedFiles
        .filter(f => f.status === 'Ready')
        .map(f => f.content)
        .join(' ');
      
      setProcessedText(allContent);
      
      // Update status to processed
      setUploadedFiles(
        uploadedFiles.map(f => ({
          ...f,
          status: f.status === 'Ready' ? 'Processed' : f.status
        }))
      );
      
      onComplete();
    }
  };

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

  const getStatusIcon = (status) => {
    switch (status) {
      case 'Ready':
      case 'Processed':
        return <CheckCircle className="w-4 h-4 text-green-500" />;
      case 'Invalid Format':
        return <AlertCircle className="w-4 h-4 text-red-500" />;
      default:
        return null;
    }
  };

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-gray-900 mb-2">Upload Documents</h2>
        <p className="text-gray-600">
          Upload your own documents to process and analyze. These will be separate from the server dataset.
        </p>
      </div>

      {/* Upload Area */}
      <div>
        <div
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          onDrop={handleDrop}
          className={`border-2 border-dashed rounded-lg p-12 text-center transition-colors ${
            isDragging
              ? 'border-blue-400 bg-blue-50'
              : 'border-gray-300 bg-gray-50'
          }`}
        >
          <Upload className="w-12 h-12 text-gray-400 mx-auto mb-4" />
          <p className="text-gray-700 mb-2">
            Drag and drop files here, or click to browse
          </p>
          <p className="text-gray-500 mb-4">
            Supported formats: .txt, .docx, .pdf
          </p>
          <label className="inline-block">
            <input
              type="file"
              multiple
              accept=".txt,.docx,.pdf"
              onChange={handleFileInput}
              className="hidden"
            />
            <span className="px-6 py-2 bg-blue-500 text-white rounded-lg cursor-pointer hover:bg-blue-600 transition-colors inline-block">
              Browse Files
            </span>
          </label>
        </div>
      </div>

      {/* Uploaded Files Table */}
      {uploadedFiles.length > 0 && (
        <div>
          <h3 className="text-gray-900 mb-4">Uploaded Files</h3>
          <div className="border border-gray-200 rounded-lg overflow-hidden">
            <table className="w-full">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-gray-700">File Name</th>
                  <th className="px-6 py-3 text-left text-gray-700">File Type</th>
                  <th className="px-6 py-3 text-left text-gray-700">Status</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-200">
                {uploadedFiles.map((file) => (
                  <tr key={file.id} className="bg-white hover:bg-gray-50">
                    <td className="px-6 py-4">
                      <div className="flex items-center gap-3">
                        {getFileIcon(file.type)}
                        <span className="text-gray-900">{file.name}</span>
                      </div>
                    </td>
                    <td className="px-6 py-4 text-gray-600">{file.type}</td>
                    <td className="px-6 py-4">
                      <div className="flex items-center gap-2">
                        {getStatusIcon(file.status)}
                        <span className="text-gray-700">{file.status}</span>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* Process Button */}
      {uploadedFiles.length > 0 && (
        <div className="flex justify-end">
          <button
            onClick={handleProcess}
            className="px-8 py-3 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors"
          >
            Process Documents
          </button>
        </div>
      )}
    </div>
  );
}
