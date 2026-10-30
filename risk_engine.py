WEIGHTS = {
    "network_exposure": 15,
    "authentication": 15,
    "encryption": 15,
    "firmware_updates": 12,
    "access_control": 12,
    "data_protection": 12,
    "default_credentials": 10,
    "open_services": 5,
    "logging": 4
}

RISK_VALUES = {
    "network_exposure": {
        "isolated": 0,
        "internal": 30,
        "internet": 100,
        "unknown": 70
    },
    "authentication": {
        "strong": 0,
        "basic": 45,
        "none": 100,
        "unknown": 70
    },
    "encryption": {
        "strong": 0,
        "partial": 50,
        "none": 100,
        "unknown": 70
    },
    "firmware_updates": {
        "automatic": 0,
        "manual": 35,
        "irregular": 75,
        "unsupported": 100,
        "unknown": 70
    },
    "access_control": {
        "role_based": 0,
        "basic": 45,
        "weak": 85,
        "none": 100,
        "unknown": 70
    },
    "data_protection": {
        "strong": 0,
        "partial": 50,
        "weak": 85,
        "none": 100,
        "unknown": 70
    },
    "default_credentials": {
        "changed": 0,
        "unchanged": 100,
        "unknown": 70
    },
    "open_services": {
        "minimal": 0,
        "several": 60,
        "excessive": 100,
        "unknown": 70
    },
    "logging": {
        "enabled": 0,
        "limited": 50,
        "disabled": 100,
        "unknown": 70
    }
}


def assess_risk(configuration):
    """
    Calculate a weighted risk score from 0 to 100.
    Higher scores indicate greater configuration risk.
    """

    total_score = 0
    findings = []

    for factor, weight in WEIGHTS.items():
        value = configuration.get(factor, "unknown")

        risk_value = RISK_VALUES[factor].get(value, 70)

        weighted_score = risk_value * weight / 100
        total_score += weighted_score

        if risk_value >= 50:
            findings.append({
                "factor": factor.replace("_", " ").title(),
                "value": value.replace("_", " ").title(),
                "risk_value": risk_value,
                "weighted_score": round(weighted_score, 2)
            })

    total_score = round(total_score, 2)

    if total_score < 25:
        risk_level = "Low"
    elif total_score < 50:
        risk_level = "Medium"
    elif total_score < 75:
        risk_level = "High"
    else:
        risk_level = "Critical"

    return {
        "risk_score": total_score,
        "risk_level": risk_level,
        "findings": findings
    }