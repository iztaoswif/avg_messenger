let token = localStorage.getItem("access_token");
console.log(token);

if (!token) {
    alert("You must log in first!");
    window.location.href = "auth.html";
}

const urlParams = new URLSearchParams(window.location.search);
const chatId = urlParams.get('chat_id') || 1;

let lastMessageId = 0;

document.getElementById('chatForm').onsubmit = async (e) => {
    e.preventDefault();

    const content = document.getElementById('msgInput').value;

    const res = await fetch("/chat/send", {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({ chat_id: parseInt(chatId), content: content })
    });

    const data = await res.json();
    console.log(data);

    document.getElementById('msgInput').value = '';
};

async function fetchMessages() {

    const res = await fetch(`/chat/messages?after_id=${lastMessageId}&chat_id=${chatId}`, {
        headers: {
            'Authorization': `Bearer ${token}`
        }
    });

    if (!res.ok) {
        console.error("Fetch failed", res.status);
        return;
    }

    const data = await res.json();
    const messages = data.messages;
    const container = document.getElementById('messages');

    messages.forEach(msg => {

        const div = document.createElement('div');
        div.classList.add('msg');

        div.innerHTML =
            `<strong>${msg.sender_username}</strong>: ${msg.content}
            <span class="timestamp">${msg.created_at}</span>`;

        container.appendChild(div);

        lastMessageId = msg.id;
    });

    container.scrollTop = container.scrollHeight;
}

setInterval(fetchMessages, 500);
