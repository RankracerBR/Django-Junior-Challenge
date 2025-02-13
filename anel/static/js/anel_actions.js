async function updateAnel(anelId, updatedData) {
    try {
        const response = await fetch(`/aneis/${anelId}/`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken'),
            },
            body: JSON.stringify(updatedData),
        });

        if (response.ok) {
            alert('Anel atualizado com sucesso!');
            window.location.reload();
        } else {
            const errorData = await response.json();
            alert(`Erro ao atualizar: ${errorData.error || 'Erro desconhecido'}`);
        }
    } catch (error) {
        console.error('Erro:', error);
        alert('Erro ao atualizar o anel.');
    }
}

async function deleteAnel(anelId) {
    try {
        const response = await fetch(`/aneis/${anelId}/`, {
            method: 'DELETE',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
            },
        });

        if (response.ok) {
            alert('Anel deletado com sucesso!');
            window.location.href = '/';
        } else {
            const errorData = await response.json();
            alert(`Erro ao deletar: ${errorData.error || 'Erro desconhecido'}`);
        }
    } catch (error) {
        console.error('Erro:', error);
        alert('Erro ao deletar o anel.');
    }
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.startsWith(name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

document.addEventListener('DOMContentLoaded', function () {
    const deleteButton = document.getElementById('delete-button');
    if (deleteButton) {
        deleteButton.addEventListener('click', function () {
            const anelId = this.dataset.anelId;
            if (confirm('Tem certeza que deseja deletar este anel?')) {
                deleteAnel(anelId);
            }
        });
    }

    const updateButton = document.getElementById('update-button');
    if (updateButton) {
        updateButton.addEventListener('click', function () {
            const anelId = this.dataset.anelId;
            const updatedData = {
                nome_anel: document.getElementById('nome_anel').value,
                poder_anel: document.getElementById('poder_anel').value,
                portador_anel: document.getElementById('portador_anel').value,
                forjadoPor_anel: document.getElementById('forjadoPor_anel').value,
                imagem_anel: document.getElementById('imagem_anel').value,
            };
            updateAnel(anelId, updatedData);
        });
    }
});