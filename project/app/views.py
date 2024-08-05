from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth import login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from .models import Blog, User
from .forms import BlogForm, CommentForm

# Create your views here.
def login_view(request):
    if request.method == "POST":
        #it checks if password is same or not ,and the username will be checked
        form = AuthenticationForm(request, data=request.POST)
        print(form.errors)

        print(form.is_valid())
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'Login successful. You are now logged in.')
            return redirect('dashboard')  # Redirect to your dashboard or success page
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field.capitalize()}: {error}')
    else:
        form = AuthenticationForm()
    
    return render(request, 'login.html', {'form': form})

def register_view(request):
    if request.method == "POST":
        #built in form to create the user
        #this is built in so the uniqueness will be handled by it
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful. You are now logged in.')
            return redirect('dashboard')  # Redirect to your dashboard or success page
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field.capitalize()}: {error}')
    else:
        initial_data={'username':'','email':'','password1':'','password2':''}
        form = UserCreationForm(initial_data)
    
    return render(request, 'registration.html', {'form': form})

def logout_view(request):
    #built in method to logout 
    logout(request)
    messages.success(request, 'Logged out successfully.')
    return redirect('dashboard')
def dashboard(request):
    return render(request,'dashboard.html')
 # Get the User model
#this decorator is used ,if we dont want to restrict others 
@login_required
def create_blog(request):
    if request.method == 'POST':
        form = BlogForm(request.POST)
        if form.is_valid():
            # Print or log form data to debug
            print(form.cleaned_data)  # Check what data is being received from the form

            # Create a new Blog instance with form data
            new_blog = form.save(commit=False)
            new_blog.author = request.user  # Assign the logged-in user as the author
            new_blog.save()
            messages.success(request, 'Your blog has been created')
            return redirect('blog-list')
        else:
            print(form.errors)  # Print form errors for debugging
    else:
        form = BlogForm()  # Create a new form instance for GET requests

    return render(request, 'create_blog.html', {'form': form})


def blog_list(request):
    #it will retrieve all the data in desc order
    blogs = Blog.objects.all().order_by('date_posted')  # Fetch all blogs ordered by date_posted descending
    paginator=Paginator(blogs,1)
    page_number=request.GET.get('page')
    page_obj=paginator.get_page(page_number)
    return render(request, 'blog-list.html', {'blogs': blogs,'page_obj':page_obj})

@login_required
def update_blog(request, pk):
    #it gets the details of blog which has id of that particular 
    blog = get_object_or_404(Blog, pk=pk)
    if request.method == 'POST':
        form = BlogForm(request.POST, instance=blog)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your Blog has been updated')
            return redirect('blog-list')  # Redirect to the blog list page after successful update
    else:
        form = BlogForm(instance=blog)
    
    return render(request, 'update_blog.html', {'form': form, 'blog': blog})

@login_required
def delete_blog(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    if request.method == 'POST':
        blog.delete()
        messages.success(request, 'Your Blog has been deleted')
        return redirect('blog-list')  # Redirect to the blog list page after successful deletion
    
    return render(request, 'delete_blog.html', {'blog': blog})

def blog_detail(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    comments = blog.comments.all()  # Get all comments for this blog
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.blog = blog
            new_comment.author = request.user
            new_comment.save()
            messages.success(request, 'Your comment has been added ')
            return redirect('blog_detail', blog_id=blog.id)
    else:
        comment_form = CommentForm()
    return render(request, 'blog_detail.html', {
        'blog': blog,
        'comments': comments,
        'comment_form': comment_form
    })

