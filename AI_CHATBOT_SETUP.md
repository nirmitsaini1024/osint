# AI Intelligence Chatbot Setup Guide

## Overview

The Sherlock application now includes an AI-powered intelligence chatbot that can:
- 🔍 **Investigation Queries**: Find accounts across 400+ platforms
- 🧠 **Intelligence Queries**: Analyze suspicious activity and platform risks
- 📊 **Analysis Queries**: Generate risk scores using AI
- 📝 **Reporting Queries**: Create comprehensive investigation reports

All intelligence, analysis, and reporting features are powered by **Groq AI** with **Llama 3.3 70B** model.

---

## Prerequisites

1. **Groq API Key** (Free tier available!)
   - Sign up at: https://console.groq.com
   - Get your API key from the dashboard
   - Free tier includes generous limits

2. **Python 3.9+** and **Node.js 18+**

---

## Setup Instructions

### Step 1: Set Up Groq API Key

#### Linux/Mac:
```bash
export GROQ_API_KEY="your-groq-api-key-here"

# To make it permanent, add to ~/.bashrc or ~/.zshrc:
echo 'export GROQ_API_KEY="your-groq-api-key-here"' >> ~/.bashrc
source ~/.bashrc
```

#### Windows (PowerShell):
```powershell
$env:GROQ_API_KEY="your-groq-api-key-here"

# To make it permanent:
[System.Environment]::SetEnvironmentVariable('GROQ_API_KEY', 'your-groq-api-key-here', 'User')
```

### Step 2: Install Backend Dependencies

The Groq SDK is already installed. If you need to reinstall:

```bash
cd sherlock
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install groq
```

### Step 3: Start the Backend

```bash
cd sherlock
source venv/bin/activate  # On Windows: venv\Scripts\activate
python api.py
```

The API will be available at `http://localhost:8000`

### Step 4: Start the Frontend

In a new terminal:

```bash
cd frontend
npm install  # If not already installed
npm run dev
```

The frontend will be available at `http://localhost:3000`

---

## Using the Chatbot

### Access the Chatbot

1. Go to `http://localhost:3000`
2. Click the "🤖 Try AI Intelligence Chatbot" button
3. Or navigate directly to `http://localhost:3000/chatbot`

### Example Queries

#### Investigation Queries (Find Accounts)
```
Find all accounts of john_doe
Search for username alice_2024
Locate accounts for bob123
```

#### Intelligence Queries (AI-Powered Risk Analysis)
```
Is john_doe suspicious?
Which platform has highest risk for alice_2024?
Analyze threats for bob123
```

#### Analysis Queries (AI Risk Scoring)
```
Show risk score for john_doe
Analyze profile alice_2024
What's the risk level for bob123?
```

#### Reporting Queries (AI-Generated Reports)
```
Generate investigation report for john_doe
Create summary for alice_2024
Summarize findings for bob123
```

---

## How It Works

### Backend Architecture

1. **AI Risk Analyzer** (`ai_risk_analyzer.py`):
   - Uses Groq API with Llama 3.3 70B model
   - Analyzes username patterns, platform distribution, and risk indicators
   - Generates natural language explanations
   - Creates comprehensive investigation reports

2. **API Endpoints** (`api.py`):
   - `/chatbot` - Main chatbot endpoint
   - Classifies queries into 4 types
   - Extracts usernames using regex patterns
   - Performs Sherlock searches
   - Uses AI for risk analysis

3. **Query Classification**:
   - Natural language processing to detect query type
   - Username extraction from conversational queries
   - Context-aware responses

### Frontend Architecture

1. **Chatbot Page** (`/chatbot/page.tsx`):
   - Real-time chat interface
   - Query type badges (Investigation, Intelligence, Analysis, Reporting)
   - Quick action buttons
   - Markdown formatting support
   - Loading animations

2. **Features**:
   - Message history
   - Real-time responses
   - Error handling
   - Mobile responsive

---

## AI Models Used

### Groq with Llama 3.3 70B
- **Speed**: Ultra-fast inference (~1-2 seconds)
- **Quality**: High-quality analysis and reasoning
- **Cost**: Generous free tier
- **Capabilities**:
  - Risk assessment
  - Pattern recognition
  - Natural language generation
  - Report writing

### Alternative Models

You can change the model in `ai_risk_analyzer.py`:

```python
self.model = "llama-3.3-70b-versatile"  # Current (best quality)
# self.model = "mixtral-8x7b-32768"     # Alternative (faster)
# self.model = "gemma2-9b-it"           # Alternative (lighter)
```

---

## API Reference

### POST /chatbot

**Request:**
```json
{
  "query": "Is john_doe suspicious?",
  "timestamp": "2026-02-05T10:30:00Z"
}
```

**Response:**
```json
{
  "query": "Is john_doe suspicious?",
  "response": "🧠 **AI Risk Analysis for 'john_doe':**...",
  "query_type": "intelligence",
  "timestamp": "2026-02-05T10:30:00Z",
  "data": {
    "username": "john_doe",
    "ai_analysis": {
      "risk_score": 3.2,
      "is_suspicious": false,
      "risk_level": "Low",
      "indicators": ["..."],
      "explanation": "..."
    }
  }
}
```

---

## Troubleshooting

### Error: "GROQ_API_KEY not found"

**Solution**: Make sure you've set the environment variable:
```bash
export GROQ_API_KEY="your-key-here"
```

Restart the backend after setting the variable.

### Error: "AI analysis unavailable"

**Causes**:
1. GROQ_API_KEY not set
2. Invalid API key
3. Network issues
4. Rate limit exceeded

**Solution**: Check your API key and internet connection. Free tier has generous limits but they do exist.

### Chatbot not responding

**Solution**:
1. Ensure backend is running on port 8000
2. Check browser console for errors
3. Verify GROQ_API_KEY is set
4. Try restarting both backend and frontend

### AI responses are slow

**Note**: First request might take 2-3 seconds. Subsequent requests are usually faster (1-2 seconds). Groq is known for being one of the fastest LLM inference platforms.

---

## Features Breakdown

### ✅ Implemented

- [x] Natural language query processing
- [x] AI-powered risk analysis
- [x] Suspicious account detection
- [x] Platform risk assessment
- [x] Risk score generation
- [x] Investigation report generation
- [x] Real-time chat interface
- [x] Query type classification
- [x] Username extraction
- [x] Integration with Sherlock search
- [x] Error handling and fallbacks

### 🚀 Potential Enhancements

- [ ] Multi-language support
- [ ] Chat history persistence
- [ ] Export reports (PDF/JSON)
- [ ] User authentication
- [ ] Rate limiting
- [ ] Caching for repeated queries
- [ ] Advanced analytics dashboard
- [ ] Batch analysis
- [ ] Custom risk scoring models

---

## Cost Information

### Groq Free Tier (Current)
- **Cost**: FREE
- **Rate Limits**: Generous (check console.groq.com for current limits)
- **Models**: All models including Llama 3.3 70B
- **Perfect for**: Development and moderate usage

### Paid Tier
- Pay-as-you-go pricing
- Very affordable compared to OpenAI
- No monthly commitments
- Check: https://groq.com/pricing

---

## Security Notes

1. **API Key Security**:
   - Never commit API keys to git
   - Use environment variables
   - Don't expose keys in frontend

2. **Rate Limiting**:
   - Consider implementing rate limiting for production
   - Monitor API usage

3. **Data Privacy**:
   - Usernames are sent to Groq API for analysis
   - Review Groq's privacy policy for compliance
   - Consider data retention policies

---

## Support

- **Groq Documentation**: https://console.groq.com/docs
- **Sherlock Project**: https://github.com/sherlock-project/sherlock
- **Issues**: Check the main README.md for project issues

---

## Example Session

```
User: Find all accounts of elonmusk

Bot: 🔍 Investigation Results for 'elonmusk':
     Found 127 accounts:
     • Twitter: https://twitter.com/elonmusk
     • Instagram: https://instagram.com/elonmusk
     ...

User: Is elonmusk suspicious?

Bot: 🧠 AI Risk Analysis for 'elonmusk':
     Is Suspicious: ✅ NO
     Risk Score: 2.1/10
     Risk Level: Low
     
     Key Indicators:
     1. High cross-platform consistency
     2. Verified accounts on major platforms
     3. Legitimate public figure presence
     
     AI Assessment: Profile shows strong legitimacy indicators...

User: Generate investigation report for elonmusk

Bot: 📝 Investigation Report
     [Comprehensive AI-generated report with findings]
```

---

**Enjoy your AI-powered intelligence chatbot! 🚀**


