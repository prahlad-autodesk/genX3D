// ChatAssistant.js: Simple floating chat assistant dialog for Cascade Studio
(function() {
  const container = document.getElementById('chat-assistant-container');
  if (!container) return;

  container.innerHTML = `
    <div id="chat-assistant-header">💬 Assistant <button id="chat-assistant-toggle-btn" style="float:right;background:none;border:none;color:#fff;font-size:18px;cursor:pointer;">&#8211;</button></div>
    <div id="chat-assistant-messages"></div>
    <div id="chat-assistant-input-row">
      <input id="chat-assistant-input" type="text" placeholder="Ask me anything..." autocomplete="off" />
      <button id="chat-assistant-send-btn">Send</button>
    </div>
  `;

  const messagesDiv = document.getElementById('chat-assistant-messages');
  const input = document.getElementById('chat-assistant-input');
  const sendBtn = document.getElementById('chat-assistant-send-btn');
  const toggleBtn = document.getElementById('chat-assistant-toggle-btn');

  let minimized = false;
  toggleBtn.onclick = function() {
    minimized = !minimized;
    if (minimized) {
      messagesDiv.style.display = 'none';
      document.getElementById('chat-assistant-input-row').style.display = 'none';
      toggleBtn.innerHTML = '&#9633;'; // maximize icon
    } else {
      messagesDiv.style.display = '';
      document.getElementById('chat-assistant-input-row').style.display = '';
      toggleBtn.innerHTML = '&#8211;'; // minimize icon
    }
  };

  function appendMessage(text, from) {
    const msg = document.createElement('div');
    msg.style.margin = '8px 0';
    msg.style.whiteSpace = 'pre-wrap';
    msg.style.wordBreak = 'break-word';
    msg.innerHTML = `<b style='color:${from==="user"?"#4CAF50":"#fff"}'>${from === "user" ? "You" : "Assistant"}:</b> ${text}`;
    messagesDiv.appendChild(msg);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
  }

  function handleSend() {
    const text = input.value.trim();
    if (!text) return;
    appendMessage(text, 'user');
    input.value = '';
    // Show loading indicator
    appendMessage('...', 'assistant');
    // Call backend endpoint
    // fetch('https://genx3d.onrender.com/graph_chat', {
    fetch('http://localhost:8000/graph_chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: text })
    })
    .then(res => res.json())
    .then(data => {
      // Remove loading indicator
      const msgs = messagesDiv.querySelectorAll('div');
      if (msgs.length > 0 && msgs[msgs.length-1].innerText.startsWith('Assistant: ...')) {
        messagesDiv.removeChild(msgs[msgs.length-1]);
      }
      // Show assistant message
      let assistantMsg = '[No response]';
      if (typeof data.response === 'string') {
        assistantMsg = data.response;
      } else if (typeof data.response === 'object' && data.response.text) {
        assistantMsg = data.response.text;
      }
      appendMessage(assistantMsg, 'assistant');

            // If GenBot or CADBot, load the model in the viewer
      if ((data.agent === "GenBot" || data.agent === "CADBot") && data.response) {
        appendMessage('🔄 Loading model into viewer...', 'assistant');
        let modelUrl = null;
        let ext = 'stl';
        
        // Debug: Log the raw response
        console.log('Raw response data:', data.response);
        console.log('Response type:', typeof data.response);
        
        // Parse the response to get model URLs
        let responseData = data.response;
        if (typeof data.response === 'string') {
          try {
            responseData = JSON.parse(data.response);
            console.log('Parsed JSON response:', responseData);
          } catch (e) {
            console.log('Failed to parse JSON, treating as string URL');
            // If it's not JSON, treat as simple string URL
            modelUrl = data.response;
          }
        } else {
          console.log('Response is already an object:', responseData);
        }
        
        // Handle our new RAG response format with STEP URL only
        if (responseData && responseData.step_url) {
          // Use STEP files for better CAD compatibility
          modelUrl = responseData.step_url;
          ext = 'step';
          console.log('Loading RAG-generated model:', responseData);
          console.log('Selected STEP URL:', modelUrl);
        } else if (responseData && responseData.model_url) {
          // Fallback to old format
          modelUrl = responseData.model_url;
          ext = responseData.model_type || 'step';
          console.log('Using fallback model URL:', modelUrl);
        } else {
          console.log('No valid model URL found in response');
        }
        
        // Wait for functions to be available and clear existing external files
        const waitForFunctions = () => {
          if (typeof clearExternalFiles === 'function') {
            console.log('Clearing existing external files...');
            clearExternalFiles();
            return true;
          } else if (window.clearExternalFiles) {
            console.log('Clearing existing external files via window...');
            window.clearExternalFiles();
            return true;
          } else {
            console.log('clearExternalFiles function not found, waiting...');
            return false;
          }
        };
        
        // Try to clear files, retry if not available
        let clearAttempts = 0;
        const maxClearAttempts = 10;
        const clearWithRetry = () => {
          if (waitForFunctions()) {
            return;
          }
          if (clearAttempts < maxClearAttempts) {
            clearAttempts++;
            setTimeout(clearWithRetry, 100);
          } else {
            console.log('clearExternalFiles function not available after retries, continuing without clearing');
          }
        };
        clearWithRetry();
        
        if (modelUrl) {
          // Add base URL if it's a relative path
          if (modelUrl.startsWith('/')) {
            // Use backend server URL instead of frontend origin
            modelUrl = 'http://localhost:8000' + modelUrl;
          }
          
          console.log('Final model URL to fetch:', modelUrl);
          console.log('Fetching model from:', modelUrl);
          
          // Small delay to ensure clearing operation completes
          setTimeout(() => {
            fetch(modelUrl)
            .then(res => {
              if (!res.ok) {
                throw new Error(`HTTP ${res.status}: ${res.statusText}`);
              }
              return res.blob();
            })
            .then(blob => {
              // Determine file extension from MIME type or URL
              if (blob.type.includes('step') || modelUrl.includes('.step')) ext = 'step';
              else if (blob.type.includes('stl') || modelUrl.includes('.stl')) ext = 'stl';
              else if (blob.type.includes('obj') || modelUrl.includes('.obj')) ext = 'obj';
              
              const fileName = `rag_model_${Date.now()}.${ext}`;
              const file = new File([blob], fileName, { type: blob.type });
              
              console.log('Created file:', fileName, 'Size:', blob.size, 'bytes');
              
              // Create a unique file input for each model to avoid caching issues
              const uniqueId = `genbot-model-input-${Date.now()}`;
              let fileInput = document.createElement('input');
              fileInput.type = 'file';
              fileInput.id = uniqueId;
              fileInput.style.display = 'none';
              document.body.appendChild(fileInput);
              
              // Clean up old file inputs to prevent memory leaks
              const oldInputs = document.querySelectorAll('[id^="genbot-model-input-"]');
              oldInputs.forEach(input => {
                if (input.id !== uniqueId) {
                  input.remove();
                }
              });
              
              // Set up the input with the file
              const dataTransfer = new DataTransfer();
              dataTransfer.items.add(file);
              fileInput.files = dataTransfer.files;
              
              console.log('File input setup complete:');
              console.log('- File input ID:', uniqueId);
              console.log('- File input files length:', fileInput.files.length);
              console.log('- File name:', fileInput.files[0]?.name);
              console.log('- File size:', fileInput.files[0]?.size);
              console.log('- File type:', fileInput.files[0]?.type);
              
              // Call the Cascade Studio loadFiles function with retry
              const callLoadFiles = () => {
                if (typeof loadFiles === 'function') {
                  console.log('Calling loadFiles function directly');
                  loadFiles(uniqueId);
                  return true;
                } else if (window.loadFiles) {
                  console.log('Calling loadFiles function via window');
                  window.loadFiles(uniqueId);
                  return true;
                } else {
                  console.log('loadFiles function not found, waiting...');
                  return false;
                }
              };
              
              let loadAttempts = 0;
              const maxLoadAttempts = 10;
              const loadWithRetry = () => {
                if (callLoadFiles()) {
                  return;
                }
                if (loadAttempts < maxLoadAttempts) {
                  loadAttempts++;
                  setTimeout(loadWithRetry, 100);
                } else {
                  console.error('loadFiles function not available after retries!');
                  console.log('Available global functions:', Object.keys(window).filter(key => typeof window[key] === 'function'));
                  // Try to find the function in the global scope
                  if (typeof cascadeStudioWorker !== 'undefined') {
                    console.log('cascadeStudioWorker found, trying alternative loading method');
                    // Try to trigger file loading through the worker
                    cascadeStudioWorker.postMessage({
                      "type": "loadFiles",
                      "payload": fileInput.files
                    });
                  }
                }
              };
              loadWithRetry();
              
              // After loading, fit the model to view
              if (window.messageHandlers && typeof window.messageHandlers.fitToView === 'function') {
                setTimeout(() => {
                  window.messageHandlers.fitToView();
                  console.log('Model loaded and fitted to view');
                  // Remove loading message and add success message
                  const msgs = messagesDiv.querySelectorAll('div');
                  if (msgs.length > 0 && msgs[msgs.length-1].innerText.includes('🔄 Loading model')) {
                    messagesDiv.removeChild(msgs[msgs.length-1]);
                  }
                  appendMessage('✅ Model loaded successfully! You can now view and interact with it in the 3D viewer.', 'assistant');
                }, 1000); // Increased delay to ensure model is fully loaded
              }
            })
            .catch(err => {
              console.error('Error loading model:', err);
              // Remove loading message
              const msgs = messagesDiv.querySelectorAll('div');
              if (msgs.length > 0 && msgs[msgs.length-1].innerText.includes('🔄 Loading model')) {
                messagesDiv.removeChild(msgs[msgs.length-1]);
              }
              appendMessage(`❌ Error loading model: ${err.message}`, 'assistant');
            });
          }, 100); // 100ms delay to ensure clearing completes
        }
      }
    })
    .catch(err => {
      // Remove loading indicator
      const msgs = messagesDiv.querySelectorAll('div');
      if (msgs.length > 0 && msgs[msgs.length-1].innerText.startsWith('Assistant: ...')) {
        messagesDiv.removeChild(msgs[msgs.length-1]);
      }
      appendMessage('Error contacting backend.', 'assistant');
    });
  }

  sendBtn.onclick = handleSend;
  input.onkeydown = function(e) {
    if (e.key === 'Enter') handleSend();
  };
})(); 