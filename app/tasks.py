from app.celery_app import celery

@celery.task
def send_sms(phone_number, message):
    """Simulated SMS sending task."""
    print(f"Sending SMS to {phone_number}: {message}")
    return f"Message sent to {phone_number}"
