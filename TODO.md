# Fix: Show ALL Symbols in Dropdown (Full ~500 USDT Perpetuals)

## Status: 🚧 In Progress (BLACKBOXAI)

### Step 1: [✅] Create this TODO.md
### Step 2: [✅] Update config.py (cache TTL)
### Step 3: [ ] Fix logic.py (debug, public client, 50-symbol fallback, 10min cache)
### Step 4: [ ] Update app.py (log count, /refresh_symbols route)
### Step 5: [ ] Update templates/index.html (show count + refresh + warning)
### Step 6: [ ] Test: Run app, check /index symbols len, dropdown, refresh
### Step 7: [ ] ✅ Complete

**Expected:** Dropdown shows all ~500 Binance USDT perpetual symbols.
**Root cause fixed:** Silent fallback to 5 symbols → full fetch + UI feedback.

Last updated: {{ now }}
