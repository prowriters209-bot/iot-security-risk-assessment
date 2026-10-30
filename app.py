import os

from flask import (
    Flask, render_template, request,
    redirect, url_for, flash, send_file, abort
)

from config import Config
from models import db, Assessment
from risk_engine import assess_risk
from recommendations import generate_recommendations
from report_generator import generate_pdf


app = Flask(__name__)
app.config.from_object(Config)

os.makedirs("instance", exist_ok=True)
os.makedirs("reports", exist_ok=True)

db.init_app(app)

with app.app_context():
    db.create_all()


OPTIONS = {
    "network_exposure": ["isolated", "internal", "internet", "unknown"],
    "authentication": ["strong", "basic", "none", "unknown"],
    "encryption": ["strong", "partial", "none", "unknown"],
    "firmware_updates": [
        "automatic", "manual", "irregular", "unsupported", "unknown"
    ],
    "access_control": [
        "role_based", "basic", "weak", "none", "unknown"
    ],
    "data_protection": [
        "strong", "partial", "weak", "none", "unknown"
    ],
    "default_credentials": ["changed", "unchanged", "unknown"],
    "open_services": ["minimal", "several", "excessive", "unknown"],
    "logging": ["enabled", "limited", "disabled", "unknown"]
}


@app.route("/")
def dashboard():
    assessments = Assessment.query.order_by(
        Assessment.created_at.desc()
    ).all()

    total = len(assessments)

    high_risk = Assessment.query.filter(
        Assessment.risk_level.in_(["High", "Critical"])
    ).count()

    average_score = (
        round(sum(a.risk_score for a in assessments) / total, 1)
        if total else 0
    )

    risk_counts = {
        level: Assessment.query.filter_by(risk_level=level).count()
        for level in ["Low", "Medium", "High", "Critical"]
    }

    return render_template(
        "dashboard.html",
        total=total,
        high_risk=high_risk,
        average_score=average_score,
        risk_counts=risk_counts,
        recent=assessments[:5]
    )


@app.route("/assessment", methods=["GET", "POST"])
def assessment():
    if request.method == "POST":
        device_name = request.form.get("device_name", "").strip()
        device_type = request.form.get("device_type", "").strip()

        if not device_name or not device_type:
            flash("Please enter the device name and device type.", "danger")
            return redirect(url_for("assessment"))

        configuration = {}

        for field, allowed_values in OPTIONS.items():
            value = request.form.get(field, "unknown")

            if value not in allowed_values:
                flash(f"Invalid value supplied for {field}.", "danger")
                return redirect(url_for("assessment"))

            configuration[field] = value

        result = assess_risk(configuration)

        recommendations = generate_recommendations(configuration)

        record = Assessment(
            device_name=device_name,
            device_type=device_type,
            configuration=configuration,
            risk_score=result["risk_score"],
            risk_level=result["risk_level"],
            findings=result["findings"],
            recommendations=recommendations
        )

        db.session.add(record)
        db.session.commit()

        flash("Assessment completed successfully.", "success")

        return redirect(
            url_for("results", assessment_id=record.id)
        )

    return render_template("assessment.html", options=OPTIONS)


@app.route("/results/<int:assessment_id>")
def results(assessment_id):
    record = db.get_or_404(Assessment, assessment_id)

    return render_template("results.html", record=record)


@app.route("/history")
def history():
    records = Assessment.query.order_by(
        Assessment.created_at.desc()
    ).all()

    return render_template("history.html", records=records)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/report/<int:assessment_id>")
def download_report(assessment_id):
    record = db.get_or_404(Assessment, assessment_id)

    filename = f"assessment_{record.id}.pdf"
    output_path = os.path.join("reports", filename)

    generate_pdf(record, output_path)

    return send_file(
        output_path,
        as_attachment=True,
        download_name=filename
    )


if __name__ == "__main__":
    app.run(debug=True)