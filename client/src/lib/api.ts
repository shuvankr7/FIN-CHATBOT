import { apiRequest } from "./queryClient";

interface ChatResponse {
  content: string;
  sessionId: string;
}

export async function sendChatMessage(
  message: string,
  sessionId: string
): Promise<ChatResponse> {
  const response = await apiRequest("POST", "/api/chat", {
    message,
    sessionId,
  });
  
  return response.json();
}

export async function getMessageHistory(
  sessionId: string
): Promise<any[]> {
  const response = await apiRequest("GET", `/api/messages?sessionId=${sessionId}`, undefined);
  
  return response.json();
}
