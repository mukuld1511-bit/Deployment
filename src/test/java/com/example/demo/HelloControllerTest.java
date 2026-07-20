package com.example.demo;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

import java.util.Map;

class HelloControllerTest {

    @Test
    void testHelloEndpoint() {
        HelloController controller = new HelloController();
        Map<String, Object> response = controller.hello();

        assertEquals("success", response.get("status"));
        assertEquals("Hello from Maven, Docker, MongoDB, and Spring Boot!", response.get("message"));
        assertEquals("MongoDB connected", response.get("database"));
        assertNotNull(response.get("timestamp"));
    }
}
