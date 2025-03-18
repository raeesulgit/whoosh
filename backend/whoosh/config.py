import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()
ADMIN_KEY = os.getenv("ADMIN_KEY")
RAZORPAY_API_KEY = os.getenv("RAZORPAY_API_KEY")
RAZORPAY_API_SECRET = os.getenv("RAZORPAY_API_SECRET")
RAZORPAY_WEBHOOK_SECRET = os.getenv("RAZORPAY_WEBHOOK_SECRET")