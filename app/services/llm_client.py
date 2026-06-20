"""
HTTP client for Person 1's LLM Service.

INPUT: messages (list of {role, content}), stream (bool), max_tokens, temperature.
OUTPUT: Streaming response from Person 1's /v1/chat/completions endpoint.

FLOW:
  1. Build request body matching OpenAI Chat Completions format
  2. Send POST to {LLM_SERVICE_URL}/v1/chat/completions
  3. If streaming: yield SSE tokens as they arrive
  4. If not streaming: return complete response

RESOURCES TO LEARN:
- OpenAI Chat Completions API: https://platform.openai.com/docs/api-reference/chat
- httpx Streaming: https://www.python-httpx.org/advanced/#streaming-responses
- YouTube: "Consuming Streaming APIs with httpx" - https://www.youtube.com/results?search_query=python+httpx+streaming+response
"""

from app.config import settings


async def query_llm(messages: list, stream: bool = True, max_tokens: int = 512, temperature: float = 0.2):
    """
    STUB: Call Person 1's LLM service.
    
    INPUT: messages = [{"role": "system", "content": "..."}, {"role": "user", "content": "..."}]
    OUTPUT: Async generator yielding SSE tokens or complete response dict.
    
    TODO:
    1. Build request body:
       {
         "messages": messages,
         "stream": stream,
         "max_tokens": max_tokens,
         "temperature": temperature
       }
    2. Use httpx.AsyncClient to POST to {settings.LLM_SERVICE_URL}/v1/chat/completions
    3. If stream=True: iterate over response.aiter_lines(), yield each SSE data line
    4. If stream=False: return response.json()
    """
    raise NotImplementedError("Implement query_llm client")


async def build_prompt(code_chunks: list, question: str) -> list:
    """
    STUB: Assemble a token-budgeted prompt from code chunks + user question.
    
    INPUT: code_chunks from Person 2's search, user's question.
    OUTPUT: messages list ready for LLM API.
    
    TODO:
    1. System message: "You are a code explanation assistant..."
    2. Concatenate code chunks into context (respecting token budget ~4000 tokens)
    3. User message: context + question
    4. Return [system_msg, user_msg]
    """
    raise NotImplementedError("Implement build_prompt")
