from crewai import Agent
from crewai_tools import SerperDevTool, FileReadTool


Search_tool = SerperDevTool()
Read_tool = FileReadTool()