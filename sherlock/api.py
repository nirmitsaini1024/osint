"""
FastAPI wrapper for Sherlock - Social Media Username Search
"""
import os
import sys
import re
from datetime import datetime
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Add the parent directory to the path to import sherlock_project
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

from sherlock_project.sherlock import sherlock
from sherlock_project.sites import SitesInformation
from sherlock_project.notify import QueryNotify
from sherlock_project.result import QueryStatus, QueryResult
from ai_risk_analyzer import AIRiskAnalyzer

app = FastAPI(title="Sherlock API", version="1.0.0")

# Enable CORS for Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000", "*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["*"],
)


class QueryNotifySilent(QueryNotify):
    """Silent query notifier that doesn't print anything."""
    
    def __init__(self):
        super().__init__()
        self.results = []
    
    def start(self, message=None):
        pass
    
    def update(self, result):
        self.results.append(result)
    
    def finish(self, message=None):
        pass


class SearchRequest(BaseModel):
    username: str
    sites: Optional[List[str]] = None
    timeout: Optional[int] = 60
    nsfw: Optional[bool] = False


class SiteResult(BaseModel):
    site_name: str
    url_main: str
    url_user: str
    status: str
    query_time: Optional[float] = None
    context: Optional[str] = None


class SearchResponse(BaseModel):
    username: str
    total_sites: int
    found_count: int
    results: List[SiteResult]


class ChatMessage(BaseModel):
    query: str
    timestamp: Optional[str] = None
    last_username: Optional[str] = None  # Remember last username from conversation


class ChatResponse(BaseModel):
    query: str
    response: str
    query_type: str
    timestamp: str
    data: Optional[Dict] = None
    last_username: Optional[str] = None  # Send back for frontend to remember


@app.get("/")
async def root():
    return {"message": "Sherlock API - Social Media Username Search", "version": "1.0.0"}


@app.get("/health")
async def health():
    return {"status": "healthy"}


@app.get("/chatbot/status")
async def chatbot_status():
    """Check if AI chatbot is properly configured."""
    try:
        ai_analyzer = AIRiskAnalyzer()
        return {
            "status": "ready",
            "ai_available": True,
            "model": ai_analyzer.model,
            "message": "AI chatbot is ready to use"
        }
    except ValueError as e:
        return {
            "status": "not_configured",
            "ai_available": False,
            "error": str(e),
            "message": "Please set GROQ_API_KEY environment variable"
        }
    except Exception as e:
        return {
            "status": "error",
            "ai_available": False,
            "error": str(e),
            "message": "AI chatbot configuration error"
        }


@app.post("/search", response_model=SearchResponse)
async def search_username(request: SearchRequest):
    """
    Search for a username across social media platforms.
    
    Args:
        request: SearchRequest containing username and optional parameters
        
    Returns:
        SearchResponse with found accounts and their details
    """
    try:
        # Load site information
        try:
            sites = SitesInformation(
                honor_exclusions=True,
                do_not_exclude=request.sites if request.sites else [],
            )
        except Exception as error:
            raise HTTPException(status_code=500, detail=f"Error loading sites: {str(error)}")
        
        # Remove NSFW sites if requested
        if not request.nsfw:
            sites.remove_nsfw_sites(do_not_remove=request.sites if request.sites else [])
        
        # Convert SitesInformation to dictionary format expected by sherlock()
        site_data = {site.name: site.information for site in sites}
        
        # Filter to specific sites if requested
        if request.sites:
            filtered_site_data = {}
            site_missing = []
            for site_name in request.sites:
                found = False
                for existing_site in site_data:
                    if site_name.lower() == existing_site.lower():
                        filtered_site_data[existing_site] = site_data[existing_site]
                        found = True
                        break
                if not found:
                    site_missing.append(site_name)
            
            if site_missing:
                raise HTTPException(
                    status_code=400,
                    detail=f"Sites not found: {', '.join(site_missing)}"
                )
            
            if not filtered_site_data:
                raise HTTPException(
                    status_code=400,
                    detail="No valid sites specified"
                )
            
            site_data = filtered_site_data
        
        # Create silent notifier
        query_notify = QueryNotifySilent()
        
        # Run the search
        query_notify.start(request.username)
        results = sherlock(
            username=request.username,
            site_data=site_data,
            query_notify=query_notify,
            dump_response=False,
            proxy=None,
            timeout=request.timeout,
        )
        query_notify.finish()
        
        # Format results
        formatted_results = []
        found_count = 0
        
        for site_name, site_info in results.items():
            status_obj: QueryResult = site_info.get("status")
            if status_obj is None:
                continue
            
            status_str = str(status_obj.status.value)
            
            if status_obj.status == QueryStatus.CLAIMED:
                found_count += 1
            
            formatted_results.append(SiteResult(
                site_name=site_name,
                url_main=site_info.get("url_main", ""),
                url_user=site_info.get("url_user", ""),
                status=status_str,
                query_time=status_obj.query_time,
                context=status_obj.context,
            ))
        
        return SearchResponse(
            username=request.username,
            total_sites=len(formatted_results),
            found_count=found_count,
            results=formatted_results,
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error searching username: {str(e)}")


def classify_query(query: str) -> str:
    """Classify the query into one of the four types."""
    query_lower = query.lower()
    
    # Investigation Queries
    if any(keyword in query_lower for keyword in ['find', 'search', 'locate', 'accounts of', 'check if', 'impersonated', 'impersonation']):
        return "investigation"
    
    # Intelligence Queries
    elif any(keyword in query_lower for keyword in ['suspicious', 'risk', 'threat', 'which platform', 'highest risk', 'dangerous']):
        return "intelligence"
    
    # Analysis Queries
    elif any(keyword in query_lower for keyword in ['risk score', 'compare', 'analyze', 'analysis', 'show score', 'score']):
        return "analysis"
    
    # Reporting Queries
    elif any(keyword in query_lower for keyword in ['report', 'generate', 'summarize', 'summary', 'findings']):
        return "reporting"
    
    return "general"


def extract_username(query: str) -> Optional[str]:
    """Extract username from query using improved NLP patterns."""
    query_lower = query.lower()
    
    # Common stop words to exclude
    stop_words = {
        'find', 'all', 'accounts', 'of', 'search', 'for', 'check', 'if', 'is', 'show',
        'analyze', 'generate', 'report', 'suspicious', 'risk', 'score', 'platform',
        'highest', 'which', 'has', 'threat', 'threats', 'profile', 'level', 'them',
        'this', 'that', 'these', 'those', 'what', 'whats', 'the', 'a', 'an', 'and',
        'or', 'but', 'in', 'on', 'at', 'to', 'from', 'with', 'about', 'give', 'me',
        'my', 'your', 'their', 'his', 'her', 'its', 'our', 'summary', 'findings',
        'investigation', 'create', 'summarize', 'name', 'it', 'him', 'her', 'they',
        'tell', 'please', 'can', 'you', 'could', 'would', 'should', 'want', 'need',
        'like', 'get', 'see', 'view', 'display', 'list', 'info', 'information'
    }
    
    # Pattern 1: "find/search/locate accounts of <username>"
    match = re.search(r'(?:accounts?\s+of|search\s+for|locate)\s+([a-zA-Z0-9_-]+)', query_lower)
    if match:
        username = match.group(1)
        if username not in stop_words:
            return username
    
    # Pattern 2: "is <username> suspicious"
    match = re.search(r'is\s+([a-zA-Z0-9_-]+)\s+suspicious', query_lower)
    if match:
        username = match.group(1)
        if username not in stop_words:
            return username
    
    # Pattern 3: "show/analyze/check <username>"
    match = re.search(r'(?:show|analyze|check|report\s+for|generate.*?for|summary\s+for|score\s+for|score\s+of)\s+([a-zA-Z0-9_-]+)', query_lower)
    if match:
        username = match.group(1)
        if username not in stop_words:
            return username
    
    # Pattern 4: "for/of <username>" (last resort)
    match = re.search(r'(?:for|of)\s+([a-zA-Z0-9_-]+)(?:\s|$)', query_lower)
    if match:
        username = match.group(1)
        if username not in stop_words and len(username) >= 3:
            return username
    
    # Pattern 5: Find the last username-like word that's not a stop word
    words = query.split()
    for word in reversed(words):  # Check from end to beginning
        word_clean = word.lower().strip('.,!?;:')
        if (re.match(r'^[a-zA-Z0-9_-]{3,}$', word_clean) and 
            word_clean not in stop_words):
            return word_clean
    
    return None


def perform_username_search(username: str, timeout: int = 60) -> List[Dict]:
    """Helper function to search for a username and return found sites."""
    sites = SitesInformation(honor_exclusions=True, do_not_exclude=[])
    sites.remove_nsfw_sites()
    site_data = {site.name: site.information for site in sites}
    query_notify = QueryNotifySilent()
    
    results = sherlock(
        username=username,
        site_data=site_data,
        query_notify=query_notify,
        dump_response=False,
        proxy=None,
        timeout=timeout,
    )
    
    found_sites = []
    for site_name, site_info in results.items():
        status_obj: QueryResult = site_info.get("status")
        if status_obj and status_obj.status == QueryStatus.CLAIMED:
            found_sites.append({
                "site": site_name,
                "url": site_info.get("url_user", ""),
                "response_time": status_obj.query_time
            })
    
    return found_sites


@app.post("/chatbot", response_model=ChatResponse)
async def chatbot_query(message: ChatMessage):
    """
    Process natural language queries about username searches and analysis using AI.
    
    Supports:
    - Investigation: "Find all accounts of john_doe"
    - Intelligence: "Is this account suspicious?" / "Which platform has highest risk?"
    - Analysis: "Show risk score for john_doe"
    - Reporting: "Generate investigation report for john_doe"
    - Context: Remembers last username from conversation
    """
    try:
        query = message.query.strip()
        query_type = classify_query(query)
        timestamp = datetime.now().isoformat()
        
        # Get the last username from conversation context
        context_username = message.last_username
        
        # Initialize AI analyzer (will fail gracefully if GROQ_API_KEY not set)
        try:
            ai_analyzer = AIRiskAnalyzer()
            ai_available = True
        except ValueError as e:
            ai_available = False
            ai_error = str(e)
        
        # Investigation Queries
        if query_type == "investigation":
            username = extract_username(query) or context_username
            
            if username:
                found_sites = perform_username_search(username)
                
                if found_sites:
                    # Check if user wants to see all results
                    show_all = any(keyword in query.lower() for keyword in ['show all', 'show more', 'all accounts', 'full list', 'complete list'])
                    display_limit = len(found_sites) if show_all else 10
                    
                    response = f"🔍 **Investigation Results for '{username}':**\n\n"
                    response += f"Found **{len(found_sites)}** accounts:\n\n"
                    for site in found_sites[:display_limit]:
                        response += f"• **{site['site']}**: {site['url']}\n"
                    if len(found_sites) > display_limit:
                        response += f"\n...and **{len(found_sites) - display_limit}** more accounts."
                        response += f"\n\n💡 *Type 'show all' to see all {len(found_sites)} accounts or click the 'Show All' button*"
                else:
                    response = f"❌ No accounts found for username '{username}'."
                
                return ChatResponse(
                    query=query,
                    response=response,
                    query_type=query_type,
                    timestamp=timestamp,
                    data={"username": username, "found_count": len(found_sites), "sites": found_sites},
                    last_username=username
                )
            else:
                return ChatResponse(
                    query=query,
                    response="Please specify a username to search for. For example: 'Find all accounts of john_doe'",
                    query_type=query_type,
                    timestamp=timestamp,
                    last_username=context_username
                )
        
        # Intelligence Queries - AI-POWERED!
        elif query_type == "intelligence":
            username = extract_username(query) or context_username
            if username:
                if not ai_available:
                    return ChatResponse(
                    
                        query=query,
                        response=f"⚠️ AI analysis unavailable: {ai_error}\n\nPlease set GROQ_API_KEY environment variable.",
                        query_type=query_type,
                        timestamp=timestamp,
                    last_username=username if "username" in locals() else context_username
                )
                
                found_sites = perform_username_search(username)
                
                if not found_sites:
                    response = f"❌ No accounts found for '{username}'. Cannot perform risk analysis."
                else:
                    query_lower = query.lower()
                    
                    # Check which specific question was asked
                    if "which platform" in query_lower and ("highest risk" in query_lower or "most risk" in query_lower):
                        # Answer: Which platform has highest risk?
                        platform_info = ai_analyzer.find_highest_risk_platform(username, found_sites)
                        
                        response = f"🎯 **Highest Risk Platform Analysis for '{username}':**\n\n"
                        response += f"**Platform:** {platform_info['platform']}\n"
                        response += f"**Risk Score:** {platform_info['risk_score']}/10\n"
                        response += f"**Reason:** {platform_info['reason']}\n\n"
                        response += f"📊 Found on {len(found_sites)} total platforms."
                        
                        return ChatResponse(
                    
                            query=query,
                            response=response,
                            query_type=query_type,
                            timestamp=timestamp,
                            data={
                                "username": username,
                                "highest_risk_platform": platform_info,
                                "total_platforms": len(found_sites)
                            }
                        )
                    else:
                        # Answer: Is account suspicious?
                        ai_analysis = ai_analyzer.analyze_account_suspicious(username, found_sites)
                        
                        response = f"🧠 **AI Risk Analysis for '{username}':**\n\n"
                        response += f"**Is Suspicious:** {'⚠️ YES' if ai_analysis['is_suspicious'] else '✅ NO'}\n"
                        response += f"**Risk Score:** {ai_analysis['risk_score']}/10\n"
                        response += f"**Risk Level:** {ai_analysis['risk_level']}\n\n"
                        response += f"**Key Indicators:**\n"
                        for i, indicator in enumerate(ai_analysis['indicators'], 1):
                            response += f"{i}. {indicator}\n"
                        response += f"\n**AI Assessment:** {ai_analysis['explanation']}\n\n"
                        response += f"📊 Analysis based on {len(found_sites)} accounts found."
                        
                        return ChatResponse(
                    
                            query=query,
                            response=response,
                            query_type=query_type,
                            timestamp=timestamp,
                            data={
                                "username": username,
                                "ai_analysis": ai_analysis,
                                "found_sites": found_sites
                            }
                        )
            else:
                response = "Please specify which account you want to analyze. For example: 'Is john_doe suspicious?'"
                return ChatResponse(
                    
                    query=query,
                    response=response,
                    query_type=query_type,
                    timestamp=timestamp,
                    last_username=username if "username" in locals() else context_username
                )
        
        # Analysis Queries - AI-powered risk scoring
        elif query_type == "analysis":
            username = extract_username(query)
            if username:
                if not ai_available:
                    return ChatResponse(
                    
                        query=query,
                        response=f"⚠️ AI analysis unavailable: {ai_error}\n\nPlease set GROQ_API_KEY environment variable.",
                        query_type=query_type,
                        timestamp=timestamp,
                    last_username=username if "username" in locals() else context_username
                )
                
                found_sites = perform_username_search(username)
                
                if not found_sites:
                    response = f"❌ No accounts found for '{username}'."
                else:
                    ai_analysis = ai_analyzer.analyze_account_suspicious(username, found_sites)
                    
                    response = f"📊 **AI Risk Score Analysis for '{username}':**\n\n"
                    response += f"**Overall Risk Score:** {ai_analysis['risk_score']}/10\n"
                    response += f"**Risk Level:** {ai_analysis['risk_level']}\n"
                    response += f"**Accounts Found:** {len(found_sites)} platforms\n"
                    response += f"**Suspicious:** {'⚠️ YES' if ai_analysis['is_suspicious'] else '✅ NO'}\n\n"
                    response += f"**Risk Breakdown:**\n"
                    for i, indicator in enumerate(ai_analysis['indicators'], 1):
                        response += f"{i}. {indicator}\n"
                    response += f"\n**AI Assessment:** {ai_analysis['explanation']}"
                
                return ChatResponse(
                    
                    query=query,
                    response=response,
                    query_type=query_type,
                    timestamp=timestamp,
                    data={"username": username, "ai_analysis": ai_analysis if found_sites else None}
                )
            else:
                response = "Please specify which profile you want to analyze. For example: 'Show risk score for john_doe'"
                return ChatResponse(
                    
                    query=query,
                    response=response,
                    query_type=query_type,
                    timestamp=timestamp,
                    last_username=username if "username" in locals() else context_username
                )
        
        # Reporting Queries - AI-generated reports
        elif query_type == "reporting":
            username = extract_username(query)
            if username:
                if not ai_available:
                    return ChatResponse(
                    
                        query=query,
                        response=f"⚠️ AI analysis unavailable: {ai_error}\n\nPlease set GROQ_API_KEY environment variable.",
                        query_type=query_type,
                        timestamp=timestamp,
                    last_username=username if "username" in locals() else context_username
                )
                
                found_sites = perform_username_search(username)
                
                if not found_sites:
                    response = f"❌ No accounts found for '{username}'. Cannot generate report."
                else:
                    # Generate AI-powered risk assessment first
                    ai_analysis = ai_analyzer.analyze_account_suspicious(username, found_sites)
                    
                    # Generate comprehensive report
                    report = ai_analyzer.generate_risk_report(username, found_sites, ai_analysis)
                    
                    response = f"📝 **Investigation Report**\n\n{report}"
                
                return ChatResponse(
                    
                    query=query,
                    response=response,
                    query_type=query_type,
                    timestamp=timestamp,
                    data={"username": username, "report_type": "full_analysis"}
                )
            else:
                response = "Please specify which account you want to generate a report for. For example: 'Generate report for john_doe'"
                return ChatResponse(
                    
                    query=query,
                    response=response,
                    query_type=query_type,
                    timestamp=timestamp,
                    last_username=username if "username" in locals() else context_username
                )
        
        # General Queries
        else:
            response = """👋 **Welcome to the Sherlock Intelligence Chatbot!**

I can help you with AI-powered social media investigations:

🔍 **Investigation Queries:**
• "Find all accounts of john_doe"
• "Search for username alice_2024"
• "Locate accounts for bob123"

🧠 **Intelligence Queries:**
• "Is john_doe suspicious?"
• "Which platform has highest risk for alice_2024?"
• "Analyze threats for bob123"

📊 **Analysis Queries:**
• "Show risk score for john_doe"
• "Analyze profile alice_2024"
• "What's the risk level for bob123?"

📝 **Reporting Queries:**
• "Generate investigation report for john_doe"
• "Create summary for alice_2024"
• "Summarize findings for bob123"

💡 **Tips:**
- All intelligence, analysis, and reporting features use AI
- Results are based on real data from 400+ social platforms
- Risk analysis considers platform security, patterns, and indicators

What would you like to investigate?"""
            
            return ChatResponse(
                    
                query=query,
                response=response,
                query_type="general",
                timestamp=timestamp,
                    last_username=username if "username" in locals() else context_username
                )
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

