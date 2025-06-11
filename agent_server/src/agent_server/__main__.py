import threading
import os

import uvicorn

from a2a.server.apps import A2AStarletteApplication
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore
from a2a.types import (
    AgentCapabilities,
    AgentCard,
    AgentSkill,
)
from .agent_executor import (
    HelloWorldAgentExecutor,  # type: ignore[import-untyped]
)

from fastapi import FastAPI


application = FastAPI()
a2a_server_host = os.environ.get("A2A_SERVER_HOST", "localhost")

@application.get("/healthz")
def health_check():
    return {"status": "healthy"}

def main() -> None:
    """Run the A2A server with a sample agent and skill."""
    # --8<-- [start:AgentSkill]
    skill = AgentSkill(
        id='hello_world',
        name='Returns hello world',
        description='just returns hello world',
        tags=['hello world'],
        examples=['hi', 'hello world'],
    )
    # --8<-- [end:AgentSkill]

    extended_skill = AgentSkill(
        id='super_hello_world',
        name='Returns a SUPER Hello World',
        description='A more enthusiastic greeting, only for authenticated users.',
        tags=['hello world', 'super', 'extended'],
        examples=['super hi', 'give me a super hello'],
    )

    # --8<-- [start:AgentCard]
    # This will be the public-facing agent card
    public_agent_card = AgentCard(
        name='Hello World Agent',
        description='Just a hello world agent',
        url=f'http://{a2a_server_host}:8080/',
        version='1.0.0',
        defaultInputModes=['text'],
        defaultOutputModes=['text'],
        capabilities=AgentCapabilities(streaming=True),
        skills=[skill],  # Only the basic skill for the public card
        supportsAuthenticatedExtendedCard=True,
    )
    # --8<-- [end:AgentCard]

    # This will be the authenticated extended agent card
    # It includes the additional 'extended_skill'
    specific_extended_agent_card = public_agent_card.model_copy(
        update={
            'name': 'Hello World Agent - Extended Edition',  # Different name for clarity
            'description': 'The full-featured hello world agent for authenticated users.',
            'version': '1.0.1',  # Could even be a different version
            # Capabilities and other fields like url, defaultInputModes, defaultOutputModes,
            # supportsAuthenticatedExtendedCard are inherited from public_agent_card unless specified here.
            'skills': [
                skill,
                extended_skill,
            ],  # Both skills for the extended card
        }
    )

    request_handler = DefaultRequestHandler(
        agent_executor=HelloWorldAgentExecutor(),
        task_store=InMemoryTaskStore(),
    )

    server = A2AStarletteApplication(
        agent_card=public_agent_card,
        http_handler=request_handler,
        extended_agent_card=specific_extended_agent_card,
    )

    def run_uvicorn(app, host, port):
        uvicorn.run(app, host=host, port=port)

    # Start FastAPI health check endpoint on a different port (e.g., 8081)
    threading.Thread(
        target=run_uvicorn,
        args=(application, a2a_server_host, 8081),
        daemon=True
    ).start()

    # Start the A2A server on the main thread (port 8080)
    uvicorn.run(server.build(), host=a2a_server_host, port=8080)

if __name__ == '__main__':
    main()