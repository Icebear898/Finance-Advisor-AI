import React from 'react';
import { Bot, User } from 'lucide-react';
import { format } from 'date-fns';

interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
  sources?: any[];
  suggestions?: string[];
}

interface ChatMessageProps {
  message: Message;
  onSuggestionClick: (suggestion: string) => void;
}

const ChatMessage: React.FC<ChatMessageProps> = ({ message, onSuggestionClick }) => {
  const isUser = message.role === 'user';

  return (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'}`}>
      <div className={`flex items-start space-x-3 max-w-3xl ${isUser ? 'flex-row-reverse space-x-reverse' : ''}`}>
        {/* Avatar */}
        <div className={`flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center ${
          isUser ? 'bg-primary-600' : 'bg-gray-200'
        }`}>
          {isUser ? (
            <User className="w-4 h-4 text-white" />
          ) : (
            <Bot className="w-4 h-4 text-gray-600" />
          )}
        </div>

        {/* Message Content */}
        <div className={`flex-1 ${isUser ? 'text-right' : ''}`}>
          <div className={`inline-block p-4 rounded-lg ${
            isUser 
              ? 'bg-primary-600 text-white' 
              : 'bg-gray-100 text-gray-900'
          }`}>
            {/* Message Text */}
            <div className="whitespace-pre-wrap">{message.content}</div>
            
            {/* Sources */}
            {message.sources && message.sources.length > 0 && (
              <div className="mt-3 pt-3 border-t border-gray-200">
                <p className="text-xs font-medium mb-2">Sources:</p>
                <div className="space-y-1">
                  {message.sources.map((source, index) => (
                    <div key={index} className="text-xs opacity-75">
                      {source.content}
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>

          {/* Timestamp */}
          <div className={`text-xs text-gray-500 mt-1 ${isUser ? 'text-right' : 'text-left'}`}>
            {format(message.timestamp, 'HH:mm')}
          </div>

          {/* Suggestions */}
          {message.suggestions && message.suggestions.length > 0 && !isUser && (
            <div className="mt-3">
              <p className="text-xs font-medium text-gray-700 mb-2">Suggested follow-ups:</p>
              <div className="flex flex-wrap gap-2">
                {message.suggestions.map((suggestion, index) => (
                  <button
                    key={index}
                    onClick={() => onSuggestionClick(suggestion)}
                    className="px-3 py-1 text-xs bg-white border border-gray-300 text-gray-700 rounded-full hover:bg-gray-50 hover:border-gray-400 transition-colors"
                  >
                    {suggestion}
                  </button>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default ChatMessage;
