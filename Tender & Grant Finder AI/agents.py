from textwrap import dedent
from crewai import Agent
from crewai.tools import BaseTool


class NotifierTools(BaseTool):
    """ simple notifier that formats report and optionally prints/sends it"""
    
    name: str = "Simple Notifier" 
    description: str = "print/send csv or text notifications to email and phone"
  

    def _run(self, contact_details:str, csv_content: str) -> str:
        return f"notifcation sent to {contact_details} with CSV content of length {len(csv_content)}"

class TenderGrantFinder_agents:
    def __init__(self, llm, research_tool=[], extract_tool=[], classify_tool=[], notify_tool=[]):
        self.llm = llm
        self.research_tool = research_tool
        self.extract_tool = extract_tool
        self.classify_tool = classify_tool
        self.notify_tool = notify_tool


    def researcher(self, keywords, sector, location):
        return Agent(
            role = "Tender and Grant Researcher",
            goal = dedent(f"""\
                Conduct indepth research on Tender and Grant openings 
                using the keywords: {keywords}, sector: {sector} and location: {location},
                use the search tool to find relevant opportunities and the link scraper tool
                to return a clean list of opportunity URLs.
                """),
            verbose = True,
            memory = True,
            backstory = dedent(f"""\
                You are an experienced researcher who excels at uncovering and gathering
                the most relevant opportunties from reliable sources.
                """),            
            llm = self.llm,
            tools = self.research_tool
    )

    def extractor_agent(self):
        return Agent(
            role = "Data Extractor",
            goal = dedent(f"""\
                Extract the most relevant details such as title, deadlines, eligibility, and funding amount
                for each page, return the title, deadline, eligiblity, and funding amount
                in a structured format.
                """),    
            verbose = True,
            memory = True,
            backstory ="You are meticulous at uncovering and presenting structured opportunity data.",
            llm = self.llm,
            tools = self.extract_tool
        )

    def classifier_agent(self):
        return Agent(
            role = "Opportunity Classifier",
            goal = "Categorize extracted Tender/Grant opportunities into their respective sector",
            verbose = True,
            memory = True,
            backstory = dedent(f"""\
                You are a meticulous and perceptive classifier,
                trained to identify and discover patterns with precision and clarity.
                You are known for your unbiased decision-making and structured categorization.
                """),
            llm = self.llm      
        )
            
    
    def notifier_agent(self):
        return Agent(
            role = "Report notifier",
            goal = "Turn categorized dataset into CSV summaries and notify users via email or phone",
            verbose = True,
            memory = True,
            backstory = "You are meticulous at formatting data and notifying users.",
            llm = self.llm,
            tools = [NotifierTools()]     
        )