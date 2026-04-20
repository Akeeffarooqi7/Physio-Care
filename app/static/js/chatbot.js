// ===== PhysioBot Chatbot =====
let chatSessionId = null;
let chatOpen = false;

function toggleChatbot() {
  chatOpen = !chatOpen;
  const panel = document.getElementById('chatbotPanel');
  const openIcon = document.getElementById('chatbotOpenIcon');
  const closeIcon = document.getElementById('chatbotCloseIcon');
  const badge = document.getElementById('chatbotBadge');

  if (chatOpen) {
    panel.classList.add('open');
    openIcon.classList.add('d-none');
    closeIcon.classList.remove('d-none');
    if (badge) badge.style.display = 'none';
    document.getElementById('chatbotInput').focus();
    scrollChat();
  } else {
    panel.classList.remove('open');
    openIcon.classList.remove('d-none');
    closeIcon.classList.add('d-none');
  }
}

function scrollChat() {
  const msgs = document.getElementById('chatbotMessages');
  if (msgs) msgs.scrollTop = msgs.scrollHeight;
}

async function sendChatMessage() {
  const input = document.getElementById('chatbotInput');
  const sendBtn = document.getElementById('chatSendBtn');
  const message = input.value.trim();
  if (!message) return;

  input.value = '';
  sendBtn.disabled = true;

  // Add user message
  addChatMessage('user', message);

  // Show typing indicator
  const typingId = showTyping();

  try {
    const res = await fetch('/api/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message, session_id: chatSessionId })
    });
    const data = await res.json();
    chatSessionId = data.session_id;

    // Remove typing, add bot message
    removeTyping(typingId);
    addChatMessage('bot', data.response);
  } catch (e) {
    removeTyping(typingId);
    addChatMessage('bot', 'Sorry, I\'m having trouble connecting. Please try again or call us at (555) 234-5678.');
  } finally {
    sendBtn.disabled = false;
    input.focus();
  }
}

function sendQuickReply(text) {
  document.getElementById('chatbotInput').value = text;
  sendChatMessage();
}

function addChatMessage(role, content) {
  const container = document.getElementById('chatbotMessages');
  const div = document.createElement('div');
  div.className = `chat-msg ${role}`;

  const avatarIcon = role === 'user' ? 'fa-user' : 'fa-robot';
  const formattedContent = formatMarkdown(content);

  div.innerHTML = `
    <div class="msg-avatar"><i class="fas ${avatarIcon}"></i></div>
    <div class="msg-bubble">${formattedContent}</div>`;
  container.appendChild(div);
  scrollChat();
}

function formatMarkdown(text) {
  // Bold
  text = text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
  // Italic
  text = text.replace(/\*(.*?)\*/g, '<em>$1</em>');
  // Bullet points
  text = text.replace(/^[•·]\s+(.+)$/gm, '<li>$1</li>');
  // Numbered list
  text = text.replace(/^\d+\.\s+(.+)$/gm, '<li>$1</li>');
  // Wrap consecutive li tags
  text = text.replace(/(<li>.*<\/li>(\n|))+/g, '<ul style="padding-left:16px;margin:6px 0">$&</ul>');
  // Emojis & line breaks
  text = text.replace(/\n\n/g, '</p><p>');
  text = text.replace(/\n/g, '<br>');
  if (!text.startsWith('<')) text = '<p>' + text + '</p>';
  return text;
}

function showTyping() {
  const container = document.getElementById('chatbotMessages');
  const id = 'typing-' + Date.now();
  const div = document.createElement('div');
  div.className = 'chat-msg bot';
  div.id = id;
  div.innerHTML = `
    <div class="msg-avatar"><i class="fas fa-robot"></i></div>
    <div class="msg-bubble" style="padding:8px 14px;">
      <div class="typing-indicator">
        <span></span><span></span><span></span>
      </div>
    </div>`;
  container.appendChild(div);
  scrollChat();
  return id;
}

function removeTyping(id) {
  const el = document.getElementById(id);
  if (el) el.remove();
}

// Keyboard shortcut to open chatbot
document.addEventListener('keydown', (e) => {
  if (e.key === '/' && !['INPUT', 'TEXTAREA'].includes(document.activeElement.tagName)) {
    e.preventDefault();
    if (!chatOpen) toggleChatbot();
    else document.getElementById('chatbotInput').focus();
  }
  if (e.key === 'Escape' && chatOpen) toggleChatbot();
});
