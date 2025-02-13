const API_URL = 'http://localhost:8000/aneis/';

async function loadAneis(){
    const response = await fetch(API_URL);
    const aneis = await response.json();
    const carouselInner = document.getElementById('carousel-inner');

    aneis.forEach((anel, index) => {
        const item = document.createElement('div');
        item.classList.add('carousel-item');

        if (index === 0) item.classList.add('active');

        item.innerHTML = `
                    <img src="${anel.imagem_anel}" class="d-block w-100" alt="${anel.nome_anel}">
            <div class="carousel-caption d-none d-md-block">
                <h5>${anel.nome_anel}</h5>
                <p>${anel.poder_anel}</p>
                <p>Portador: ${anel.portador_anel}</p>
                <p>Forjado por: ${anel.forjadoPor_anel}</p>
            </div>
        `;
        carouselInner.appendChild(item);
    })
}

document.addEventListener('DOMContentLoaded', loadAneis);