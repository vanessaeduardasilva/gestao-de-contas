/**
 * ORGANIZERION - CORE ENGINE
 */

document.addEventListener('DOMContentLoaded', () => {
    // 1. Inicializa a lógica de usuário
    initPaginaUsuario();
    
    // 2. Verifica se estamos no Dashboard
    const isDashboard = document.getElementById('ACCOUNT-FORM') || 
                        document.getElementById('account-form') || 
                        window.location.pathname.includes('conta.html');

    if (isDashboard) {
        exibirBoasVindas();
        if (typeof initPaginaContas === "function") {
            initPaginaContas();
        }
    }
});

// --- LÓGICA DE USUÁRIO (VÍNCULO COM GOOGLE) ---

async function initPaginaUsuario() {
    const form = document.getElementById('user-form');
    if (!form) return;

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const btn = form.querySelector('button');
        const originalText = btn.innerText;
        btn.innerText = "ABRINDO LOGIN GOOGLE..."; 
        btn.disabled = true;

        const nome = document.getElementById('user-nome').value;
        const email = document.getElementById('user-email').value;

        try {
            // ROTA CORRETA: /api/vincular para ativar o main.py no Python
            const response = await fetch('http://localhost:5000/api/vincular', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ nome, email })
            });

            if (response.ok) {
                localStorage.setItem('organizerion_user', JSON.stringify({
                    id: Date.now(),
                    nome: nome,
                    email: email
                }));
                // Redireciona para o dashboard após o Python abrir o navegador
                window.location.href = 'conta.html';
            } else {
                throw new Error("Falha na comunicação com o servidor.");
            }

        } catch (error) {
            console.error("Erro:", error);
            // Fallback apenas salva local se o servidor estiver realmente offline
            localStorage.setItem('organizerion_user', JSON.stringify({
                id: Date.now(),
                nome: nome
            }));
            window.location.href = 'conta.html';
        }
    });
}

function exibirBoasVindas() {
    const dadosRaw = localStorage.getItem('organizerion_user');
    if (!dadosRaw) return;

    const dados = JSON.parse(dadosRaw);
    const navLogo = document.querySelector('.nav-logo'); 

    if (dados && dados.nome && navLogo) {
        if (document.getElementById('user-welcome-msg')) return;

        const userDisplay = document.createElement('span');
        userDisplay.id = 'user-welcome-msg';
        userDisplay.style.cssText = "margin-left: 15px; font-size: 0.85rem; color: var(--text-muted); font-weight: 400; text-transform: none;";
        userDisplay.innerHTML = `| Olá, <strong>${dados.nome.split(' ')[0]}</strong>`;
        navLogo.appendChild(userDisplay);
    }
}