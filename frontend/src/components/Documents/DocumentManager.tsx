import React, { useState, useRef } from 'react';
import { Upload, FileText, Trash2, Search, Eye } from 'lucide-react';
import toast from 'react-hot-toast';
import { uploadDocument, deleteDocument } from '../../services/api';

interface Document {
  document_id: string;
  filename: string;
  file_type: string;
  content_length: number;
  uploaded_at: string;
  description?: string;
}

const DocumentManager: React.FC = () => {
  const [documents, setDocuments] = useState<Document[]>([]);
  const [loading] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFileUpload = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const files = event.target.files;
    if (!files || files.length === 0) return;

    const file = files[0];
    
    // Validate file type
    const allowedTypes = ['pdf', 'docx', 'xlsx', 'xls', 'txt'];
    const fileExtension = file.name.split('.').pop()?.toLowerCase();
    
    if (!fileExtension || !allowedTypes.includes(fileExtension)) {
      toast.error('Invalid file type. Please upload PDF, DOCX, XLSX, XLS, or TXT files.');
      return;
    }

    // Validate file size (10MB limit)
    if (file.size > 10 * 1024 * 1024) {
      toast.error('File size too large. Please upload files smaller than 10MB.');
      return;
    }

    try {
      setUploading(true);
      const response = await uploadDocument(file);
      
      setDocuments(prev => [response.document, ...prev]);
      toast.success('Document uploaded successfully!');
      
      // Reset file input
      if (fileInputRef.current) {
        fileInputRef.current.value = '';
      }
    } catch (error) {
      console.error('Error uploading document:', error);
      toast.error('Failed to upload document. Please try again.');
    } finally {
      setUploading(false);
    }
  };

  const handleDeleteDocument = async (documentId: string) => {
    if (!window.confirm('Are you sure you want to delete this document?')) {
      return;
    }

    try {
      await deleteDocument(documentId);
      setDocuments(prev => prev.filter(doc => doc.document_id !== documentId));
      toast.success('Document deleted successfully!');
    } catch (error) {
      console.error('Error deleting document:', error);
      toast.error('Failed to delete document. Please try again.');
    }
  };

  const filteredDocuments = documents.filter(doc =>
    doc.filename.toLowerCase().includes(searchQuery.toLowerCase()) ||
    doc.description?.toLowerCase().includes(searchQuery.toLowerCase())
  );

  const formatFileSize = (bytes: number) => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const getFileIcon = (fileType: string) => {
    switch (fileType.toLowerCase()) {
      case 'pdf':
        return '📄';
      case 'docx':
        return '📝';
      case 'xlsx':
      case 'xls':
        return '📊';
      case 'txt':
        return '📄';
      default:
        return '📄';
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Document Manager</h1>
          <p className="text-gray-600">Upload and manage your financial documents</p>
        </div>
        <button
          onClick={() => fileInputRef.current?.click()}
          disabled={uploading}
          className="btn-primary flex items-center space-x-2"
        >
          <Upload className="w-4 h-4" />
          <span>{uploading ? 'Uploading...' : 'Upload Document'}</span>
        </button>
      </div>

      {/* Hidden file input */}
      <input
        ref={fileInputRef}
        type="file"
        onChange={handleFileUpload}
        accept=".pdf,.docx,.xlsx,.xls,.txt"
        className="hidden"
      />

      {/* Search */}
      <div className="relative">
        <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
        <input
          type="text"
          placeholder="Search documents..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent"
        />
      </div>

      {/* Documents Grid */}
      {filteredDocuments.length === 0 ? (
        <div className="text-center py-12">
          <div className="flex items-center justify-center w-16 h-16 bg-gray-100 rounded-full mx-auto mb-4">
            <FileText className="w-8 h-8 text-gray-400" />
          </div>
          <h3 className="text-lg font-medium text-gray-900 mb-2">No documents found</h3>
          <p className="text-gray-500 mb-6">
            {searchQuery ? 'No documents match your search.' : 'Upload your first document to get started.'}
          </p>
          {!searchQuery && (
            <button
              onClick={() => fileInputRef.current?.click()}
              className="btn-primary"
            >
              Upload Document
            </button>
          )}
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredDocuments.map((doc) => (
            <div key={doc.document_id} className="card hover:shadow-md transition-shadow">
              <div className="flex items-start justify-between mb-3">
                <div className="flex items-center space-x-3">
                  <span className="text-2xl">{getFileIcon(doc.file_type)}</span>
                  <div>
                    <h4 className="font-medium text-gray-900 truncate max-w-32">
                      {doc.filename}
                    </h4>
                    <p className="text-sm text-gray-500">{doc.file_type.toUpperCase()}</p>
                  </div>
                </div>
                <div className="flex items-center space-x-1">
                  <button
                    onClick={() => {/* TODO: View document */}}
                    className="p-1 text-gray-400 hover:text-gray-600 hover:bg-gray-100 rounded transition-colors"
                    title="View document"
                  >
                    <Eye className="w-4 h-4" />
                  </button>
                  <button
                    onClick={() => handleDeleteDocument(doc.document_id)}
                    className="p-1 text-gray-400 hover:text-red-600 hover:bg-red-50 rounded transition-colors"
                    title="Delete document"
                  >
                    <Trash2 className="w-4 h-4" />
                  </button>
                </div>
              </div>
              
              {doc.description && (
                <p className="text-sm text-gray-600 mb-3 line-clamp-2">
                  {doc.description}
                </p>
              )}
              
              <div className="flex items-center justify-between text-xs text-gray-500">
                <span>{formatFileSize(doc.content_length)}</span>
                <span>{formatDate(doc.uploaded_at)}</span>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Upload Instructions */}
      <div className="card bg-blue-50 border-blue-200">
        <h3 className="text-lg font-semibold text-blue-900 mb-3">Supported File Types</h3>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
          <div className="flex items-center space-x-2">
            <span>📄</span>
            <span className="text-blue-800">PDF Documents</span>
          </div>
          <div className="flex items-center space-x-2">
            <span>📝</span>
            <span className="text-blue-800">Word Documents</span>
          </div>
          <div className="flex items-center space-x-2">
            <span>📊</span>
            <span className="text-blue-800">Excel Spreadsheets</span>
          </div>
          <div className="flex items-center space-x-2">
            <span>📄</span>
            <span className="text-blue-800">Text Files</span>
          </div>
        </div>
        <p className="text-sm text-blue-700 mt-3">
          Maximum file size: 10MB. Documents will be analyzed for financial insights.
        </p>
      </div>
    </div>
  );
};

export default DocumentManager;
