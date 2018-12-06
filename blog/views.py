from django.shortcuts import render
from django.utils import timezone
from .models import Post
from django.shortcuts import render, get_object_or_404
from .forms import PostForm
from django.shortcuts import redirect

def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
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

def list(request, category=None, username=None, date=None):
    """
    List all entries, paginated
    """
    template_name = 'list.html'
    context = {}
    per_page = 5
    page = INT(request.GET.get('page', '1'))

    if category:
        context['category'] = category
        grouped_list = entries_by_category(request, category)
    elif username:
        context['author'] = username
        try:
            user = User.objects.get(username=username)
            grouped_list = Post.objects.filter(author=user.id).order_by('-created_at')
        except ObjectDoesNotExist:
            grouped_list = None
    elif date:
        context['date'] = date
        grouped_list = Post.objects.filter(created_at__startswith=date, publish=True).order_by('-created_at')
    else:
        grouped_list = Post.objects.filter(publish=True).order_by('-created_at')

    for entry in grouped_list:
        entry.category_list = Category.objects.filter(postcategory__post__pk=entry.id)
        entry.comments = Comment.objects.filter(post=entry.id)

    total_entries = grouped_list.count()
    total_pages = (total_entries/per_page)+1
    context['page_range'] = range(1, total_pages+1)

    offset = (page * per_page) - per_page
    limit = offset + per_page
    entry_list = grouped_list[offset:limit]
    context['entry_list'] = entry_list

    return render_to_response(template_name, context, context_instance=RequestContext(request))

def entries_by_category(request, category):
    try:
        post_category = Category.objects.get(slug=category)
    except ObjectDoesNotExist:
        post_category = None
    if post_category: entry_list = Post.objects.filter(postcategory__category=post_category.id, publish=True)
    return entry_list    