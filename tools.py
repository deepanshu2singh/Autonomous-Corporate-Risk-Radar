import os
from firecrawl import FirecrawlApp
from langchain.tools import tool

# --- STEP A: PASTE YOUR KEY HERE ---
os.environ["FIRECRAWL_API_KEY"] = "paste you FIRECRAWL_API_KEY here"

# Add this new import at the very top of your file
from langchain_community.tools.tavily_search import TavilySearchResults

# ... [Your existing Firecrawl code stays exactly the same] ...

# --- NEW: SET UP THE TAVILY SEARCH ENGINE ---
os.environ["TAVILY_API_KEY"] = "pate your tavily API key here"

# Initialize the search tool. We set max_results=3 so the AI gets highly focused answers.
search_tool = TavilySearchResults(max_results=3)

# Initialize the scraper
app = FirecrawlApp(api_key=os.environ.get("Your FIRECRAWL_API_KEY Here"))

@tool
def scrape_uk_financial_data(url: str) -> str:
    """
    Scrapes a specific URL and returns the content in clean Markdown format.
    Use this for: Bank of England policy summaries, major bank press releases.
    """
    print(f"\n[Agent is working... Reading: {url}]\n")
    
    try:
        # UPDATED: The newest version uses '.scrape' instead of '.scrape_url'
        scrape_result = app.scrape(url, formats=['markdown'])
        
        # UPDATED: Safely pull the markdown out of the new result format
        if isinstance(scrape_result, dict):
            content = scrape_result.get('markdown', 'No content found.')
        else:
            content = getattr(scrape_result, 'markdown', 'No content found.')
            
        return content[:15000] # Limit to 15,000 characters
        
    except Exception as e:
        return f"Failed to scrape the source. Error: {str(e)}"

# --- STEP B: THE TEST RUN ---
if __name__ == "__main__":
    print("Starting test...")
    test_url = "https://www.bankofengland.co.uk/monetary-policy-summary-and-minutes/2026/may-2026"
    
    # Run the tool
    result = scrape_uk_financial_data.invoke({"url": test_url})
    
    # We check if the word 'Failed' is in the result to know if it actually worked
    if "Failed to scrape" in result:
        print("\n--- TEST FAILED ---")
        print(result)
        print("-------------------")
    else:
        print("\n--- TEST RESULT (SUCCESS) ---")
        print(result[:500]) 
        print("\n-----------------------------")
        print("YOUR TOOL IS FULLY WORKING!")