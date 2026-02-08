"""
AI-Powered Risk Analysis Module using Groq
Analyzes social media accounts for suspicious patterns and risk indicators
"""

import os
import json
import re
from typing import Dict, List, Optional
from groq import Groq
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class AIRiskAnalyzer:
    """AI-powered risk analyzer using Groq's fast LLM inference"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the AI Risk Analyzer with Groq API
        
        Args:
            api_key: Groq API key (defaults to GROQ_API_KEY env variable)
        """
        self.api_key = api_key or os.getenv("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("GROQ_API_KEY not found in environment variables")
        
        self.client = Groq(api_key=self.api_key)
        # Using llama-3.3-70b-versatile for best quality, or mixtral-8x7b-32768 for speed
        self.model = "llama-3.3-70b-versatile"
    
    def analyze_account_suspicious(
        self, 
        username: str, 
        found_sites: List[Dict]
    ) -> Dict:
        """
        Analyze if an account shows suspicious patterns using AI
        
        Args:
            username: The username to analyze
            found_sites: List of sites where the username was found
            
        Returns:
            Dict with risk_score, is_suspicious, indicators, and detailed analysis
        """
        if not found_sites:
            return {
                "username": username,
                "risk_score": 0.0,
                "is_suspicious": False,
                "risk_level": "Unknown",
                "indicators": ["No accounts found"],
                "explanation": f"No accounts found for username '{username}'. Cannot perform risk analysis.",
                "total_accounts": 0
            }
        
        # Prepare platform list for AI
        platform_list = [site['site'] for site in found_sites[:30]]  # Limit for token management
        
        prompt = f"""You are a cybersecurity expert specializing in social media threat analysis and digital forensics.

Analyze this username for suspicious activity and security risks:

**Username:** {username}
**Total Accounts Found:** {len(found_sites)}
**Platforms:** {', '.join(platform_list)}

Perform a comprehensive risk assessment considering:
1. Username patterns (e.g., random characters, numbers, suspicious keywords)
2. Platform distribution (presence on high-risk platforms like Telegram, Discord)
3. Account quantity (too many or too few accounts can indicate issues)
4. Platform variety (legitimate users typically have diverse social presence)
5. Common fraud indicators

Respond with ONLY a valid JSON object (no markdown, no explanations outside JSON):
{{
  "risk_score": <float 0-10>,
  "is_suspicious": <boolean>,
  "risk_level": "<Low|Medium|High|Critical>",
  "indicators": ["specific indicator 1", "specific indicator 2", "specific indicator 3"],
  "explanation": "2-3 sentence professional assessment"
}}"""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a cybersecurity risk analyst. Respond ONLY with valid JSON. No markdown formatting, no code blocks, just pure JSON."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.3,  # Lower temperature for consistent analysis
                max_tokens=500,
                top_p=0.9
            )
            
            # Extract JSON from response
            content = response.choices[0].message.content.strip()
            
            # Clean up any markdown formatting if present
            content = re.sub(r'^```json\s*', '', content, flags=re.MULTILINE)
            content = re.sub(r'^```\s*', '', content, flags=re.MULTILINE)
            content = re.sub(r'\s*```$', '', content, flags=re.MULTILINE)
            
            # Try to extract JSON object if there's extra text
            json_match = re.search(r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}', content, re.DOTALL)
            if json_match:
                content = json_match.group(0)
            
            # Parse JSON
            ai_analysis = json.loads(content)
            
            # Ensure required fields
            ai_analysis['username'] = username
            ai_analysis['total_accounts'] = len(found_sites)
            
            return ai_analysis
            
        except json.JSONDecodeError as e:
            return {
                "username": username,
                "risk_score": 5.0,
                "is_suspicious": False,
                "risk_level": "Medium",
                "indicators": ["AI analysis produced invalid JSON"],
                "explanation": f"AI analysis failed to parse: {str(e)}",
                "total_accounts": len(found_sites)
            }
        except Exception as e:
            return {
                "username": username,
                "risk_score": 5.0,
                "is_suspicious": False,
                "risk_level": "Medium",
                "indicators": [f"AI error: {type(e).__name__}"],
                "explanation": f"Could not complete AI analysis: {str(e)}",
                "total_accounts": len(found_sites)
            }
    
    def find_highest_risk_platform(
        self, 
        username: str, 
        found_sites: List[Dict]
    ) -> Dict:
        """
        Determine which platform poses the highest risk
        
        Args:
            username: The username being analyzed
            found_sites: List of sites where the username was found
            
        Returns:
            Dict with highest risk platform and reasoning
        """
        if not found_sites:
            return {
                "platform": "None",
                "reason": "No accounts found",
                "risk_score": 0.0
            }
        
        platform_list = [site['site'] for site in found_sites[:30]]
        
        prompt = f"""You are a cybersecurity expert analyzing social media platforms for risk assessment.

**Username:** {username}
**Platforms Found:** {', '.join(platform_list)}

Identify which single platform poses the HIGHEST security risk for this user and explain why.

Consider:
- Platform security features
- Common use in scams/fraud
- Privacy concerns
- Potential for impersonation
- Platform's reputation for security issues

Respond with ONLY valid JSON (no markdown):
{{
  "platform": "<exact platform name from the list>",
  "reason": "specific reason why this platform is highest risk",
  "risk_score": <float 0-10 for this specific platform>
}}"""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a cybersecurity analyst. Respond ONLY with valid JSON."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.3,
                max_tokens=300
            )
            
            content = response.choices[0].message.content.strip()
            content = re.sub(r'^```json\s*', '', content, flags=re.MULTILINE)
            content = re.sub(r'^```\s*', '', content, flags=re.MULTILINE)
            content = re.sub(r'\s*```$', '', content, flags=re.MULTILINE)
            
            # Try to extract JSON object if there's extra text
            json_match = re.search(r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}', content, re.DOTALL)
            if json_match:
                content = json_match.group(0)
            
            return json.loads(content)
            
        except Exception as e:
            # Fallback to first platform
            return {
                "platform": found_sites[0]['site'] if found_sites else "Unknown",
                "reason": f"AI analysis unavailable: {str(e)}",
                "risk_score": 5.0
            }
    
    def generate_risk_report(
        self, 
        username: str, 
        found_sites: List[Dict],
        risk_analysis: Optional[Dict] = None
    ) -> str:
        """
        Generate a comprehensive risk assessment report
        
        Args:
            username: The username being analyzed
            found_sites: List of sites where the username was found
            risk_analysis: Optional pre-computed risk analysis
            
        Returns:
            Formatted risk report as string
        """
        if not risk_analysis:
            risk_analysis = self.analyze_account_suspicious(username, found_sites)
        
        platform_list = [site['site'] for site in found_sites[:20]]
        
        prompt = f"""You are a cybersecurity analyst writing a professional investigation report.

Create a comprehensive risk assessment report for:

**Username:** {username}
**Accounts Found:** {len(found_sites)}
**Platforms:** {', '.join(platform_list)}
**Risk Score:** {risk_analysis.get('risk_score', 'N/A')}/10
**Risk Level:** {risk_analysis.get('risk_level', 'Unknown')}

Generate a professional report with:
1. Executive Summary (2-3 sentences)
2. Key Findings (3-4 bullet points)
3. Platform Analysis (brief overview)
4. Risk Indicators (specific concerns)
5. Recommendations (2-3 actionable items)

Keep it concise and professional. Use clear formatting with sections."""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a professional cybersecurity analyst writing investigation reports."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.4,
                max_tokens=800
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            # Fallback to basic report
            report = f"""RISK ASSESSMENT REPORT
{'=' * 50}

Username: {username}
Date: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

EXECUTIVE SUMMARY
-----------------
Analysis of username '{username}' across {len(found_sites)} platforms.
Risk Score: {risk_analysis.get('risk_score', 'N/A')}/10
Risk Level: {risk_analysis.get('risk_level', 'Unknown')}

KEY FINDINGS
------------
• Total accounts found: {len(found_sites)}
• Risk assessment: {risk_analysis.get('risk_level', 'Unknown')}
• {risk_analysis.get('explanation', 'Analysis incomplete')}

RECOMMENDATIONS
---------------
• Monitor account activity across platforms
• Verify account authenticity
• Review security settings

Note: AI report generation encountered an error."""
            return report

