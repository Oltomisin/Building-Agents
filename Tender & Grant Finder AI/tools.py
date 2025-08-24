from crewai_tools import SerperDevTool, ScrapeWebsiteTool, ScrapeElementFromWebsiteTool, FileReadTool
from dotenv import load_dotenv

import os
load_dotenv()

class TenderGrantFinder_tools:
    def __init__(self):
        self.serper_api_key = os.getenv("SERPER_API_KEY")
        if not self.serper_api_key:
            raise ValueError("SERPER_API_KEY not found in environment variables.")
        
        # Initializing my tools 

        # google search tool for related opportunities
        self.search_tool = SerperDevTool(
        api_key = self.serper_api_key
        )

        # ScrapeElementFromWebsiteTool for getting all links from pages
        self.link_scraper_tool = ScrapeElementFromWebsiteTool(
            selectors = {"links": "a"},
            multiple = True
        )

        # extraction tool to get structured opportunity fields
        self.scraper_tool = ScrapeElementFromWebsiteTool(
            selectors={
                "title": ".tender-title",  
                "deadline": ".deadline-date",
                "eligibility": ".eligibility-section p",
                "funding_amount": ".funding-amount"
            },
        multiple=True  # To grab multiple tenders per page
        )

        # full page scraper (fallback if selectors fail)
        self.page_scarper_tool = ScrapeWebsiteTool()

        # to read saved files
        self.read_tool = FileReadTool()
     
     # Research phase tools (search + get links)
    def get_research_tools(self):
        return [self.search_tool, self.scraper_tool]
    
    # Extraction phase tools (extract structured data)
    def get_extract_tools(self):
        return [self.scraper_tool, self.page_scarper_tool]
    