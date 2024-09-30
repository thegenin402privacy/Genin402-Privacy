from fastapi import FastAPI
from pydantic import BaseModel

from .models import ShadowTransfer
from .engine import PrivacyEngine

app = FastAPI(title="Genin402 Privacy API", version="1.0.0")
_engine = PrivacyEngine()


class TransferRequest(BaseModel):
    wallet_address: str
    transfer_amount_sol: float
    hop_count: int
    mixer_pools_used: int
    decoy_tx_count: int
    payment_gate_active: int
    route_splits: int
    time_delay_blocks: int
    dummy_outputs: int
    memo_obfuscated: int
    token_program_obscured: int
    fee_randomized: int


class BatchRequest(BaseModel):
    transfers: list[TransferRequest]


def _to_model(r: TransferRequest) -> ShadowTransfer:
    return ShadowTransfer(**r.model_dump())


@app.post("/analyze")
def analyze(req: TransferRequest):
    return _engine.analyze(_to_model(req))


@app.post("/analyze/batch")
def analyze_batch(req: BatchRequest):
    return _engine.analyze_batch([_to_model(t) for t in req.transfers])


@app.get("/health")
def health():
    return {"status": "ok", "service": "genin402"}
