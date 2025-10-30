import React, { useState, useRef, useEffect } from 'react';
import styled from 'styled-components';
import { Send, Minimize2, MessageCircle } from 'lucide-react';
import toast from 'react-hot-toast';
import axios from 'axios';
import { getApiUrl, getModelUrl } from '../config';

const ChatContainer = styled.div`
  position: fixed;
  bottom: 20px;
  right: 20px;
  width: 350px;
  height: 500px;
  background: #2a2a2a;
  border: 1px solid #444;
  border-radius: 8px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
  display: flex;
  flex-direction: column;
  z-index: 1000;
  font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
`;

const ChatHeader = styled.div`
  background: #333;
  color: white;
  padding: 12px 16px;
  border-radius: 8px 8px 0 0;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid #444;
`;

const ChatTitle = styled.div`
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 600;
`;

const MinimizedChat = styled.div`
  position: fixed;
  bottom: 20px;
  right: 20px;
  width: 60px;
  height: 60px;
  background: #4CAF50;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
  z-index: 1000;
  transition: all 0.3s ease;

  &:hover {
    transform: scale(1.1);
    background: #45a049;
  }
`;

const MessagesContainer = styled.div`
  flex: 1;
  padding: 16px;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 12px;
  background: #1a1a1a;

  &::-webkit-scrollbar {
    width: 6px;
  }

  &::-webkit-scrollbar-track {
    background: #2a2a2a;
  }

  &::-webkit-scrollbar-thumb {
    background: #555;
    border-radius: 3px;
  }
`;

const Message = styled.div`
  padding: 12px 16px;
  border-radius: 8px;
  max-width: 80%;
  word-wrap: break-word;
  white-space: pre-wrap;
  font-size: 14px;
  line-height: 1.4;

  ${props => props.$isUser ? `
    background: #4CAF50;
    color: white;
    align-self: flex-end;
    margin-left: auto;
  ` : `
    background: #333;
    color: #fff;
    align-self: flex-start;
    margin-right: auto;
  `}
`;

const InputContainer = styled.div`
  padding: 16px;
  border-top: 1px solid #444;
  background: #2a2a2a;
  border-radius: 0 0 8px 8px;
  display: flex;
  gap: 8px;
`;

const Input = styled.input`
  flex: 1;
  padding: 12px;
  border: 1px solid #555;
  border-radius: 6px;
  background: #1a1a1a;
  color: white;
  font-family: inherit;
  font-size: 14px;

  &:focus {
    outline: none;
    border-color: #4CAF50;
  }

  &::placeholder {
    color: #888;
  }
`;

const SendButton = styled.button`
  padding: 12px 16px;
  background: #4CAF50;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background 0.3s ease;

  &:hover {
    background: #45a049;
  }

  &:disabled {
    background: #666;
    cursor: not-allowed;
  }
`;

const LoadingMessage = styled.div`
  padding: 12px 16px;
  background: #333;
  color: #fff;
  border-radius: 8px;
  align-self: flex-start;
  margin-right: auto;
  font-style: italic;
  opacity: 0.7;
`;

const ChatAssistant = () => {
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [isMinimized, setIsMinimized] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSend = async () => {
    const message = inputValue.trim();
    if (!message || isLoading) return;

    // Add user message
    const userMessage = { text: message, isUser: true, timestamp: new Date() };
    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);

    try {
      // Send to backend
      const response = await axios.post(getApiUrl('/graph_chat'), { message });
      
      if (response.data.success) {
        const assistantResponse = response.data.response;
        
        // Parse the response
        let responseText = '';
        let modelData = null;

        if (typeof assistantResponse === 'string') {
          try {
            const parsed = JSON.parse(assistantResponse);
            responseText = parsed.text || parsed.error || assistantResponse;
            modelData = parsed;
          } catch {
            responseText = assistantResponse;
          }
        } else {
          responseText = assistantResponse.text || assistantResponse.error || 'No response';
          modelData = assistantResponse;
        }

        // Add assistant message
        const assistantMessage = { 
          text: responseText, 
          isUser: false, 
          timestamp: new Date(),
          modelData 
        };
        setMessages(prev => [...prev, assistantMessage]);

        // Handle model loading if present
        if (modelData && (modelData.step_url || modelData.stl_url)) {
          const modelUrl = modelData.step_url || modelData.stl_url;
          const modelType = modelData.step_url ? 'step' : 'stl';
          
          console.log('Model data received:', modelData);
          console.log('Model URL:', modelUrl);
          console.log('Model type:', modelType);
          
          // Trigger model loading
          window.dispatchEvent(new CustomEvent('loadModel', {
            detail: {
              model: {
                url: getModelUrl(modelUrl),
                type: modelType,
                modelId: modelData.model_id,
                prompt: message,
                modelType: modelData.model_type,
                similarityScore: modelData.similarity_score
              }
            }
          }));

          toast.success('3D model loaded successfully!');
        } else {
          console.log('No model data in response:', modelData);
        }
      } else {
        throw new Error(response.data.error || 'Unknown error');
      }
    } catch (error) {
      console.error('Chat error:', error);
      const errorMessage = { 
        text: `Error: ${error.message || 'Failed to get response'}`, 
        isUser: false, 
        timestamp: new Date() 
      };
      setMessages(prev => [...prev, errorMessage]);
      toast.error('Failed to get response from server');
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const formatTimestamp = (timestamp) => {
    return timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  if (isMinimized) {
    return (
      <MinimizedChat onClick={() => setIsMinimized(false)}>
        <MessageCircle size={24} color="white" />
      </MinimizedChat>
    );
  }

  return (
    <ChatContainer>
      <ChatHeader>
        <ChatTitle>
          <MessageCircle size={16} />
          💬 Assistant
        </ChatTitle>
        <button
          onClick={() => setIsMinimized(true)}
          style={{
            background: 'none',
            border: 'none',
            color: 'white',
            cursor: 'pointer',
            padding: '4px'
          }}
        >
          <Minimize2 size={16} />
        </button>
      </ChatHeader>

      <MessagesContainer>
        {messages.map((message, index) => (
          <Message key={index} $isUser={message.isUser}>
            <div>{message.text}</div>
            <div style={{ fontSize: '10px', opacity: 0.7, marginTop: '4px' }}>
              {formatTimestamp(message.timestamp)}
            </div>
          </Message>
        ))}
        
        {isLoading && (
          <LoadingMessage>
            Thinking...
          </LoadingMessage>
        )}
        
        <div ref={messagesEndRef} />
      </MessagesContainer>

      <InputContainer>
        <Input
          ref={inputRef}
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder="Ask me anything..."
          disabled={isLoading}
        />
        <SendButton onClick={handleSend} disabled={isLoading || !inputValue.trim()}>
          <Send size={16} />
        </SendButton>
      </InputContainer>
    </ChatContainer>
  );
};

export default ChatAssistant; 