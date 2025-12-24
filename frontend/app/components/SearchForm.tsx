"use client";

import { useState, FormEvent } from "react";

interface SearchFormProps {
  onSearch: (username: string, sites?: string[], timeout?: number, nsfw?: boolean) => void;
  isLoading: boolean;
}

export default function SearchForm({ onSearch, isLoading }: SearchFormProps) {
  const [username, setUsername] = useState("");
  const [sites, setSites] = useState("");
  const [timeout, setTimeout] = useState(60);
  const [nsfw, setNsfw] = useState(false);

  const handleSubmit = (e: FormEvent) => {
    e.preventDefault();
    if (!username.trim()) return;

    const siteList = sites
      .split(",")
      .map((s) => s.trim())
      .filter((s) => s.length > 0);

    onSearch(
      username.trim(),
      siteList.length > 0 ? siteList : undefined,
      timeout,
      nsfw
    );
  };

  return (
    <div className="bg-white dark:bg-slate-800 rounded-lg shadow-lg p-6 mb-6">
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label
            htmlFor="username"
            className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-2"
          >
            Username
          </label>
          <input
            type="text"
            id="username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            placeholder="Enter username to search"
            className="w-full px-4 py-2 border border-slate-300 dark:border-slate-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:bg-slate-700 dark:text-slate-100"
            required
            disabled={isLoading}
          />
        </div>

        <div>
          <label
            htmlFor="sites"
            className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-2"
          >
            Specific Sites (Optional)
            <span className="text-xs text-slate-500 dark:text-slate-400 ml-2">
              Comma-separated list (e.g., Twitter, GitHub, Instagram)
            </span>
          </label>
          <input
            type="text"
            id="sites"
            value={sites}
            onChange={(e) => setSites(e.target.value)}
            placeholder="Leave empty to search all sites"
            className="w-full px-4 py-2 border border-slate-300 dark:border-slate-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:bg-slate-700 dark:text-slate-100"
            disabled={isLoading}
          />
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label
              htmlFor="timeout"
              className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-2"
            >
              Timeout (seconds)
            </label>
            <input
              type="number"
              id="timeout"
              value={timeout}
              onChange={(e) => setTimeout(Number(e.target.value))}
              min="10"
              max="300"
              className="w-full px-4 py-2 border border-slate-300 dark:border-slate-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:bg-slate-700 dark:text-slate-100"
              disabled={isLoading}
            />
          </div>

          <div className="flex items-center pt-8">
            <label className="flex items-center cursor-pointer">
              <input
                type="checkbox"
                checked={nsfw}
                onChange={(e) => setNsfw(e.target.checked)}
                className="w-4 h-4 text-blue-600 border-slate-300 rounded focus:ring-blue-500 dark:bg-slate-700 dark:border-slate-600"
                disabled={isLoading}
              />
              <span className="ml-2 text-sm text-slate-700 dark:text-slate-300">
                Include NSFW sites
              </span>
            </label>
          </div>
        </div>

        <button
          type="submit"
          disabled={isLoading || !username.trim()}
          className="w-full py-3 px-4 bg-blue-600 hover:bg-blue-700 disabled:bg-slate-400 disabled:cursor-not-allowed text-white font-semibold rounded-lg transition-colors duration-200"
        >
          {isLoading ? (
            <span className="flex items-center justify-center">
              <svg
                className="animate-spin -ml-1 mr-3 h-5 w-5 text-white"
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
              >
                <circle
                  className="opacity-25"
                  cx="12"
                  cy="12"
                  r="10"
                  stroke="currentColor"
                  strokeWidth="4"
                ></circle>
                <path
                  className="opacity-75"
                  fill="currentColor"
                  d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                ></path>
              </svg>
              Searching...
            </span>
          ) : (
            "Search"
          )}
        </button>
      </form>
    </div>
  );
}

