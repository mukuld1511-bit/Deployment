// State Variables
let currentDetectedUrl = "";
const statsIntervalTime = 3000;
const messagesIntervalTime = 2500;
const ledgerIntervalTime = 3000;

// DOM Elements
const cpuValueEl = document.getElementById("cpu-value");
const cpuProgressEl = document.getElementById("cpu-progress");
const ramValueEl = document.getElementById("ram-value");
const ramProgressEl = document.getElementById("ram-progress");
const osValEl = document.getElementById("os-val");
const javaValEl = document.getElementById("java-val");
const uptimeValEl = document.getElementById("uptime-val");

const detectedHostEl = document.getElementById("detected-host");
const tunnelUrlInputEl = document.getElementById("tunnel-url-input");
const qrImageEl = document.getElementById("qr-image");
const qrPlaceholderEl = document.getElementById("qr-placeholder");
const copyBtnEl = document.getElementById("copy-btn");

const messagesListEl = document.getElementById("messages-list");
const messageFormEl = document.getElementById("message-form");
const senderInputEl = document.getElementById("sender-input");
const textInputEl = document.getElementById("text-input");

const ledgerListEl = document.getElementById("ledger-list");
const paymentFormEl = document.getElementById("payment-form");
const payOverlayEl = document.getElementById("payment-overlay");
const paySenderInputEl = document.getElementById("pay-sender-input");
const payAmountInputEl = document.getElementById("pay-amount-input");

// Fetch and Update System Diagnostics
async function fetchSystemStats() {
    try {
        const response = await fetch("/api/system-stats");
        if (!response.ok) throw new Error("Failed to fetch system stats");
        const data = await response.json();

        // Update CPU progress
        const cpuLoad = data.cpuLoad || 0.0;
        cpuValueEl.textContent = `${cpuLoad.toFixed(1)}%`;
        cpuProgressEl.style.width = `${Math.min(cpuLoad, 100)}%`;

        // Update RAM progress
        const usedRam = data.usedMemoryMb || 0;
        const totalRam = data.totalMemoryMb || 1;
        const ramPercent = Math.min((usedRam / totalRam) * 100, 100);
        ramValueEl.textContent = `${usedRam} / ${totalRam} MB`;
        ramProgressEl.style.width = `${ramPercent}%`;

        // Update general details
        osValEl.textContent = data.osName || "Unknown OS";
        javaValEl.textContent = `Java ${data.javaVersion || "Unknown"}`;
        
        // Format uptime
        const uptimeSec = data.uptimeSeconds || 0;
        uptimeValEl.textContent = formatUptime(uptimeSec);

        // Dynamic QR code generation based on host header
        const detectedUrl = data.detectedUrl;
        if (detectedUrl && detectedUrl !== currentDetectedUrl) {
            currentDetectedUrl = detectedUrl;
            updateQrCode(detectedUrl);
        }

    } catch (error) {
        console.error("Error fetching stats:", error);
        cpuValueEl.textContent = "Offline";
        ramValueEl.textContent = "Offline";
    }
}

// Format Uptime (seconds to readable format)
function formatUptime(seconds) {
    if (seconds < 60) return `${seconds}s`;
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    if (mins < 60) return `${mins}m ${secs}s`;
    const hrs = Math.floor(mins / 60);
    const rmMs = mins % 60;
    return `${hrs}h ${rmMs}m`;
}

// Generate QR Code URL from open API
function updateQrCode(url) {
    detectedHostEl.textContent = url;
    tunnelUrlInputEl.value = url;
    
    // Use QR Server API to generate QR Code image
    const qrApiUrl = `https://api.qrserver.com/v1/create-qr-code/?size=160x160&data=${encodeURIComponent(url)}&color=070913&bgcolor=ffffff`;
    
    qrImageEl.src = qrApiUrl;
    qrImageEl.onload = () => {
        qrPlaceholderEl.style.display = "none";
        qrImageEl.style.display = "block";
    };
}

// Fetch Messages Feed
async function fetchMessages() {
    try {
        const response = await fetch("/api/messages");
        if (!response.ok) throw new Error("Failed to fetch messages");
        const messages = await response.json();
        
        // Render Messages
        const shouldScroll = messagesListEl.scrollHeight - messagesListEl.scrollTop === messagesListEl.clientHeight;
        
        messagesListEl.innerHTML = messages.map(msg => {
            const isSys = msg.sender === "System Console";
            const dateStr = new Date(msg.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' });
            return `
                <div class="message-bubble ${isSys ? 'system-msg' : 'user-msg'}">
                    <div class="msg-header">
                        <span class="msg-sender">${escapeHtml(msg.sender)}</span>
                        <span class="msg-time">${dateStr}</span>
                    </div>
                    <div class="msg-text">${escapeHtml(msg.text)}</div>
                </div>
            `;
        }).join("");

        // Keep scrolled to bottom if it was already at the bottom
        if (shouldScroll) {
            messagesListEl.scrollTop = messagesListEl.scrollHeight;
        }

    } catch (error) {
        console.error("Error fetching messages:", error);
    }
}

// Post New Message
async function postMessage(event) {
    event.preventDefault();
    const sender = senderInputEl.value.trim();
    const text = textInputEl.value.trim();

    if (!text) return;

    try {
        const response = await fetch("/api/messages", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ sender, text })
        });
        
        if (response.ok) {
            textInputEl.value = "";
            await fetchMessages();
            // Force scroll to bottom after user posts
            messagesListEl.scrollTop = messagesListEl.scrollHeight;
        }
    } catch (error) {
        console.error("Error posting message:", error);
    }
}

// Fetch Transaction History Ledger
async function fetchTransactionLedger() {
    try {
        const response = await fetch("/api/payments/history");
        if (!response.ok) throw new Error("Failed to fetch payments");
        const txns = await response.json();

        // Render Ledger
        // Sort descending so the newest shows up at the top
        const sortedTxns = [...txns].sort((a, b) => b.timestamp - a.timestamp);

        ledgerListEl.innerHTML = sortedTxns.map(txn => {
            const statusClass = txn.status.toLowerCase();
            return `
                <div class="ledger-item">
                    <div class="ledger-details">
                        <div class="ledger-top">
                            <span class="ledger-id">${txn.txnId}</span>
                            <span class="ledger-method">${escapeHtml(txn.method)}</span>
                        </div>
                        <span class="ledger-sender">${escapeHtml(txn.sender)}</span>
                    </div>
                    <div class="ledger-meta">
                        <span class="ledger-amount">₹${txn.amount}</span>
                        <span class="status-badge ${statusClass}">${txn.status}</span>
                    </div>
                </div>
            `;
        }).join("");

    } catch (error) {
        console.error("Error fetching transactions:", error);
    }
}

// Initiate Mock Payment
async function initiateMockPayment(event) {
    event.preventDefault();
    const sender = paySenderInputEl.value.trim();
    const amount = payAmountInputEl.value.trim();
    const method = document.querySelector('input[name="pay-method"]:checked').value;

    if (!sender || !amount) return;

    // Show Overlay Spinner
    payOverlayEl.style.display = "flex";

    // Simulate 1.5 second loading latency for Bank contact
    setTimeout(async () => {
        try {
            const response = await fetch("/api/payments/charge", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ sender, amount, method })
            });

            if (response.ok) {
                // Clear inputs
                paySenderInputEl.value = "";
                payAmountInputEl.value = "";
                
                // Refresh Ledger
                await fetchTransactionLedger();
            }
        } catch (error) {
            console.error("Payment charge error:", error);
        } finally {
            // Hide Overlay Spinner
            payOverlayEl.style.display = "none";
        }
    }, 1500);
}

// Escape HTML helper
function escapeHtml(text) {
    const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    };
    return text.replace(/[&<>"']/g, function(m) { return map[m]; });
}

// Copy Tunnel URL Clipboard Handler
copyBtnEl.addEventListener("click", () => {
    tunnelUrlInputEl.select();
    tunnelUrlInputEl.setSelectionRange(0, 99999);
    navigator.clipboard.writeText(tunnelUrlInputEl.value)
        .then(() => {
            const oldText = copyBtnEl.textContent;
            copyBtnEl.textContent = "COPIED!";
            setTimeout(() => {
                copyBtnEl.textContent = oldText;
            }, 1500);
        })
        .catch(err => {
            console.error("Failed to copy text: ", err);
        });
});

// Event Listeners & Bootstrapping
messageFormEl.addEventListener("submit", postMessage);
paymentFormEl.addEventListener("submit", initiateMockPayment);

// Initial Load & Intervals
fetchSystemStats();
fetchMessages();
fetchTransactionLedger();
setInterval(fetchSystemStats, statsIntervalTime);
setInterval(fetchMessages, messagesIntervalTime);
setInterval(fetchTransactionLedger, ledgerIntervalTime);
