import os
import chainlit as cl
import json

class Agent:
    """
    Base class for all agents.
    """

    tools = [
        {
            "type": "function",
            "function": {
                "name": "updateArtifact",
                "description": "Update an artifact file which is HTML, CSS, or markdown with the given contents.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "filename": {
                            "type": "string",
                            "description": "The name of the file to update.",
                        },
                        "contents": {
                            "type": "string",
                            "description": "The markdown, HTML, or CSS contents to write to the file.",
                        },
                    },
                    "required": ["filename", "contents"],
                    "additionalProperties": False,
                },
            }
        },
        {
            "type": "function",
            "function": {
                "name": "callAgent",
                "description": "Calls another agent as specified by the agentName parameter.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "agentName": {
                            "type": "string",
                            "description": "The name of the agent to call, such as 'implementation'.",
                        },
                    },
                    "required": ["agentName"],
                    "additionalProperties": False,
                },
            }
        }
    ]

    def __init__(self, name, client, prompt="", gen_kwargs=None):
        self.name = name
        self.client = client
        self.prompt = prompt
        self.gen_kwargs = gen_kwargs or {
            "model": "gpt-4o-mini",
            "temperature": 0.2
        }

    async def execute(self, message_history):
        """
        Executes the agent's main functionality.

        Note: probably shouldn't couple this with chainlit, but this is just a prototype.
        """

        # We want to preserve the message history, but use the system prompt from the agent.
        copied_message_history = message_history.copy()

        # Check if the first message is a system prompt
        if copied_message_history and copied_message_history[0]["role"] == "system":
            # Replace the system prompt with the agent's prompt
            copied_message_history[0] = {"role": "system", "content": self._build_system_prompt()}
        else:
            # Insert the agent's prompt at the beginning
            copied_message_history.insert(0, {"role": "system", "content": self._build_system_prompt()})

        response_message = cl.Message(content="")
        await response_message.send()

        stream = await self.client.chat.completions.create(messages=copied_message_history, stream=True, tools=self.tools, tool_choice="auto", **self.gen_kwargs)
            
        functions_called = {} # dictionary in the form of {index: {function_name: arguments}}
        async for part in stream:
            if part.choices[0].delta.tool_calls:
                tool_call = part.choices[0].delta.tool_calls[0]

                tool_call_index = tool_call.index
                function_name_delta = tool_call.function.name or ""
                arguments_delta = tool_call.function.arguments or ""
                function_name = functions_called.get(tool_call_index, {}).get("function_name", "")
                arguments = functions_called.get(tool_call_index, {}).get("arguments", "")
                function_name += function_name_delta
                arguments += arguments_delta

                functions_called.update({
                    tool_call_index: {
                        "function_name": function_name,
                        "arguments": arguments
                    }
                })
        
            if token := part.choices[0].delta.content or "":
                await response_message.stream_token(token)        

        print("DEBUG: functions_called:", functions_called)

        if functions_called:
            for tool_call_index, tool_call_info in functions_called.items():
                function_name = tool_call_info.get("function_name", "")
                arguments = tool_call_info.get("arguments", "")

                if function_name == "updateArtifact":
                    print("DEBUG: updating artifact")
                    arguments_dict = json.loads(arguments)
                    filename = arguments_dict.get("filename")
                    contents = arguments_dict.get("contents")

                    if filename and contents:
                        os.makedirs("artifacts", exist_ok=True)
                        with open(os.path.join("artifacts", filename), "w") as file:
                            file.write(contents)
                    
                        # Add a message to the message history
                        message_history.append({
                            "role": "system",
                            "content": f"The artifact '{filename}' was updated."
                        })

                        stream = await self.client.chat.completions.create(messages=message_history, stream=True, **self.gen_kwargs)
                        async for part in stream:
                            if token := part.choices[0].delta.content or "":
                                await response_message.stream_token(token)

                elif function_name == "callAgent":
                    print("DEBUG: calling agent")
                    arguments_dict = json.loads(arguments)
                    agent_name = arguments_dict.get("agentName")
                    print("DEBUG: agent_name:", agent_name)

                    if agent_name == "implementation":
                        print("DEBUG: calling implementation agent")

                        from agents.implementation_agent import ImplementationAgent

                        implementation_agent = ImplementationAgent(name="Implementation Agent", client=self.client)
                        await implementation_agent.execute(message_history)

                        # Add a message to the message history
                        message_history.append({
                            "role": "system",
                            "content": "The implementation agent has finished."
                        })

                        print("DEBUG: The implementation agent has finished.")

        else:
            print("No tool call")

        await response_message.update()

        return response_message.content

    def _build_system_prompt(self):
        """
        Builds the system prompt including the agent's prompt and the contents of the artifacts folder.
        """
        artifacts_content = "<ARTIFACTS>\n"
        artifacts_dir = "artifacts"

        if os.path.exists(artifacts_dir) and os.path.isdir(artifacts_dir):
            for filename in os.listdir(artifacts_dir):
                if filename != '.DS_Store': # Ignore .DS_Store file
                    file_path = os.path.join(artifacts_dir, filename)
                    if os.path.isfile(file_path):
                        with open(file_path, "r") as file:
                            file_content = file.read()
                            artifacts_content += f"<FILE name='{filename}'>\n{file_content}\n</FILE>\n"

        artifacts_content += "</ARTIFACTS>"

        return f"{self.prompt}\n{artifacts_content}"