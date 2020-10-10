from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from django.views.generic import \
    ListView, DetailView, CreateView, \
    DeleteView, UpdateView
from .models import Post
from django.contrib.auth.mixins import \
    LoginRequiredMixin, UserPassesTestMixin


class PostListView(ListView):
    model = Post  # default render variable is called object list
    template_name = 'home.html'
    context_object_name = 'posts'  # alternative to object
    ordering = ['-date_posted']
    paginate_by = 6


class PostDetailView(DetailView):
    model = Post  # default render variable is called object
    template_name = 'post_detail.html'


# login required
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post  # default render variable is called object
    fields = ['title', 'content']
    template_name = 'post_form.html'

    # override the form valid method to be able to save a form and
    # assign a post to an owner
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


# login required, Post owner only can update
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post  # default render variable is called object
    fields = ['title', 'content']
    template_name = 'post_form.html'

    # override the form valid method to assign a post to an owner
    # to save a form

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    # Checking owner of an exact post we are updating
    def test_func(self):
        post = self.get_object()
        # check if current user is the owner of the post
        if self.request.user == post.author:
            return True
        return False


# we want the user to be logged in first
# and the user is the author of the post
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post  # default render variable is called object
    template_name = 'post_confirm_delete.html'
    success_url = '/'

    # Checking owner of an exact post we are updating
    def test_func(self):
        post = self.get_object()
        # check if current user is the owner of the post
        if self.request.user == post.author:
            return True
        return False


def about(request):
    return render(request, 'about.html', {})


# all user in the database
class UsersListView(ListView):
    model = User  # default render variable is called object
    template_name = 'users.html'
    context_object_name = 'users'


# post from a particular user
class UserPostListView(ListView):
    model = Post  # default render variable is called object list
    template_name = 'user_post.html'
    context_object_name = 'posts'  # alternative to object
    paginate_by = 5

    # assuming we have a username variable passed into the url
    # modifying the queryset
    def get_queryset(self):
        # username is gotten from the url
        # kwargs is the query parameter for the url
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')




