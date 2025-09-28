from google.adk.agents import Agent

# Define the agent by instantiating the Agent class directly.
# A simple greeter doesn't need a tool; the instruction is enough
# for the Gemini model to know how to behave.
root_agent = Agent(
    name="greeter_agent",
    model="gemini-2.0-flash",
    description="A simple agent that greets the user.",
    instruction="""
    You are a friendly and helpful AI Meeting Assistant.
    Your only job right now is to greet the user warmly and introduce yourself.
    Keep your greeting concise.
    """
)

# This block runs the agent when you execute the python script.
if __name__ == "__main__":
    run_in_terminal(root_agent)

