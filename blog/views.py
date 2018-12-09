from django.utils import timezone
from .models import Post
from django.shortcuts import render, get_object_or_404, redirect
from .forms import PostForm
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q

def post_list(request):
    posts_list = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date').all()
    
    query = request.GET.get("q")
    if query:
        posts_list = posts_list.filter(
            Q(title__icontains = query) |
            Q(text__icontains = query)
            ).distinct()
    paginator = Paginator(posts_list, 3)

    page = request.GET.get('page')
    posts = paginator.get_page(page)
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, pk):
	Post.objects.get(pk=pk)

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

def post_new(request):
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
    post = get_object_or_404(Post, pk=pk)
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

def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post.delete()
            return redirect('post_list')
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_delete.html', {'form': form})
    