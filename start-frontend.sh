#!/bin/bash

# Start the Next.js frontend server

cd "$(dirname "$0")/frontend"

echo "Starting Next.js development server on http://localhost:3000"
npm run dev

