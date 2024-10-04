from agents.base_agent import Agent

class ImplementationAgent(Agent):
    """
    Subclass of Agent with an implementation prompt, responsible for implementing 
    the web page by following the milestones specified in plan.md file in the artifacts section.
    """

    IMPLEMENTATION_PROMPT = """
    You are a software developer, and your task is to look at the plan.md file in the \
    artifacts section below, and implement the first uncompleted milestone in HTML and CSS.

    Output the updated HTML and CSS files as index.html and style.css respectively, \
    using your tools to update the files.

    When the milestone is completed, check it off the milestones list in the plan.md file, \
    and use your tools to update the file.
    """

    def __init__(self, name, client, prompt=IMPLEMENTATION_PROMPT, gen_kwargs=None):
        super().__init__(name, client, prompt, gen_kwargs)

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
