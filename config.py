# # Binance Credentials - IMPORTANT: Keep these secure!

# BINANCE_KEY = 'iyK0QCtq44CZb7K5BlRcZPCrjn2i7zeL52KQXxs9654NWkQnfQIvm1rKBaNhbXob'
# BINANCE_SECRET = 'EowxqqSJr8vD15Bk8oUGArIn9TrYaXlmPjoccV7TVLqLFZ7aqId3KzJY9l5iurOp'

# # Trading Configuration
# MAX_TRADES_PER_DAY = 4
# MAX_TRADES_PER_SYMBOL_PER_DAY = 2  # Maximum 2 trades per symbol per day

# # Risk Management
# MAX_RISK_PERCENT = 1.0  # 1% risk per trade
# SL_EDIT_MIN_PERCENT = -1.0  # Minimum SL adjustment (can move SL up to -1%)
# SL_EDIT_MAX_PERCENT = 0.0   # Maximum SL adjustment (cannot move beyond entry)

# # Update Intervals (seconds)
# POSITION_UPDATE_INTERVAL = 3
# PRICE_UPDATE_INTERVAL = 5

# # API Rate Limiting Protection
# PRICE_CACHE_DURATION = 5  # Cache prices for 5 seconds
# SYMBOL_CACHE_DURATION = 3600  # Cache symbols for 1 hour
# MAX_RETRIES = 3  # Retry failed API calls
# RETRY_DELAY = 1  # Delay between retries in seconds

# # Razorpay Configuration
# RAZORPAY_KEY_ID = 'rzp_live_SK0QFnXQv9Ed4b'  # Replace with your Razorpay Key ID
# RAZORPAY_KEY_SECRET = 'y5QeUePyOVDeqN0fGOeH6FSo'  # Replace with your Razorpay Key Secret
# RAZORPAY_PLAN_ID = 'your_razorpay_plan_id'  # Replace with your Razorpay Plan ID

# # Subscription Configuration
# SUBSCRIPTION_PRICE_INR = 499  # ₹500 per month

# RAZORPAY_YEARLY_PLAN_ID="plan_SK12UnaDI5gGcd"
# RAZORPAY_MONTHLY_PLAN_ID="plan_SK10d2Fpo8noaR"


# config.py

# Binance Credentials
BINANCE_KEY = 'iyK0QCtq44CZb7K5BlRcZPCrjn2i7zeL52KQXxs9654NWkQnfQIvm1rKBaNhbXob'
BINANCE_SECRET = 'EowxqqSJr8vD15Bk8oUGArIn9TrYaXlmPjoccV7TVLqLFZ7aqId3KzJY9l5iurOp'

# Razorpay Configuration
RAZORPAY_KEY_ID = 'rzp_live_SK0QFnXQv9Ed4b' 
RAZORPAY_KEY_SECRET = 'y5QeUePyOVDeqN0fGOeH6FSo'

# Correct Plan IDs
RAZORPAY_MONTHLY_PLAN_ID = "plan_SK10d2Fpo8noaR"
RAZORPAY_YEARLY_PLAN_ID = "plan_SK12UnaDI5gGcd"

# Trading Configuration
MAX_TRADES_PER_DAY = 4
MAX_TRADES_PER_SYMBOL_PER_DAY = 2
MAX_RISK_PERCENT = 1.0
SL_EDIT_MIN_PERCENT = -1.0
SL_EDIT_MAX_PERCENT = 0.0
POSITION_UPDATE_INTERVAL = 3
PRICE_UPDATE_INTERVAL = 5
PRICE_CACHE_DURATION = 5
SYMBOL_CACHE_DURATION = 3600
MAX_RETRIES = 3
RETRY_DELAY = 1