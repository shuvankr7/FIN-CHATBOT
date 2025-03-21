import { useState, useCallback, useEffect } from "react";
import { v4 as uuidv4 } from "uuid";
import { sendChatMessage } from "@/lib/api";
import type { ChatMessage } from "@shared/schema";

export function useChat() {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<Error | null>(null);
  const [sessionId, setSessionId] = useState("");

  // Initialize session ID
  useEffect(() => {
    const storedSessionId = localStorage.getItem("chatSessionId");
    if (storedSessionId) {
      setSessionId(storedSessionId);
    } else {
      const newSessionId = uuidv4();
      localStorage.setItem("chatSessionId", newSessionId);
      setSessionId(newSessionId);
    }
  }, []);

  // Load saved messages for this session
  useEffect(() => {
    if (sessionId) {
      const fetchMessages = async () => {
        try {
          const response = await fetch(`/api/messages?sessionId=${sessionId}`);
          if (!response.ok) {
            throw new Error("Failed to fetch messages history");
          }
          const data = await response.json();
          setMessages(data);
        } catch (err) {
          console.error("Error fetching messages:", err);
          // Don't set error state here, we'll just start with empty messages
        }
      };

      fetchMessages();
    }
  }, [sessionId]);

  const sendMessage = useCallback(async (content: string) => {
    if (!content.trim() || !sessionId) return;
    
    setIsLoading(true);
    setError(null);
    
    // Add user message immediately
    const userMessage: ChatMessage = {
      id: uuidv4(),
      content,
      role: "user",
      createdAt: new Date()
    };
    
    setMessages(prev => [...prev, userMessage]);
    
    try {
      // Send to API
      const response = await sendChatMessage(content, sessionId);
      
      // Add assistant response
      setMessages(prev => [...prev, {
        id: uuidv4(),
        content: response.content,
        role: "assistant",
        createdAt: new Date()
      }]);
    } catch (err) {
      console.error("Error sending message:", err);
      setError(err instanceof Error ? err : new Error("Failed to send message"));
    } finally {
      setIsLoading(false);
    }
  }, [sessionId]);

  return {
    messages,
    isLoading,
    error,
    sendMessage
  };
}
