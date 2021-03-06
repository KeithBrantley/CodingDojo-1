from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import Book, Author, Review
from loginApp.models import User

# Create your views here.
def index(request):
    if 'user_id' not in request.session:
        return redirect('/')
    else:
        user = User.objects.get(id=request.session['user_id'])
        context = {
            'user': user,
            'reviews': reversed(Review.objects.all()),
            'all_books': Book.objects.all(),
        }
        return render(request, 'books.html', context)

# add a book and review
def add(request):
    if 'user_id' not in request.session:
        return redirect('/')
    else:
        context = {
            'all_authors': Author.objects.all()
        }
        return render(request, 'create.html', context)
#add books works 
def create(request):
    if 'user_id' not in request.session:
        return redirect('/')
    else:
        user = User.objects.get(id=request.session['user_id'])
        if (len(request.POST['new_author']) > 1):
            author = Author.objects.create(name=request.POST['new_author'])
        else:
            author = Author.objects.filter(name=request.POST['authors_dropdown'])
        book = Book.objects.create(
            title=request.POST['title'],
            author=author)
        Review.objects.create(
            review=request.POST['review'], 
            rating=request.POST['rating'], 
            book=book,
            user=user, 
            )
        # book.reviews.add(review)
        return redirect('/books')

# view all books with reviews and ratings
def rating(request, bookId):
    if 'user_id' not in request.session:
        return redirect('/')
    context = {
        'book': Book.objects.get(id=bookId),
        'reviews': Book.objects.get(id=bookId).review.all(),
    }
    return render(request, 'ratings.html', context)

def postRating(request, bookId):
    if 'user_id' not in request.session:
        return redirect('/')
    else:
        user = User.objects.get(id=request.session['user_id'])
        book = Book.objects.filter(id=bookId)[0]
        Review.objects.create(
            review=request.POST['review'],
            rating=request.POST['rating'],
            book=book,
            user=user,
        )
        return redirect(f'/books/{bookId}')

# end of Ratings Page Actions

def delete(request, bookId, reviewId):
    if 'user_id' not in request.session:
        return redirect('/')
    review = Review.objects.filter(id=reviewId)[0]
    if review.user.id != request.session['user_id']:
        return redirect(f'/books/{bookId}')
    review.delete()
    return redirect(f'/books/{bookId}')

def logout(request):
    request.session.flush()
    return redirect('/')
