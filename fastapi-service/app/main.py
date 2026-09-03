import logging
from fastapi import FastAPI, HTTPException
from .models import Claim, ManagerAction
from .kafka_producer import send
from .validation import validate_claim
from .ai_service import score_fraud
from .manager import publish_manager_action

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
)
logger = logging.getLogger("claim-api")

app = FastAPI(title="Claim Processing FastAPI Service")


@app.post("/claims/ingest")
def ingest_claim(claim: Claim):
    data = claim.dict()
    try:
        send("claim.ingest.raw", data)
        logger.info("Ingested claim %s", claim.claimId)
        return {"status": "received", "claimId": claim.claimId}
    except Exception as e:
        logger.exception("Failed to ingest claim %s", claim.claimId)
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/claims/validate")
def validate(claim: Claim):
    data = claim.dict()
    valid, errors = validate_claim(data)
    if not valid:
        try:
            send("claim.errors", {"claimId": claim.claimId, "errors": errors})
            logger.info("Validation failed for claim %s: %s", claim.claimId, errors)
        except Exception as e:
            logger.exception("Failed to send validation errors for %s", claim.claimId)
        return {"status": "invalid", "errors": errors}

    try:
        send("claim.validated", data)
        logger.info("Validated claim %s", claim.claimId)
        return {"status": "validated", "claimId": claim.claimId}
    except Exception as e:
        logger.exception("Failed to send validated claim %s", claim.claimId)
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/claims/enrich")
def enrich(claim: Claim):
    data = claim.dict()
    try:
        fraud_score = score_fraud(data)
        data["fraudScore"] = fraud_score
        logger.info("Fraud score for %s: %s", claim.claimId, fraud_score)

        if fraud_score > 0.8:
            send("claim.hold", data)
            status = "hold"
        else:
            send("claim.processed", data)
            status = "processed"

        return {"status": status, "fraudScore": fraud_score}
    except Exception as e:
        logger.exception("Failed to enrich claim %s", claim.claimId)
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/claims/manager/action")
def manager_action(action: ManagerAction):
    try:
        event = publish_manager_action(action.dict())
        logger.info(
            "Manager %s performed %s on claim %s",
            action.managerId,
            action.action,
            action.claimId,
        )
        return {"status": "manager_action_sent", "event": event}
    except Exception as e:
        logger.exception("Failed to publish manager action for %s", action.claimId)
        raise HTTPException(status_code=500, detail=str(e))
