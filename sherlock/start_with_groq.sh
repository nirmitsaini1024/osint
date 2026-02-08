#!/bin/bash

# Start Sherlock Backend with Groq API Key
# Usage: ./start_with_groq.sh YOUR_GROQ_API_KEY

if [ -z "$1" ]; then
    echo "❌ Error: No API key provided"
    echo ""
    echo "Usage: ./start_with_groq.sh YOUR_GROQ_API_KEY"
    echo ""
    echo "Or set it manually:"
    echo "  export GROQ_API_KEY='your-key-here'"
    echo "  python api.py"
    exit 1
fi

echo "🔑 Setting GROQ_API_KEY..."
export GROQ_API_KEY="$1"

echo "✅ API Key set!"
echo ""
echo "🚀 Starting backend..."
python api.py


