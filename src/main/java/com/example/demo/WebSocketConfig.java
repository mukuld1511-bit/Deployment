package com.example.demo;

import org.springframework.context.annotation.Configuration;
import org.springframework.web.socket.config.annotation.*;

@Configuration
@EnableWebSocket
public class WebSocketConfig implements WebSocketConfigurer {

    private final RealtimeHandler realtimeHandler;

    public WebSocketConfig(RealtimeHandler realtimeHandler) {
        this.realtimeHandler = realtimeHandler;
    }

    @Override
    public void registerWebSocketHandlers(WebSocketHandlerRegistry registry) {
        registry.addHandler(realtimeHandler, "/ws-updates").setAllowedOrigins("*");
    }
}
