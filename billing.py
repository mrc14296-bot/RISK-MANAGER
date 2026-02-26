from datetime import datetime
from models import db, SubscriptionHistory

def log_subscription(user, plan):
    history = SubscriptionHistory(
        user_id=user.id,
        plan_type=plan,
        start_date=user.subscription_start,
        end_date=user.subscription_end,
        status="active"
    )
    db.session.add(history)
    db.session.commit()