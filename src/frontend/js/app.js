/**
 * ORGANIZERION - CORE ENGINE (FINAL)
 */

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
});


// ============================
// BUSCAR CONTAS
// ============================
async function carregarContas() {
    try {
        const response = await fetch('http://127.0.0.1:5000/api/contas/2');
        contasGlobais = await response.json();
        renderizarTabela(contasGlobais);
    } catch (error) {
        console.error("Erro ao carregar contas:", error);
    }
}


// ============================
// RENDERIZAR TABELA
// ============================
function renderizarTabela(contas) {
    const tbody = document.getElementById('table-body');
    tbody.innerHTML = "";

    if (!contas.length) {
        tbody.innerHTML = `
            <tr>
                <td colspan="5" style="text-align:center;">
                    Nenhuma conta registrada
                </td>
            </tr>
        `;
        return;
    }

    contas.forEach(conta => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td>${conta.descricao}</td>
            <td>${formatarData(conta.vencimento)}</td>
            <td>R$ ${conta.valor.toFixed(2)}</td>
            <td>${conta.tipo}</td>
            <td></td>
        `;
        tbody.appendChild(tr);
    });
}


// ============================
// FILTROS
// ============================
function filtrar(tipo) {
    if (tipo === 'todas') {
        renderizarTabela(contasGlobais);
        return;
    }

    const filtradas = contasGlobais.filter(
        c => c.tipo === tipo
    );

    renderizarTabela(filtradas);
}


// ============================
// UTIL
// ============================
function formatarData(dataISO) {
    return new Date(dataISO).toLocaleDateString('pt-BR');
}


// ============================
// PARCELAS
// ============================
function toggleParcelas() {
    const tipo = document.getElementById('modalidade').value;
    document.getElementById('group-parcelas').style.display =
        tipo === 'parcelada' ? 'block' : 'none';
}
