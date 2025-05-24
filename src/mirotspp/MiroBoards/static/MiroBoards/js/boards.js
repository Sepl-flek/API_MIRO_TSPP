document.addEventListener('DOMContentLoaded', function () {
    loadBoards();

    document.getElementById('addBoardForm').addEventListener('submit', function (e) {
        e.preventDefault();
        createBoard();
    });
});

function loadBoards() {
    fetch('/MiroBoard/api/board/')
        .then(response => {
            if (!response.ok) throw new Error('Network response was not ok');
            return response.json();
        })
        .then(data => {
            const container = document.getElementById('boards-container');
            container.innerHTML = '';

            if (data.length === 0) {
                container.innerHTML = '<div class="col-12"><div class="alert alert-info">You have no boards yet.</div></div>';
                return;
            }

            data.forEach(board => {
                const boardCard = `
                    <div class="col-md-4 mb-4">
                        <div class="card board-card">
                            <div class="card-body">
                                <h5 class="card-title">${board.name}</h5>
                                <p class="card-text">Board ID: ${board.board_id}</p>
                                <div class="d-flex justify-content-between">
                                    <a href="/MiroBoard/board/${board.id}/items/" class="btn btn-primary">View Items</a>
                                    <button class="btn btn-danger btn-sm" onclick="deleteBoard(${board.id})">🗑 Delete</button>
                                </div>
                            </div>
                        </div>
                    </div>
                `;
                container.insertAdjacentHTML('beforeend', boardCard);
            });
        })
        .catch(error => {
            console.error('Error fetching boards:', error);
            document.getElementById('boards-container').innerHTML =
                '<div class="col-12"><div class="alert alert-danger">Error loading boards. Please try again later.</div></div>';
        });
}

function createBoard() {
    const name = document.getElementById('boardName').value;
    const board_id = document.getElementById('boardId').value;
    const api_key = document.getElementById('apiKey').value;

    fetch('/MiroBoard/api/board/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken(),
        },
        body: JSON.stringify({ name, board_id, api_key }),
    })
        .then(response => {
            if (!response.ok) throw new Error('Failed to create board');
            return response.json();
        })
        .then(data => {
            document.getElementById('addBoardForm').reset();
            const modal = bootstrap.Modal.getInstance(document.getElementById('addBoardModal'));
            modal.hide();
            loadBoards();
        })
        .catch(error => {
            alert('Error creating board: ' + error.message);
        });
}

function deleteBoard(boardId) {
    if (!confirm('Are you sure you want to delete this board?')) return;

    fetch(`/MiroBoard/api/board/${boardId}/`, {
        method: 'DELETE',
        headers: {
            'X-CSRFToken': getCSRFToken(),
        },
    })
        .then(response => {
            if (!response.ok) throw new Error('Failed to delete board');
            loadBoards();
        })
        .catch(error => {
            alert('Error deleting board: ' + error.message);
        });
}

function getCSRFToken() {
    const name = 'csrftoken';
    const cookies = document.cookie.split(';');
    for (let cookie of cookies) {
        cookie = cookie.trim();
        if (cookie.startsWith(name + '=')) {
            return decodeURIComponent(cookie.slice(name.length + 1));
        }
    }
    return '';
}
