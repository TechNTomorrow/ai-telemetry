import asyncio, os
from langfuse import get_client

import openlit

from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.function_choice_behavior import FunctionChoiceBehavior
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
from semantic_kernel.connectors.ai.prompt_execution_settings import PromptExecutionSettings
from semantic_kernel.functions.kernel_arguments import KernelArguments
from semantic_kernel.functions.kernel_function_decorator import kernel_function

from dotenv import load_dotenv
load_dotenv()

langfuse = get_client()
 
# Verify connection
if langfuse.auth_check():
    print("Langfuse client is authenticated and ready!")
else:
    print("Authentication failed. Please check your credentials and host.")


# Initialize OpenLIT instrumentation. The disable_batch flag is set to true to process traces immediately. 
# Also set the langfuse tracer to use the langfuse tracer.
openlit.init(tracer=langfuse._otel_tracer, disable_batch=True)

class BookingPlugin:
    @kernel_function(
        name="find_available_rooms",
        description="Find available conference rooms for today.",
    )
    def find_available_rooms(self,) -> list[str]:
        return ["Room 101", "Room 201", "Room 301"]

    @kernel_function(
        name="book_room",
        description="Book a conference room.",
    )
    def book_room(self, room: str) -> str:
        return f"Room {room} booked."


async def main():
    # Create a kernel and add a service
    kernel = Kernel()
    service_id = "azure_openai"
    kernel.add_service(AzureChatCompletion(service_id=service_id, 
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            deployment_name=os.getenv("AZURE_OPENAI_CHAT_COMPLETION_MODEL"),
            endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
            ))
    kernel.add_plugin(BookingPlugin(), "BookingPlugin")

    answer = await kernel.invoke_prompt(
        "Reserve a conference room for me today.",
        arguments=KernelArguments(
            settings=PromptExecutionSettings(
                function_choice_behavior=FunctionChoiceBehavior.Auto(),
            ),
        ),
    )
    print(answer)

if __name__ == "__main__":
    asyncio.run(main())