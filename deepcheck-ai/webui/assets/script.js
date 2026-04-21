document.addEventListener('DOMContentLoaded', () => {
    const path = window.location.pathname;

    if (path.includes('/Chat/')) {
        initChat();
    } else if (path.includes('/Admin/')) {
        initAdmin();
    }
});

/* --- AUTH LOGIC --- */
function handleLogin(e) {
    e.preventDefault();
    const btn = e.target.querySelector('button');
    btn.innerHTML = '<i class="ph ph-spinner ph-spin"></i> Iniciando...';
    btn.style.opacity = '0.8';
    setTimeout(() => { window.location.href = '../Info/index.html'; }, 1500);
}

function handleRegister(e) {
    e.preventDefault();
    const btn = e.target.querySelector('button');
    btn.innerHTML = '<i class="ph ph-spinner ph-spin"></i> Creando cuenta...';
    setTimeout(() => {
        alert('Cuenta creada con éxito.');
        window.location.href = '../Acceso/index.html';
    }, 1500);
}

function handleAdminLogin(e) {
    e.preventDefault();
    const btn = e.target.querySelector('button');
    btn.innerHTML = '<i class="ph ph-spinner ph-spin"></i> Verificando...';
    btn.style.opacity = '0.8';
    setTimeout(() => {
        // Show warning modal
        const modal = document.getElementById('admin-warning-modal');
        if (modal) {
            modal.showModal();
        }
    }, 1500);
}

function closeAdminWarning() {
    const modal = document.getElementById('admin-warning-modal');
    if (modal) {
        modal.close();
    }
    // Redirect to dashboard after closing
    setTimeout(() => {
        window.location.href = 'dashboard.html';
    }, 300);
}

/* --- CHAT LOGIC --- */
function initChat() {
    const input = document.getElementById('chat-input');
    const sendBtn = document.getElementById('send-btn');
    const inputWrapper = document.querySelector('.input-area-wrapper');

    // Start centered
    if (inputWrapper) inputWrapper.classList.add('centered');

    window.autoResize = function (el) {
        el.style.height = 'auto';
        el.style.height = el.scrollHeight + 'px';
        if (el.value.trim().length > 0) sendBtn.classList.add('active');
        else sendBtn.classList.remove('active');
    };

    input.addEventListener('focus', () => {
        // Move to bottom on focus
        if (inputWrapper) inputWrapper.classList.remove('centered');
    });

    input.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });
}

function toggleDropdown() {
    document.getElementById('model-dropdown').classList.toggle('show');
}

function selectModel(name) {
    document.getElementById('selected-model').innerText = name;
    document.querySelectorAll('.dropdown-item').forEach(item => item.classList.remove('active'));
    event.currentTarget.classList.add('active');
    toggleDropdown();
}

function openHelpModal() { document.getElementById('help-modal').showModal(); }
function closeHelpModal() { document.getElementById('help-modal').close(); }

function sendMessage() {
    const input = document.getElementById('chat-input');
    const text = input.value.trim();
    if (!text) return;

    const inputWrapper = document.querySelector('.input-area-wrapper');
    if (inputWrapper) inputWrapper.classList.remove('centered');

    appendMessage('user', text);
    input.value = '';
    input.style.height = 'auto';
    document.getElementById('send-btn').classList.remove('active');

    const loadingId = appendLoading();
    scrollToBottom();

    setTimeout(() => {
        removeMessage(loadingId);
        const response = generateMockResponse(text);
        appendMessage('ai', response);
        scrollToBottom();
    }, 2000);
}

function appendMessage(role, text) {
    const container = document.getElementById('chat-container');
    const div = document.createElement('div');
    div.className = `message ${role}-message`;
    const avatar = role === 'ai' ? '<i class="ph-fill ph-shield-check"></i>' : '<i class="ph-fill ph-user"></i>';
    const content = role === 'ai' && window.marked ? marked.parse(text) : text;
    div.innerHTML = `<div class="message-avatar">${avatar}</div><div class="message-content">${content}</div>`;
    container.appendChild(div);
    return div.id;
}

function appendLoading() {
    const container = document.getElementById('chat-container');
    const div = document.createElement('div');
    div.className = 'message ai-message';
    div.id = 'loading-' + Date.now();
    div.innerHTML = `<div class="message-avatar"><i class="ph-fill ph-shield-check"></i></div><div class="message-content"><i class="ph ph-dots-three ph-beat" style="font-size: 1.5rem;"></i></div>`;
    container.appendChild(div);
    return div.id;
}

function removeMessage(id) { const el = document.getElementById(id); if (el) el.remove(); }
function scrollToBottom() { const container = document.getElementById('chat-container'); container.scrollTop = container.scrollHeight; }

function startNewChat() {
    const container = document.getElementById('chat-container');
    container.innerHTML = ''; // Clear chat
    document.getElementById('drawer-toggle').checked = false;
    // Reset to center
    const inputWrapper = document.querySelector('.input-area-wrapper');
    if (inputWrapper) inputWrapper.classList.add('centered');
}

function generateMockResponse(input) {
    const responses = [
        "Entendido. Analizando los logs del sistema...",
        "Para configurar la red en Docker Compose, usa `networks`...",
        "He escaneado el código y todo parece correcto.",
        "Aquí tienes un ejemplo de configuración de Nginx..."
    ];
    return responses[Math.floor(Math.random() * responses.length)];
}

/* --- ADMIN LOGIC --- */
function initAdmin() {
    // Chart Init
    const ctx = document.getElementById('serverChart');
    if (ctx) {
        new Chart(ctx, {
            type: 'line',
            data: {
                labels: ['10:00', '10:05', '10:10', '10:15', '10:20', '10:25'],
                datasets: [{
                    label: 'CPU',
                    data: [45, 50, 48, 65, 78, 72],
                    borderColor: '#4f46e5',
                    backgroundColor: 'rgba(79, 70, 229, 0.1)',
                    fill: true,
                    tension: 0.4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: { legend: { display: false } },
                scales: {
                    y: { grid: { color: '#e2e8f0' }, ticks: { color: '#64748b' } },
                    x: { grid: { display: false }, ticks: { color: '#64748b' } }
                }
            }
        });
    }

    // Tab Navigation Logic
    const navItems = document.querySelectorAll('.nav-item[data-view]');
    navItems.forEach(item => {
        item.addEventListener('click', (e) => {
            e.preventDefault();
            const viewId = item.getAttribute('data-view');

            // Update Nav
            navItems.forEach(n => n.classList.remove('active'));
            item.classList.add('active');

            // Update View
            document.querySelectorAll('.admin-view').forEach(v => v.classList.remove('active'));
            document.getElementById(viewId).classList.add('active');
        });
    });
}
