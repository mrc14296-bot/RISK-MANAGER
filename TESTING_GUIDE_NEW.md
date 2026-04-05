# 🧪 Complete Testing Guide - MindRiskControl Trading Platform

**Last Updated:** April 4, 2026  
**Version:** 3.0 - Full step-by-step walkthrough with all features

---

## ⚡ Quick Start (5 minutes)

### Step 1: Start the App
```bash
cd "c:/Users/isalo/Downloads/mindriskcontrol/Trade-flask-fixed (1)"
python app.py
```
Wait for: `Running on http://127.0.0.1:5000`

### Step 2: Access Dashboard
- Browser: `http://localhost:5000`
- Register → Login → Subscribe → Connect Binance

### Step 3: Start Testing
```
Left Panel: Trading controls
Right Panel: Live positions, trade history, trade log
```

---

## 📋 PHASE 1: Account Setup & Authentication

### **Step 1.1: Start Your Application**

Open Terminal/Command Prompt and run:
```bash
cd "c:\Users\isalo\Downloads\mindriskcontrol\Trade-flask-fixed (1)"
python app.py
```

**Expected Output:**
```
⚠️ WARNING: Binance Keys missing from Environment!
 * Running on http://127.0.0.1:5000
```

✅ **SUCCESS**: App is running locally

---

### **Step 1.2: Register a Test Account**

1. Open browser: **`http://localhost:5000`**
2. Click **"Register"** button
3. Fill in form:
   - **Email**: `test@example.com`
   - **Username**: `testuser`
   - **Password**: `Test@123456` (use uppercase + numbers)
4. Click **"Submit"**

**Expected Result**: 
- ✅ Account created
- ✅ Redirected to login page

---

### **Step 1.3: Login**

1. Click **"Login"**
2. Enter credentials:
   - **Username**: `testuser`
   - **Password**: `Test@123456`
3. Click **"Login"**

**Expected Result**:
- ✅ Logged in successfully
- ✅ Redirected to subscription page

---

## 💳 PHASE 2: Subscription & Payment

### **Step 2.1: Choose a Plan**

On the subscription page:
1. Select Plan: **"Monthly - ₹500"** (or Yearly for larger amount)
2. Click **"Subscribe Now"**

**Expected**: Payment gateway opens (Razorpay)

---

### **Step 2.2: Complete Test Payment**

A payment modal will appear:

| Field | Value |
|-------|-------|
| **Card Number** | 4242 4242 4242 4242 |
| **Expiry** | 12/25 |
| **CVV** | 123 |
| **Name** | Test User |

1. Enter above card details
2. Click **"Pay ₹500"**

**Expected Result**:
- ✅ Payment successful (test card auto-passes)
- ✅ Redirected to **Trading Dashboard**
- ✅ Subscription active message shown

---

## 🔌 PHASE 3: Binance Exchange Connection

### **Step 3.1: Get Binance API Keys**

#### **Option A: Using LIVE Binance (Real Trading)**

1. Go to: **https://www.binance.com/en/my/settings/api-management**
2. Login with your Binance account
3. Click **"Create API"**
4. Fill in:
   - **API Label**: `MindRiskControl`
   - Verify with 2FA
5. Set Restrictions:
   - ✅ **Enable Reading** - Yes
   - ✅ **Enable Futures** - YES (required)
   - ✅ **Enable Margin** - Yes
6. **Copy & Save:**
   - **API Key** (20+ characters)
   - **Secret Key** (keep secure!)

#### **Option B: Using Binance TESTNET (Recommended for Testing)**

1. Go to: **https://testnet.binancefuture.com**
2. Login with Binance account (or create testnet account)
3. Go to: **Account → API Management**
4. Following steps same as Option A
5. Get testnet API keys (separate from live)

✅ **RECOMMENDATION**: Start with testnet to avoid losing real funds

---

### **Step 3.2: Connect to MindRiskControl**

1. From Dashboard, click **"Exchange Connections"** (top menu)
2. Click **"Connect Binance"** button
3. Paste your details:
   - **API Key**: `[paste from Binance]`
   - **Secret Key**: `[paste from Binance]`
4. Click **"Connect"**

**Expected Result**:
- ✅ Green checkmark appears
- ✅ Status shows "Connected"
- ✅ Message: "Connection Successful"

**Troubleshooting**:
- ❌ "Invalid API Key" → Check Futures permission enabled
- ❌ "Connection Failed" → Verify API keys are correct (no extra spaces)
- ❌ "IP Restricted" → Disable IP whitelist on Binance

---

## 🎯 PHASE 4: Trading & Order Placement

### **Step 4.1: Fill Trading Form**

Return to main dashboard. On the **LEFT PANEL**, fill out the trading form:

| Field | Example | Notes |
|-------|---------|-------|
| **Symbol** | BTCUSDT | BTC/USD perpetual futures |
| **Side** | LONG | Choose direction |
| **Order Type** | MARKET | Fills immediately |
| **Entry Price** | [Click Live] | Gets current market price |
| **SL Method** | SL % Movement | Stop loss |
| **SL %** | 2 | Required - closes at -2% |
| **TP1 Method** | TP1 Price | First take profit |
| **TP1 Price** | [above entry] | Must be above entry for LONG |
| **TP1 QTY %** | 50 | Closes 50% at TP1 |
| **TP2 Price** | [even higher] | Second take profit level |
| **TP2 QTY %** | 50 | Closes remaining 50% |
| **Leverage** | 1 | Or higher (10-20x optional) |

---

### **Step 4.2: Real-Time Form Validation**

As you fill the form, **watch for warnings**:

✅ **Accepted** (Green):
- Entry price is positive
- SL below entry (for LONG)
- TP1 above entry
- TP1 > TP2 for LONG
- Order size ≥ $5 USDT

❌ **Blocked** (Red - Won't let you submit):
- Entry is 0 or negative
- SL above entry (for LONG trades)
- TP1 below entry
- Order too small (< $5 notional)
- Any required field missing

**Example Error Message**:
```
⚠️ Order quantity too small!
   Current: 0.0001 BTC ($9.34)
   Minimum needed: $5 USDT
   With your SL at 2%, you need entry amount ≥ $2,500
```

---

### **Step 4.3: Execute Trade (MARKET Order)**

1. **All validations pass** → Button is clickable
2. Click **"✅ EXECUTE EXCHANGE ORDER"**
3. **Confirmation dialog appears:**

```
🔥 CONFIRM TRADE EXECUTION

📊 BTCUSDT - LONG MARKET ORDER
💰 Entry Price: $93,450.00
📦 Order Qty: 0.002 BTC
🛡️ Stop Loss: $91,581.00 (2% below)
🎯 TP1: $95,000.00 (50% qty)
🎯 TP2: $97,000.00 (50% qty)
⚡ Leverage: 10x
💸 Est. Margin Used: $1,869.00

⚠️ Are you sure?
```

4. Click **"OK"** to confirm

**Expected Result**:
- ✅ Success message: "Trade opened successfully"
- ✅ Redirected to dashboard
- ✅ Position appears in RIGHT PANEL
- ✅ Live log shows order confirmation

---

### **Step 4.4: Verify Orders on Binance**

Check that Binance received your orders:

1. Go to **Binance Dashboard** (https://www.binancefuture.com or testnet)
2. Navigate to **"Orders"** section
3. You should see **4 ORDERS**:
   - ✅ **MARKET** - Your entry (filled)
   - ✅ **STOP_MARKET** - Your SL (pending)
   - ✅ **TAKE_PROFIT_MARKET** - Your TP1 (pending)
   - ✅ **TAKE_PROFIT_MARKET** - Your TP2 (pending)

**If you see all 4 orders**: ✅ **TRADING CORE WORKS**

---

## 📊 PHASE 5: Position Management & Monitoring

### **Step 5.1: Monitor Live Position**

In the **RIGHT PANEL**, you'll see your open position:

```
═══════════════════════════
📈 POSITIONS
═══════════════════════════

BTCUSDT | 10x | LONG
Entry: $93,450.00
Current: $93,850.00
PnL: +$80.00 | ROI: +0.43%

Margin: $1,869.00
Position Size: $18,690.00

[Close] [Close %] [Trail SL]
═══════════════════════════
```

**Live Updates Every 10 Seconds**:
- Entry price
- Current market price
- Unrealized PnL
- ROI percentage
- Margin usage

---

### **Step 5.2: Test Close Position**

Click **[Close]** button to immediately exit:

1. Click **[Close]** button
2. Confirmation dialog appears
3. Click **OK**

**Expected Result**:
- ✅ "Position closed successfully"
- ✅ Trade history updated
- ✅ Position removed from dashboard
- ✅ Live log shows close event

---

### **Step 5.3: Test Partial Close**

To close only **25% of position**:

1. Click **[Close %]** button
2. Enter: `25`
3. Click OK

**Expected Result**:
- ✅ Message: "Closed 25% of position"
- ✅ Remaining qty updated
- ✅ Position still shows with 75% qty

---

### **Step 5.4: Test Trailing Stop Loss**

To move your SL **0.5% closer to entry** (lock profits):

1. Click **[Trail SL]** button
2. Enter: `-0.5` (negative = closer to entry)
3. Click OK

**Expected Result**:
- ✅ Message: "SL updated to $91,131.00"
- ✅ New SL visible in position
- ✅ Binance order updated

---

### **Step 5.5: Monitor Trade History**

In the **TRADE HISTORY** section (below Positions):

```
═══════════════════════════════════════════════
📊 TRADE HISTORY (Last 10 Closed Trades)
═══════════════════════════════════════════════
BTCUSDT | LONG | M | Closed
Entry: $93,450 | Exit: $95,230 | PnL: +$71.04
Time: 2 min ago

ETHUSDT | SHORT | M | Closed
Entry: $3,150 | Exit: $3,100 | PnL: +$50.00
Time: 15 min ago
═══════════════════════════════════════════════
```

**Updated Every 30 Seconds**

---

## ⚙️ PHASE 6: Advanced Features Testing

### **Step 6.1: Test LIMIT Orders (Instead of MARKET)**

In the trading form:
1. Change **Order Type** → **"LIMIT"**
2. Set **Limit Price** (where you want to buy, e.g., 5% below current)
3. Set **Time in Force** → TIF (Good-til-Cancel)
4. Fill rest normally
5. Execute

**Expected**: Order appears in Binance as LIMIT (not immediately filled)

---

### **Step 6.2: Test Different Leverage**

Try trading with different leverage:
1. **1x**: Least risky, maximum capital needed
2. **5x**: Medium risk
3. **10-20x**: High risk, small capital

**Note**: Your account must have futures enabled for leverage

---

### **Step 6.3: Test Error Prevention**

Try to break the form validation:

#### ❌ **Scenario 1: Order Too Small**
```
Entry: $100
SL: 2%
Expected Order: 0.00001 BTC = $1 (too small!)
Expected Error: "Order too small... minimum $5"
Result: ✅ Blocked at validation
```

#### ❌ **Scenario 2: Invalid SL for LONG**
```
Side: LONG
Entry: $50,000
SL: $55,000 (ABOVE entry - wrong!)
Expected Error: "SL must be BELOW entry for LONG"
Result: ✅ Warning prevented execution
```

#### ❌ **Scenario 3: Invalid TP for SHORT**
```
Side: SHORT
Entry: $50,000
TP1: $52,000 (ABOVE entry - wrong!)
Expected Error: "TP must be BELOW entry for SHORT"
Result: ✅ Validation blocked
```

#### ❌ **Scenario 4: No Exchange Connection**
```
1. Remove Binance connection
2. Try to place trade
Expected Error: "❌ No exchange connected. Please add your API keys"
Result: ✅ Graceful error handling
```

---

## 🔍 PHASE 7: Live Monitoring Dashboard

### **Real-Time Components**

| Component | Update Frequency | Purpose |
|-----------|------------------|---------|
| **Entry Price** | ~5 sec | Latest market data |
| **Positions** | ~10 sec | PnL, ROI updates |
| **Trade History** | ~30 sec | Closed trade records |
| **Live Log** | ~2 sec | Order confirmations, events |

### **Step 7.1: Watch Live Log**

At the **BOTTOM** of the dashboard is the **Live Trade Log**:

```
🔴 LIVE TRADE LOG
═════════════════════════════════════════
[14:25:32] ✅ MARKET ORDER FILLED
  BTCUSDT | LONG | 0.002 BTC at $93,450

[14:25:33] ✅ STOP LOSS PLACED
  Order ID: 2847192 | At: $91,581

[14:25:34] ✅ TP1 PLACED
  Order ID: 2847193 | At: $95,000

[14:25:35] ✅ TP2 PLACED
  Order ID: 2847194 | At: $97,000

[14:26:45] 📊 POSITION UPDATE
  PnL: +$150 | ROI: +0.81%

[14:27:12] ⛔ PRICE HIT SL!
  BTCUSDT closed at $91,580
  Final PnL: -$143.50
═════════════════════════════════════════
```

✅ Every action logged and timestamped

---

## ✅ Complete Testing Checklist

Check off each item as you test:

### **Authentication (5 min)**
- [ ] Register new account
- [ ] Login works
- [ ] Can logout
- [ ] Session persists on page reload

### **Subscription (3 min)**
- [ ] Subscription page loads
- [ ] Payment form appears
- [ ] Test card accepted
- [ ] Marked as subscribed

### **Exchange Connection (3 min)**
- [ ] Can add Binance API key
- [ ] Connection status verified
- [ ] Can view connected exchanges
- [ ] Can disconnect exchange

### **Trading Form (5 min)**
- [ ] All fields present
- [ ] Real price button works
- [ ] Live 5s updates
- [ ] Form validation appears real-time

### **Trade Execution (5 min)**
- [ ] Market order fills
- [ ] 4 orders created (entry + SL + TP1 + TP2)
- [ ] All orders visible in Binance
- [ ] Confirmation dialog accurate
- [ ] Entry price matches Binance

### **Position Management (5 min)**
- [ ] Position displays correctly
- [ ] PnL updates every 10s
- [ ] Close button works
- [ ] Partial close works
- [ ] Trail SL works

### **Live Monitoring (3 min)**
- [ ] Positions update
- [ ] Trade history updates
- [ ] Live log shows events
- [ ] No delays or loading screens

### **Error Handling (5 min)**
- [ ] Form warns about invalid SL
- [ ] Form warns about small orders
- [ ] Error messages are clear
- [ ] No JavaScript errors in console

### **TOTAL TEST TIME: ~35 minutes**

---

## 🐛 Troubleshooting Guide

### **App Won't Start**
```
Error: No module named 'flask'
Solution: pip install -r requirements.txt
Then: python app.py
```

### **Binance Connection Failed**
```
Error: "Connection to Binance Failed"
Solution #1: Check API key is copied correctly (no spaces)
Solution #2: Enable Futures permission on Binance
Solution #3: Try testnet keys first
Solution #4: Disable IP whitelist on Binance
```

### **Order Too Small Error**
```
Error: "Order's notional must be >= 5"
Solution: VALIDATION now prevents this!
If it happens anyway: Your SL % too large relative to entry
Try: Entry $10,000 + SL 2% + increase qty
```

### **Database Lock Error**
```
Error: "database is locked"
Solution: Close other instances of app
Solution: Delete instance/trading.db and restart
Solution: Ensure only 1 Python process running
```

### **Live Updates Frozen**
```
Problem: Position PnL not updating
Solution #1: Wait 10 seconds (update interval)
Solution #2: Check browser console for errors
Solution #3: Reload page and try again
Solution #4: Verify Binance connection still active
```

### **Form Validation Not Working**
```
Problem: No warnings appearing
Solution: Open browser DevTools (F12)
Check: Console for JavaScript errors
Check: Network tab - are API calls working?
Try: Hard refresh (Ctrl+Shift+R)
```

### **Payment Gateway Stuck**
```
Problem: Razorpay modal won't close
Solution: Refresh page
Solution: Check test card details (4242...)
Solution: Try different browser
```

---

## 📞 Support & Next Steps

If all tests pass:
- ✅ Your platform is **production-ready**
- ✅ Users can trade with their own money
- ✅ All features working as designed

If issues remain:
1. Check troubleshooting above
2. Review environment variables
3. Check Binance API permissions
4. Verify database connections

**You're ready to deploy! 🚀**
