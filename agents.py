from textwrap import dedent
from crewai import Agent, LLM
from tools import Search_tool, Read_tool
from dotenv import load_dotenv

import os

load_dotenv()

llm = LLM(
    model="gemini/gemini-2.0-flash-lite",  
    temperature =0.7,  
    provider = "Google",   
    stream=True,
    api_key = os.getenv("Gemini_API_Key")
)

class BlogPostAgents:
    def blog_post_researcher(self, topic):
       return Agent(
          role = "Senior Blog Post Researcher",
          goal = f"Uncover cutting-edge developments in {topic}",
          tools = [Search_tool],
          backstory = dedent(f"""
                You're a seasoned researcher with a knack for uncovering the latest
                developments in {topic}. Known for your ability to find the most relevant
                information and present it in a clear and concise manner.
          """),
          verbose = True,
          memory = True,
          llm = llm
       )  
    
    def blog_post_writer(self, topic):
        return Agent(
            role = "Blog Post Writer",
            goal = f"Create captivating contents based on researches done on {topic}",
            tools = [Read_tool],
            backstory = dedent(f"""
                You're a skilled content creator who creates engaging and well structured blog content on {topic}. 
                You're known for your ability to turn information into captivating blog post, ensuring polished grammar 
                and making contents enjoyable while reading
            """),
            verbose = True,
            memory = True,
            llm = llm
        )
    

  
  
  