let token = localStorage.getItem("access_token");
console.log(token);

if (!token) {
    alert("You must log in first!");
    window.location.href = "auth.html";
}

document.getElementById('backToChatsBtn').onclick = () => {
    window.location.href = 'chat_list.html';
};


const urlParams = new URLSearchParams(window.location.search);
const chatId = urlParams.get('chat_id') || 1;


async function fetchChatName() {
    try {
        const res = await fetch(`/chat/${chatId}`, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });

        if (!res.ok) {
            console.error("Failed to fetch chat name:", res.status);
            window.location.href = "chat_list.html";
            return;
        }

        const data = await res.json();

        const chatTitle = document.getElementById("chatTitle");
        chatTitle.textContent = `Chat - ${data.chat_name}`;

    } catch (err) {
        alert(`Error fetching chat name: ${err}`);
        window.location.href = "chat_list.html";
    }
}

fetchChatName();


document.getElementById('addUserBtn').onclick = async () => {
    const newUserId = window.prompt("Enter the User ID of the person you want to add:");

    if (!newUserId || newUserId.trim() === "") return;

    const userIdInt = parseInt(newUserId);
    if (isNaN(userIdInt)) {
        alert("Please enter a valid numeric User ID.");
        return;
    }

    try {
        const res = await fetch("/chat/add", {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({ 
                chat_id: parseInt(chatId), 
                new_user_id: userIdInt 
            })
        });

        const data = await res.json();

        if (!res.ok) {
            alert(`Failed to add user: ${data.detail || "Unknown error"}`);
            return;
        }

        alert(data.message);

    } catch (err) {
        alert(`Network error: ${err.message}`);
    }
};


document.getElementById('meBtn').onclick = async () => {
    try {
        const res = await fetch("/auth/me", {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });

        const data = await res.json();

        if (!res.ok) {
            alert(`Error: ${data.detail || "Could not retrieve user info"}`);
            
            if (res.status === 401) {
                window.location.href = "auth.html";
            }
            return;
        }

        alert(`Your User ID is: ${data.user_id}`);

    } catch (err) {
        alert(`Network error: ${err.message}`);
    }
};


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

    const container = document.getElementById('messages');

    const isNearBottom =
        container.scrollTop + container.clientHeight >= container.scrollHeight - 20;

    const res = await fetch(`/chat/messages?after_id=${lastMessageId}&chat_id=${chatId}`, {
        headers: {
            'Authorization': `Bearer ${token}`
        }
    });

    if (!res.ok) {
        console.error("Fetch failed", res.status);
        alert("An error occured! Please re-login");
        window.location.href = "auth.html";
    }

    const data = await res.json();
    const messages = data.messages;

    messages.forEach(msg => {
        const div = document.createElement('div');
        div.classList.add('msg');

        div.innerHTML = `
            <strong>${msg.sender_username}</strong>: ${msg.content}
            <span class="timestamp">${msg.created_at}</span>
        `;

        container.appendChild(div);
        lastMessageId = msg.id;
    });

    if (isNearBottom) {
        container.scrollTop = container.scrollHeight;
    }
}


setInterval(fetchMessages, 500);
