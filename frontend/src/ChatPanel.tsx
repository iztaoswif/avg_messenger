import { createSignal, Show, For } from 'solid-js';

const token = localStorage.getItem("access_token");

if (!token) {
    alert("You must log in first!");
    window.location.href = "index.html";
}

// Refetch key signal to trigger data reload on new chat creation
const [refetchKey, setRefetchKey] = createSignal(0);

// Fetch logic integrated directly into Solid's async reactive system
const chatsData = createAsync(async () => {
    refetchKey(); // Tracks changes to force a re-fetch
    const res = await fetch('/chat/list', {
    headers: {
        'Authorization': `Bearer ${token}`,
        'Accept': 'application/json'
    }
    });

    if (!res.ok) {
    throw new Error(`Failed to fetch chats: ${res.status}`);
    }

    const data = await res.json();
    return data.chats || [];
});

const handleCreateChat = async () => {
    const chatName = window.prompt("Enter a name for your new chat:");
    if (!chatName || !chatName.trim()) return;

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

    // Trigger re-fetch by updating signal state
    setRefetchKey(k => k + 1);
    } catch (err) {
    alert(`Network error: ${err.message}`);
    }
};


const ChatPanel = () => (


return (
    <main style={{ "max-width": "600px", margin: "40px auto", "font-family": "Arial, sans-serif" }}>
    <h1 style={{ "text-align": "center" }}>Your Chats</h1>

    <div class="actions" style={{ "text-align": "right", "margin-bottom": "20px" }}>
        <button id="createChatBtn" onClick={handleCreateChat}>
        + New Chat
        </button>
    </div>

    <div id="content">
        <Show 
        when={!chatsData.error} 
        fallback={<p class="error">{chatsData.error?.message}</p>}
        >
        <Show 
            when={chatsData()} 
            fallback={<p>Loading chats...</p>}
        >
            {(chats) => (
            <Show 
                when={chats().length > 0} 
                fallback={<p>No chats found.</p>}
            >
                <ul style={{ padding: 0, "list-style": "none" }}>
                <For each={chats()}>
                    {(chat) => (
                    <li 
                        onClick={() => window.location.href = `chat.html?chat_id=${chat.id}`}
                        style={{
                        padding: "15px",
                        margin: "5px 0",
                        background: "#f2f2f2",
                        "border-radius": "6px",
                        cursor: "pointer",
                        border: "1px solid #ddd"
                        }}
                    >
                        {chat.name}
                    </li>
                    )}
                </For>
                </ul>
            </Show>
            )}
        </Show>
        </Show>
    </div>
    </main>
);
)