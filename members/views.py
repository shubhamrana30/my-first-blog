from django.shortcuts import render
from django.utils import timezone
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from django.contrib.auth.forms import UserCreationForm
from blog.models import Post

def test(request):
    return redirect('post_list')

def members_register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'members/register.html', {'form': form})



