from flask import Blueprint, request, jsonify
from database import get_db_connection

applications_bp = Blueprint("applications", __name__)

ALLOWED_STATUSES = [
    "saved",
    "applied",
    "interview",
    "rejected",
    "offer"
]


from datetime import datetime

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

    if not applied_date:
        applied_date = datetime.now().strftime("%Y-%m-%d")

    notes = data.get("notes")

    if not user_id or not company or not position:
        return jsonify({"error": "user_id, company and position are required"}), 400

    if status not in ALLOWED_STATUSES:
        return jsonify({"error": "Invalid status"}), 400
    
    def application_to_dict(application):
        return {
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
        }
    
    conn = get_db_connection()

    user = conn.execute(
        "SELECT * FROM users WHERE id = ?",
        (user_id,)
    ).fetchone()

    if user is None:
        conn.close()
        return jsonify({"error": "User not found"}), 404

    cursor = conn.execute("""
        INSERT INTO applications 
        (user_id, company, position, location, remote_type, status, applied_date, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (user_id, company, position, location, remote_type, status, applied_date, notes))

    conn.commit()

    new_application_id = cursor.lastrowid

    conn.close()

    return jsonify({
        "message": "Application created successfully",
        "application_id": new_application_id
    }), 201


@applications_bp.route("/applications", methods=["GET"])
def get_applications():
    status = request.args.get("status")
    
    if status and status not in ALLOWED_STATUSES:
        return jsonify({"error": "Invalid status filter"}), 400

    company = request.args.get("company")
    user_id = request.args.get("user_id")
    sort = request.args.get("sort", "created_at")

    query = "SELECT * FROM applications WHERE 1=1"
    params = []

    if status:
        query += " AND status = ?"
        params.append(status)

    if company:
        query += " AND company LIKE ?"
        params.append(f"%{company}%")

    allowed_sort_fields = {
        "created_at": "created_at",
        "applied_date": "applied_date",
        "company": "company",
        "status": "status"
    }

    sort_column = allowed_sort_fields.get(sort, "created_at")

    if user_id:
        query += " AND user_id = ?"
        params.append(user_id)

    query += f" ORDER BY {sort_column} DESC"

    conn = get_db_connection()
    applications = conn.execute(query, params).fetchall()
    conn.close()

    applications_list = [application_to_dict(application) for application in applications]

    return jsonify(application_to_dict(application)), 200


@applications_bp.route("/applications/summary", methods=["GET"])
def get_applications_summary():
    user_id = request.args.get("user_id")

    query = """
        SELECT status, COUNT(*) as total
        FROM applications
        WHERE 1=1
    """
    params = []

    if user_id:
        query += " AND user_id = ?"
        params.append(user_id)

    query += " GROUP BY status"

    conn = get_db_connection()
    rows = conn.execute(query, params).fetchall()
    conn.close()

    summary = {
        "saved": 0,
        "applied": 0,
        "interview": 0,
        "rejected": 0,
        "offer": 0
    }

    for row in rows:
        summary[row["status"]] = row["total"]

    summary["total"] = sum(summary.values())

    return jsonify(summary), 200


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


@applications_bp.route("/applications/<int:application_id>", methods=["PUT"])
def update_application(application_id):
    data = request.get_json()

    company = data.get("company")
    position = data.get("position")
    location = data.get("location")
    remote_type = data.get("remote_type")
    status = data.get("status")
    applied_date = data.get("applied_date")
    notes = data.get("notes")

    if not company or not position:
        return jsonify({"error": "company and position are required"}), 400

    if status not in ALLOWED_STATUSES:
        return jsonify({"error": "Invalid status"}), 400

    conn = get_db_connection()

    application = conn.execute(
        "SELECT * FROM applications WHERE id = ?",
        (application_id,)
    ).fetchone()

    if application is None:
        conn.close()
        return jsonify({"error": "Application not found"}), 404

    conn.execute("""
        UPDATE applications
        SET company = ?,
            position = ?,
            location = ?,
            remote_type = ?,
            status = ?,
            applied_date = ?,
            notes = ?
        WHERE id = ?
    """, (
        company,
        position,
        location,
        remote_type,
        status,
        applied_date,
        notes,
        application_id
    ))

    conn.commit()
    conn.close()

    return jsonify({"message": "Application updated successfully"}), 200


@applications_bp.route("/applications/<int:application_id>", methods=["DELETE"])
def delete_application(application_id):
    conn = get_db_connection()

    application = conn.execute(
        "SELECT * FROM applications WHERE id = ?",
        (application_id,)
    ).fetchone()

    if application is None:
        conn.close()
        return jsonify({"error": "Application not found"}), 404

    conn.execute(
        "DELETE FROM applications WHERE id = ?",
        (application_id,)
    )

    conn.commit()
    conn.close()

    return jsonify({"message": "Application deleted successfully"}), 200