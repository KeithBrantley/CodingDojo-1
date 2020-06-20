from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import Book, Review
from loginApp.models import User

# Create your views here.
def index(request):
    if 'user_id' not in request.session:
        return redirect('/')
    else:
        user = User.objects.get(id=request.session['user_id'])
        context = {
            'user': user,
            'review': reversed(Review.objects.all()),
            'all_books': Book.objects.all(),
        }
        return render(request, 'books.html', context)

def add(request):
    if 'user_id' not in request.session:
        return redirect('/')
    else:
        context = {
            'authors' : Book.objects.values_list('author', flat=True)
        }
        return render(request, 'create.html', context)

def create(request):
    if 'user_id' not in request.session:
        if 'author_select' in request.POST:
            newBook = Book.objects.create(
                title = request.POST['author'],
                name = request.POST['author_select'],
            )
        elif request.POST['author_input'] != '':
            newBook = Book.objects.create(
                title = request.POST['title'],
                author = request.POST['author_input'],
            )
        Review.objects.create(
            review = request.POST['review'],
            rating = request.POST['rating'],
            user = User.objects.get(id=request.session['user_id']),
            book = Book.objects.get(id=newBook.id),
        )
        return redirect('/books')
    return redirect('/')

def rating(request):
    if 'user_id' not in request.session:
        return redirect('/')
    return render(request, 'ratings.html')

def delete(request, bookId, reviewId):
    if 'user_id' not in request.session:
        return redirect('/')
    review = Review.object.filter(id=reviewId)[0]
    if review.user_reviewed.id != request.session['user.id']:
        return redirect(f'/books/{bookId}')

def logout(request):
    request.session.flush()
    return redirect('/')
