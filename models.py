from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class Assessment(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    device_name = db.Column(db.String(150), nullable=False)
    device_type = db.Column(db.String(100), nullable=False)

    configuration = db.Column(db.JSON, nullable=False)

    risk_score = db.Column(db.Float, nullable=False)
    risk_level = db.Column(db.String(30), nullable=False)

    findings = db.Column(db.JSON, nullable=False)
    recommendations = db.Column(db.JSON, nullable=False)

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    def __repr__(self):
        return f"<Assessment {self.device_name}>"