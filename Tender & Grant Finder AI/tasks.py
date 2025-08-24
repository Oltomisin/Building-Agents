from textwrap import dedent
from crewai import Task


class TenderGrantFinder_tasks:
    def search_task(self, agent, keywords, sector, location):
        return Task(
            description = dedent(f"""\
                Conduct a thorough, indepth and extensive search for opportunities 
                related to {keywords}, sector: {sector} and location: {location}.

                Focus on finding current and ongoing 
                - tenders, 
                - grants,
                - competitions,
                - funding opportunities
                
                Return only a structured lists of URLs with a short description of each.
                """),
            agent = agent,
            expected_output = "A JSON list of dicts: [{{'title': str, 'url': str, 'summary': str}}]"
        )
    
    def extract_task(self, agent, search_results):
        return Task(
            description = dedent(f"""\
                Visit each of the provided URLs and extract structured data fields:
                    - Title
                    - Deadline
                    - Eligibility
                    - Funding Amount

                Summarize the opportunity in 2-3 sentences.
                
                Ensure the result is structured and clean, ready for downstream use.
                """),
            agent = agent,
            context = [],
            expected_output = "A JSON list of dicts: [{{'title': str, 'deadline': str, 'eligibility': str, 'funding_amount': str, 'summary': str, 'url': str}}]"         
        )
    
    def classify_task(self, agent, extracted_data):
         return Task(
             description = dedent(f"""\
                Categorize the provided opportunities into their respective sectors.
                
                For each opportunity, enrich the record with:
                - sector (determined from keywords and context)
                                  
                Ensure clarity, accuracy, and unbiased classification.                                   
                """),
             agent = agent,
             context = [],
             expected_output = "A JSON list of dicts: [{{'title': str, 'deadline': str, 'eligibility': str, 'funding_amount': str, 'summary': str, 'url': str}}]"
        )

    def notifier_task(self, agent, classified_data, contact_details):
        return Task(
            description = dedent(f"""\
                Convert the provided opportunities into a clean CSV string
                                 
                Ensure it contains headers:
                title, deadline, eligibility, funding_amount, sector, summary, url
                
                Then prepare it to be sent to the user at: {contact_details}.                               
                """),
            agent = agent,
            context = [],
            expected_output = "A CSV formatted string ready for sending."
        )