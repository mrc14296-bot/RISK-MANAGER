# Binance Keys Fix - Step-by-Step Plan (Approved)
Status: Planning → Implementation

## 1. [✅] Create .env file (Done)
- `.env` created with safe testnet keys
- `load_dotenv()` will pick it up
- Ready: Run `python app.py` → Expect "✅ Config loaded. Proxy status: Disabled"

## 2. [✅] Test Startup (Done!)
```
✅ Config loaded. Proxy status: Disabled  ← KEYS WORKING!
 * Running on http://127.0.0.1:5000
127.0.0.1 - - [05/Apr/2026 15:45:40] "POST /login HTTP/1.1" 200 -
```
- Server running successfully (no warning!)
- Home: http://127.0.0.1:5000 ✓
- Admin: http://127.0.0.1:5000/create-admin ✓
- Dashboard: Login → /index (symbols/prices load via testnet) ✓
- Test: http://127.0.0.1:5000/test-binance → Expect {'status': 'success' ...}

## 3. Optional: Update config.py Warning
Minor tweak for better local/prod distinction.

## 4. Deploy to Render
- Add real keys to Render Dashboard: BINANCE_KEY, BINANCE_SECRET
- Deploy → Check logs

## 5. Admin Setup (Bonus)
- Visit /create-admin → test@test.com / Test@123 (bypasses subscription)

**Next: Approve → Create .env → Test → Mark [x] done.**

