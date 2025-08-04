import React, { useState, useRef, useEffect } from "react";
import { Send, Bot, User, Loader2, BookOpen } from "lucide-react";
import { ChatMessage, Source } from "../types/chat";
import { chatAPI } from "../services/api";
import MessageBubble from "./MessageBubble";
import SourcesPanel from "./SourcesPanel";

const ChatInterface: React.FC = () => {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [inputMessage, setInputMessage] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [currentSources, setCurrentSources] = useState<Source[]>([]);
  const [showSources, setShowSources] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLTextAreaElement>(null);

  // Auto-scroll to bottom when new messages are added
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  // Focus input on mount
  useEffect(() => {
    inputRef.current?.focus();
  }, []);

  const handleSendMessage = async () => {
    if (!inputMessage.trim() || isLoading) return;

    const userMessage: ChatMessage = {
      role: "user",
      content: inputMessage.trim(),
      timestamp: new Date().toISOString(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setInputMessage("");
    setIsLoading(true);
    setCurrentSources([]);
    setShowSources(false);

    try {
      // Send message and get response
      const response = await chatAPI.sendMessage({
        message: userMessage.content,
        conversation_history: messages,
        use_rag: true,
      });

      const assistantMessage: ChatMessage = {
        role: "assistant",
        content: response.response,
        timestamp: new Date().toISOString(),
      };

      setMessages((prev) => [...prev, assistantMessage]);

      if (response.sources && response.sources.length > 0) {
        setCurrentSources(response.sources);
        setShowSources(true);
      }
    } catch (error) {
      console.error("Error sending message:", error);

      const errorMessage: ChatMessage = {
        role: "assistant",
        content:
          "Sorry, I encountered an error while processing your message. Please try again.",
        timestamp: new Date().toISOString(),
      };

      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  const clearChat = () => {
    setMessages([]);
    setCurrentSources([]);
    setShowSources(false);
  };

  return (
    <div className="flex flex-col h-screen">
      {/* Chat Header */}
      <div className="bg-white border-b border-gray-200 px-4 py-3">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <Bot className="h-5 w-5 text-primary-600" />
            <h2 className="text-lg font-semibold text-gray-900">Chat</h2>
          </div>
          <div className="flex items-center space-x-2">
            {currentSources.length > 0 && (
              <button
                onClick={() => setShowSources(!showSources)}
                className="btn btn-sm btn-outline">
                <BookOpen className="h-4 w-4 mr-1" />
                Sources ({currentSources.length})
              </button>
            )}
            <button onClick={clearChat} className="btn btn-sm btn-secondary">
              Clear Chat
            </button>
          </div>
        </div>
      </div>

      {/* Messages Area */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.length === 0 ? (
          <div className="flex flex-col items-center justify-center h-full text-center">
            <Bot className="h-16 w-16 text-gray-300 mb-4" />
            <h3 className="text-xl font-semibold text-gray-900 mb-2">
              Welcome to Student LLM Assistant
            </h3>
            <p className="text-gray-600 max-w-md">
              I'm here to help you with your studies! Ask me anything about
              programming, machine learning, or any other academic topic. I can
              also help you understand documents you upload.
            </p>
            <div className="mt-6 space-y-2">
              <p className="text-sm text-gray-500">Try asking:</p>
              <div className="space-y-1">
                <button
                  onClick={() => setInputMessage("What is machine learning?")}
                  className="block text-sm text-primary-600 hover:text-primary-700">
                  "What is machine learning?"
                </button>
                <button
                  onClick={() => setInputMessage("Explain Python functions")}
                  className="block text-sm text-primary-600 hover:text-primary-700">
                  "Explain Python functions"
                </button>
                <button
                  onClick={() => setInputMessage("How does React work?")}
                  className="block text-sm text-primary-600 hover:text-primary-700">
                  "How does React work?"
                </button>
              </div>
            </div>
          </div>
        ) : (
          messages.map((message, index) => (
            <MessageBubble key={index} message={message} />
          ))
        )}

        {isLoading && (
          <div className="flex items-start space-x-3">
            <div className="flex-shrink-0">
              <div className="w-8 h-8 bg-primary-100 rounded-full flex items-center justify-center">
                <Bot className="h-4 w-4 text-primary-600" />
              </div>
            </div>
            <div className="flex-1 bg-white rounded-lg border border-gray-200 p-4">
              <div className="flex items-center space-x-2">
                <Loader2 className="h-4 w-4 animate-spin text-gray-500" />
                <span className="text-gray-500">Thinking...</span>
              </div>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Sources Panel */}
      {showSources && currentSources.length > 0 && (
        <SourcesPanel
          sources={currentSources}
          onClose={() => setShowSources(false)}
        />
      )}

      {/* Input Area */}
      <div className="bg-white border-t border-gray-200 p-4">
        <div className="flex space-x-3">
          <div className="flex-1">
            <textarea
              ref={inputRef}
              value={inputMessage}
              onChange={(e) => setInputMessage(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Type your message here..."
              className="textarea resize-none"
              rows={1}
              disabled={isLoading}
            />
          </div>
          <button
            onClick={handleSendMessage}
            disabled={!inputMessage.trim() || isLoading}
            className="btn btn-primary btn-md self-end">
            <Send className="h-4 w-4" />
          </button>
        </div>
        <div className="mt-2 text-xs text-gray-500">
          Press Enter to send, Shift+Enter for new line
        </div>
      </div>
    </div>
  );
};

export default ChatInterface;
