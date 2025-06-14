import os
import asyncio
import threading
from uuid import uuid4
from fastapi import FastAPI, Query
from pydantic import BaseModel
from typing import List, Dict, Any, Optional, Literal

from pii.pii import analyze_and_mask_text
from toxicity.toxic_bert import detect_toxicity
from prompt_secure.prompt_break import classify_prompt_injection
from log_guardrails.log_anomaly import AnomalyStorage
from get_reports import generate_anomaly_report

app = FastAPI(
    title="LLM Guardrails Server",
    description="Request/Response Guard rails",
    version="1.0.0"
)

# === Request Models ===

class ToxiRequest(BaseModel):
    content: str
    treshold: float = 0.5


class Prompt(BaseModel):
    content: str


class TransformRequest(BaseModel):
    content: str
    guardrails: List[str]
    treshold: float = 0.5
    custom_entities: Optional[List[Dict]] = None
    action: Optional[Literal["mask", "block"]] = None
    compitator_loc: Optional[str] = None
    block_loc: Optional[str] = None


class Compitator(BaseModel):
    content: str
    action: Literal["mask", "block"]
    compitator_loc: Optional[str] = None
    block_loc: Optional[str] = None


# === Guardrails Client ===

class GuardrailsClient:
    def __init__(self):
        enable_logging_env = os.getenv("ENABLE_LOGGING", "false").lower()
        self.enable_logging = enable_logging_env in ["true", "1", "yes"]
        self.dsn = os.getenv("ANOMALY_DB_DSN")

        self.logger: Optional[AnomalyStorage] = None

        if self.enable_logging and self.dsn:
            self.logger = AnomalyStorage(dsn=self.dsn)
            self.logger.init()
        elif self.enable_logging:
            raise ValueError("ENABLE_LOGGING is true, but ANOMALY_DB_DSN is not set.")

    def _generate_request_id(self, prefix: str) -> str:
        return f"{prefix}-{uuid4().hex[:8]}"

    def log_if_needed(self, anomaly_type: str, details: Dict[str, Any]):
        if not (self.enable_logging and self.logger):
            return  # No-op

        request_id = self._generate_request_id(anomaly_type)
        thread = threading.Thread(
            target=self.logger.store_anomaly,
            args=(request_id, anomaly_type, details),
            daemon=True
        )
        thread.start()


# === Instantiate Client Once ===

guardrails_client = GuardrailsClient()


# === API Endpoints ===

@app.get("/api/v1/get_report")
async def generate_report(group_by: str = Query("day", enum=["day", "anomaly_type"])):
    return generate_anomaly_report(group_by=group_by)

@app.get("/api/v1/guardrails")
async def list_guardrails():
    return {"guardrails": ["pii", "toxicity", "prompt_injection"]}


@app.post("/api/v1/toxicity")
async def validate_content(request: ToxiRequest):
    result = await detect_toxicity(request.content, request.treshold)

    if os.getenv("ENABLE_LOGGING") and result.get("toxic", False):
        guardrails_client.log_if_needed(
            anomaly_type="toxicity",
            details={"input": request.dict(), "result": result}
        )

    return result


@app.post("/api/v1/mask_pii")
async def transform_content(request: TransformRequest):
    result = await analyze_and_mask_text(
        request.content, request.guardrails, request.custom_entities, request.treshold)
    
    if os.getenv("ENABLE_LOGGING") and result.get("pii_found"):
        guardrails_client.log_if_needed(
            anomaly_type="pii",
            details={"input": request.dict(), "result": result}
        )

    return result


@app.post("/api/v1/prompt_injection")
async def prompt_injection(request: Prompt):
    result = await classify_prompt_injection(request.content)
    if os.getenv("ENABLE_LOGGING") and result.get("is_prompt_injection", False):
        guardrails_client.log_if_needed(
            anomaly_type="prompt_injection",
            details={"input": request.dict(), "result": result}
        )

    return result


@app.post("/api/v1/run_all_guardrails")
async def run_all_guardrails(request: TransformRequest):
    pii_result, toxicity_result, prompt_injection_result = await asyncio.gather(
        analyze_and_mask_text(
            request.content, request.guardrails, request.custom_entities, request.treshold),
        detect_toxicity(request.content, request.treshold),
        classify_prompt_injection(request.content)
    )

    result = {
        "pii": pii_result,
        "toxicity": toxicity_result,
        "prompt_injection": prompt_injection_result
    }

    # Collect triggered anomalies
    triggered = []
    if pii_result.get("action_taken") or pii_result.get("pii_found"):
        triggered.append("pii")
    if toxicity_result.get("toxic", False):
        triggered.append("toxicity")
    if prompt_injection_result.get("is_prompt_injection", False):
        triggered.append("prompt_injection")
    """if moderate_result.get("action_taken"):
        triggered.append("banned_words")"""

    if os.getenv("ENABLE_LOGGING") and triggered:
        guardrails_client.log_if_needed(
            anomaly_type=",".join(triggered),
            details={"input": request.dict(), "result": result}
        )

    return result


@app.get("/health")
async def health_check():
    return "success"