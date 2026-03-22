# Binance API Fix - Error -2015 & Balance/Price Issues
Status: ✅ In Progress by BLACKBOXAI

## Steps:
- [x] 1. Add BINANCE_ERROR_CODES mapping to config.py
- [x] 2. Enhance app.py /add-exchange & /verify-exchange with specific error handling
- [x] 3. Fix logic.py get_user_exchange_client() with BinanceAPIException handling
- [ ] 4. Add diagnostics to balance/price endpoints
- [ ] 5. Test: Invalid keys → clear errors, valid keys → balance/prices work
- [ ] 6. Update TODO.md ✅ COMPLETE

## Root Causes Fixed:
- ❌ Error -2015: Invalid key/IP/permissions → Specific user guidance
- ❌ No balance/prices: Client auth fails silently → Better error propagation
- ✅ Google Cloud: US IP → No geo-restriction expected

**Next**: User MUST whitelist Google Cloud IP on Binance OR use their personal keys.

