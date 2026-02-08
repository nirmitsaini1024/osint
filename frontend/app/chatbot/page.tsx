"use client";

import { useState, useRef, useEffect } from "react";
import Link from "next/link";

interface Message {
  id: string;
  text: string;
  sender: "user" | "bot";
  timestamp: string;
  queryType?: string;
  data?: any;
  showFullList?: boolean;
}

export default function ChatbotPage() {
  const [lastUsername, setLastUsername] = useState<string | null>(null);
  
  const toggleShowFullList = (messageId: string) => {
    setMessages((prev) =>
      prev.map((msg) =>
        msg.id === messageId ? { ...msg, showFullList: !msg.showFullList } : msg
      )
    );
  };
  
  const [messages, setMessages] = useState<Message[]>([
    {
      id: "welcome",
      text: `👋 **Welcome to the Sherlock Intelligence Chatbot!**

I can help you with AI-powered social media investigations:

🔍 **Investigation Queries:**
• "Find all accounts of john_doe"
• "Search for username alice_2024"

🧠 **Intelligence Queries:**
• "Is john_doe suspicious?"
• "Which platform has highest risk for alice_2024?"

📊 **Analysis Queries:**
• "Show risk score for john_doe"
• "Analyze profile alice_2024"

📝 **Reporting Queries:**
• "Generate investigation report for john_doe"
• "Create summary for alice_2024"

💡 All intelligence, analysis, and reporting features use AI powered by Groq!

**Try asking:** "Find all accounts of john_doe"`,
      sender: "bot",
      timestamp: new Date().toISOString(),
    },
  ]);
  const [inputValue, setInputValue] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSendMessage = async () => {
    if (!inputValue.trim() || isLoading) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      text: inputValue,
      sender: "user",
      timestamp: new Date().toISOString(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setInputValue("");
    setIsLoading(true);

    try {
      const response = await fetch("http://localhost:8000/chatbot", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          query: inputValue,
          timestamp: new Date().toISOString(),
          last_username: lastUsername,
        }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || "Failed to get response from chatbot");
      }

      const data = await response.json();

      const botMessage: Message = {
        id: (Date.now() + 1).toString(),
        text: data.response,
        sender: "bot",
        timestamp: data.timestamp,
        queryType: data.query_type,
        data: data.data,
      };

      setMessages((prev) => [...prev, botMessage]);
      
      // Update last username for conversation context
      if (data.last_username) {
        setLastUsername(data.last_username);
      } else if (data.data?.username) {
        setLastUsername(data.data.username);
      }
    } catch (error) {
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        text: `❌ **Error:** ${error instanceof Error ? error.message : "An error occurred"}\n\nPlease make sure:\n1. The backend is running on port 8000\n2. GROQ_API_KEY is set in your environment`,
        sender: "bot",
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

  const getQueryTypeColor = (queryType?: string) => {
    switch (queryType) {
      case "investigation":
        return "bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-300";
      case "intelligence":
        return "bg-purple-100 text-purple-800 dark:bg-purple-900/30 dark:text-purple-300";
      case "analysis":
        return "bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-300";
      case "reporting":
        return "bg-orange-100 text-orange-800 dark:bg-orange-900/30 dark:text-orange-300";
      default:
        return "bg-gray-100 text-gray-800 dark:bg-gray-900/30 dark:text-gray-300";
    }
  };

  const getQueryTypeEmoji = (queryType?: string) => {
    switch (queryType) {
      case "investigation":
        return "🔍";
      case "intelligence":
        return "🧠";
      case "analysis":
        return "📊";
      case "reporting":
        return "📝";
      default:
        return "💬";
    }
  };

  const getQueryTypeLabel = (queryType?: string) => {
    switch (queryType) {
      case "investigation":
        return "Investigation";
      case "intelligence":
        return "Intelligence";
      case "analysis":
        return "Analysis";
      case "reporting":
        return "Reporting";
      case "general":
        return "General";
      default:
        return "";
    }
  };

  // Quick action buttons
  const quickActions = [
    { label: "Find accounts for...", query: "Find all accounts of " },
    { label: "Is account suspicious?", query: "Is  suspicious?" },
    { label: "Show risk score", query: "Show risk score for " },
    { label: "Generate report", query: "Generate investigation report for " },
  ];

  const handleQuickAction = (query: string) => {
    setInputValue(query);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100 dark:from-slate-900 dark:to-slate-800">
      <div className="container mx-auto px-4 py-6 max-w-6xl h-screen flex flex-col">
        {/* Header */}
        <header className="mb-4">
          <div className="flex items-center justify-between mb-3">
            <Link
              href="/"
              className="text-sm text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-slate-100 flex items-center gap-2 transition-colors"
            >
              ← Back to Search
            </Link>
            <h1 className="text-2xl font-bold text-slate-900 dark:text-slate-100">
              🤖 Intelligence Chatbot
            </h1>
            <div className="w-32"></div> {/* Spacer for centering */}
          </div>
          <p className="text-xs text-center text-slate-600 dark:text-slate-400">
            AI-powered investigations using Groq • Ask questions in natural language
          </p>
        </header>

        {/* Chat Container */}
        <div className="flex-1 bg-white dark:bg-slate-800 rounded-lg shadow-xl flex flex-col overflow-hidden border border-slate-200 dark:border-slate-700">
          {/* Messages Area */}
          <div className="flex-1 overflow-y-auto p-4 space-y-3">
            {messages.map((message) => (
              <div
                key={message.id}
                className={`flex ${message.sender === "user" ? "justify-end" : "justify-start"}`}
              >
                <div
                  className={`max-w-[85%] rounded-lg p-3 ${
                    message.sender === "user"
                      ? "bg-blue-500 text-white"
                      : "bg-slate-100 dark:bg-slate-700 text-slate-900 dark:text-slate-100"
                  }`}
                >
                  {message.sender === "bot" && message.queryType && message.queryType !== "general" && (
                    <div className="mb-2">
                      <span className={`text-xs px-2 py-1 rounded-full ${getQueryTypeColor(message.queryType)}`}>
                        {getQueryTypeEmoji(message.queryType)} {getQueryTypeLabel(message.queryType)}
                      </span>
                    </div>
                  )}
                  <div className="whitespace-pre-wrap text-sm leading-relaxed">
                    {message.text.split('\n').map((line, i) => {
                      // Handle markdown-style bold
                      if (line.includes('**')) {
                        const parts = line.split('**');
                        return (
                          <div key={i}>
                            {parts.map((part, j) => 
                              j % 2 === 1 ? <strong key={j}>{part}</strong> : <span key={j}>{part}</span>
                            )}
                          </div>
                        );
                      }
                      return <div key={i}>{line || '\u00A0'}</div>;
                    })}
                  </div>
                  
                  {/* Show All Accounts Button for Investigation Results */}
                  {message.sender === "bot" && 
                   message.queryType === "investigation" && 
                   message.data?.sites && 
                   message.data.sites.length > 10 && (
                    <div className="mt-3 pt-3 border-t border-slate-200 dark:border-slate-600">
                      {!message.showFullList ? (
                        <button
                          onClick={() => toggleShowFullList(message.id)}
                          className="text-xs px-3 py-2 bg-blue-500 hover:bg-blue-600 text-white rounded-md transition-colors font-medium"
                        >
                          📋 Show All {message.data.sites.length} Accounts
                        </button>
                      ) : (
                        <>
                          <div className="text-xs mb-2 font-semibold text-slate-700 dark:text-slate-300">
                            📋 All {message.data.sites.length} Accounts:
                          </div>
                          <div className="max-h-96 overflow-y-auto bg-slate-50 dark:bg-slate-800 rounded p-3 space-y-1">
                            {message.data.sites.map((site: any, idx: number) => (
                              <div key={idx} className="text-xs">
                                <strong>{idx + 1}. {site.site}:</strong>{" "}
                                <a 
                                  href={site.url} 
                                  target="_blank" 
                                  rel="noopener noreferrer"
                                  className="text-blue-500 hover:text-blue-600 dark:text-blue-400 underline"
                                >
                                  {site.url}
                                </a>
                              </div>
                            ))}
                          </div>
                          <button
                            onClick={() => toggleShowFullList(message.id)}
                            className="text-xs px-3 py-2 mt-2 bg-slate-400 hover:bg-slate-500 text-white rounded-md transition-colors"
                          >
                            ↑ Show Less
                          </button>
                        </>
                      )}
                    </div>
                  )}
                  
                  <div className={`text-xs mt-2 ${message.sender === "user" ? "opacity-80" : "opacity-60"}`}>
                    {new Date(message.timestamp).toLocaleTimeString()}
                  </div>
                </div>
              </div>
            ))}
            {isLoading && (
              <div className="flex justify-start">
                <div className="bg-slate-100 dark:bg-slate-700 rounded-lg p-4">
                  <div className="flex space-x-2">
                    <div className="w-2 h-2 bg-slate-400 rounded-full animate-bounce"></div>
                    <div className="w-2 h-2 bg-slate-400 rounded-full animate-bounce" style={{ animationDelay: "0.1s" }}></div>
                    <div className="w-2 h-2 bg-slate-400 rounded-full animate-bounce" style={{ animationDelay: "0.2s" }}></div>
                  </div>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          {/* Quick Actions */}
          <div className="border-t border-slate-200 dark:border-slate-700 px-4 py-2 bg-slate-50 dark:bg-slate-800/50">
            <div className="flex gap-2 flex-wrap">
              <span className="text-xs text-slate-500 dark:text-slate-400 self-center">Quick actions:</span>
              {quickActions.map((action, idx) => (
                <button
                  key={idx}
                  onClick={() => handleQuickAction(action.query)}
                  className="text-xs px-3 py-1 bg-white dark:bg-slate-700 text-slate-700 dark:text-slate-300 rounded-full hover:bg-slate-100 dark:hover:bg-slate-600 transition-colors border border-slate-200 dark:border-slate-600"
                  disabled={isLoading}
                >
                  {action.label}
                </button>
              ))}
            </div>
          </div>

          {/* Input Area */}
          <div className="border-t border-slate-200 dark:border-slate-700 p-4 bg-white dark:bg-slate-800">
            <div className="flex gap-2">
              <input
                type="text"
                value={inputValue}
                onChange={(e) => setInputValue(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder="Ask me anything... (e.g., 'Find all accounts of john_doe')"
                className="flex-1 px-4 py-3 border border-slate-300 dark:border-slate-600 rounded-lg bg-white dark:bg-slate-700 text-slate-900 dark:text-slate-100 focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm"
                disabled={isLoading}
              />
              <button
                onClick={handleSendMessage}
                disabled={isLoading || !inputValue.trim()}
                className="px-6 py-3 bg-blue-500 text-white rounded-lg hover:bg-blue-600 disabled:bg-slate-300 dark:disabled:bg-slate-600 disabled:cursor-not-allowed transition-colors font-medium text-sm"
              >
                {isLoading ? "..." : "Send"}
              </button>
            </div>
            <div className="mt-2 text-xs text-slate-500 dark:text-slate-400">
              Press Enter to send • Powered by AI (Groq + Llama 3.3)
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

