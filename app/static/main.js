document.querySelectorAll('.like-button').forEach(function (button) {
    button.addEventListener('click', function () {
        let bookIsbn = this.dataset.bookIsbn;
        let likeIconElement = this.querySelector('.like-icon');
        let likeCountElement = this.querySelector('.like-count');
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

                    likeCountElement.textContent = '(' + data.like_count + ')';
                    // Toggle the like icon from filled to unfilled and vice versa
                    if (likeIconElement.firstChild.classList.contains('bi-star-fill')) {
                        likeIconElement.innerHTML = '<i class="bi bi-star"></i>';
                    } else {
                        likeIconElement.innerHTML = '<i class="bi bi-star-fill"></i>';
                    }
                }
            });
    });
});

document.querySelectorAll('.unlike-button').forEach(function (button) {
    button.addEventListener('click', function () {
        let bookIsbn = this.dataset.bookIsbn;
        let unlikeIconElement = this.querySelector('.unlike-icon');
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
                    console.log(data.error);
                } else {
                    console.log(data.message);
                    // Remove the book from the wishlist on the webpage
                    button.parentElement.remove();
                    // Toggle the unlike icon from filled to unfilled and vice versa
                    if (unlikeIconElement.firstChild.classList.contains('bi-x-circle-fill')) {
                        unlikeIconElement.innerHTML = '<i class="bi bi-x-circle"></i>';
                    } else {
                        unlikeIconElement.innerHTML = '<i class="bi bi-x-circle-fill"></i>';
                    }
                }
            });
    });
});
