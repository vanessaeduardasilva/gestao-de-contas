let contasGlobais = [];

document.addEventListener('DOMContentLoaded', () => {
    const accountForm = document.getElementById('account-form');

    if (accountForm) {
        carregarContas();

        accountForm.addEventListener('submit', async (e) => {
            e.preventDefault();

            const dados = {
                descricao: document.getElementById('descricao').value,
                valor: document.getElementById('valor').value,
                data: document.getElementById('data').value,
                modalidade: document.getElementById('modalidade').value,
                usuario_id: 2
            };

            try {
                const response = await fetch('http://127.0.0.1:5000/api/contas', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(dados)
                });

                const result = await response.json();

                if (!response.ok || result.success === false) {
                    throw new Error(result.error || 'Erro desconhecido');
                }

                accountForm.reset();
                carregarContas();

            } catch (error) {
                alert("Erro ao salvar: " + error.message);
            }
        });
    }

    const userForm = document.getElementById('user-form');

    if (userForm) {
        userForm.addEventListener('submit', async (e) => {
            e.preventDefault();

            const dados = {
                nome: document.getElementById('user-nome').value,
                email: document.getElementById('user-email').value
            };

            try {
                const response = await fetch('http://127.0.0.1:5000/api/usuarios', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(dados)
                });

                const result = await response.json();

                if (!response.ok || result.success === false) {
                    throw new Error(result.error || 'Erro desconhecido');
                }

                window.location.href = '/conta.html';

            } catch (error) {
                alert("Erro ao vincular conta: " + error.message);
            }
        });
    }
});

async function carregarContas() {
    try {
        const response = await fetch('http://127.0.0.1:5000/api/contas/2');
        contasGlobais = await response.json();
        renderizarTabela(contasGlobais);
    } catch (error) {
        console.error("Erro ao carregar contas:", error);
    }
}

function renderizarTabela(contas) {
    const tbody = document.getElementById('table-body');
    tbody.innerHTML = "";

    const seletor = document.getElementById('filtro-mes');
    const mesSelecionado = seletor ? seletor.value : new Date().toISOString().slice(0, 7);

    const contasFiltradas = contas.filter(c => c.vencimento.slice(0, 7) === mesSelecionado);

    let totalMes = 0;
    let vencendoHoje = 0;
    const hojeStr = new Date().toISOString().split('T')[0];

    contasFiltradas.forEach(conta => {
        totalMes += conta.valor;
        if (conta.vencimento === hojeStr) vencendoHoje++;
    });

    document.getElementById('total-mes').textContent =
        `R$ ${totalMes.toFixed(2).replace('.', ',')}`;
    document.getElementById('total-vencendo').textContent = vencendoHoje;

    if (!contasFiltradas.length) {
        tbody.innerHTML = `
            <tr>
                <td colspan="5" style="text-align:center;">
                    Nenhuma conta neste mês
                </td>
            </tr>
        `;
        return;
    }

    contasFiltradas.forEach(conta => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td>${conta.descricao}</td>
            <td>${formatarData(conta.vencimento)}</td>
            <td>R$ ${conta.valor.toFixed(2).replace('.', ',')}</td>
            <td>${conta.tipo}</td>
            <td>
                <button onclick="deletarConta(${conta.id})"
                    style="background:none; border:none; color:#e74c3c; cursor:pointer; font-size:16px;">
                    ✕
                </button>
            </td>
        `;
        tbody.appendChild(tr);
    });
}

function filtrar(tipo) {
    if (tipo === 'todas') {
        renderizarTabela(contasGlobais);
    } else {
        const filtradas = contasGlobais.filter(c => c.tipo === tipo);
        renderizarTabela(filtradas);
    }
}

function formatarData(dataISO) {
    return new Date(dataISO).toLocaleDateString('pt-BR');
}

function toggleParcelas() {
    const tipo = document.getElementById('modalidade').value;
    document.getElementById('group-parcelas').style.display =
        tipo === 'parcelada' ? 'block' : 'none';
}

async function deletarConta(id) {
    if (!confirm("Deseja deletar esta conta?")) return;

    try {
        const response = await fetch(`http://127.0.0.1:5000/api/contas/${id}`, {
            method: 'DELETE'
        });

        const result = await response.json();

        if (result.success) {
            carregarContas();
        } else {
            alert("Erro ao deletar: " + result.error);
        }
    } catch (error) {
        alert("Erro ao deletar: " + error.message);
    }
}