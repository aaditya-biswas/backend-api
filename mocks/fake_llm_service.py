"""
Mock LLM Service — matches Person 1's contract exactly.

Run this on a separate port (e.g., 8001) so Person 3 can develop
the full orchestration logic before Person 1's real service is ready.

INPUT: POST /v1/chat/completions with OpenAI-compatible request body.
OUTPUT: SSE stream of canned tokens (placeholder response).

USAGE:
  uvicorn mocks.fake_llm_service:app --port 8001

RESOURCES TO LEARN:
- FastAPI StreamingResponse: https://fastapi.tiangolo.com/advanced/custom-response/#streamingresponse
- OpenAI Streaming Format: https://platform.openai.com/docs/api-reference/chat/streaming
"""

import json
import asyncio
from fastapi import FastAPI
from fastapi.responses import StreamingResponse

app = FastAPI(title="Fake LLM Service")


@app.post("/v1/chat/completions")
async def fake_completion(body: dict):
    async def fake_stream():
        words = "This is a placeholder response from the LLM service. Replace with Person 1's real model.".split()
        for word in words:
            chunk = {
                "choices": [{"delta": {"content": word + " "}, "index": 0}]
            }
            yield f"data: {json.dumps(chunk)}\n\n"
            await asyncio.sleep(0.05)
        yield "data: [DONE]\n\n"

    return StreamingResponse(fake_stream(), media_type="text/event-stream")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
