from crewai import Agent, Task, Crew, Process
from agents import TenderGrantFinder_agents
from tasks import TenderGrantFinder_tasks
from tools import TenderGrantFinder_tools
from crewai import LLM
from dotenv import load_dotenv
import json, csv

import os
load_dotenv()

# llm instance
llm = LLM(
    model = "gemini/gemini-2.0-flash-lite",
    temperature = 0.3,
    api_key=os.getenv("GEMINI_API_KEY"),
    stream = True
    )

# prompt user for keywords, sector, location and contact details
keywords = input("enter what you are looking for: ").strip()
sector = input("what sector are you in: ").strip()
location = input("can you supply your location pls: ").strip()
contact_details = input("enter your phone or email for notifications: ").strip()

# instantiate the class
tools = TenderGrantFinder_tools()

agents = TenderGrantFinder_agents(
    llm=llm,
    research_tool=tools.get_research_tools(),
    extract_tool=tools.get_extract_tools()    
)

tasks = TenderGrantFinder_tasks()

# create the agents
researcher = agents.researcher(keywords, sector, location)
extractor = agents.extractor_agent()
classifier = agents.classifier_agent()
notifier = agents.notifier_agent()


# Search
print("\n=== Step 1: Running search task ===")
search_task = tasks.search_task(researcher, keywords, sector, location)
search_crew = Crew(
    agents=[researcher],
    tasks=[search_task],
    process=Process.sequential
)

search_result = search_crew.kickoff()
if isinstance(search_result, str):
    try:
        search_result = json.loads(search_result)
    except:
        search_result = [search_result]  # fallback

print("Search Result:", search_result.raw)

# Extract
print("\n=== Step 2: Running extraction task ===")
extract_task = tasks.extract_task(extractor, search_result.raw)
extract_crew = Crew(
    agents=[extractor],
    tasks=[extract_task],
    process=Process.sequential
)

extract_result = extract_crew.kickoff()
try:
    extract_result = json.loads(extract_result) if isinstance(extract_result, str) else extract_result
except:
     extract_result = [extract_result]

print("Extract Result:", extract_result.raw)

# Classify
print("\n=== Step 3: Running classification task ===")
classify_task = tasks.classify_task(classifier, extract_result.raw)
classify_crew = Crew(
    agents=[classifier],
    tasks=[classify_task],
    process=Process.sequential
)

classify_result = classify_crew.kickoff()
print("Classify Result:", classify_result)

# parse result
try:
    classified_data = json.loads(classify_result.raw)
except json.JSONDecodeError:
    print ("Could not decode JSON, saving raw text instead")
    classified_data = [{"raw_output": classify_result.raw}]


# save csv
with open("classified_results.csv", "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=classified_data[0].keys())
        writer.writeheader()
        writer.writerows(classified_data)


# Notify
print("\n=== Step 4: Running notifier task ===")
notify_task = tasks.notifier_task(notifier, classified_data, contact_details)
notify_crew = Crew(
    agents=[notifier],
    tasks=[notify_task]
)

notify_result = notify_crew.kickoff()
print("Notify Result:", notify_result.raw)


print("\n=== All steps completed successfully ===")
