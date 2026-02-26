from datetime import datetime, timedelta
from models import User
from email_utils import send_email

def send_expiry_reminders():
    today = datetime.utcnow().date()

    users = User.query.filter(User.subscription_end != None).all()

    for user in users:
        days_left = (user.subscription_end.date() - today).days

        if days_left == 3:
            send_email(
                user.email,
                "Subscription Expiring Soon",
                "Your subscription expires in 3 days."
            )

        if days_left == 0:
            send_email(
                user.email,
                "Subscription Expired",
                "Your subscription has expired. Please renew."
            )