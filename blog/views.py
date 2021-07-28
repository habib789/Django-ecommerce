from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, PostComment
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from .forms import PostForm, CommentForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.http import Http404
from django.contrib.auth import get_user_model
User = get_user_model()


class PostView(ListView):
    model = Post
    paginate_by = 3


class PostDetailView(DetailView):
    model = Post

    def get_context_data(self, *args, **kwargs):
        context = super(PostDetailView, self).get_context_data(*args, **kwargs)
        likes = get_object_or_404(Post, id=self.kwargs['pk'])
        context['post_likes'] = likes.total_likes()
        context['users_like'] = User.objects.filter(post_likes__id=self.kwargs['pk'])
        return context


class UserPost(ListView):
    model = Post

    # def get_queryset(self):
    #     try:
    #         self.post.user = User.objects.prefetch_related('posts').get(username__ixact=self.kwargs.get('username'))
    #     except DoesNotExist:
    #         raise Http404
    #     else:
    #         return self.post_user.posts.all()
    #
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['post_user'] = self.post_user
    #     return context


class PostDelete(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('blog:blog')


class PostCreate(LoginRequiredMixin, CreateView):
    login_url = '/accounts/login/'
    model = Post
    form_class = PostForm


def post_searched(request):
    if request.method == 'POST':
        searched = request.POST['searched']
        blog_title = Post.objects.filter(title__icontains=searched)
        blog_content = Post.objects.filter(description__icontains=searched)
        # blog_search = blog_title.union(blog_content)
        blog_search = blog_title | blog_content

        return render(request, 'blog/blog_search.html', {'searched': searched,
                                                         'blog_search': blog_search})


class PostUpdate(LoginRequiredMixin, UpdateView):
    model = Post
    fields = ('title', 'description')
    template_name = 'blog/post_update.html'


@login_required
def add_comment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('blog:post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/comment_form.html', {'form': form})


@login_required
def remove_comment(request, pk):
    comment = get_object_or_404(PostComment,pk=pk)
    post_pk = comment.post.pk
    comment.delete()
    return redirect('blog:post_detail', pk=post_pk)


@login_required
def PostLike(request, pk):
    post = get_object_or_404(Post, id=request.POST.get('p_id'))
    post.likes.add(request.user)
    return redirect('blog:blog')