import logging

logger = logging.getLogger("ai-service")


def score_fraud(claim: dict) -> float:
    """
    Simple stub fraud scoring:
    - High amount => higher score
    - Could be replaced with real ML model or external service.
    """
    amount = float(claim.get("amount", 0.0))
    claim_type = claim.get("claimType", "").lower()

    base = 0.2
    if amount > 10000:
        base = 0.9
    elif amount > 5000:
        base = 0.6

    if "auto" in claim_type:
        base += 0.05
    if "medical" in claim_type:
        base += 0.1

    score = min(base, 0.99)
    logger.debug("Computed fraud score %s for claim %s", score, claim.get("claimId"))
    return score
