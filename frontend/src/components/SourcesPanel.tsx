import React from "react";
import { X, FileText, ExternalLink } from "lucide-react";
import { Source } from "../types/chat";

interface SourcesPanelProps {
  sources: Source[];
  onClose: () => void;
}

const SourcesPanel: React.FC<SourcesPanelProps> = ({ sources, onClose }) => {
  const formatScore = (score: number) => {
    return (score * 100).toFixed(1);
  };

  return (
    <div className="bg-white border-t border-gray-200 p-4">
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center space-x-2">
          <FileText className="h-5 w-5 text-primary-600" />
          <h3 className="text-lg font-semibold text-gray-900">
            Sources ({sources.length})
          </h3>
        </div>
        <button onClick={onClose} className="p-2 rounded-md hover:bg-gray-100">
          <X className="h-5 w-5" />
        </button>
      </div>

      <div className="space-y-3 max-h-64 overflow-y-auto">
        {sources.map((source, index) => (
          <div key={index} className="border border-gray-200 rounded-lg p-3">
            <div className="flex items-start justify-between mb-2">
              <div className="flex items-center space-x-2">
                <FileText className="h-4 w-4 text-gray-500" />
                <span className="text-sm font-medium text-gray-900">
                  {source.source}
                </span>
              </div>
              <span className="text-xs text-gray-500 bg-gray-100 px-2 py-1 rounded">
                {formatScore(source.score)}% match
              </span>
            </div>

            <div className="text-sm text-gray-700 leading-relaxed">
              {source.content}
            </div>

            <div className="mt-2 flex items-center justify-between">
              <span className="text-xs text-gray-500">
                Source: {source.source}
              </span>
              <button className="text-xs text-primary-600 hover:text-primary-700 flex items-center space-x-1">
                <ExternalLink className="h-3 w-3" />
                <span>View</span>
              </button>
            </div>
          </div>
        ))}
      </div>

      <div className="mt-4 pt-3 border-t border-gray-200">
        <p className="text-xs text-gray-500">
          These sources were used to generate the response above. Higher match
          percentages indicate more relevant content.
        </p>
      </div>
    </div>
  );
};

export default SourcesPanel;
