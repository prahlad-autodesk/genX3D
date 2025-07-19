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
      appendMessage(data.response || '[No response]', 'assistant');
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