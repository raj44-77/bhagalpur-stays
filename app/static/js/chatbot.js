// Bhagalpur Stays - AI Chatbot
(function() {
  var widget = document.createElement('div');
  widget.id = 'chatbot-widget';
  widget.innerHTML = `
    <button class="chatbot-toggle" onclick="toggleChat()" title="Chat with us">💬</button>
    <div class="chatbot-box" id="chatbot-box">
      <div class="chatbot-header">
        <div>
          <h4>Bhagalpur Stays AI</h4>
          <small>🟢 Online · Ask me anything!</small>
        </div>
        <button class="close-btn" onclick="toggleChat()">✕</button>
      </div>
      <div class="chatbot-messages" id="chatbot-messages"></div>
      <div class="chatbot-suggestions" id="chatbot-suggestions">
        <button onclick="sendQuickReply('🏨 Show luxury hotels')">🏨 Luxury Hotels</button>
        <button onclick="sendQuickReply('💰 Budget stays')">💰 Budget Stays</button>
        <button onclick="sendQuickReply('🏛️ Places to visit')">🏛️ Places to visit</button>
        <button onclick="sendQuickReply('📞 Customer support')">📞 Support</button>
      </div>
      <div class="chatbot-input">
        <input type="text" id="chatbot-input" placeholder="Ask me anything..." onkeypress="if(event.key==='Enter')sendMessage()">
        <button onclick="sendMessage()"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="18" height="18"><line x1="22" y1="2" x2="11" y2="13"/><polygon points="22 2 15 22 11 13 2 9 22 2"/></svg></button>
      </div>
    </div>`;
  document.body.appendChild(widget);

  // Add CSS
  var link = document.createElement('link');
  link.rel = 'stylesheet';
  link.href = '../static/css/chatbot.css';
  document.head.appendChild(link);

  // Greeting
  setTimeout(function() {
    addMessage('bot', '👋 <b>Namaste!</b> I\'m your Bhagalpur Stays assistant. I can help you find hotels, suggest places to visit, or answer questions about Silk City!');
  }, 1000);
})();

function toggleChat() {
  var box = document.getElementById('chatbot-box');
  box.classList.toggle('open');
  if (box.classList.contains('open')) {
    document.getElementById('chatbot-input').focus();
  }
}

function sendQuickReply(text) {
  document.getElementById('chatbot-input').value = text;
  sendMessage();
}

function addMessage(type, html) {
  var msgs = document.getElementById('chatbot-messages');
  var div = document.createElement('div');
  div.className = 'chatbot-msg ' + type;
  div.innerHTML = html;
  msgs.appendChild(div);
  msgs.scrollTop = msgs.scrollHeight;
}

function showTyping() {
  var msgs = document.getElementById('chatbot-messages');
  var div = document.createElement('div');
  div.className = 'chatbot-msg bot';
  div.id = 'typing-indicator';
  div.innerHTML = '<div class="chatbot-typing"><span></span><span></span><span></span></div>';
  msgs.appendChild(div);
  msgs.scrollTop = msgs.scrollHeight;
}

function hideTyping() {
  var typing = document.getElementById('typing-indicator');
  if (typing) typing.remove();
}

async function sendMessage() {
  var input = document.getElementById('chatbot-input');
  var msg = input.value.trim();
  if (!msg) return;
  
  addMessage('user', msg);
  input.value = '';
  showTyping();

  var response = await getAIResponse(msg);
  
  hideTyping();
  addMessage('bot', response);
}

async function getAIResponse(msg) {
  var lower = msg.toLowerCase();

  // Hotel search patterns
  if (lower.includes('luxury') || lower.includes('5 star') || lower.includes('premium')) {
    try {
      var res = await fetch('/api/hotels/?limit=4');
      var data = await res.json();
      var hotels = data.hotels || [];
      var luxury = hotels.filter(function(h) { return h.star_rating >= 4; });
      if (luxury.length > 0) {
        var html = '🏨 <b>Top luxury hotels in Bhagalpur:</b><br><br>';
        for (var i = 0; i < Math.min(luxury.length, 4); i++) {
          html += '⭐ <a href="/hotel-details?slug=' + (luxury[i].slug || luxury[i].id) + '">' + luxury[i].name + '</a> — ' + luxury[i].star_rating + ' Star<br>';
        }
        html += '<br><a href="/hotels" class="btn btn-primary btn-sm">View All Hotels →</a>';
        return html;
      }
    } catch(e) {}
    return 'Let me find luxury hotels for you. <a href="/hotels">Browse all hotels →</a>';
  }

  if (lower.includes('budget') || lower.includes('cheap') || lower.includes('affordable') || lower.includes('low price')) {
    try {
      var res = await fetch('/api/hotels/?limit=8');
      var data = await res.json();
      var hotels = data.hotels || [];
      var budget = hotels.filter(function(h) { return h.star_rating <= 3; });
      if (budget.length > 0) {
        var html = '💰 <b>Budget-friendly stays:</b><br><br>';
        for (var i = 0; i < Math.min(budget.length, 4); i++) {
          html += '🏨 <a href="/hotel-details?slug=' + (budget[i].slug || budget[i].id) + '">' + budget[i].name + '</a><br>';
        }
        html += '<br><a href="/hotels" class="btn btn-primary btn-sm">View All Hotels →</a>';
        return html;
      }
    } catch(e) {}
    return 'Check our budget options. <a href="/hotels">Browse hotels →</a>';
  }

  if (lower.includes('hotel') || lower.includes('stay') || lower.includes('room') || lower.includes('book')) {
    try {
      var res = await fetch('/api/hotels/?limit=6');
      var data = await res.json();
      var hotels = data.hotels || [];
      if (hotels.length > 0) {
        var html = '🏨 <b>Here are our hotels:</b><br><br>';
        for (var i = 0; i < Math.min(hotels.length, 4); i++) {
          html += '• <a href="/hotel-details?slug=' + (hotels[i].slug || hotels[i].id) + '">' + hotels[i].name + '</a> — ' + hotels[i].star_rating + ' ★<br>';
        }
        html += '<br><a href="/hotels" class="btn btn-primary btn-sm">Browse All →</a>';
        return html;
      }
    } catch(e) {}
    return 'Browse our verified hotels. <a href="/hotels">Click here →</a>';
  }

  // Local attractions
  if (lower.includes('visit') || lower.includes('place') || lower.includes('sight') || lower.includes('attraction') || lower.includes('tourist') || lower.includes('travel')) {
    return '🏛️ <b>Must-visit places in Bhagalpur:</b><br><br>' +
      '🕍 <b>Vikramshila University</b> — Ancient Buddhist ruins (38 km)<br>' +
      '🛕 <b>Ajgaibinath Temple</b> — Rock-cut Shiva temple, Sultanganj<br>' +
      '⛰️ <b>Mandar Hill</b> — Mythological hill with panoramic views<br>' +
      '🕉️ <b>Budhanath Temple</b> — Riverside Shiva temple<br>' +
      '🌊 <b>Kuppa Ghat</b> — Serene Ganga ghat, Barari<br>' +
      '🐬 <b>Dolphin Sanctuary</b> — Gangetic dolphins, Vikramshila<br><br>' +
      '<a href="/travel-guide">📖 Full Travel Guide →</a>';
  }

  // Silk City
  if (lower.includes('silk') || lower.includes('fabric') || lower.includes('textile') || lower.includes('weaving')) {
    return '🧵 <b>Bhagalpur — The Silk City!</b><br><br>' +
      'Bhagalpur is world-famous for <b>Tussar silk</b>. The silk industry here is over 200 years old and employs thousands of families.<br><br>' +
      'Visit the silk market to see weavers at work and buy authentic handloom products.<br><br>' +
      '<a href="/travel-guide">📖 Read more →</a>';
  }

  // Food
  if (lower.includes('food') || lower.includes('eat') || lower.includes('cuisine') || lower.includes('dish') || lower.includes('restaurant')) {
    return '🍽️ <b>Local Bhagalpuri delicacies:</b><br><br>' +
      '🥘 <b>Litti Chokha</b> — Baked wheat balls with roasted veggies<br>' +
      '🍚 <b>Sattu Paratha</b> — Gram flour stuffed flatbread<br>' +
      '🍬 <b>Khaja</b> — Flaky sweet pastry<br>' +
      '🍵 <b>Malpua</b> — Sweet fried pancakes<br><br>' +
      '<a href="/travel-guide">📖 Full Food Guide →</a>';
  }

  // Support
  if (lower.includes('support') || lower.includes('help') || lower.includes('complain') || lower.includes('issue') || lower.includes('contact') || lower.includes('phone') || lower.includes('call')) {
    return '📞 <b>Customer Support</b><br><br>' +
      '📱 <b>Phone:</b> +91 800 123 4567<br>' +
      '✉️ <b>Email:</b> hello@bhagalpurstays.com<br>' +
      '🕐 <b>Hours:</b> 24×7 Hindi & English<br>' +
      '📍 <b>Office:</b> Silk Plaza, Adampur, Bhagalpur<br><br>' +
      '<a href="/contact">📧 Contact Us →</a> | <a href="/faq">❓ FAQs →</a>';
  }

  // Booking help
  if (lower.includes('cancel') || lower.includes('refund') || lower.includes('modify')) {
    return '📋 <b>Booking Help:</b><br><br>' +
      '✅ <b>Free cancellation</b> up to 24 hours before check-in<br>' +
      '💵 <b>Refunds</b> processed within 5-7 business days<br>' +
      '🔄 <b>Modify booking</b> from <a href="/my-bookings">My Bookings</a> page<br><br>' +
      'Need more help? <a href="/contact">Contact Support →</a>';
  }

  // Greetings
  if (lower.match(/^(hi|hello|hey|namaste|hola)/)) {
    return '👋 <b>Namaste!</b> Welcome to Bhagalpur Stays!<br><br>I can help you:<br>🏨 Find hotels<br>🏛️ Discover local attractions<br>📞 Get customer support<br>❓ Answer FAQs<br><br>Just ask me anything!';
  }

  // Thanks
  if (lower.includes('thank') || lower.includes('thanks') || lower.includes('dhanyavad')) {
    return '🙏 You\'re welcome! Enjoy your stay in <b>Silk City</b>! Need anything else?';
  }

  // Default
  return 'I can help you with:<br><br>' +
    '🏨 <b>"Show me hotels"</b> — Browse stays<br>' +
    '💰 <b>"Budget hotels"</b> — Affordable options<br>' +
    '🏛️ <b>"Places to visit"</b> — Local attractions<br>' +
    '📞 <b>"Customer support"</b> — Get help<br>' +
    '🍽️ <b>"Local food"</b> — Bhagalpuri cuisine<br><br>' +
    'What would you like to know?';
}