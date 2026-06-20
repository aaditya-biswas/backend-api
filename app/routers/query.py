"""
POST /query — Ask a natural-language question about an ingested repo.

INPUT: QueryRequest {repo_id, question, stream}
  - repo_id: UUID of the ingested repo
  - question: Natural language question (e.g., "How does authentication work?")
  - stream: Whether to stream the answer via SSE (default: true)

OUTPUT: Server-Sent Events (SSE) stream of answer tokens
  - Each event is a JSON chunk matching OpenAI's streaming format
  - Final event is "data: [DONE]"

FLOW:
  1. Call Person 2's /search endpoint to get relevant code chunks
  2. Assemble a prompt with the chunks as context + the user's question
  3. Call Person 1's /v1/chat/completions with stream=true
  4. Forward the SSE tokens directly to the client

RESOURCES TO LEARN:
- SSE (Server-Sent Events): https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events
- sse-starlette: https://github.com/sysid/sse-starlette
- RAG Pattern: https://www.youtube.com/results?search_query=rag+retrieval+augmented+generation+python
- YouTube: "Streaming Responses in FastAPI" - https://www.youtube.com/results?search_query=fastapi+streaming+response+sse
- YouTube: "Build a RAG System" - https://www.youtube.com/results?search_query=build+rag+system+python+fastapi
"""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import StreamingResponse

from app.database import get_db
from app.schemas import QueryRequest

router = APIRouter()


@router.post("")
async def query_repo(body: QueryRequest, db: AsyncSession = Depends(get_db)):
    """
    STUB: Ask a question about a repo and stream the answer.
    
    TODO:
    1. Validate that the repo exists and is in "ready" status
    2. Call Person 2's /search endpoint (httpx.AsyncClient)
       POST {INGESTION_SERVICE_URL}/search
       Body: {"repo_id": str(body.repo_id), "query": body.question, "top_k": 6}
    3. Assemble a token-budgeted prompt:
       System: "You are a code explanation assistant. Use the following code context..."
       User: [code chunks as context] + body.question
    4. Call Person 1's /v1/chat/completions (httpx.AsyncClient)
       POST {LLM_SERVICE_URL}/v1/chat/completions
       Body: {"messages": [...], "stream": true, "max_tokens": 512, "temperature": 0.2}
    5. Stream the response back as SSE
    """
    raise NotImplementedError("Implement POST /query")
