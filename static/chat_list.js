const token = localStorage.getItem("access_token");

if (!token) {
    alert("You must log in first!");
    window.location.href = "index.html";
}


async function fetchChats() {
    const contentDiv = document.getElementById('content');

    try {
        const res = await fetch('/chat/list', {
            headers: { 
                'Authorization': `Bearer ${token}`,
                'Accept': 'application/json'
            }
        });

        if (!res.ok) {
            contentDiv.innerHTML = `<p class="error">Failed to fetch chats: ${res.status}</p>`;
            return;
        }

        const data = await res.json();

        if (!data.chats || data.chats.length === 0) {
            contentDiv.innerHTML = `<p>No chats found.</p>`;
            return;
        }

        const ul = document.createElement('ul');

        data.chats.forEach(chat => {
            const li = document.createElement('li');
            li.textContent = chat.name;

            li.onclick = () => {
                window.location.href = `chat.html?chat_id=${chat.id}`;
            }

            ul.appendChild(li);
        });

        contentDiv.innerHTML = '';
        contentDiv.appendChild(ul);

    } catch (err) {
        contentDiv.innerHTML = `<p class="error">Error: ${err.message}</p>`;
        console.error("Fetch Error:", err);
    }
}


window.addEventListener('DOMContentLoaded', () => {
    fetchChats();

    const createBtn = document.getElementById('createChatBtn');
    if (createBtn) {
        createBtn.onclick = async () => {
            const chatName = window.prompt("Enter a name for your new chat:");

            if (!chatName || chatName.trim() === "") return;

            try {
                const res = await fetch("/chat/create", {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${token}`
                    },
                    body: JSON.stringify({ name: chatName.trim() })
                });

                const data = await res.json();

                if (!res.ok) {
                    alert(`Could not create chat: ${data.detail || "Unknown error"}`);
                    return;
                }

                console.log("Success: Chat created", data);
                
                await fetchChats();

            } catch (err) {
                alert(`Network error: ${err.message}`);
            }
        };
    } else {
        console.warn("Element 'createChatBtn' not found in HTML.");
    }
});