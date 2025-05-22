function openModal(type) {
    document.getElementById("itemType").value = type;
    document.getElementById("modalTitle").textContent =
        `Добавить ${type === 'stick' ? 'стикер' : type === 'txt' ? 'текст' : 'изображение'}`;
    document.getElementById("x").value = "";
    document.getElementById("y").value = "";
    document.getElementById("contentJson").value = "";
    document.getElementById("itemModal").style.display = "block";
}

function closeModal() {
    document.getElementById("itemModal").style.display = "none";
}

document.getElementById("add-text").addEventListener("click", () => openModal("txt"));
document.getElementById("add-image").addEventListener("click", () => openModal("img"));
document.getElementById("add-sticker").addEventListener("click", () => openModal("stick"));

document.getElementById("itemForm").addEventListener("submit", async function(event) {
    event.preventDefault();

    const type = document.getElementById("itemType").value;
    const x = document.getElementById("x").value;
    const y = document.getElementById("y").value;
    const contentJsonRaw = document.getElementById("contentJson").value;

    let contentJson;
    try {
        contentJson = JSON.parse(contentJsonRaw);
    } catch (e) {
        alert("Ошибка: введённый JSON некорректен.");
        return;
    }

    const response = await fetch(`/MiroBoard/api/board/${boardId}/items/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        },
        body: JSON.stringify({
            x_coordinate: x,
            y_coordinate: y,
            type: type,
            content: JSON.stringify(contentJson)
        })
    });

    if (response.ok) {
        closeModal();
        fetchItems();
    } else {
        const error = await response.json();
        alert("Ошибка: " + JSON.stringify(error));
    }
});

function renderItems(items) {
    const tbody = document.getElementById("itemsTableBody");
    tbody.innerHTML = "";

    if (items.length === 0) {
        tbody.innerHTML = `<tr><td colspan="6">Нет items на этой доске</td></tr>`;
        return;
    }

    items.forEach(item => {
        const tr = document.createElement("tr");
        tr.innerHTML = `
            <td>${item.item_id}</td>
            <td>${item.x_coordinate}</td>
            <td>${item.y_coordinate}</td>
            <td>${item.type}</td>
            <td><pre>${JSON.stringify(item.content, null, 2)}</pre></td>
            <td><button class="save-item" data-item-id="${item.id}">Save</button></td>
        `;
        tbody.appendChild(tr);
    });
}

async function fetchItems() {
    try {
        const response = await fetch(`/MiroBoard/api/board/${boardId}/items/`);
        if (!response.ok) throw new Error("Ошибка загрузки items");

        const data = await response.json();
        renderItems(data);
    } catch (err) {
        alert("Ошибка при получении данных: " + err.message);
    }
}

document.addEventListener("DOMContentLoaded", fetchItems);
