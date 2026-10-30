# Cybersecurity in the Internet of Things: Vulnerabilities, Threats, and Countermeasures

## Project Information

**Student Name:** FALEGAN ABIODUN KUNLE

**Supervisor Name:** AMANINDER SINGH

## Project Overview

This project investigates cybersecurity vulnerabilities and threats affecting Internet of Things (IoT) environments and explores appropriate security countermeasures.

The practical artefact is a Python-based IoT Security Risk Assessment Tool.

The application evaluates user-provided IoT device security configurations using a weighted, rule-based assessment engine. It identifies potential weaknesses, calculates risk scores, classifies security risks, and provides recommendations.

## Key Features

- IoT device security assessment
- Weighted risk scoring
- Risk classification: Low, Medium, High, Critical
- Automated security recommendations
- Assessment history
- PDF risk assessment reports
- Dashboard with risk statistics

## Technologies

- Python
- Flask
- Flask-SQLAlchemy
- SQLite
- HTML, CSS and JavaScript
- Bootstrap
- ReportLab

## Installation

1. Clone the repository.
2. Create a virtual environment:

   `python -m venv venv`

3. Activate it:

   `venv\Scripts\activate`

4. Install dependencies:

   `pip install -r requirements.txt`

5. Run the application:

   `python app.py`

6. Open `http://127.0.0.1:5000` in your browser.

## Scope and Limitations

This is a configuration-based prototype. It evaluates security information entered by the user. It does not perform live network scanning, penetration testing, or automatic vulnerability verification.

Risk scores and thresholds are illustrative design choices developed for this prototype.

## Project Status

Under development and testing.