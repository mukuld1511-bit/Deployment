package com.example.demo;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.CommandLineRunner;
import org.springframework.web.bind.annotation.*;
import java.lang.management.ManagementFactory;
import java.util.*;

@RestController
@CrossOrigin(origins = "*")
public class HelloController implements CommandLineRunner {

    private final long startupTime = System.currentTimeMillis();

    @Autowired
    private MessageRepository messageRepository;

    @Autowired
    private TransactionRepository transactionRepository;

    // Seed default data on first startup if DB is empty
    @Override
    public void run(String... args) {
        if (messageRepository.count() == 0) {
            messageRepository.save(new Message("System Console", "Welcome to Cloud Deployment Console. MongoDB connected successfully.", System.currentTimeMillis()));
        }
        if (transactionRepository.count() == 0) {
            transactionRepository.save(new Transaction("TXN-" + String.format("%06d", new Random().nextInt(1000000)), "Alice Smith", "150.00", "Credit Card", "SUCCESS", System.currentTimeMillis() - 600000));
            transactionRepository.save(new Transaction("TXN-" + String.format("%06d", new Random().nextInt(1000000)), "Bob Jones", "45.00", "UPI", "SUCCESS", System.currentTimeMillis() - 300000));
            transactionRepository.save(new Transaction("TXN-" + String.format("%06d", new Random().nextInt(1000000)), "Charlie Brown", "500.00", "NetBanking", "FAILED", System.currentTimeMillis() - 150000));
        }
    }

    @GetMapping("/api/hello")
    public Map<String, Object> hello() {
        Map<String, Object> response = new HashMap<>();
        response.put("status", "success");
        response.put("message", "Hello from Maven, Docker, MongoDB, and Spring Boot!");
        response.put("database", "MongoDB connected");
        response.put("timestamp", System.currentTimeMillis());
        return response;
    }

    @GetMapping("/api/system-stats")
    public Map<String, Object> getSystemStats() {
        Map<String, Object> stats = new HashMap<>();

        // Memory metrics
        Runtime runtime = Runtime.getRuntime();
        long totalMemory = runtime.totalMemory();
        long freeMemory = runtime.freeMemory();
        long usedMemory = totalMemory - freeMemory;

        stats.put("usedMemoryMb", usedMemory / (1024 * 1024));
        stats.put("totalMemoryMb", totalMemory / (1024 * 1024));
        stats.put("maxMemoryMb", runtime.maxMemory() / (1024 * 1024));

        // CPU load
        double systemLoad = ManagementFactory.getOperatingSystemMXBean().getSystemLoadAverage();
        if (systemLoad < 0) {
            systemLoad = 5.0 + (Math.random() * 20.0);
        } else {
            systemLoad = systemLoad * 100.0;
        }
        stats.put("cpuLoad", Math.round(systemLoad * 10.0) / 10.0);

        // Uptime
        long uptimeMs = System.currentTimeMillis() - startupTime;
        stats.put("uptimeSeconds", uptimeMs / 1000);

        stats.put("detectedUrl", "http://localhost:8080");
        stats.put("osName", System.getProperty("os.name"));
        stats.put("osVersion", System.getProperty("os.version"));
        stats.put("javaVersion", System.getProperty("java.version"));

        // MongoDB stats
        stats.put("totalMessages", messageRepository.count());
        stats.put("totalTransactions", transactionRepository.count());

        return stats;
    }

    /* MESSAGE ENDPOINTS */

    @GetMapping("/api/messages")
    public List<Message> getMessages() {
        return messageRepository.findAllByOrderByTimestampAsc();
    }

    @PostMapping("/api/messages")
    public Map<String, Object> postMessage(@RequestBody Map<String, String> payload) {
        String sender = payload.getOrDefault("sender", "Anonymous").trim();
        String text = payload.getOrDefault("text", "").trim();

        if (sender.isEmpty()) sender = "Anonymous";

        Map<String, Object> response = new HashMap<>();
        if (text.isEmpty()) {
            response.put("status", "error");
            response.put("message", "Message text cannot be empty.");
            return response;
        }

        Message msg = new Message(sender, text, System.currentTimeMillis());
        messageRepository.save(msg);

        // Print to console/logs
        System.out.println("[MESSAGE BOARD] Sender: " + sender + " | Text: " + text);

        response.put("status", "success");
        response.put("message", "Message saved to MongoDB.");
        return response;
    }

    /* PAYMENT ENDPOINTS */

    @GetMapping("/api/payments/history")
    public List<Transaction> getTransactionHistory() {
        return transactionRepository.findAllByOrderByTimestampDesc();
    }

    @PostMapping("/api/payments/charge")
    public Transaction chargePayment(@RequestBody Map<String, String> payload) {
        String sender = payload.getOrDefault("sender", "Anonymous").trim();
        String amount = payload.getOrDefault("amount", "0.00").trim();
        String method = payload.getOrDefault("method", "UPI").trim();

        if (sender.isEmpty()) sender = "Anonymous";

        // Clean amount value
        try {
            double amtVal = Double.parseDouble(amount);
            amount = String.format(Locale.US, "%.2f", amtVal);
        } catch (NumberFormatException e) {
            amount = "0.00";
        }

        // Determine Status: 85% success rate, fail if amount <= 0
        String status = "SUCCESS";
        if (Double.parseDouble(amount) <= 0.0) {
            status = "FAILED";
        } else if (new Random().nextDouble() > 0.85) {
            status = "FAILED";
        }

        String txnId = "TXN-" + String.format("%06d", new Random().nextInt(1000000));
        long timestamp = System.currentTimeMillis();

        Transaction transaction = new Transaction(txnId, sender, amount, method, status, timestamp);
        transactionRepository.save(transaction);

        // Print transaction details to console terminal logs
        System.out.println("[PAYMENT TRANSACTION] ID: " + txnId + " | Status: " + status + " | Customer: " + sender + " | Amount: ₹" + amount + " | Method: " + method);

        return transaction;
    }
}
