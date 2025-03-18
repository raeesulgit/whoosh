import smtplib
from email.mime.text import MIMEText
from models import Booking
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USERNAME = "raeesulasad@gmail.com"
SMTP_PASSWORD = "mjvn flvu ntwj vllj"

def send_booking_email(booking: Booking):
    subject = f"Booking Confirmed - {booking.vehicle_type} Wash"
    body = f"""
    Hi {booking.customer_name},

    Thank you for choosing our doorstep vehicle wash service! 🚗✨

    Your booking details are as follows:

    - Vehicle Type: {booking.vehicle_type}
    - Service: {booking.service}
    - Appointment Date & Time: {booking.appointment_time.strftime('%Y-%m-%d %H:%M')}

    Our team will arrive at your doorstep on time to ensure your vehicle gets the care it deserves. If you need to reschedule or cancel your booking, feel free to do so via the app.

    We look forward to serving you!

    Regards,  
    Team Whoosh 🚿
    """

    send_email(booking.customer_email, subject, body)

def send_cancellation_email(booking: Booking):
    subject = f"Booking Cancelled - {booking.vehicle_type} Wash"
    body = f"""
    Hi {booking.customer_name},

    We’re sorry to hear you’ve cancelled your vehicle wash appointment. 😔

    Here are the cancelled booking details for your reference:

    - Vehicle Type: {booking.vehicle_type}
    - Service: {booking.service}
    - Original Appointment Date & Time: {booking.appointment_time.strftime('%Y-%m-%d %H:%M')}

    If you change your mind, we’d love to help you reschedule a convenient time for your vehicle wash.

    Thank you for considering our service, and we hope to serve you in the future! 🚗✨

    Regards,  
    Team Whoosh 🚿
    """

    send_email(booking.customer_email, subject, body)

def send_email(to, subject, body):
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = SMTP_USERNAME
    msg["To"] = to

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()  # This is missing in your code (mandatory)
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            #server.sendmail(SMTP_USERNAME, [to], msg.as_string())
        print(f"Email sent to {to}")
    except Exception as e:
        print(f"Failed to send email: {e}")
