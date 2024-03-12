import os
from crewai import Agent, Task, Crew, Process
from crewai_tools import SerperDevTool

from traceloop.sdk import Traceloop
from traceloop.sdk.decorators import workflow, task
  
Traceloop.init(disable_batch=True, api_key="YOUR_KEY")

os.environ["OPENAI_API_KEY"] = "YOUR_KEY"
os.environ["SERPER_API_KEY"] = "YOUR_KEY" # serper.dev API key

# You can choose to use a local model through Ollama for example. See https://docs.crewai.com/how-to/LLM-Connections/ for more information.

# os.environ["OPENAI_API_BASE"] = 'http://localhost:11434/v1'
os.environ["OPENAI_MODEL_NAME"] ='gpt-3.5-turbo'  # Adjust based on available model
# os.environ["OPENAI_API_KEY"] ='sk-111111111111111111111111111111111111111111111111'

search_tool = SerperDevTool()

# Define your agents with roles and goals
researcher = Agent(
  role='Senior Research Analyst',
  goal='Uncover cutting-edge developments in AI and data science',
  backstory="""You work at a leading tech think tank.
  Your expertise lies in identifying emerging trends.
  You have a knack for dissecting complex data and presenting actionable insights.""",
  verbose=False,
  allow_delegation=False,
  tools=[search_tool]
)
writer = Agent(
  role='Tech Content Strategist',
  goal='Craft compelling content on tech advancements',
  backstory="""You are a renowned Content Strategist, known for your insightful and engaging articles.
  You transform complex concepts into compelling narratives.""",
  verbose=False,
  allow_delegation=False
)

critic = Agent(
  role='Tech Critique',
  goal='Provide your review on the AI advancements in terms of their pros and cons',
  backstory="""You are a renowned Crtique who does a great job in indentifying the limitations of
  different advancements. Be sure to critque to the fullest""",
  verbose=False,
  allow_delegation=False
)

# Create tasks for your agents
task1 = Task(
  description="""Conduct a comprehensive analysis of the latest advancements in AI in 2024.
  Identify key trends, breakthrough technologies, and potential industry impacts.""",
  expected_output="Full analysis report in bullet points",
  agent=researcher
)

task2 = Task(
  description="""Using the insights provided, develop an engaging blog
  post that highlights the most significant AI advancements.
  Your post should be informative yet accessible, catering to a tech-savvy audience.
  Make it sound cool, avoid complex words so it doesn't sound like AI.""",
  expected_output="Full blog post of at least 4 paragraphs",
  agent=writer
)


task3 = Task(
  description="""Using the insights provided, provide feedback on why certain advancements
  have not been very great.Your post should be informative yet accessible, catering to a tech-savvy audience.
  Make it sound cool, avoid complex words so it doesn't sound like AI.""",
  expected_output="Full blog post of at least 2 paragraphs",
  agent=critic
)

@workflow(name="CrewSetupI")
def crewsetup():
# Instantiate your crew with a sequential process
	crew = Crew(
	  agents=[researcher,writer,critic],
	  tasks=[task1,task2,task3],
	  verbose=0, # You can set it to 1 or 2 to different logging levels
	)
	print("Crew object initialized")

	# Get your crew to work!
	result = crew.kickoff()

	print("######################")
	print(result)
crewsetup()