from django.db.models import Count, Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404, redirect, reverse
from . import models, forms
from marketing.models import Signup
from django.views.generic import View, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin


def search(request):
    query = request.GET.get('q')
    queryset = models.Post.objects.all()
    if query:
        queryset = queryset.filter(
            Q(title__icontains=query) |
            Q(overview__icontains=query)

        ).distinct()

    return render(request, 'search_results.html', {
        'queryset': queryset,
    })


def get_author(user):
    qs = models.Author.objects.filter(user=user)
    if qs.exists():
        return qs[0]
    else:
        x = models.Author.objects.create(user=user)
        return x


def get_category_count():
    queryset = models.Post\
        .objects.values('categories__title')\
        .annotate(Count('categories__title')
                  )
    return queryset


def index(request):
    featured = models.Post.objects.filter(featured=True)
    latest = models.Post.objects.order_by('-timestamp')[:3]

    if request.method == 'POST':
        email = request.POST['email']
        new_signup = Signup()
        new_signup.email = email
        new_signup.save()

    return render(request, 'index.html', {
        'object_list': featured,
        'latest': latest
    })


def blog(request):
    category_count = get_category_count()

    most_recent = models.Post.objects.order_by('-timestamp')[:3]
    post_list = models.Post.objects.all()
    paginator = Paginator(post_list, 4)

    page_request_var = 'page'
    page = request.GET.get(page_request_var)

    try:
        paginated_queryset = paginator.page(page)
    except PageNotAnInteger:
        paginated_queryset = paginator.page(1)
    except EmptyPage:
        paginated_queryset = paginator.page(paginator.num_pages)

    return render(request, 'blog.html', {
        'queryset': paginated_queryset,
        'most_recent': most_recent,
        'page_request_var': page_request_var,
        "category_count": category_count,
    })


def post(request, id):
    most_recent = models.Post.objects.order_by('-timestamp')[:3]
    category_count = get_category_count()
    post = get_object_or_404(models.Post, id=id)
    form = forms.CommentForm(request.POST or None)

    if request.user.is_authenticated:
        models.PostView.objects.get_or_create(user=request.user, post=post)

    if request.method == 'POST':
        if form.is_valid():
            form.instance.user = request.user
            form.instance.post = post
            form.save()
            return redirect(reverse("post-detail", kwargs={
                'id': post.pk,
            }))

    return render(request, 'post.html', {
        'form': form,
        'post': post,
        'most_recent': most_recent,
        "category_count": category_count,
    })


class PostCreateView(CreateView, LoginRequiredMixin):
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'
    
    model = models.Post
    template_name = 'post_create.html'
    form_class = forms.PostForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create'
        return context

    def form_valid(self, form):
        form.instance.author = get_author(self.request.user)
        return super().form_valid(form)
        # form.save()
        # return redirect(reverse("post-detail", kwargs={
        #     'pk': form.instance.pk
        # }))


def post_update(request, id):
    title = 'Update'
    post = get_object_or_404(models.Post, id=id)
    form = forms.PostForm(request.POST or None,
                          request.FILES or None, instance=post)
    author = get_author(request.user)
    if request.method == 'POST':
        if form.is_valid():
            form.instance.author = author
            form.save()
            return redirect(reverse('post-detail', kwargs={
                'id': form.instance.id
            }))

    return render(request, "post_create.html", context={
        'form': form,
        'title': title,
    })


def post_delete(request, id):
    post = get_object_or_404(models.Post, id=id)
    post.delete()
    return redirect(reverse('post-list'))
