from django.http.response import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.utils import timezone
from .models import Comment, Post
from django.shortcuts import render, get_object_or_404
from .forms import PostForm, CommentForm
from django.shortcuts import redirect
from django.urls import reverse


def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})
def post_new(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})
def post_edit(request, pk):
    post = get_object_or_404(Post,pk=pk)
    if request.user == post.author:
        if request.method == "POST":
            form = PostForm(request.POST, instance=post)
            if form.is_valid():
                post = form.save(commit=False)
                post.author = request.user
                post.published_date = timezone.now()
                post.save()
                return redirect('post_detail', pk=post.pk)
        else:
            form = PostForm(instance=post)
        return render(request, 'blog/post_edit.html', {'form': form})
    return render(request,'blog/error.html')

def my_post(request):
    try:
        post = Post.objects.filter(author = request.user)
    except:
        return redirect('login')
    return render(request, 'blog/my_post.html', {'posts':post})

def post_like(request,pk):
    if not request.user.is_authenticated:
        return redirect('login')
    post = get_object_or_404(Post,pk=request.POST.get('post_pk'))
    post.likes.add(request.user)
    return HttpResponseRedirect(reverse('post_detail',args=[str(pk)]))

def add_comment(request,pk):
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.name = request.user
            post = get_object_or_404(Post,pk=pk)
            comment.post = post
            comment.published_date = timezone.now()
            comment.save()
            return redirect('post_detail', pk = pk)
    else:
        form = CommentForm()
    return render(request, 'blog/add_comment.html', {'form': form})

def post_delete(request,pk):
    post = get_object_or_404(Post,pk=pk)
    if request.user == post.author:
        post.delete()
        return redirect('post_list')
    return render(request,'blog/error.html',{})