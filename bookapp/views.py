from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from bookapp.models import Book, AllBooks
from bookapp.forms import BookForm, BooksInList, UserForm, ERROR_DUPLICATE_BOOKS


def new_book_form(request):
    return render(request, "bookForm.html", {"form": BookForm()})


@login_required
def view_list(request, all_books_id):
    """View for displaying book list."""
    labels = []
    data = []

    all_books = AllBooks.objects.get(id=all_books_id)
    all_books_progess_chart = Book.objects.filter(all_books=all_books)

    for book in all_books_progess_chart:
        labels.append(book.title)
        percentage = round(book.current_page / book.total_pages * 100, 2)
        data.append(percentage)

    form = BooksInList(for_list=all_books, user=request.user)
    if request.method == "POST":
        form = BooksInList(for_list=all_books,
                           user=request.user, data=request.POST)
        if form.is_valid():
            form = None
            form = BookForm(data=request.POST)
            form = form.save(for_list=all_books)
            form.user = request.user
            form.save()
            return redirect(all_books)

    return render(request, "list.html", {"labels": labels,
                                         "data": data,
                                         "all_books": all_books,
                                         "form": form,
                                         })


@login_required
def new_list(request):
    """View for new user's book list."""
    form = BookForm(data=request.POST)
    if form.is_valid():
        all_books = AllBooks.objects.create()
        form = form.save(for_list=all_books)
        form.user = request.user
        form.all_books = all_books
        form = form.save()

        return redirect(all_books)

    else:
        return render(request, "bookForm.html", {"form": form})


@login_required
def my_list(request):
    """View for manage book list form."""
    all_books_progess_chart = Book.objects.filter(user=request.user)

    book_set_id = []
    all_books_set_id = []
    for i in all_books_progess_chart:
        book_set_id.append(i.id)
        all_books_set_id.append(i.all_books_id)

    labels = []
    data = []

    if all_books_set_id != []:
        for book in all_books_progess_chart:
            labels.append(book.title)
            percentage = round(book.current_page / book.total_pages * 100, 2)
            data.append(percentage)

        all_books = AllBooks.objects.get(id=all_books_set_id[0])
        form = BooksInList(for_list=all_books, user=request.user)

        if request.method == "POST":
            form = BooksInList(for_list=all_books,
                               user=request.user, data=request.POST)
            if form.is_valid():
                form = None
                form = BookForm(data=request.POST)
                form = form.save(for_list=all_books)
                form.user = request.user
                form.save()
                return redirect(all_books)

            else:
                messages.error(request, ERROR_DUPLICATE_BOOKS)

        form = BooksInList(for_list=all_books, user=request.user)

        return render(request, "myList.html", {"labels": labels,
                                               "data": data,
                                               "all_books": all_books,
                                               "form": form,
                                               })

    else:
        return render(request, "bookForm.html", {"form": BookForm()})


def register(request):
    """Register new user to database."""
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            return render(request, 'registered.html', {'user': user})
    else:
        form = UserForm()
    return render(request, 'register.html', {'form': form})


def login_view(request):
    """Log in user and redirect to home page."""
    username = request.POST["username"]
    password = request.POST["password"]
    user = authenticate(request, username=username, password=password)
    if user:
        login(request, user)
        return render(request, "/")
        ...
    else:
        messages.error(request, "Invalid login")


def logout_view(request):
    """Log out user and redirect to login pagel."""
    logout(request)
    return redirect(request, "/login")


def delete_book(request, pk):
    """Delete book from list."""
    book = Book.objects.get(pk=pk)
    if request.method == "POST":
        book.delete()
        return redirect("/")

    return render(request, "myList.html", {"book": book})
