import os
from crewai import Agent, Task, Crew, Process
from crewai_tools import SerperDevTool

from traceloop.sdk import Traceloop
from traceloop.sdk.decorators import workflow, task, agent
  
Traceloop.init(disable_batch=True, api_key="XXX")

os.environ["OPENAI_API_KEY"] = "XXX"
os.environ["SERPER_API_KEY"] = "XXXX" # serper.dev API key

# You can choose to use a local model through Ollama for example. See https://docs.crewai.com/how-to/LLM-Connections/ for more information.

# os.environ["OPENAI_API_BASE"] = 'http://localhost:11434/v1'
os.environ["OPENAI_MODEL_NAME"] ='gpt-3.5-turbo'  # Adjust based on available model
# os.environ["OPENAI_API_KEY"] ='sk-111111111111111111111111111111111111111111111111'

search_tool = SerperDevTool()

@agent(name="researcher")
def researcher ():
    return Agent(
    role='Senior Research Analyst',
    goal='Uncover cutting-edge developments in AI and data science',
    backstory="""You work at a leading tech think tank.
    Your expertise lies in identifying emerging trends.
    You have a knack for dissecting complex data and presenting actionable insights.""",
    verbose=False,
    allow_delegation=False,
    tools=[search_tool]
    )

@agent(name="writer")
def writer():
    return Agent(
    role='Tech Content Strategist',
    goal='Craft compelling content on tech advancements',
    backstory="""You are a renowned Content Strategist, known for your insightful and engaging articles.
    You transform complex concepts into compelling narratives.""",
    verbose=False,
    allow_delegation=False
    )

@agent(name="critic")
def critic():
    return Agent(
    role='Tech Critique',
    goal='Provide your review on the AI advancements in terms of their pros and cons',
    backstory="""You are a renowned Crtique who does a great job in indentifying the limitations of
    different advancements. Be sure to critque to the fullest""",
    verbose=False,
    allow_delegation=False
    )

@task(name="Analayst_Report")
def task1(agenttype):
    return Task(
    description="""Conduct a comprehensive analysis of the latest advancements in AI in 2024.
    Identify key trends, breakthrough technologies, and potential industry impacts.""",
    expected_output="Full analysis report in bullet points",
    agent=agenttype
    )

@task(name = "Content_Blog")
def task2(agenttype):
    return Task(
    description="""Using the insights provided, develop an engaging blog
    post that highlights the most significant AI advancements.
    Your post should be informative yet accessible, catering to a tech-savvy audience.
    Make it sound cool, avoid complex words so it doesn't sound like AI.""",
    expected_output="Full blog post of at least 4 paragraphs",
    agent=agenttype
    )

@task(name = "Critic")
def task3(agenttype):
    return Task(
    description="""Using the insights provided, provide feedback on why certain advancements
    have not been very great.Your post should be informative yet accessible, catering to a tech-savvy audience.
    Make it sound cool, avoid complex words so it doesn't sound like AI.""",
    expected_output="Full blog post of at least 2 paragraphs",
    agent=agenttype
    )

@workflow(name="CrewSetupI")
def crewsetup():
# Instantiate your crew with a sequential process
    r,w,c = researcher(),writer(),critic()
    crew = Crew(
	  agents=[r,w,c],
	  tasks=[task1(r),task2(w),task3(c)],
	  verbose=0, # You can set it to 1 or 2 to different logging levels
	)
    print("Crew object initialized")

	# Get your crew to work!
    result = crew.kickoff()
    print("######################")
    print(result)
crewsetup()