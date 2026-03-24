const token = localStorage.getItem("access_token");

if (!token) {
    alert("You must log in first!");
    window.location.href = "auth.html";
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
        console.error(err);
    }
}

window.addEventListener('DOMContentLoaded', fetchChats);
