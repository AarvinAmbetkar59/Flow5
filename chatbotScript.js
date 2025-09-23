const messageInput = document.getElementById("messageInput");
const chatMessages = document.getElementById("chatMessages");
const sendButton = document.getElementById("sendButton");

// ---------------------------
// Helpers
// ---------------------------
function appendMessage(sender, text, isSchemes = false, schemes = []) {
  const msgDiv = document.createElement("div");
  msgDiv.classList.add("message", sender);
  
  if (isSchemes && schemes.length > 0) {
    let schemesHtml = `<div class="message-text">${text.replace(/\n/g, '<br>')}</div><div class="schemes-container">`;
    schemes.forEach((scheme, index) => {
      schemesHtml += `
        <div class="scheme-card">
          <div class="scheme-header">
            <span class="scheme-number">#${index + 1}</span>
            <span class="scheme-name">${scheme.name}</span>
            ${scheme.score > 0 ? `<span class="match-score">Score: ${scheme.score}</span>` : ''}
          </div>
          <div class="scheme-id">ID: ${scheme.id} | Category: ${scheme.category}</div>
          <div class="scheme-benefits">💎 ${scheme.benefits}</div>
        </div>`;
    });
    schemesHtml += `</div>`;
    msgDiv.innerHTML = schemesHtml;
  } else {
    msgDiv.innerHTML = `<div class="message-text">${text.replace(/\n/g, '<br>')}</div>`;
  }
  
  chatMessages.appendChild(msgDiv);
  chatMessages.scrollTop = chatMessages.scrollHeight;
}

function showTypingIndicator() {
  const typingDiv = document.createElement("div");
  typingDiv.classList.add("message", "bot", "typing");
  typingDiv.innerHTML = `
    <div class="typing-dots">
      <div class="dot"></div>
      <div class="dot"></div>
      <div class="dot"></div>
    </div>`;
  chatMessages.appendChild(typingDiv);
  chatMessages.scrollTop = chatMessages.scrollHeight;
  return typingDiv;
}

function removeTypingIndicator() {
  const typingDiv = chatMessages.querySelector(".typing");
  if (typingDiv) {
    typingDiv.remove();
  }
}

// ---------------------------
// Main send handler
// ---------------------------
async function sendMessage() {
  const input = messageInput.value.trim();
  if (!input) return;

  appendMessage("user", input);
  messageInput.value = "";

  const typingIndicator = showTypingIndicator();

  try {
    const response = await fetch("http://127.0.0.1:5000/chat", {
      method: "POST",
      headers: { 
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ message: input })
    });
    const data = await response.json();

    removeTypingIndicator();

    if (data.type === "schemes" && data.schemes && data.schemes.length > 0) {
      appendMessage("bot", data.reply, true, data.schemes);
      
      setTimeout(() => {
        appendMessage("bot", "Want to know more about any specific scheme? Just ask me about it by name!");
      }, 1000);
    } else {
      appendMessage("bot", data.reply);
    }
  } catch (err) {
    removeTypingIndicator();
    console.error(err);
    appendMessage("bot", "Oops! Something went wrong. Please try again later.");
  }
}

// ---------------------------
// Event handlers
// ---------------------------
function handleKeyPress(event) {
  if (event.key === "Enter") {
    sendMessage();
  }
}

// ---------------------------
// Initialize
// ---------------------------
window.addEventListener("load", () => {
  appendMessage("bot", "🤖Hello! I'm SchemeBot - your friendly government scheme assistant!\n\n 💬I can help you with information about government schemes in our database.\n\n✨Type 'schemes' to see all available schemes.  Please choose a language to proceed in!");
  messageInput.focus();
});