package com.example.demo;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;
import java.util.HashMap;
import java.util.Map;

@RestController
public class HelloController {

    @GetMapping("/api/hello")
    public Map<String, Object> hello() {
        Map<String, Object> response = new HashMap<>();
        response.put("status", "success");
        response.put("message", "Hello from Maven, Docker, and Spring Boot!");
        response.put("tunnel", "Exposed securely via ngrok");
        response.put("timestamp", System.currentTimeMillis());
        return response;
    }
}
