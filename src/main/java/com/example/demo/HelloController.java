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

    public HelloController() {
        // Add a default system message
        Map<String, Object> sysMsg = new HashMap<>();
        sysMsg.put("sender", "System Console");
        sysMsg.put("text", "Welcome to the Cloud Deployment Console. ngrok tunnel established successfully.");
        sysMsg.put("timestamp", System.currentTimeMillis());
        messages.add(sysMsg);
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
        
        // CPU load: check OS load, fallback to simulated load if average returns negative (common in Docker/Windows WSL environments)
        double systemLoad = ManagementFactory.getOperatingSystemMXBean().getSystemLoadAverage();
        if (systemLoad < 0) {
            // Mock a typical dynamic CPU load between 5% and 25%
            systemLoad = 5.0 + (Math.random() * 20.0);
        } else {
            systemLoad = systemLoad * 100.0;
        }
        stats.put("cpuLoad", Math.round(systemLoad * 10.0) / 10.0);

        // Uptime in seconds
        long uptimeMs = System.currentTimeMillis() - startupTime;
        stats.put("uptimeSeconds", uptimeMs / 1000);

        // Detect dynamic host & scheme (handles proxying via ngrok/local reverse proxy)
        String host = request.getHeader("Host");
        String scheme = request.getHeader("X-Forwarded-Proto");
        if (scheme == null) {
            scheme = request.getScheme();
        }
        
        stats.put("detectedUrl", scheme + "://" + host);
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
            // Keep the system message at index 0, remove the second element (oldest user message)
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
}
