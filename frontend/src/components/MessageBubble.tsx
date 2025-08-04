import React from "react";
import { Bot, User } from "lucide-react";
import ReactMarkdown from "react-markdown";
import { Prism as SyntaxHighlighter } from "react-syntax-highlighter";
import { tomorrow } from "react-syntax-highlighter/dist/esm/styles/prism";
import { ChatMessage } from "../types/chat";

interface MessageBubbleProps {
  message: ChatMessage;
}

const MessageBubble: React.FC<MessageBubbleProps> = ({ message }) => {
  const isUser = message.role === "user";
  const timestamp = message.timestamp
    ? new Date(message.timestamp).toLocaleTimeString([], {
        hour: "2-digit",
        minute: "2-digit",
      })
    : "";

  return (
    <div
      className={`flex items-start space-x-3 ${
        isUser ? "justify-end" : "justify-start"
      }`}>
      {!isUser && (
        <div className="flex-shrink-0">
          <div className="w-8 h-8 bg-primary-100 rounded-full flex items-center justify-center">
            <Bot className="h-4 w-4 text-primary-600" />
          </div>
        </div>
      )}

      <div className={`flex-1 max-w-3xl ${isUser ? "order-first" : ""}`}>
        <div
          className={`rounded-lg p-4 ${
            isUser
              ? "bg-primary-600 text-white"
              : "bg-white border border-gray-200"
          }`}>
          <div className={`markdown ${isUser ? "text-white" : ""}`}>
            <ReactMarkdown
              components={{
                code({ node, inline, className, children, ...props }) {
                  const match = /language-(\w+)/.exec(className || "");
                  return !inline && match ? (
                    <SyntaxHighlighter
                      style={tomorrow}
                      language={match[1]}
                      PreTag="div"
                      {...props}>
                      {String(children).replace(/\n$/, "")}
                    </SyntaxHighlighter>
                  ) : (
                    <code
                      className={`${className} ${
                        isUser ? "bg-primary-700 text-white" : "bg-gray-100"
                      } px-1 py-0.5 rounded text-sm font-mono`}
                      {...props}>
                      {children}
                    </code>
                  );
                },
                // Override link colors for user messages
                a: ({ children, ...props }) => (
                  <a
                    {...props}
                    className={
                      isUser
                        ? "text-blue-200 hover:text-blue-100 underline"
                        : ""
                    }>
                    {children}
                  </a>
                ),

                // Override pre colors for user messages
                pre: ({ children, ...props }) => (
                  <pre
                    {...props}
                    className={`${
                      isUser ? "bg-primary-700" : "bg-gray-100"
                    } p-4 rounded-lg overflow-x-auto mb-3`}>
                    {children}
                  </pre>
                ),
              }}>
              {message.content}
            </ReactMarkdown>
          </div>
        </div>

        {timestamp && (
          <div
            className={`text-xs text-gray-500 mt-1 ${
              isUser ? "text-right" : "text-left"
            }`}>
            {timestamp}
          </div>
        )}
      </div>

      {isUser && (
        <div className="flex-shrink-0">
          <div className="w-8 h-8 bg-gray-200 rounded-full flex items-center justify-center">
            <User className="h-4 w-4 text-gray-600" />
          </div>
        </div>
      )}
    </div>
  );
};

export default MessageBubble;
