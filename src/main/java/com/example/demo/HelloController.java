package com.example.demo;

import org.springframework.web.bind.annotation.*;
import jakarta.servlet.http.HttpServletRequest;
import java.lang.management.ManagementFactory;
import java.util.*;
import java.util.concurrent.CopyOnWriteArrayList;

@RestController
@CrossOrigin(origins = "*")
public class HelloController {

    private final long startupTime = System.currentTimeMillis();
    private final List<Map<String, Object>> messages = new CopyOnWriteArrayList<>();
    private final List<Map<String, Object>> transactions = new CopyOnWriteArrayList<>();

    public HelloController() {
        // Add a default system message
        Map<String, Object> sysMsg = new HashMap<>();
        sysMsg.put("sender", "System Console");
        sysMsg.put("text", "Welcome to the Cloud Deployment Console. ngrok tunnel established successfully.");
        sysMsg.put("timestamp", System.currentTimeMillis());
        messages.add(sysMsg);

        // Pre-populate some historical mock transactions
        addMockTransaction("Alice Smith", "150.00", "Credit Card", "SUCCESS", System.currentTimeMillis() - 600000);
        addMockTransaction("Bob Jones", "45.00", "UPI", "SUCCESS", System.currentTimeMillis() - 300000);
        addMockTransaction("Charlie Brown", "500.00", "NetBanking", "FAILED", System.currentTimeMillis() - 150000);
    }

    private void addMockTransaction(String sender, String amount, String method, String status, long timestamp) {
        Map<String, Object> txn = new HashMap<>();
        txn.put("txnId", "TXN-" + String.format("%06d", new Random().nextInt(1000000)));
        txn.put("sender", sender);
        txn.put("amount", amount);
        txn.put("method", method);
        txn.put("status", status);
        txn.put("timestamp", timestamp);
        transactions.add(txn);
    }

    @GetMapping("/api/hello")
    public Map<String, Object> hello() {
        Map<String, Object> response = new HashMap<>();
        response.put("status", "success");
        response.put("message", "Hello from Maven, Docker, and Spring Boot!");
        response.put("tunnel", "Exposed securely via ngrok");
        response.put("timestamp", System.currentTimeMillis());
        return response;
    }

    @GetMapping("/api/system-stats")
    public Map<String, Object> getSystemStats(HttpServletRequest request) {
        Map<String, Object> stats = new HashMap<>();
        
        // Memory metrics
        Runtime runtime = Runtime.getRuntime();
        long totalMemory = runtime.totalMemory();
        long freeMemory = runtime.freeMemory();
        long usedMemory = totalMemory - freeMemory;
        long maxMemory = runtime.maxMemory();

        stats.put("usedMemoryMb", usedMemory / (1024 * 1024));
        stats.put("totalMemoryMb", totalMemory / (1024 * 1024));
        stats.put("maxMemoryMb", maxMemory / (1024 * 1024));
        
        // CPU load: check OS load, fallback to simulated load if average returns negative
        double systemLoad = ManagementFactory.getOperatingSystemMXBean().getSystemLoadAverage();
        if (systemLoad < 0) {
            systemLoad = 5.0 + (Math.random() * 20.0);
        } else {
            systemLoad = systemLoad * 100.0;
        }
        stats.put("cpuLoad", Math.round(systemLoad * 10.0) / 10.0);

        // Uptime in seconds
        long uptimeMs = System.currentTimeMillis() - startupTime;
        stats.put("uptimeSeconds", uptimeMs / 1000);

        stats.put("detectedUrl", "http://localhost:8080");
        stats.put("osName", System.getProperty("os.name"));
        stats.put("osVersion", System.getProperty("os.version"));
        stats.put("javaVersion", System.getProperty("java.version"));
        
        return stats;
    }

    @GetMapping("/api/messages")
    public List<Map<String, Object>> getMessages() {
        return messages;
    }

    @PostMapping("/api/messages")
    public Map<String, Object> postMessage(@RequestBody Map<String, String> payload) {
        String sender = payload.getOrDefault("sender", "Anonymous").trim();
        String text = payload.getOrDefault("text", "").trim();

        if (sender.isEmpty()) {
            sender = "Anonymous";
        }

        Map<String, Object> response = new HashMap<>();
        if (text.isEmpty()) {
            response.put("status", "error");
            response.put("message", "Message text cannot be empty.");
            return response;
        }

        // Limit in-memory message history list size
        if (messages.size() > 50) {
            messages.remove(1);
        }

        Map<String, Object> newMsg = new HashMap<>();
        newMsg.put("sender", sender);
        newMsg.put("text", text);
        newMsg.put("timestamp", System.currentTimeMillis());
        messages.add(newMsg);

        // Print message to console/logs
        System.out.println("[MESSAGE BOARD] Sender: " + sender + " | Text: " + text);

        response.put("status", "success");
        response.put("message", "Message posted successfully.");
        return response;
    }

    /* PAYMENT ENDPOINTS */

    @GetMapping("/api/payments/history")
    public List<Map<String, Object>> getTransactionHistory() {
        return transactions;
    }

    @PostMapping("/api/payments/charge")
    public Map<String, Object> chargePayment(@RequestBody Map<String, String> payload) {
        String sender = payload.getOrDefault("sender", "Anonymous").trim();
        String amount = payload.getOrDefault("amount", "0.00").trim();
        String method = payload.getOrDefault("method", "UPI").trim();

        if (sender.isEmpty()) {
            sender = "Anonymous";
        }

        // Clean amount value
        try {
            double amtVal = Double.parseDouble(amount);
            amount = String.format(Locale.US, "%.2f", amtVal);
        } catch (NumberFormatException e) {
            amount = "0.00";
        }

        // Determine Status: 85% success rate, mock fail if amount is <= 0
        String status = "SUCCESS";
        if (Double.parseDouble(amount) <= 0.0) {
            status = "FAILED";
        } else if (new Random().nextDouble() > 0.85) {
            status = "FAILED";
        }

        String txnId = "TXN-" + String.format("%06d", new Random().nextInt(1000000));
        long timestamp = System.currentTimeMillis();

        Map<String, Object> transaction = new HashMap<>();
        transaction.put("txnId", txnId);
        transaction.put("sender", sender);
        transaction.put("amount", amount);
        transaction.put("method", method);
        transaction.put("status", status);
        transaction.put("timestamp", timestamp);

        // Limit transactions list size
        if (transactions.size() > 50) {
            transactions.remove(0);
        }
        transactions.add(transaction);

        // Print transaction details to console terminal logs
        System.out.println("[PAYMENT TRANSACTION] ID: " + txnId + " | Status: " + status + " | Customer: " + sender + " | Amount: ₹" + amount + " | Method: " + method);

        return transaction;
    }
}
