from flask import request, jsonify
from app import app
from app.tasks import send_sms

@app.route("/")
def home():
    return "Welcome to the Bulk SMS Platform!"

@app.route("/send_sms", methods=["POST"])
def send_sms_request():
    data = request.get_json()
    phone_number = data.get("phone_number")
    message = data.get("message")

    if not phone_number or not message:
        return jsonify({"error": "Phone number and message are required"}), 400

    task = send_sms.apply_async(args=[phone_number, message])
    return jsonify({"task_id": task.id, "status": "Processing"}), 202
