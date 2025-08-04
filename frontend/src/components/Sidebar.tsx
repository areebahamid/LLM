import React, { useState, useEffect } from "react";
import {
  X,
  Settings,
  FileText,
  Database,
  Info,
  Upload,
  Plus,
} from "lucide-react";
import { healthAPI, documentsAPI } from "../services/api";
import { KnowledgeBaseInfo } from "../types/chat";

interface SidebarProps {
  isOpen: boolean;
  onClose: () => void;
}

const Sidebar: React.FC<SidebarProps> = ({ isOpen, onClose }) => {
  const [kbInfo, setKbInfo] = useState<KnowledgeBaseInfo | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    if (isOpen) {
      loadKnowledgeBaseInfo();
    }
  }, [isOpen]);

  const loadKnowledgeBaseInfo = async () => {
    try {
      setIsLoading(true);
      const info = await healthAPI.checkRAGStatus();
      setKbInfo(info.knowledge_base);
    } catch (error) {
      console.error("Failed to load knowledge base info:", error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleFileUpload = async (
    event: React.ChangeEvent<HTMLInputElement>
  ) => {
    const file = event.target.files?.[0];
    if (!file) return;

    try {
      await documentsAPI.uploadDocument(file);
      loadKnowledgeBaseInfo(); // Refresh info
    } catch (error) {
      console.error("Failed to upload document:", error);
    }
  };

  return (
    <>
      {/* Overlay */}
      {isOpen && (
        <div
          className="fixed inset-0 bg-black bg-opacity-50 z-40 lg:hidden"
          onClick={onClose}
        />
      )}

      {/* Sidebar */}
      <div
        className={`
        fixed inset-y-0 left-0 z-50 w-80 bg-white border-r border-gray-200 transform transition-transform duration-300 ease-in-out lg:translate-x-0 lg:static lg:inset-0
        ${isOpen ? "translate-x-0" : "-translate-x-full"}
      `}>
        <div className="flex flex-col h-full">
          {/* Header */}
          <div className="flex items-center justify-between p-4 border-b border-gray-200">
            <h2 className="text-lg font-semibold text-gray-900">Settings</h2>
            <button
              onClick={onClose}
              className="p-2 rounded-md hover:bg-gray-100 lg:hidden">
              <X className="h-5 w-5" />
            </button>
          </div>

          {/* Content */}
          <div className="flex-1 overflow-y-auto p-4 space-y-6">
            {/* Knowledge Base Info */}
            <div className="card">
              <div className="card-header">
                <div className="flex items-center space-x-2">
                  <Database className="h-5 w-5 text-primary-600" />
                  <h3 className="card-title text-lg">Knowledge Base</h3>
                </div>
                <p className="card-description">
                  Information about your document collection
                </p>
              </div>
              <div className="card-content">
                {isLoading ? (
                  <div className="animate-pulse space-y-2">
                    <div className="h-4 bg-gray-200 rounded"></div>
                    <div className="h-4 bg-gray-200 rounded w-3/4"></div>
                  </div>
                ) : kbInfo ? (
                  <div className="space-y-2 text-sm">
                    <div className="flex justify-between">
                      <span className="text-gray-600">Documents:</span>
                      <span className="font-medium">
                        {kbInfo.total_documents}
                      </span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-600">Chunks:</span>
                      <span className="font-medium">{kbInfo.index_size}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-600">Model:</span>
                      <span className="font-medium text-xs">
                        {kbInfo.embedding_model.split("/").pop()}
                      </span>
                    </div>
                  </div>
                ) : (
                  <p className="text-gray-500 text-sm">
                    No information available
                  </p>
                )}
              </div>
            </div>

            {/* Upload Documents */}
            <div className="card">
              <div className="card-header">
                <div className="flex items-center space-x-2">
                  <Upload className="h-5 w-5 text-primary-600" />
                  <h3 className="card-title text-lg">Upload Documents</h3>
                </div>
                <p className="card-description">
                  Add documents to enhance responses
                </p>
              </div>
              <div className="card-content">
                <label className="btn btn-outline w-full cursor-pointer">
                  <input
                    type="file"
                    className="hidden"
                    accept=".txt,.md,.pdf,.docx"
                    onChange={handleFileUpload}
                  />
                  <Plus className="h-4 w-4 mr-2" />
                  Choose File
                </label>
                <p className="text-xs text-gray-500 mt-2">
                  Supported: TXT, MD, PDF, DOCX (max 10MB)
                </p>
              </div>
            </div>

            {/* Quick Actions */}
            <div className="card">
              <div className="card-header">
                <div className="flex items-center space-x-2">
                  <Settings className="h-5 w-5 text-primary-600" />
                  <h3 className="card-title text-lg">Quick Actions</h3>
                </div>
              </div>
              <div className="card-content space-y-2">
                <button className="btn btn-secondary w-full justify-start">
                  <FileText className="h-4 w-4 mr-2" />
                  View Documents
                </button>
                <button className="btn btn-secondary w-full justify-start">
                  <Database className="h-4 w-4 mr-2" />
                  Clear Knowledge Base
                </button>
              </div>
            </div>

            {/* About */}
            <div className="card">
              <div className="card-header">
                <div className="flex items-center space-x-2">
                  <Info className="h-5 w-5 text-primary-600" />
                  <h3 className="card-title text-lg">About</h3>
                </div>
              </div>
              <div className="card-content">
                <p className="text-sm text-gray-600 mb-3">
                  Student LLM Assistant powered by RAG, LangChain, and Ollama.
                </p>
                <div className="text-xs text-gray-500 space-y-1">
                  <div>Version: 1.0.0</div>
                  <div>Backend: FastAPI + LangChain</div>
                  <div>Frontend: React + TypeScript</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </>
  );
};

export default Sidebar;
