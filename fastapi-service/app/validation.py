def validate_claim(claim: dict):
    errors = []

    if not claim.get("claimId"):
        errors.append("claimId is required")
    if not claim.get("customerId"):
        errors.append("customerId is required")

    try:
        amount = float(claim.get("amount", 0.0))
        if amount <= 0:
            errors.append("amount must be positive")
    except (TypeError, ValueError):
        errors.append("amount must be a valid number")

    if not claim.get("claimType"):
        errors.append("claimType is required")

    if not claim.get("description"):
        errors.append("description is required")

    if not isinstance(claim.get("timestamp"), int):
        errors.append("timestamp must be an integer epoch millis")

    if errors:
        return False, errors
    return True, None
