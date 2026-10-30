RECOMMENDATIONS = {
    "network_exposure": {
        "internet": "Restrict direct internet exposure. Use firewalls, network segmentation and secure gateways.",
        "internal": "Apply network segmentation and restrict access to trusted internal networks.",
        "unknown": "Verify the device's network exposure and document its accessible interfaces."
    },
    "authentication": {
        "basic": "Replace basic authentication with stronger authentication mechanisms.",
        "none": "Implement authentication before allowing access to device functions.",
        "unknown": "Verify the authentication mechanisms supported by the device."
    },
    "encryption": {
        "partial": "Extend encryption to all relevant communications and stored sensitive data.",
        "none": "Implement encryption for sensitive data in transit and at rest.",
        "unknown": "Verify encryption support and configuration."
    },
    "firmware_updates": {
        "manual": "Establish a documented and regular firmware update process.",
        "irregular": "Introduce a consistent firmware patching schedule.",
        "unsupported": "Evaluate replacing the unsupported device or isolating it from sensitive networks.",
        "unknown": "Verify the device's firmware update policy and support lifecycle."
    },
    "access_control": {
        "basic": "Introduce role-based access control and review user permissions.",
        "weak": "Strengthen access restrictions and apply least-privilege principles.",
        "none": "Implement access controls to prevent unauthorized device administration.",
        "unknown": "Review the device's user roles and access permissions."
    },
    "data_protection": {
        "partial": "Improve data protection through encryption, secure storage and retention controls.",
        "weak": "Strengthen data handling, storage and transmission protections.",
        "none": "Introduce appropriate safeguards for sensitive device data.",
        "unknown": "Identify the data collected and verify how it is protected."
    },
    "default_credentials": {
        "unchanged": "Immediately replace default credentials with unique, strong passwords.",
        "unknown": "Verify that default credentials have been changed."
    },
    "open_services": {
        "several": "Disable unnecessary services and restrict exposed ports.",
        "excessive": "Reduce the attack surface by disabling unnecessary services and filtering network traffic.",
        "unknown": "Review exposed ports and running network services."
    },
    "logging": {
        "limited": "Improve event logging and establish regular log reviews.",
        "disabled": "Enable security logging and monitor relevant device activities.",
        "unknown": "Verify whether security events can be logged and monitored."
    }
}


def generate_recommendations(configuration):
    recommendations = []

    for factor, options in RECOMMENDATIONS.items():
        value = configuration.get(factor, "unknown")

        if value in options:
            recommendations.append({
                "area": factor.replace("_", " ").title(),
                "recommendation": options[value]
            })

    return recommendations