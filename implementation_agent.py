from agents.base_agent import Agent

class ImplementationAgent(Agent):
    """
    Agent responsible for implementing the web page based on the plan.
    """

    def __init__(self, name, client, prompt="", gen_kwargs=None):
        super().__init__(name, client, prompt, gen_kwargs)
        self.prompt = """
You are a skilled web developer tasked with implementing the web page according to the plan provided in plan.md.
Your role is to write HTML and CSS code to create the web page as described in the plan.
Follow the milestones outlined in the plan, and implement each section carefully.
Use semantic HTML5 elements where appropriate and write clean, well-structured CSS.
Ensure that your implementation matches the layout and design described in the plan.
If you need clarification on any part of the plan, ask for it before proceeding with the implementation.

You need to generate index.html and style.css files and use the updateArtifact tool to save them in the artifacts folder.
"""

    async def execute(self, message_history):
        """
        Executes the implementation agent's functionality.
        This method should be called to start the implementation process.
        """
        return await super().execute(message_history)

    def _build_system_prompt(self):
        """
        Builds the system prompt including the agent's prompt and the contents of the artifacts folder.
        """
        return super()._build_system_prompt()




from agents.base_agent import Agent

class ImplementationAgent(Agent):
    """
    Subclass of Agent with an implementation prompt.
    """

    IMPLEMENTATION_PROMPT = """
    You are a software developer, and your task is to look at the plan.md file in the \
    artifacts section below, and implement the first uncompleted milestone in HTML and CSS.

    Output the updated HTML and CSS files as index.html and style.css respectively, \
    using your tools to update the files.
    """

    def __init__(self, name, client, prompt=IMPLEMENTATION_PROMPT, gen_kwargs=None):
        super().__init__(name, client, prompt, gen_kwargs)