from crewai import Agent, Crew, Task, Process
from tasks import BlogPostTasks
from agents import BlogPostAgents
from datetime import datetime
import time
import re

# ask user for topic
topic = input("Enter blog topic: ").strip()

# ask user for the year to cover, if blank, current year will be used
year_input = input("Enter year (leave blank for current): ").strip()
if year_input:
    year = year_input
else:
    year = datetime.now().year


# ensuring a safe file name version for topic
safe_topic = re.sub(r'[^a-zA-Z0-9_-]', '_', topic)

# this is to avoid overwriting your last run
timestamp = datetime.now().strftime("%Y%m%d_%H%M")   

# instantiate the class
tasks = BlogPostTasks()
agents = BlogPostAgents()

# create agents
researcher_agent = agents.blog_post_researcher(topic)
writing_agent = agents.blog_post_writer(topic)

# First task: Research
research = tasks.research_task(researcher_agent, topic, year)

# Create crew for the first task with sequential process
crew1 = Crew(
    agents=[researcher_agent],
    tasks=[research],
    process=Process.sequential  
)

# Run the first crew
result1 = crew1.kickoff()

# Convert to string before saving
research_text = result1.output if hasattr(result1, 'output') else str(result1)

# Save the first result with the topic considered
research_filename = f"research_{safe_topic}_{timestamp}.txt" # pyright: ignore[reportUndefinedVariable]
with open(research_filename, "w", encoding="utf-8") as file:
    file.write(research_text)

print(f"[INFO] Research file saved as {research_filename}")

# wait before starting the next task
time.sleep(10)

# Second task: Writing, using saved research filename as context
writing = tasks.writing_task(writing_agent, topic, research_filename)

# Create crew for the second task
crew2 = Crew(
    agents=[writing_agent],
    tasks=[writing]   
)

# Run the second crew
result2 = crew2.kickoff()

# converting to string before saving
writing_text = str(result2.raw) if hasattr(result2, "raw") else str(result2)

# Save the final result
blog_filename = f"blogpost_{safe_topic}_{timestamp}.md" # type: ignore
with open(blog_filename, "w", encoding="utf-8") as file:
    file.write(writing_text)


print(f"[INFO] Blog post saved as {blog_filename}")
print("BlogPost creation completed")





