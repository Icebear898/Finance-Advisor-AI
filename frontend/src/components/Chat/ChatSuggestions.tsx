import React from 'react';

interface ChatSuggestionsProps {
  onSuggestionClick: (suggestion: string) => void;
}

const ChatSuggestions: React.FC<ChatSuggestionsProps> = ({ onSuggestionClick }) => {
  const suggestions = [
    {
      icon: "💰",
      title: "Personal Finance",
      questions: [
        "How can I save more money?",
        "What's a good budget for my income?",
        "How much should I save for emergency fund?"
      ]
    },
    {
      icon: "📈",
      title: "Investments",
      questions: [
        "What are good investment options for beginners?",
        "Should I invest in stocks or mutual funds?",
        "How to start SIP investment?"
      ]
    },
    {
      icon: "📋",
      title: "Tax Planning",
      questions: [
        "What are the best tax-saving investments?",
        "How to maximize Section 80C deductions?",
        "What documents do I need for tax filing?"
      ]
    },
    {
      icon: "🏦",
      title: "Loans & EMI",
      questions: [
        "How to calculate EMI for different amounts?",
        "What is the best home loan interest rate?",
        "How to improve my credit score?"
      ]
    }
  ];

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-4 max-w-4xl mx-auto">
      {suggestions.map((category, categoryIndex) => (
        <div key={categoryIndex} className="card">
          <div className="flex items-center mb-3">
            <span className="text-2xl mr-2">{category.icon}</span>
            <h4 className="font-medium text-gray-900">{category.title}</h4>
          </div>
          <div className="space-y-2">
            {category.questions.map((question, questionIndex) => (
              <button
                key={questionIndex}
                onClick={() => onSuggestionClick(question)}
                className="w-full text-left p-2 text-sm text-gray-600 hover:bg-gray-50 hover:text-gray-900 rounded transition-colors"
              >
                {question}
              </button>
            ))}
          </div>
        </div>
      ))}
    </div>
  );
};

export default ChatSuggestions;
