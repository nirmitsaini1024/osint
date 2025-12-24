"""
FastAPI wrapper for Sherlock - Social Media Username Search
"""
import os
import sys
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict

# Add the parent directory to the path to import sherlock_project
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

from sherlock_project.sherlock import sherlock
from sherlock_project.sites import SitesInformation
from sherlock_project.notify import QueryNotify
from sherlock_project.result import QueryStatus, QueryResult

app = FastAPI(title="Sherlock API", version="1.0.0")

# Enable CORS for Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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


@app.get("/")
async def root():
    return {"message": "Sherlock API - Social Media Username Search", "version": "1.0.0"}


@app.get("/health")
async def health():
    return {"status": "healthy"}


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


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

