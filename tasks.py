from textwrap import dedent
from crewai import Task


class BlogPostTasks:
   def research_task(self, agent, topic, year):
     return Task (
       description = dedent(f"""\
          Conduct a thorough and indepth research on {topic} 
          Your goal is to gather:
          - Latest developments, trends and facts 
          - Make sure you find any interesting and relevant information given
    
          Keep in mind attention to detail is crucial, ensure the research is accurate and well-structured
          so it can feed into the blog writing process.
    
          Summarize your findings in a clear and concise manner, possibly 5 bulleted points with detailed summary
          The current year is {year}.
        """),
        agent = agent,
        expected_output= f"5 detailed bullet points summarizing key findings on {topic}."
    )
   
   
   def writing_task(self, agent, topic, research_file):
    return Task(
      description=dedent(f"""\
          Use the FileReadTool to open and read the content from the file located at: {research_file}. 

          Review and expand the research findings into a well-written, engaging blog post section on the {topic}.
          Expand these bullets point into a well written, engaging blog post section.
    
          Write exactly five full paragraphs, ensuring the content: 
          - covers the most relevant information from the research
          - maintains accuracy and logical flow

          The blogpost  should be formatted in Markdown without '```'
          The tone should be clear, professional, and engaging for the intended audience
      """), 
      agent = agent,
      context = [],
      expected_output= "A Five-paragraph blog post in Markdown format, based on the research findings."
  ) 
  

