"use client";

import { useState } from "react";
import Link from "next/link";
import SearchForm from "./components/SearchForm";
import SearchResults from "./components/SearchResults";

export interface SiteResult {
  site_name: string;
  url_main: string;
  url_user: string;
  status: string;
  query_time?: number;
  context?: string;
}

export interface SearchResponse {
  username: string;
  total_sites: number;
  found_count: number;
  results: SiteResult[];
}

export default function Home() {
  const [searchResults, setSearchResults] = useState<SearchResponse | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSearch = async (username: string, sites?: string[], timeout?: number, nsfw?: boolean) => {
    setIsLoading(true);
    setError(null);
    setSearchResults(null);

    try {
      const response = await fetch("http://localhost:8000/search", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          username,
          sites: sites && sites.length > 0 ? sites : undefined,
          timeout: timeout || 60,
          nsfw: nsfw || false,
        }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || "Failed to search username");
      }

      const data: SearchResponse = await response.json();
      setSearchResults(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "An error occurred");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100 dark:from-slate-900 dark:to-slate-800">
      <div className="container mx-auto px-4 py-8 max-w-6xl">
        <header className="text-center mb-8">
          <h1 className="text-4xl font-bold text-slate-900 dark:text-slate-100 mb-2">
            🔍 Sherlock
          </h1>
          <p className="text-lg text-slate-600 dark:text-slate-400 mb-4">
            Hunt down social media accounts by username across 400+ social networks
          </p>
          <div className="flex justify-center gap-3">
            <Link
              href="/chatbot"
              className="inline-flex items-center gap-2 px-6 py-3 bg-gradient-to-r from-blue-500 to-purple-600 text-white rounded-lg hover:from-blue-600 hover:to-purple-700 transition-all font-medium shadow-lg hover:shadow-xl transform hover:scale-105"
            >
              🤖 Try AI Intelligence Chatbot
            </Link>
          </div>
        </header>

        <SearchForm onSearch={handleSearch} isLoading={isLoading} />

        {error && (
          <div className="mt-6 p-4 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg">
            <p className="text-red-800 dark:text-red-200">{error}</p>
          </div>
        )}

        {searchResults && <SearchResults results={searchResults} />}
      </div>
    </div>
  );
}
