// ✅ ENHANCED POSITION DISPLAY WITH BINANCE-STYLE UI
// This file contains all position management functions

function updateLivePositions() {
    fetch('/get_open_positions')
    .then(r => r.json())
    .then(data => {
        const container = document.getElementById('live_positions');
        const header = document.getElementById('position_header');
        if (data.positions && data.positions.length > 0) {
            let totalOrders = 0;
            let html = '';
            data.positions.forEach(pos => {
                const pnlColor = pos.unrealized_pnl >= 0 ? '#00ff88' : '#ff4d4d';
                const roiPercent = (pos.dashboard_roi_percent ?? pos.roi_percent).toFixed(2);
                const marginRatio = (pos.dashboard_margin_ratio ?? pos.margin_ratio).toFixed(2);
                const entryPrice = parseFloat(pos.entry_price || 0).toFixed(8);
                const markPrice = parseFloat(pos.mark_price || 0).toFixed(8);
                const liqPrice = parseFloat(pos.liquidation_price || 0).toFixed(8);
                const sizeUsdt = parseFloat(pos.size_usdt || 0).toFixed(2);
                const marginUsdt = parseFloat(pos.margin_usdt || 0).toFixed(2);
                const pnlUsdt = parseFloat(pos.unrealized_pnl || 0).toFixed(2);
                
                totalOrders += pos.open_orders ? pos.open_orders.length : 0;
                
                // ✅ BINANCE-STYLE POSITION CARD
                html += `
                    <div style="border: 1px solid #2a2a2a; padding: 16px; margin-bottom: 12px; border-radius: 8px; background: #0f1419; box-shadow: 0 2px 8px rgba(0,0,0,0.3);">
                        
                        <!-- HEADER: Symbol & Status -->
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; padding-bottom: 12px; border-bottom: 1px solid #2a2a2a;">
                            <div>
                                <div style="font-weight: bold; font-size: 16px; color: ${pos.side === 'LONG' ? '#00ff88' : '#ff4444'};  cursor: pointer;" onclick="showCoinDetails()">${pos.symbol}</div>
                                <small style="color: #888;">Isolated ${pos.leverage}x</small>
                            </div>
                            <div style="text-align: right;">
                                <div style="font-size: 14px; font-weight: bold; color: #ff9800;">-0.05%</div>
                                <small style="color: #888;">${pos.side}</small>
                            </div>
                        </div>
                        
                        <!-- METRICS GRID: PNL, ROI, Size, Margin Ratio -->
                        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-bottom: 12px;">
                            
                            <!-- PNL (USDT) -->
                            <div style="background: #1a1a2e; padding: 10px; border-radius: 6px;">
                                <div style="font-size: 11px; color: #888; margin-bottom: 4px;">PNL (USDT)</div>
                                <div style="font-size: 18px; font-weight: bold; color: ${pnlColor};">$${pnlUsdt}</div>
                            </div>
                            
                            <!-- ROI -->
                            <div style="background: #1a1a2e; padding: 10px; border-radius: 6px; cursor: pointer;" onclick="showCoinDetails()">
                                <div style="font-size: 11px; color: #888; margin-bottom: 4px;">ROI</div>
                                <div style="font-size: 18px; font-weight: bold; color: ${roiPercent >= 0 ? '#00ff88' : '#ff4444'}; text-decoration: underline;">+${roiPercent}%</div>
                                <small style="color: #666; font-size: 9px;">click for details</small>
                            </div>
                            
                            <!-- Size (USDT) -->
                            <div style="background: #1a1a2e; padding: 10px; border-radius: 6px;">
                                <div style="font-size: 11px; color: #888; margin-bottom: 4px;">Size (USDT)</div>
                                <div style="font-size: 16px; font-weight: bold; color: #fff;">$${sizeUsdt}</div>
                            </div>
                            
                            <!-- Margin Ratio -->
                            <div style="background: #1a1a2e; padding: 10px; border-radius: 6px; cursor: pointer;" onclick="showCoinDetails()">
                                <div style="font-size: 11px; color: #888; margin-bottom: 4px;">Margin Ratio</div>
                                <div style="font-size: 16px; font-weight: bold; color: ${marginRatio > 50 ? '#ff6b6b' : marginRatio > 30 ? '#ffaa00' : '#00ff88'};">${marginRatio}%</div>
                                <small style="color: #666; font-size: 9px;">click for details</small>
                            </div>
                        </div>
                        
                        <!-- MARGIN (USDT) with Add Button -->
                        <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 12px; padding: 10px; background: #1a1a2e; border-radius: 6px;">
                            <div style="flex: 1;">
                                <div style="font-size: 11px; color: #888; margin-bottom: 4px;">Margin (USDT)</div>
                                <div style="font-size: 16px; font-weight: bold; color: #fff;">$${marginUsdt}</div>
                            </div>
                            <button onclick="openAddMarginModal('${pos.symbol}', ${marginUsdt})" style="background: #0d6efd; color: white; border: none; padding: 8px 16px; border-radius: 4px; cursor: pointer; font-weight: bold; font-size: 14px;">
                                +
                            </button>
                        </div>
                        
                        <!-- PRICES: Entry, Mark, Liquidation -->
                        <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 10px; margin-bottom: 12px;">
                            <div style="background: #1a1a2e; padding: 8px; border-radius: 6px;">
                                <div style="font-size: 10px; color: #888; margin-bottom: 3px;">Entry Price (USDT)</div>
                                <div style="font-size: 13px; font-weight: bold; color: #fff; word-break: break-all;">$${entryPrice}</div>
                            </div>
                            <div style="background: #1a1a2e; padding: 8px; border-radius: 6px;">
                                <div style="font-size: 10px; color: #888; margin-bottom: 3px;">Mark Price (USDT)</div>
                                <div style="font-size: 13px; font-weight: bold; color: #fff; word-break: break-all;">$${markPrice}</div>
                            </div>
                            <div style="background: #1a1a2e; padding: 8px; border-radius: 6px;">
                                <div style="font-size: 10px; color: #888; margin-bottom: 3px;">Liq. Price (USDT)</div>
                                <div style="font-size: 13px; font-weight: bold; color: #ff6b6b; word-break: break-all;">$${liqPrice}</div>
                            </div>
                        </div>
                        
                        <!-- ACTION BUTTONS: Leverage, TP/SL, Close -->
                        <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 8px; margin-bottom: 10px;">
                            <button onclick="openEditLeverageModal('${pos.symbol}', ${pos.leverage})" style="background: #1a1a2e; color: #00d4ff; border: 1px solid #00d4ff; padding: 8px; border-radius: 4px; cursor: pointer; font-weight: bold; font-size: 12px;">
                                ⚙️ Leverage
                            </button>
                            <button onclick="openTPSLModal('${pos.symbol}')" style="background: #1a1a2e; color: #00d4ff; border: 1px solid #00d4ff; padding: 8px; border-radius: 4px; cursor: pointer; font-weight: bold; font-size: 12px;">
                                🎯 TP/SL
                            </button>
                            <button onclick="closePosition('${pos.symbol}')" style="background: #dc3545; color: white; border: none; padding: 8px; border-radius: 4px; cursor: pointer; font-weight: bold; font-size: 12px;">
                                ✕ Close
                            </button>
                        </div>
                        
                        <!-- ADDITIONAL ACTION BUTTONS -->
                        <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 8px;">
                            <button onclick="moveTrailingSL('${pos.symbol}')" style="background: #4d1a1a; color: #ff9800; border: 1px solid #ff9800; padding: 6px; border-radius: 4px; cursor: pointer; font-size: 11px;">
                                📍 Trail SL
                            </button>
                            <button onclick="partialClose('${pos.symbol}')" style="background: #1a2a1a; color: #00ff88; border: 1px solid #00ff88; padding: 6px; border-radius: 4px; cursor: pointer; font-size: 11px;">
                                📊 Partial Close
                            </button>
                            <button onclick="showCoinDetails()" style="background: #1a1a2a; color: #00d4ff; border: 1px solid #00d4ff; padding: 6px; border-radius: 4px; cursor: pointer; font-size: 11px;">
                                📋 Full Details
                            </button>
                        </div>
                        
                        <!-- OPEN ORDERS (if any) -->
                        ${pos.open_orders && pos.open_orders.length > 0 ? `
                            <div style="margin-top: 12px; padding-top: 12px; border-top: 1px solid #2a2a2a;">
                                <small style="color: #888;">Open Orders (${pos.open_orders.length}):</small>
                                <div style="margin-top: 6px; display: flex; gap: 4px; flex-wrap: wrap;">
                                    ${pos.open_orders.map(o => `<span style="background: #1a1a2e; padding: 4px 8px; border-radius: 3px; font-size: 10px; color: #aaa;">${o.type} ${o.side} @$${o.price}</span>`).join('')}
                                </div>
                            </div>
                        ` : ''}
                    </div>
                `;
            });
            header.textContent = `POSITIONS (${data.positions.length}) | Open Orders (${totalOrders})`;
            container.innerHTML = html;
        } else {
            header.textContent = 'POSITIONS (0)';
            container.innerHTML = '<div style="text-align: center; color: #888; padding-top: 60px;">No open positions<br><small>Connect Binance account</small></div>';
        }
    }).catch(() => {
        document.getElementById('live_positions').innerHTML = '<div style="text-align: center; color: #ff4444; padding: 60px;">Connection Error</div>';
    });
}

// ✅ EDIT LEVERAGE MODAL
function openEditLeverageModal(symbol, currentLev) {
    const modal = document.getElementById('leverage-modal') || createLeverageModal();
    document.getElementById('leverage-symbol').textContent = symbol;
    document.getElementById('leverage-input').value = currentLev;
    document.getElementById('leverage-input').min = 1;
    document.getElementById('leverage-input').max = 125;
    modal.style.display = 'flex';
    
    document.getElementById('leverage-submit').onclick = function() {
        const newLev = parseInt(document.getElementById('leverage-input').value);
        if (isNaN(newLev) || newLev < 1 || newLev > 125) {
            alert('Invalid leverage');
            return;
        }
        changeLeverage(symbol, newLev);
        modal.style.display = 'none';
    };
}

function createLeverageModal() {
    const modal = document.createElement('div');
    modal.id = 'leverage-modal';
    modal.style.cssText = 'display:none;position:fixed;z-index:10000;left:0;top:0;width:100%;height:100%;background-color:rgba(0,0,0,0.7);align-items:center;justify-content:center;';
    modal.innerHTML = `
        <div style="background-color: #0d1117; padding: 25px; border: 2px solid #00d4ff; border-radius: 8px; width: 90%; max-width: 400px; color: #fff; box-shadow: 0 0 30px rgba(0, 212, 255, 0.3);">
            <h3 style="color: #00d4ff; margin-top: 0;">⚙️ Edit Leverage</h3>
            <p style="color: #888; margin: 10px 0;">Position: <strong id="leverage-symbol" style="color: #fff;">BTCUSDT</strong></p>
            <label style="color: #aaa; display: block; margin-bottom: 8px;">New Leverage (1-125x):</label>
            <input type="number" id="leverage-input" value="10" min="1" max="125" style="width: 100%; padding: 10px; background: #1a1a2e; border: 1px solid #00d4ff; color: #fff; border-radius: 4px; margin-bottom: 15px; font-size: 14px;">
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px;">
                <button onclick="document.getElementById('leverage-modal').style.display='none'" style="background: #6c757d; color: white; border: none; padding: 10px; border-radius: 4px; cursor: pointer; font-weight: bold;">Cancel</button>
                <button id="leverage-submit" style="background: #00d4ff; color: #000; border: none; padding: 10px; border-radius: 4px; cursor: pointer; font-weight: bold;">Confirm</button>
            </div>
        </div>
    `;
    modal.onclick = function(e) {
        if (e.target === modal) modal.style.display = 'none';
    };
    document.body.appendChild(modal);
    return modal;
}

function changeLeverage(symbol, newLev) {
    fetch('/change_leverage', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ symbol: symbol, leverage: newLev })
    })
    .then(r => r.json())
    .then(data => {
        if (data.success) {
            alert(`✅ Leverage changed to ${newLev}x`);
            updateLivePositions();
        } else {
            alert(`❌ Error: ${data.message || 'Failed to change leverage'}`);
        }
    })
    .catch(e => alert(`Error: ${e.message}`));
}

// ✅ ADD MARGIN MODAL
function openAddMarginModal(symbol, currentMargin) {
    const modal = document.getElementById('margin-modal') || createAddMarginModal();
    document.getElementById('margin-symbol').textContent = symbol;
    document.getElementById('margin-amount').value = '';
    modal.style.display = 'flex';
    
    document.getElementById('margin-submit').onclick = function() {
        const amount = parseFloat(document.getElementById('margin-amount').value);
        if (isNaN(amount) || amount <= 0) {
            alert('Invalid amount');
            return;
        }
        addMargin(symbol, amount);
        modal.style.display = 'none';
    };
}

function createAddMarginModal() {
    const modal = document.createElement('div');
    modal.id = 'margin-modal';
    modal.style.cssText = 'display:none;position:fixed;z-index:10000;left:0;top:0;width:100%;height:100%;background-color:rgba(0,0,0,0.7);align-items:center;justify-content:center;';
    modal.innerHTML = `
        <div style="background-color: #0d1117; padding: 25px; border: 2px solid #00d4ff; border-radius: 8px; width: 90%; max-width: 400px; color: #fff; box-shadow: 0 0 30px rgba(0, 212, 255, 0.3);">
            <h3 style="color: #00d4ff; margin-top: 0;">➕ Add Margin</h3>
            <p style="color: #888; margin: 10px 0;">Position: <strong id="margin-symbol" style="color: #fff;">BTCUSDT</strong></p>
            <label style="color: #aaa; display: block; margin-bottom: 8px;">Amount (USDT):</label>
            <input type="number" id="margin-amount" placeholder="Enter amount" step="0.01" min="0" style="width: 100%; padding: 10px; background: #1a1a2e; border: 1px solid #00d4ff; color: #fff; border-radius: 4px; margin-bottom: 15px; font-size: 14px;">
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px;">
                <button onclick="document.getElementById('margin-modal').style.display='none'" style="background: #6c757d; color: white; border: none; padding: 10px; border-radius: 4px; cursor: pointer; font-weight: bold;">Cancel</button>
                <button id="margin-submit" style="background: #00d4ff; color: #000; border: none; padding: 10px; border-radius: 4px; cursor: pointer; font-weight: bold;">Add</button>
            </div>
        </div>
    `;
    modal.onclick = function(e) {
        if (e.target === modal) modal.style.display = 'none';
    };
    document.body.appendChild(modal);
    return modal;
}

function addMargin(symbol, amount) {
    fetch('/add_margin', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ symbol: symbol, amount: amount })
    })
    .then(r => r.json())
    .then(data => {
        if (data.success) {
            alert(`✅ Added $${amount} margin`);
            updateLivePositions();
        } else {
            alert(`❌ Error: ${data.message || 'Failed to add margin'}`);
        }
    })
    .catch(e => alert(`Error: ${e.message}`));
}

// ✅ TP/SL SETUP MODAL
function openTPSLModal(symbol) {
    const modal = document.getElementById('tpsl-modal') || createTPSLModal();
    document.getElementById('tpsl-symbol').textContent = symbol;
    document.getElementById('tpsl-tp-price').value = '';
    document.getElementById('tpsl-sl-price').value = '';
    modal.style.display = 'flex';
    
    document.getElementById('tpsl-submit').onclick = function() {
        const tp = parseFloat(document.getElementById('tpsl-tp-price').value);
        const sl = parseFloat(document.getElementById('tpsl-sl-price').value);
        if (isNaN(tp) || isNaN(sl) || tp <= 0 || sl <= 0) {
            alert('Invalid TP or SL price');
            return;
        }
        setTPSL(symbol, tp, sl);
        modal.style.display = 'none';
    };
}

function createTPSLModal() {
    const modal = document.createElement('div');
    modal.id = 'tpsl-modal';
    modal.style.cssText = 'display:none;position:fixed;z-index:10000;left:0;top:0;width:100%;height:100%;background-color:rgba(0,0,0,0.7);align-items:center;justify-content:center;';
    modal.innerHTML = `
        <div style="background-color: #0d1117; padding: 25px; border: 2px solid #00d4ff; border-radius: 8px; width: 90%; max-width: 400px; color: #fff; box-shadow: 0 0 30px rgba(0, 212, 255, 0.3);">
            <h3 style="color: #00d4ff; margin-top: 0;">🎯 Set TP / SL</h3>
            <p style="color: #888; margin: 10px 0;">Position: <strong id="tpsl-symbol" style="color: #fff;">BTCUSDT</strong></p>
            <label style="color: #aaa; display: block; margin-bottom: 6px;">Take Profit Price:</label>
            <input type="number" id="tpsl-tp-price" placeholder="Enter TP price" step="any" style="width: 100%; padding: 10px; background: #1a1a2e; border: 1px solid #00ff88; color: #fff; border-radius: 4px; margin-bottom: 12px; font-size: 14px;">
            <label style="color: #aaa; display: block; margin-bottom: 6px;">Stop Loss Price:</label>
            <input type="number" id="tpsl-sl-price" placeholder="Enter SL price" step="any" style="width: 100%; padding: 10px; background: #1a1a2e; border: 1px solid #ff4d4d; color: #fff; border-radius: 4px; margin-bottom: 15px; font-size: 14px;">
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px;">
                <button onclick="document.getElementById('tpsl-modal').style.display='none'" style="background: #6c757d; color: white; border: none; padding: 10px; border-radius: 4px; cursor: pointer; font-weight: bold;">Cancel</button>
                <button id="tpsl-submit" style="background: #00d4ff; color: #000; border: none; padding: 10px; border-radius: 4px; cursor: pointer; font-weight: bold;">Set</button>
            </div>
        </div>
    `;
    modal.onclick = function(e) {
        if (e.target === modal) modal.style.display = 'none';
    };
    document.body.appendChild(modal);
    return modal;
}

function setTPSL(symbol, tp, sl) {
    fetch('/set_tpsl', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ symbol: symbol, tp_price: tp, sl_price: sl })
    })
    .then(r => r.json())
    .then(data => {
        if (data.success) {
            alert(`✅ TP/SL set successfully`);
            updateLivePositions();
        } else {
            alert(`❌ Error: ${data.message || 'Failed to set TP/SL'}`);
        }
    })
    .catch(e => alert(`Error: ${e.message}`));
}
