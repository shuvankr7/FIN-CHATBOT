import { useState, useEffect, useRef } from "react";
import { ChatInterface } from "@/components/chat-interface";
import { useToast } from "@/hooks/use-toast";
import { useChat } from "@/hooks/use-chat";

export default function Chat() {
  const { toast } = useToast();
  const { 
    messages, 
    isLoading, 
    sendMessage, 
    error 
  } = useChat();

  // Show error toast if there's an error
  useEffect(() => {
    if (error) {
      toast({
        title: "Error",
        description: error.message || "Failed to send message. Please try again.",
        variant: "destructive",
      });
    }
  }, [error, toast]);

  return (
    <div className="flex flex-col h-screen">
      {/* Header */}
      <header className="bg-primary shadow-md">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center">
              <svg xmlns="http://www.w3.org/2000/svg" className="h-8 w-8 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <h1 className="ml-2 text-xl font-semibold text-white">FinChat</h1>
            </div>
            <div>
              <span className="inline-flex items-center px-3 py-0.5 rounded-full text-sm font-medium bg-primary-100 text-primary-900">
                Finance AI Assistant
              </span>
            </div>
          </div>
        </div>
      </header>

      {/* Chat Interface */}
      <ChatInterface 
        messages={messages} 
        isLoading={isLoading}
        onSendMessage={sendMessage}
      />
    </div>
  );
}
