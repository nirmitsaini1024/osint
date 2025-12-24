"use client";

import { SearchResponse, SiteResult } from "../page";
import { useState } from "react";

interface SearchResultsProps {
  results: SearchResponse;
}

export default function SearchResults({ results }: SearchResultsProps) {
  const [filterStatus, setFilterStatus] = useState<"all" | "claimed" | "available">("all");

  const filteredResults =
    filterStatus === "all"
      ? results.results
      : filterStatus === "claimed"
        ? results.results.filter((r) => r.status === "Claimed")
        : results.results.filter((r) => r.status === "Available");

  const getStatusBadge = (status: string) => {
    switch (status) {
      case "Claimed":
        return (
          <span className="px-2 py-1 text-xs font-semibold rounded-full bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-300">
            ✓ Found
          </span>
        );
      case "Available":
        return (
          <span className="px-2 py-1 text-xs font-semibold rounded-full bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-300">
            Not Found
          </span>
        );
      case "Unknown":
        return (
          <span className="px-2 py-1 text-xs font-semibold rounded-full bg-yellow-100 text-yellow-800 dark:bg-yellow-900/30 dark:text-yellow-300">
            Unknown
          </span>
        );
      case "Illegal":
        return (
          <span className="px-2 py-1 text-xs font-semibold rounded-full bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-300">
            Illegal
          </span>
        );
      case "WAF":
        return (
          <span className="px-2 py-1 text-xs font-semibold rounded-full bg-orange-100 text-orange-800 dark:bg-orange-900/30 dark:text-orange-300">
            Blocked
          </span>
        );
      default:
        return (
          <span className="px-2 py-1 text-xs font-semibold rounded-full bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-300">
            {status}
          </span>
        );
    }
  };

  return (
    <div className="bg-white dark:bg-slate-800 rounded-lg shadow-lg p-6">
      <div className="mb-6">
        <div className="flex flex-col md:flex-row md:items-center md:justify-between mb-4">
          <div>
            <h2 className="text-2xl font-bold text-slate-900 dark:text-slate-100 mb-2">
              Results for <span className="text-blue-600 dark:text-blue-400">{results.username}</span>
            </h2>
            <p className="text-sm text-slate-600 dark:text-slate-400">
              Found {results.found_count} of {results.total_sites} sites checked
            </p>
          </div>
          <div className="flex gap-2 mt-4 md:mt-0">
            <button
              onClick={() => setFilterStatus("all")}
              className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                filterStatus === "all"
                  ? "bg-blue-600 text-white"
                  : "bg-slate-100 text-slate-700 dark:bg-slate-700 dark:text-slate-300 hover:bg-slate-200 dark:hover:bg-slate-600"
              }`}
            >
              All ({results.total_sites})
            </button>
            <button
              onClick={() => setFilterStatus("claimed")}
              className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                filterStatus === "claimed"
                  ? "bg-green-600 text-white"
                  : "bg-slate-100 text-slate-700 dark:bg-slate-700 dark:text-slate-300 hover:bg-slate-200 dark:hover:bg-slate-600"
              }`}
            >
              Found ({results.found_count})
            </button>
            <button
              onClick={() => setFilterStatus("available")}
              className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                filterStatus === "available"
                  ? "bg-gray-600 text-white"
                  : "bg-slate-100 text-slate-700 dark:bg-slate-700 dark:text-slate-300 hover:bg-slate-200 dark:hover:bg-slate-600"
              }`}
            >
              Not Found ({results.total_sites - results.found_count})
            </button>
          </div>
        </div>
      </div>

      <div className="space-y-3 max-h-[600px] overflow-y-auto">
        {filteredResults.length === 0 ? (
          <p className="text-center text-slate-500 dark:text-slate-400 py-8">
            No results match the selected filter.
          </p>
        ) : (
          filteredResults.map((result: SiteResult) => (
            <div
              key={result.site_name}
              className="flex items-center justify-between p-4 border border-slate-200 dark:border-slate-700 rounded-lg hover:bg-slate-50 dark:hover:bg-slate-700/50 transition-colors"
            >
              <div className="flex-1 min-w-0">
                <div className="flex items-center gap-3 mb-2">
                  <h3 className="font-semibold text-slate-900 dark:text-slate-100">
                    {result.site_name}
                  </h3>
                  {getStatusBadge(result.status)}
                </div>
                {result.status === "Claimed" && result.url_user && (
                  <a
                    href={result.url_user}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-sm text-blue-600 dark:text-blue-400 hover:underline truncate block"
                  >
                    {result.url_user}
                  </a>
                )}
                {result.query_time && (
                  <p className="text-xs text-slate-500 dark:text-slate-400 mt-1">
                    Response time: {Math.round(result.query_time * 1000)}ms
                  </p>
                )}
                {result.context && (
                  <p className="text-xs text-slate-500 dark:text-slate-400 mt-1">
                    {result.context}
                  </p>
                )}
              </div>
              {result.status === "Claimed" && result.url_user && (
                <a
                  href={result.url_user}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="ml-4 px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white text-sm font-medium rounded-lg transition-colors whitespace-nowrap"
                >
                  Visit →
                </a>
              )}
            </div>
          ))
        )}
      </div>
    </div>
  );
}

