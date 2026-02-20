from flask import session
from datetime import datetime
from binance.client import Client
from binance.exceptions import BinanceAPIException
import config
import math
import traceback
import time
import hmac
import hashlib
import requests

# ==============================
# GLOBAL VARIABLES
# ==============================

_client = None
_symbol_cache = None
_symbol_cache_time = 0

_price_cache = {}
_last_call_time = 0

_positions_cache_time = 0   # ✅ FIXED (was missing → caused 500 error)

CACHE_DURATION = 5


# ==============================
# BINANCE CLIENT
# ==============================

def sync_time_with_binance():
    try:
        response = requests.get('https://fapi.binance.com/fapi/v1/time')
        server_time = response.json()['serverTime']
        local_time = int(time.time() * 1000)
        return server_time - local_time
    except:
        return 0


def get_client():
    global _client

    if _client is None:
        try:
            time_offset = sync_time_with_binance()

            _client = Client(
                config.BINANCE_KEY,
                config.BINANCE_SECRET,
                {'timeout': 20}
            )

            if abs(time_offset) > 1000:
                _client.timestamp_offset = time_offset

            _client.futures_account(recvWindow=60000)

        except Exception as e:
            print("Binance init error:", e)
            _client = None

    return _client


# ==============================
# SESSION INIT
# ==============================

def initialize_session():
    if "trades" not in session:
        session["trades"] = []

    if "stats" not in session:
        session["stats"] = {}

    session.modified = True


# ==============================
# SYMBOL + PRICE
# ==============================

def get_all_exchange_symbols():
    global _symbol_cache, _symbol_cache_time

    if _symbol_cache and (time.time() - _symbol_cache_time) < 3600:
        return _symbol_cache

    try:
        client = get_client()
        if client is None:
            return ["BTCUSDT", "ETHUSDT"]

        info = client.futures_exchange_info()
        symbols = sorted([
            s["symbol"]
            for s in info["symbols"]
            if s["status"] == "TRADING" and s["quoteAsset"] == "USDT"
        ])

        _symbol_cache = symbols
        _symbol_cache_time = time.time()
        return symbols

    except Exception as e:
        print("Symbol error:", e)
        return ["BTCUSDT", "ETHUSDT"]


def get_live_price(symbol):
    global _price_cache, _last_call_time

    if symbol in _price_cache and (time.time() - _last_call_time) < 2:
        return _price_cache[symbol]

    try:
        client = get_client()
        ticker = client.futures_symbol_ticker(symbol=symbol)
        price = float(ticker['price'])

        _price_cache[symbol] = price
        _last_call_time = time.time()

        return price

    except Exception as e:
        print("Price error:", e)
        return _price_cache.get(symbol, 0)


# ==============================
# BALANCE
# ==============================

def get_live_balance():
    try:
        client = get_client()
        if client is None:
            return None, None

        acc = client.futures_account(recvWindow=10000)
        return float(acc["totalWalletBalance"]), float(acc["totalInitialMargin"])

    except Exception as e:
        print("Balance error:", e)
        return None, None


# ==============================
# ROUNDING HELPERS
# ==============================

def get_symbol_filters(symbol):
    try:
        client = get_client()
        info = client.futures_exchange_info()
        for s in info["symbols"]:
            if s["symbol"] == symbol:
                return s["filters"]
    except:
        pass
    return []


def round_qty(symbol, qty):
    for f in get_symbol_filters(symbol):
        if f["filterType"] == "LOT_SIZE":
            step = float(f["stepSize"])
            precision = abs(int(round(-math.log10(step))))
            return round(qty - (qty % step), precision)

    return round(qty, 3)


def round_price(symbol, price):
    for f in get_symbol_filters(symbol):
        if f["filterType"] == "PRICE_FILTER":
            tick = float(f["tickSize"])
            precision = abs(int(round(-math.log10(tick))))
            return round(price - (price % tick), precision)

    return round(price, 2)


# ==============================
# POSITION SIZING
# ==============================

def calculate_position_sizing(unutilized_margin, entry, sl_type, sl_value):

    if entry <= 0:
        return {"error": "Invalid Entry"}

    risk_amount = unutilized_margin * (config.MAX_RISK_PERCENT / 100)

    if sl_value > 0:

        if sl_type == "SL % Movement":
            sl_percent = sl_value
        else:
            sl_percent = abs((entry - sl_value) / entry) * 100

        if sl_percent <= 0:
            return {"error": "Invalid SL"}

        leverage = min(int(100 / (sl_percent + 0.2)), 125)
        position_value = (risk_amount / (sl_percent + 0.2)) * 100
        units = position_value / entry

    else:
        leverage = 10
        units = risk_amount / entry

    return {
        "suggested_units": round(units, 6),
        "suggested_leverage": leverage,
        "max_leverage": leverage,
        "risk_amount": round(risk_amount, 2),
        "error": None
    }


# ==============================
# TRADE EXECUTION
# ==============================

def execute_trade_action(balance, symbol, side, entry, order_type,
                         sl_type, sl_value, sizing,
                         user_units, user_lev, margin_mode,
                         tp1, tp1_pct, tp2):

    client = get_client()
    if not client:
        return {"success": False, "message": "Connection Failed"}

    try:
        qty = round_qty(symbol,
                        user_units if user_units > 0 else sizing["suggested_units"])

        lev = int(user_lev) if user_lev > 0 else sizing["max_leverage"]

        try:
            client.futures_change_leverage(symbol=symbol, leverage=lev)
        except:
            pass

        entry_side = Client.SIDE_BUY if side == "LONG" else Client.SIDE_SELL
        exit_side = Client.SIDE_SELL if side == "LONG" else Client.SIDE_BUY

        # MARKET ENTRY
        client.futures_create_order(
            symbol=symbol,
            side=entry_side,
            type="MARKET",
            quantity=qty
        )

        time.sleep(0.5)

        # STOP LOSS
        if sl_type == "SL % Movement":
            sl_price = entry * (1 - sl_value / 100) if side == "LONG" \
                else entry * (1 + sl_value / 100)
        else:
            sl_price = sl_value

        sl_price = round_price(symbol, sl_price)

        client.futures_create_order(
            symbol=symbol,
            side=exit_side,
            type="STOP_MARKET",
            stopPrice=sl_price,
            closePosition=True,
            workingType="MARK_PRICE"
        )

        return {"success": True,
                "message": f"{side} {symbol} Opened | SL: {sl_price}"}

    except Exception as e:
        traceback.print_exc()
        return {"success": False,
                "message": str(e)}