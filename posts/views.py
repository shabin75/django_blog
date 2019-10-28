from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .models import Post, Author
from django.db.models import Count, Q
from marketing.models import Signup
from .forms import CommentForm, PostForm
from django.contrib.auth import get_user_model

User = get_user_model()


def get_category_count():
    queryset = Post.objects.values('categories__title').annotate(Count('categories__title'))
    return queryset


def index(request):
    featured = Post.objects.filter(featured=True)
    latest = Post.objects.order_by('-timestamp')[0:3]

    if request.method == 'POST':
        email = request.POST['email']
        new_signup = Signup()
        new_signup.email = email
        new_signup.save()

    return render(request, 'index.html', {'objects': featured,
                                          'latest': latest, })


def blog(request):
    category_count = get_category_count()
    print(category_count)
    most_recent = Post.objects.order_by('-timestamp')[0:3]
    post_list = Post.objects.all()
    paginator = Paginator(post_list, 4)
    page = request.GET.get('page')

    try:
        paginated_queryset = paginator.get_page(page)

    except PageNotAnInteger:

        paginated_queryset = paginator.get_page(1)

    except EmptyPage:

        paginated_queryset = paginator.page(paginator.num_pages)

    return render(request, 'blog.html', {'paginated_queryset': paginated_queryset,
                                         'most_recent': most_recent,
                                         'category_count': category_count})


def post(request, id):
    posts = get_object_or_404(Post, id=id)
    forms = CommentForm(request.POST or None)
    if forms.is_valid():
        forms.instance.user = request.user
        forms.instance.post = posts
        forms.save()
        forms = CommentForm()
        return redirect(reverse('post-detail', kwargs={'id': posts.pk}))

    return render(request, 'post.html', {'post': posts,
                                         'form': forms})


def search(request):
    queryset = Post.objects.all()
    query = request.GET.get('f')
    if query:
        queryset = queryset.filter(Q(title__icontains=query) | Q(overview__icontains=query)).distinct()

    return render(request, 'search.html', {'queryset': queryset})


def gey_user(user):
    qs = Author.objects.filter(user=user)
    if qs.exists():
        print(qs[0])

        print(qs)
        return qs[0]
    return None


def post_create(request):
    title = 'Create'
    form = PostForm(request.POST or None, request.FILES or None)
    if request.method == 'POST':
        if form.is_valid():
            form.instance.author = gey_user(request.user)
            form.save()
            return redirect(reverse('post-detail', kwargs={'id': form.instance.id}))

    return render(request, 'post_create.html', {'form': form,
                                                'title': title})


def post_update(request, id):
    post = get_object_or_404(Post, id=id)
    title = 'Update'
    form = PostForm(request.POST or None, request.FILES or None, instance=post)
    if request.method == 'POST':
        if form.is_valid():
            form.instance.author = gey_user(request.user)
            form.save()
            return redirect(reverse('post-detail', kwargs={'id': form.instance.id}))

    return render(request, 'post_create.html', {'form': form,
                                                'title': title})


def post_delete(request, id):
    post = get_object_or_404(Post, id=id)
    post.delete()
    return redirect(reverse('post-list'))
