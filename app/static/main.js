document.querySelectorAll('.like-button').forEach(function(button) {
    button.addEventListener('click', function() {
        var bookIsbn = this.dataset.bookIsbn;
        var likeIconElement = this.querySelector('.like-icon');
        var likeCountElement = this.querySelector('.like-count');
        fetch('/like_book', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                'book_isbn': bookIsbn
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert(data.error);
            } else {
                alert(data.message);
                likeCountElement.textContent = '(' + data.like_count + ')';
                if (likeIconElement.firstChild.classList.contains('bi-star-fill')) {
                    likeIconElement.innerHTML = '<i class="bi bi-star"></i>';
                } else {
                    likeIconElement.innerHTML = '<i class="bi bi-star-fill"></i>';
                }
            }
        });
    });
});

document.querySelectorAll('.unlike-button').forEach(function(button) {
    button.addEventListener('click', function() {
        var bookIsbn = this.dataset.bookIsbn;
        fetch('/unlike_book', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                'book_isbn': bookIsbn
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert(data.error);
            } else {
                alert(data.message);
                // Remove the book from the wishlist on the webpage
                button.parentElement.remove();
            }
        });
    });
});
