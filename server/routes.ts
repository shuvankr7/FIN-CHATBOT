import type { Express } from "express";
import { createServer, type Server } from "http";
import { storage } from "./storage";
import { z } from "zod";
import { chatWithGroq } from "./groq";
import { insertMessageSchema } from "@shared/schema";
import { nanoid } from "nanoid";

export async function registerRoutes(app: Express): Promise<Server> {
  // API route for chat
  app.post("/api/chat", async (req, res) => {
    try {
      // Validate request body
      const schema = z.object({
        message: z.string().min(1),
        sessionId: z.string().min(1),
      });

      const result = schema.safeParse(req.body);
      if (!result.success) {
        return res.status(400).json({ 
          message: "Invalid request body", 
          errors: result.error.format() 
        });
      }

      const { message, sessionId } = result.data;

      // Store user message
      await storage.createMessage({
        content: message,
        role: "user",
        sessionId,
      });

      // Get response from GROQ
      const response = await chatWithGroq(message, sessionId);

      // Store assistant response
      await storage.createMessage({
        content: response,
        role: "assistant",
        sessionId,
      });

      // Send response
      res.json({
        content: response,
        sessionId,
      });
    } catch (error) {
      console.error("Error in chat API:", error);
      res.status(500).json({ 
        message: "Failed to process chat message",
        error: error instanceof Error ? error.message : "Unknown error"
      });
    }
  });

  // API route to get message history for a session
  app.get("/api/messages", async (req, res) => {
    try {
      const sessionId = req.query.sessionId as string;
      
      if (!sessionId) {
        return res.status(400).json({ message: "sessionId is required" });
      }

      const messages = await storage.getMessagesBySessionId(sessionId);
      res.json(messages);
    } catch (error) {
      console.error("Error fetching messages:", error);
      res.status(500).json({ 
        message: "Failed to fetch message history",
        error: error instanceof Error ? error.message : "Unknown error"
      });
    }
  });

  const httpServer = createServer(app);
  return httpServer;
}
