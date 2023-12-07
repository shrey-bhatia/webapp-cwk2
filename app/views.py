# __author__ = 'Shrey Bhatia'
# __email__ = 'fy21sb@leeds.ac.uk'
from flask import jsonify
from flask import render_template, request, flash, redirect, url_for
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash

from app import app
from app import db
from app.models import Book, User, Cart


@app.route('/', defaults={'page': 1})
@app.route('/page/<int:page>')
def homepage(page):
    per_page = 12
    query = request.args.get('query', '')
    books = Book.query.filter(Book.BookTitle.ilike(f'%{query}%')).paginate(
        page, per_page, False)
    return render_template('homePage.html', title='Home Page', books=books,
                           query=query)


@app.route('/add_to_cart', methods=['POST'])
@login_required
def add_to_cart():
    # Get the book ISBN from the form data
    book_isbn = request.form.get('book_isbn')

    # Retrieve the book from the database
    book = Book.query.filter_by(ISBN=book_isbn).first()

    # Check if the book exists
    if book is None:
        flash('Book not found', 'error')
        return redirect(url_for('homepage'))

    # Check if the book is in stock
    if book.stock <= 0:
        flash('Book is out of stock', 'error')
        return redirect(url_for('homepage'))

    # Decrement the book's stock
    book.stock -= 1

    # Add the book to the cart
    cart_item = Cart(user_id=current_user.id, book_isbn=book.ISBN,
                     price=book.Price)
    db.session.add(cart_item)

    db.session.commit()

    # Redirect the user back to the homepage
    return redirect(url_for('homepage'))


@app.route('/remove_from_cart', methods=['POST'])
@login_required
def remove_from_cart():
    # Get the book ISBN from the form data
    book_isbn = request.form.get('book_isbn')

    # Retrieve the cart item from the database
    cart_item = Cart.query.filter_by(user_id=current_user.id,
                                     book_isbn=book_isbn).first()

    # Check if the cart item exists
    if cart_item is None:
        flash('Item not found in cart', 'error')
        return redirect(url_for('viewcartpage'))

    # Retrieve the book from the database
    book = Book.query.filter_by(ISBN=book_isbn).first()

    # Check if the book exists
    if book is None:
        flash('Book not found', 'error')
        return redirect(url_for('viewcartpage'))

    # Increment the book's stock
    book.stock += 1

    # Remove the item from the cart
    db.session.delete(cart_item)

    db.session.commit()

    # Redirect the user back to the view cart page
    return redirect(url_for('viewcartpage'))


@app.route('/like_book', methods=['POST'])
@login_required
def like_book():
    # Get the book ISBN from the AJAX request
    book_isbn = request.json.get('book_isbn')

    # Retrieve the book from the database
    book = Book.query.filter_by(ISBN=book_isbn).first()

    # Check if the book exists
    if book is None:
        return jsonify({'error': 'Book not found'}), 404

    # Check if the current user has already liked the book
    if current_user.has_liked(book):
        # If the user has already liked the book, unlike it
        current_user.likes.remove(book)
        book.like_count -= 1
        db.session.commit()
        return jsonify({'message': 'Book unliked successfully',
                        'like_count': book.like_count}), 200

    # If the user has not liked the book, like it
    current_user.likes.append(book)
    book.like_count += 1
    db.session.commit()
    return jsonify({'message': 'Book liked successfully',
                    'like_count': book.like_count}), 200


@app.route('/unlike_book', methods=['POST'])
@login_required
def unlike_book():
    # Get the book ISBN from the AJAX request
    book_isbn = request.json.get('book_isbn')

    # Retrieve the book from the database
    book = Book.query.filter_by(ISBN=book_isbn).first()

    # Check if the book exists
    if book is None:
        return jsonify({'error': 'Book not found'}), 404

    # Check if the current user has liked the book
    if not current_user.has_liked(book):
        return jsonify({'error': 'You have not liked this book'}), 400

    # Unlike the book
    current_user.likes.remove(book)
    book.like_count -= 1
    db.session.commit()

    # Return a successful response
    return jsonify({'message': 'Book unliked successfully'}), 200


@app.route('/checkoutPage', methods=['GET', 'POST'])
@login_required
def checkoutpage():
    # Retrieve the cart items from the database
    cart_items = Cart.query.filter_by(user_id=current_user.id).all()

    # Calculate the total cost
    total_cost = sum(item.price for item in cart_items)

    # If the form is submitted, clear the cart and redirect to the success page
    if request.method == 'POST':
        Cart.query.filter_by(user_id=current_user.id).delete()
        db.session.commit()
        return redirect(url_for('checkout_success'))

    # Pass the total cost to the template
    return render_template('checkoutPage.html', title='Checkout',
                           total_cost=total_cost)


@app.route('/checkoutSuccessPage', methods=['GET'])
@login_required
def checkout_success():
    return render_template('checkout_success.html', title='Order Placed')


@app.route('/userSignupPage', methods=['GET', 'POST'])
def usersignuppage():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if a user with the provided username already exists
        user = User.query.filter_by(username=username).first()
        if user:
            return 'A user with that username already exists'

        # Create a new user with the provided username and password
        hashed_password = generate_password_hash(password)
        new_user = User(username=username, password=hashed_password)

        # Add the new user to the database and commit the changes
        db.session.add(new_user)
        db.session.commit()

        # Redirect the user to the login page
        return redirect(url_for('userloginpage'))

    return render_template('userSignupPage.html', title='User Signup')


@app.route('/userLoginPage', methods=['GET', 'POST'])
def userloginpage():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('homepage'))
        else:
            return 'Invalid username or password'
    return render_template('userLoginPage.html', title='User Login')


@app.route('/logoutPage')
def logout():
    logout_user()
    return redirect(url_for('homepage'))


@app.route('/wishlistPage', methods=['GET'])
@login_required
def wishlistpage():
    # Retrieve the books that the current user has liked
    liked_books = current_user.likes

    # Pass the liked books to the template
    return render_template('wishlistPage.html', title='Wishlist',
                           books=liked_books)


@app.route('/viewCartPage', methods=['GET', 'POST'])
@login_required
def viewcartpage():
    # Retrieve the cart items from the database
    cart_items = Cart.query.filter_by(user_id=current_user.id).all()

    # Calculate the total cost
    total_cost = sum(item.price for item in cart_items)

    # Pass the cart items and total cost to the template
    return render_template('viewCartPage.html', title='View Cart',
                           cart_items=cart_items, total_cost=total_cost)
