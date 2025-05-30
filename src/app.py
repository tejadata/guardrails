
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from pii.pii import analyze_and_mask_text
from toxicity.toxic_bert import detect_toxicity
app = FastAPI(
    title="LLM Guardrails Server",
    description="Request/Response Guard rails",
    version="1.0.0"
)


class ToxiRequest(BaseModel):
    content: str
    treshold: float = 0.5


class TransformRequest(BaseModel):
    content: str
    guardrails: List[str]
    custom_entities: Optional[List[Dict]] = None


@app.get("/api/v1/guardrails")
async def list_guardrails():
    """List all available guardrails and their capabilities."""
    return {"guardrails": 123}


@app.post("/api/v1/toxicity")
async def validate_content(request: ToxiRequest):
    """Validate content against specified guardrails."""
    result = detect_toxicity(request.content, request.treshold)
    return result


@app.post("/api/v1/mask_pii")
async def transform_content(request: TransformRequest):
    """Transform content using specified guardrails."""
    res = analyze_and_mask_text(
        request.content, request.guardrails, request.custom_entities)
    return res


@app.get("/health")
async def health_check():
    """Health check."""
    # Check if all registered guardrails are properly initialized

    return "success"
