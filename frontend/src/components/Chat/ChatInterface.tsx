import React, { useState, useRef, useEffect } from 'react';
import { Send, Bot, Paperclip, Mic } from 'lucide-react';
import toast from 'react-hot-toast';
import ChatMessage from './ChatMessage';
import ChatSuggestions from './ChatSuggestions';
import { sendChatMessage } from '../../services/api';

interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
  sources?: any[];
  suggestions?: string[];
}

const ChatInterface: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [selectedDocuments] = useState<string[]>([]);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSendMessage = async () => {
    if (!inputMessage.trim() || isLoading) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: inputMessage,
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputMessage('');
    setIsLoading(true);

    try {
      const response = await sendChatMessage({
        message: inputMessage,
        document_ids: selectedDocuments.length > 0 ? selectedDocuments : undefined
      });

      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: response.message,
        timestamp: new Date(),
        sources: response.sources,
        suggestions: response.suggestions
      };

      setMessages(prev => [...prev, assistantMessage]);
      toast.success('Response received!');
    } catch (error) {
      console.error('Error sending message:', error);
      toast.error('Failed to send message. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  const handleSuggestionClick = (suggestion: string) => {
    setInputMessage(suggestion);
  };

  const handleFileUpload = () => {
    // TODO: Implement file upload functionality
    toast('File upload feature coming soon!', {
      icon: '📁',
      duration: 3000,
    });
  };

  const handleVoiceInput = () => {
    // TODO: Implement voice input functionality
    toast('Voice input feature coming soon!', {
      icon: '🎤',
      duration: 3000,
    });
  };

  return (
    <div className="flex flex-col h-[calc(100vh-8rem)] bg-white rounded-lg shadow-sm border border-gray-200">
      {/* Header */}
      <div className="flex items-center justify-between p-4 border-b border-gray-200">
        <div className="flex items-center space-x-3">
          <div className="flex items-center justify-center w-10 h-10 bg-primary-100 rounded-full">
            <Bot className="w-5 h-5 text-primary-600" />
          </div>
          <div>
            <h2 className="text-lg font-semibold text-gray-900">AI Finance Advisor</h2>
            <p className="text-sm text-gray-500">Ask me anything about finance</p>
          </div>
        </div>
        <div className="flex items-center space-x-2">
          <span className={`w-2 h-2 rounded-full ${isLoading ? 'bg-yellow-400 animate-pulse' : 'bg-green-400'}`}></span>
          <span className="text-sm text-gray-500">
            {isLoading ? 'Thinking...' : 'Online'}
          </span>
        </div>
      </div>

      {/* Messages Area */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.length === 0 ? (
          <div className="text-center py-12">
            <div className="flex items-center justify-center w-16 h-16 bg-primary-100 rounded-full mx-auto mb-4">
              <Bot className="w-8 h-8 text-primary-600" />
            </div>
            <h3 className="text-lg font-medium text-gray-900 mb-2">Welcome to AI Finance Advisor</h3>
            <p className="text-gray-500 mb-6 max-w-md mx-auto">
              I'm here to help you with all your financial questions. Ask me about investments, 
              tax planning, budgeting, or any other financial topics.
            </p>
            <ChatSuggestions onSuggestionClick={handleSuggestionClick} />
          </div>
        ) : (
          messages.map((message) => (
            <ChatMessage
              key={message.id}
              message={message}
              onSuggestionClick={handleSuggestionClick}
            />
          ))
        )}
        
        {isLoading && (
          <div className="flex items-center space-x-3 p-4 bg-gray-50 rounded-lg">
            <div className="flex items-center justify-center w-8 h-8 bg-primary-100 rounded-full">
              <Bot className="w-4 h-4 text-primary-600" />
            </div>
            <div className="loading-dots">
              <span></span>
              <span></span>
              <span></span>
            </div>
          </div>
        )}
        
        <div ref={messagesEndRef} />
      </div>

      {/* Input Area */}
      <div className="p-4 border-t border-gray-200">
        <div className="flex items-end space-x-3">
          <div className="flex-1">
            <textarea
              value={inputMessage}
              onChange={(e) => setInputMessage(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Ask me about your finances..."
              className="w-full px-4 py-3 border border-gray-300 rounded-lg resize-none focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent"
              rows={1}
              disabled={isLoading}
            />
          </div>
          
          <div className="flex items-center space-x-2">
            <button
              onClick={handleFileUpload}
              className="p-2 text-gray-400 hover:text-gray-600 hover:bg-gray-100 rounded-lg transition-colors"
              disabled={isLoading}
            >
              <Paperclip className="w-5 h-5" />
            </button>
            
            <button
              onClick={handleVoiceInput}
              className="p-2 text-gray-400 hover:text-gray-600 hover:bg-gray-100 rounded-lg transition-colors"
              disabled={isLoading}
            >
              <Mic className="w-5 h-5" />
            </button>
            
            <button
              onClick={handleSendMessage}
              disabled={!inputMessage.trim() || isLoading}
              className="p-3 bg-primary-600 text-white rounded-lg hover:bg-primary-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            >
              <Send className="w-5 h-5" />
            </button>
          </div>
        </div>
        
        {/* Quick Actions */}
        {messages.length > 0 && (
          <div className="mt-3 flex flex-wrap gap-2">
            <button
              onClick={() => handleSuggestionClick("How can I save more money?")}
              className="px-3 py-1 text-xs bg-gray-100 text-gray-700 rounded-full hover:bg-gray-200 transition-colors"
            >
              💰 Save Money
            </button>
            <button
              onClick={() => handleSuggestionClick("What are good investment options?")}
              className="px-3 py-1 text-xs bg-gray-100 text-gray-700 rounded-full hover:bg-gray-200 transition-colors"
            >
              📈 Investments
            </button>
            <button
              onClick={() => handleSuggestionClick("Help me with tax planning")}
              className="px-3 py-1 text-xs bg-gray-100 text-gray-700 rounded-full hover:bg-gray-200 transition-colors"
            >
              📋 Tax Planning
            </button>
            <button
              onClick={() => handleSuggestionClick("Calculate my EMI")}
              className="px-3 py-1 text-xs bg-gray-100 text-gray-700 rounded-full hover:bg-gray-200 transition-colors"
            >
              🏦 EMI Calculator
            </button>
          </div>
        )}
      </div>
    </div>
  );
};

export default ChatInterface;
