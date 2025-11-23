import { useState, useRef, useEffect } from 'react';
import {
  Button,
  TextArea,
  Loading,
} from '@carbon/react';
import { Send, Close, Chat } from '@carbon/icons-react';
import axios from 'axios';
import { API_ENDPOINTS } from '../config/api';
import './ChatClient.scss';

const ChatClient = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSendMessage = async () => {
    if (!input.trim() || isLoading) return;

    const userMessage = {
      role: 'user',
      content: input,
      timestamp: new Date().toISOString(),
    };

    setMessages(prev => [...prev, userMessage]);
    const currentInput = input;
    setInput('');
    setIsLoading(true);

    try {
      const response = await axios.get('https://pink-fish-chat.up.railway.app/chat/v2', {
        params: {
          query: currentInput
        }
      });

      const assistantMessage = {
        role: 'assistant',
        content: response.data.response || response.data.message || response.data || 'No response',
        timestamp: new Date().toISOString(),
      };

      setMessages(prev => [...prev, assistantMessage]);
    } catch (error) {
      console.error('Chat error:', error);
      const errorMessage = {
        role: 'assistant',
        content: 'Sorry, I encountered an error. Please try again.',
        timestamp: new Date().toISOString(),
        isError: true,
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  return (
    <>
      {/* Chat Toggle Button */}
      {!isOpen && (
        <Button
          className="chat-toggle-btn"
          renderIcon={Chat}
          kind="primary"
          size="lg"
          onClick={() => setIsOpen(true)}
          aria-label="Open chat"
        >
          Chat with PlantOps AI
        </Button>
      )}

      {/* Chat Window */}
      {isOpen && (
        <div className="chat-client">
          <div className="chat-header">
            <div className="chat-header-content">
              <Chat size={20} />
              <h4>PlantOps AI Assistant</h4>
            </div>
            <Button
              hasIconOnly
              renderIcon={Close}
              iconDescription="Close chat"
              kind="ghost"
              size="sm"
              onClick={() => setIsOpen(false)}
            />
          </div>

          <div className="chat-messages">
            {messages.length === 0 && (
              <div className="chat-welcome">
                <Chat size={32} />
                <p>Hello! I'm your PlantOps AI Assistant.</p>
                <p>Ask me anything about your plant operations, zones, or energy usage.</p>
              </div>
            )}
            
            {messages.map((msg, index) => (
              <div
                key={index}
                className={`chat-message ${msg.role} ${msg.isError ? 'error' : ''}`}
              >
                <div className="message-content">
                  <p>{msg.content}</p>
                  <span className="message-time">
                    {new Date(msg.timestamp).toLocaleTimeString([], {
                      hour: '2-digit',
                      minute: '2-digit',
                    })}
                  </span>
                </div>
              </div>
            ))}
            
            {isLoading && (
              <div className="chat-message assistant loading-message">
                <Loading small withOverlay={false} />
                <span>Thinking...</span>
              </div>
            )}
            
            <div ref={messagesEndRef} />
          </div>

          <div className="chat-input-container">
            <TextArea
              id="chat-input"
              labelText=""
              placeholder="Ask about your plant operations..."
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyPress={handleKeyPress}
              rows={2}
              disabled={isLoading}
            />
            <Button
              renderIcon={Send}
              kind="primary"
              onClick={handleSendMessage}
              disabled={!input.trim() || isLoading}
              hasIconOnly
              iconDescription="Send message"
              size="lg"
            />
          </div>
        </div>
      )}
    </>
  );
};

export default ChatClient;
