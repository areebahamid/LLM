import axios, { AxiosResponse } from "axios";
import {
  ChatRequest,
  ChatResponse,
  ChatStreamResponse,
  ModelInfo,
  KnowledgeBaseInfo,
  SearchResult,
} from "../types/chat";

// Create axios instance with default configuration
const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || "http://localhost:8000",
  timeout: 30000,
  headers: {
    "Content-Type": "application/json",
  },
});

// Request interceptor for logging
api.interceptors.request.use(
  (config) => {
    console.log(`API Request: ${config.method?.toUpperCase()} ${config.url}`);
    return config;
  },
  (error) => {
    console.error("API Request Error:", error);
    return Promise.reject(error);
  }
);

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    console.error("API Response Error:", error.response?.data || error.message);
    return Promise.reject(error);
  }
);

// Chat API
export const chatAPI = {
  // Send a chat message and get response
  sendMessage: async (request: ChatRequest): Promise<ChatResponse> => {
    const response: AxiosResponse<ChatResponse> = await api.post(
      "/api/chat/",
      request
    );
    return response.data;
  },

  // Stream chat response
  streamMessage: async (
    request: ChatRequest
  ): Promise<ReadableStream<ChatStreamResponse>> => {
    const response = await fetch(`${api.defaults.baseURL}/api/chat/stream`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(request),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const reader = response.body?.getReader();
    if (!reader) {
      throw new Error("No response body reader available");
    }

    return new ReadableStream({
      start(controller) {
        const decoder = new TextDecoder();
        let buffer = "";

        function pump() {
          return reader.read().then(({ done, value }) => {
            if (done) {
              controller.close();
              return;
            }

            buffer += decoder.decode(value, { stream: true });
            const lines = buffer.split("\n");
            buffer = lines.pop() || "";

            for (const line of lines) {
              if (line.startsWith("data: ")) {
                try {
                  const data = JSON.parse(line.slice(6));
                  controller.enqueue(data);
                } catch (e) {
                  console.warn("Failed to parse stream data:", line);
                }
              }
            }

            return pump();
          });
        }

        return pump();
      },
    });
  },

  // Get available models
  getModels: async (): Promise<ModelInfo[]> => {
    const response: AxiosResponse<ModelInfo[]> = await api.get(
      "/api/chat/models"
    );
    return response.data;
  },

  // Search knowledge base
  searchKnowledgeBase: async (
    query: string,
    topK: number = 5
  ): Promise<SearchResult> => {
    const response: AxiosResponse<SearchResult> = await api.get(
      "/api/chat/search",
      {
        params: { query, top_k: topK },
      }
    );
    return response.data;
  },

  // Get knowledge base info
  getKnowledgeBaseInfo: async (): Promise<KnowledgeBaseInfo> => {
    const response: AxiosResponse<KnowledgeBaseInfo> = await api.get(
      "/api/chat/knowledge-base/info"
    );
    return response.data;
  },

  // Clear knowledge base
  clearKnowledgeBase: async (): Promise<{ message: string }> => {
    const response: AxiosResponse<{ message: string }> = await api.delete(
      "/api/chat/knowledge-base"
    );
    return response.data;
  },
};

// Health API
export const healthAPI = {
  // Basic health check
  checkHealth: async (): Promise<{
    status: string;
    timestamp: number;
    service: string;
  }> => {
    const response = await api.get("/api/health");
    return response.data;
  },

  // Detailed health check
  checkDetailedHealth: async (): Promise<any> => {
    const response = await api.get("/api/health/detailed");
    return response.data;
  },

  // Check Ollama status
  checkOllamaStatus: async (): Promise<any> => {
    const response = await api.get("/api/health/ollama");
    return response.data;
  },

  // Check RAG status
  checkRAGStatus: async (): Promise<any> => {
    const response = await api.get("/api/health/rag");
    return response.data;
  },
};

// Documents API
export const documentsAPI = {
  // Upload document
  uploadDocument: async (file: File, description?: string): Promise<any> => {
    const formData = new FormData();
    formData.append("file", file);
    if (description) {
      formData.append("description", description);
    }

    const response = await api.post("/api/documents/upload", formData, {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    });
    return response.data;
  },

  // Add text document
  addTextDocument: async (
    text: string,
    source: string = "manual_input",
    description?: string
  ): Promise<any> => {
    const formData = new FormData();
    formData.append("text", text);
    formData.append("source", source);
    if (description) {
      formData.append("description", description);
    }

    const response = await api.post("/api/documents/text", formData);
    return response.data;
  },

  // List documents
  listDocuments: async (): Promise<any> => {
    const response = await api.get("/api/documents/list");
    return response.data;
  },

  // Download document
  downloadDocument: async (filename: string): Promise<Blob> => {
    const response = await api.get(`/api/documents/download/${filename}`, {
      responseType: "blob",
    });
    return response.data;
  },

  // Delete document
  deleteDocument: async (
    filename: string
  ): Promise<{ message: string; filename: string }> => {
    const response = await api.delete(`/api/documents/${filename}`);
    return response.data;
  },
};

export default api;
