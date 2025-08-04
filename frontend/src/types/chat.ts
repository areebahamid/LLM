export interface ChatMessage {
  role: "user" | "assistant";
  content: string;
  timestamp?: string;
}

export interface ChatRequest {
  message: string;
  conversation_history?: ChatMessage[];
  use_rag?: boolean;
  model_params?: Record<string, any>;
}

export interface ChatResponse {
  response: string;
  sources?: Source[];
  model_used: string;
  processing_time: number;
  tokens_used?: number;
  conversation_id?: string;
}

export interface ChatStreamResponse {
  chunk: string;
  done: boolean;
  sources?: Source[];
  model_used?: string;
  error?: string;
}

export interface Source {
  content: string;
  source: string;
  score: number;
}

export interface ModelInfo {
  name: string;
  provider: string;
  context_length?: number;
  parameters?: number;
  is_available: boolean;
}

export interface Conversation {
  id: string;
  title: string;
  messages: ChatMessage[];
  created_at: string;
  updated_at: string;
  metadata?: Record<string, any>;
}

export interface KnowledgeBaseInfo {
  total_documents: number;
  index_size: number;
  embedding_model: string;
  chunk_size: number;
  chunk_overlap: number;
  index_path: string;
}

export interface SearchResult {
  query: string;
  results: Source[];
  total_results: number;
}
