from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from .models import Forum
from django.views.generic import ListView, CreateView, DetailView, UpdateView,  DeleteView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .forms import CommentForm
from .models import Comment
from django.urls import reverse_lazy
from django.db.models import Q
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import ObjectDoesNotExist
from account.models import Profile
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

@method_decorator(login_required, name='dispatch')
class ForumListView(ListView):
    model = Forum
    template_name = 'forum_list.html'
    context_object_name = "objForums"
    queryset = Forum.objects.order_by('-created_at')
    paginate_by = 3

@method_decorator(login_required, name='dispatch')
class ForumCreate(SuccessMessageMixin, CreateView):
    model = Forum
    fields = ['title', 'desc']
    success_message = 'Post was successfully created'
    template_name = 'forum_form.html'
    
    def form_valid(self, form):
        try:
            profile = self.request.user.profile  # Use the correct related_name
        except ObjectDoesNotExist:
            # Handle the case when the profile does not exist
            return redirect('create_profile')  # Redirect to the profile creation page
        form.instance.user = self.request.user
        return super().form_valid(form)


# class ForumCreate(SuccessMessageMixin, CreateView):
#     model = Forum
#     fields = ['title', 'desc']
#     success_message = 'Post was successfully created'
#     template_name = 'forum_form.html'
    
#     def form_valid(self, form):
#         form.instance.user = self.request.user
#         return super().form_valid(form)
@method_decorator(login_required, name='dispatch')
class ForumUserListView(ListView):
    template_name = 'forum_by_user.html'
    paginate_by = 3
    def get_queryset(self):
        self.user = get_object_or_404(User, username=self.kwargs['username'])
        return Forum.objects.filter(user=self.user)

class OwnerProtectMixin(object):#bao ve url
    def dispatch(self, request, *args, **kwargs):
        objectUser = self.get_object()
        if objectUser.user != self.request.user:
            return HttpResponseForbidden()
        return super(OwnerProtectMixin, self).dispatch(request, *args, **kwargs)

# class ForumDetailView(DetailView):
#     model = Forum
#     template_name = 'forum_detail.html'
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['form_comment'] = CommentForm()
#         return context


@method_decorator(login_required, name='dispatch')
class ForumDetailView(DetailView):
    model = Forum
    template_name = 'forum_detail.html'
    context_object_name = 'forum'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        forum = self.get_object()
        parent_comments = Comment.objects.filter(forum=forum, parent__isnull=True)
        context['parent_comments'] = parent_comments
        context['user'] = forum.user
        return context
@method_decorator(login_required, name='dispatch')
class ForumUpdateView(SuccessMessageMixin, OwnerProtectMixin, UpdateView):
    model = Forum
    fields = ['title', 'desc']
    template_name = 'forum_update_form.html'
    success_message = 'Post was successfully updated'

    def get_success_url(self):
        return reverse_lazy('forum-detail', kwargs={'slug': self.object.slug})

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
@method_decorator(login_required, name='dispatch')
class ForumDeleteView(SuccessMessageMixin, OwnerProtectMixin, DeleteView):
    model = Forum
    success_url = '/forum'
    template_name = 'forum_detail.html'
    success_message = 'Post was successfully deleted'
    
# @method_decorator(login_required, name='dispatch')
# class CommentCreateView(CreateView):
#     model = Comment
#     fields = ['desc']

#     def form_valid(self, form):
#         _forum = get_object_or_404(Forum, id=self.kwargs['pk'])
#         form.instance.user = self.request.user
#         form.instance.forum = _forum
#         return super().form_valid(form)
#     def get_success_url(self):
#         return reverse_lazy('forum-detail', kwargs={'slug': self.object.forum.slug})
@method_decorator(login_required, name='dispatch')
class CommentCreateView(CreateView):
    model = Comment
    fields = ['desc']

    def form_valid(self, form):
        _forum = get_object_or_404(Forum, id=self.kwargs['pk'])
        form.instance.user = self.request.user
        form.instance.forum = _forum
        parent_id = self.request.POST.get('parent_id')
        if parent_id:
            form.instance.parent = Comment.objects.get(id=parent_id)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('forum-detail', kwargs={'slug': self.object.forum.slug})
@method_decorator(login_required, name='dispatch') 
class CommentUpdateView(OwnerProtectMixin, UpdateView): # bảo vệ dữ liệu người dùng khỏi những người dùng khác
    model = Comment
    fields = ['desc']
    template_name = 'forum_update_comment.html'
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('forum-detail', kwargs={'slug': self.object.forum.slug})

@method_decorator(login_required, name='dispatch')
class CommentDeleteView(OwnerProtectMixin, DeleteView):
    model = Comment
    success_url = '/forum'
    def get_success_url(self):
        return reverse_lazy('forum-detail', kwargs={'slug': self.object.forum.slug})

# def forum_search(request):
#     query = request.GET.get('q')
#     results = []
#     if query:
#         results = Forum.objects.filter(title__icontains=query)
#     return render(request, 'forum_search.html', {'query': query, 'results': results})
def forum_search(request):
    query = request.GET.get('q')
    results = []
    if query:
        results = Forum.objects.filter(title__icontains=query)
    
    paginator = Paginator(results, 3)  # Show results per page
    page = request.GET.get('page')
    
    try:
        results = paginator.page(page)
    except PageNotAnInteger:
        results = paginator.page(1)
    except EmptyPage:
        results = paginator.page(paginator.num_pages)
    
    return render(request, 'forum_search.html', {
        'query': query,
        'results': results,
        'is_paginated': results.has_other_pages()
    })