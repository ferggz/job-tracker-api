from flask import Blueprint, request, jsonify
from database import get_db_connection

applications_bp = Blueprint("applications", __name__)


@applications_bp.route("/applications", methods=["POST"])
def create_application():
    data = request.get_json()

    user_id = data.get("user_id")
    company = data.get("company")
    position = data.get("position")
    location = data.get("location")
    remote_type = data.get("remote_type")
    status = data.get("status", "saved")
    applied_date = data.get("applied_date")
    notes = data.get("notes")

    if not user_id or not company or not position:
        return jsonify({"error": "user_id, company and position are required"}), 400

    conn = get_db_connection()

    conn.execute("""
        INSERT INTO applications 
        (user_id, company, position, location, remote_type, status, applied_date, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (user_id, company, position, location, remote_type, status, applied_date, notes))

    conn.commit()
    conn.close()

    return jsonify({"message": "Application created successfully"}), 201


@applications_bp.route("/applications", methods=["GET"])
def get_applications():
    conn = get_db_connection()

    applications = conn.execute(
        "SELECT * FROM applications ORDER BY created_at DESC"
    ).fetchall()

    conn.close()

    applications_list = []

    for application in applications:
        applications_list.append({
            "id": application["id"],
            "user_id": application["user_id"],
            "company": application["company"],
            "position": application["position"],
            "location": application["location"],
            "remote_type": application["remote_type"],
            "status": application["status"],
            "applied_date": application["applied_date"],
            "notes": application["notes"],
            "created_at": application["created_at"]
        })

    return jsonify(applications_list), 200


@applications_bp.route("/applications/<int:application_id>", methods=["GET"])
def get_application(application_id):
    conn = get_db_connection()

    application = conn.execute(
        "SELECT * FROM applications WHERE id = ?",
        (application_id,)
    ).fetchone()

    conn.close()

    if application is None:
        return jsonify({"error": "Application not found"}), 404

    return jsonify({
        "id": application["id"],
        "user_id": application["user_id"],
        "company": application["company"],
        "position": application["position"],
        "location": application["location"],
        "remote_type": application["remote_type"],
        "status": application["status"],
        "applied_date": application["applied_date"],
        "notes": application["notes"],
        "created_at": application["created_at"]
    }), 200