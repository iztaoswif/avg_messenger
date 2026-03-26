document.getElementById('loginForm').onsubmit = async (e) => {
    e.preventDefault();
    const username = document.getElementById('loginUsername').value;
    const password = document.getElementById('loginPassword').value;

    const formData = new URLSearchParams();
    formData.append('username', username);
    formData.append('password', password);

    try {
        const res = await fetch('/auth/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
            body: formData
        });

        if (!res.ok) throw new Error(`Login failed: ${res.status}`);
        const data = await res.json();
        localStorage.setItem('access_token', data.access_token);
        alert('Logged in! Token stored.');

        window.location.href = 'chat.html';

    } catch (err) {
        alert(err);
        console.error(err);
    }
}

document.getElementById('registerForm').onsubmit = async (e) => {
    e.preventDefault();
    const username = document.getElementById('regUsername').value;
    const password = document.getElementById('regPassword').value;

    try {
        const res = await fetch('/auth/register', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, password })
        });

        if (!res.ok) throw new Error(`Register failed: ${res.status}`);
        const data = await res.json();
        alert(data.message || 'Registered successfully!');

    } catch (err) {
        alert(err);
        console.error(err);
    }
}
