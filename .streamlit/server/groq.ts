import fetch from "node-fetch";

// The GROQ API key
const GROQ_API_KEY = process.env.GROQ_API_KEY || "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";
const GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions";

// Helper function to get chat history from storage
import { storage } from "./storage";

/**
 * Send a message to GROQ API and get a response
 * @param message The user's message
 * @param sessionId The session ID for context
 * @returns The AI assistant's response
 */
export async function chatWithGroq(message: string, sessionId: string): Promise<string> {
  try {
    // Get previous messages for context
    const previousMessages = await storage.getMessagesBySessionId(sessionId);
    
    // Format messages for GROQ API
    const messages = [
      {
        role: "system",
        content: `You are FinChat, a specialized AI assistant focused exclusively on personal finance topics.
Your expertise includes:
- Money management and budgeting
- Investment strategies and financial planning
- Tax information and advice
- Finance news and market trends
- Credit, debt management, and loans
- Retirement planning
- Insurance

Guidelines:
1. Provide accurate, helpful information on financial topics.
2. If asked about non-financial topics, politely redirect the conversation to finance.
3. Use clear, concise language that is easy to understand.
4. When appropriate, structure your responses with bullet points for readability.
5. Always disclose that your advice is informational only and not professional financial advice.
6. Stay current with general financial concepts.
7. For very specific tax or investment questions, recommend consulting with a certified professional.`
      },
      ...previousMessages.map(msg => ({
        role: msg.role,
        content: msg.content
      })),
      {
        role: "user",
        content: message
      }
    ];

    // Call GROQ API
    const response = await fetch(GROQ_API_URL, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${GROQ_API_KEY}`
      },
      body: JSON.stringify({
        model: "llama3-70b-8192",
        messages,
        temperature: 0.7,
        max_tokens: 1024,
      })
    });

    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(`GROQ API error: ${response.status} ${errorText}`);
    }

    const data = await response.json() as any;
    return data.choices[0].message.content;
  } catch (error) {
    console.error("Error calling GROQ API:", error);
    throw new Error("Failed to get response from AI. Please try again later.");
  }
}
