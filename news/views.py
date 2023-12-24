from django.shortcuts import render, get_object_or_404,redirect
from .models import *
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .filters import PostFilter
from .forms import PostForm 
from datetime import datetime
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
# Create your views here.
from django.views.generic.edit import CreateView
from django.contrib.auth.decorators import login_required



from django.shortcuts import render, reverse, redirect
from django.views import View
from django.core.mail import mail_admins, mail_managers # импортируем функцию для массовой отправки писем админам
from datetime import datetime

from django.template.loader import render_to_string 


class NewsList(ListView):
    # Указываем модель, объекты которой мы будем выводить
    model = Post
    # Поле, которое будет использоваться для сортировки объектов
    ordering = '-time_in'
    # Указываем имя шаблона, в котором будут все инструкции о том,
    # как именно пользователю должны быть показаны наши объекты
    template_name = 'News.html'
    # Это имя списка, в котором будут лежать все объекты.
    # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.
    context_object_name = 'news'
    paginate_by = 10



class NewsSearch(ListView):
    model = Post
    ordering = 'title'
    template_name = 'news_search.html'
    context_object_name = 'news_search'

    def get_queryset(self):
       queryset = super().get_queryset()
       self.filterset = PostFilter(self.request.GET, queryset)
       return self.filterset.qs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context





class PostDetail(DetailView):
    # Модель всё та же, но мы хотим получать информацию по отдельному товару
    model = Post
    # Используем другой шаблон — post.html
    template_name = 'Post.html'
    # Название объекта, в котором будет выбранный пользователем продукт
    context_object_name = 'post'

class PostCreate(CreateView,LoginRequiredMixin, PermissionRequiredMixin):
    permission_required = 'news.add_post' 
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    success_url = reverse_lazy('news')
    # def form_valid(self, form):
    #     post = form.save(commit=False)
    #     post.name = 'NW'
    #     return super().form_valid(form)
    


class PostUpdate(UpdateView, LoginRequiredMixin, PermissionRequiredMixin):
    permission_required = 'news.update_post'
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
   

class PostDelete(DeleteView, PermissionRequiredMixin):
    permission_required = 'news.delete_post'
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('news')


class ArticleCreate(CreateView, LoginRequiredMixin, PermissionRequiredMixin):
    permission_required = 'news.add_post'
    form_class = PostForm
    model = Post
    template_name = 'article_edit.html'
    success_url = reverse_lazy('news')
    def form_valid(self, form):
        post = form.save(commit=False)
        post.name = 'AR'
        return super().form_valid(form)
    


class ArticleUpdate(UpdateView, LoginRequiredMixin, PermissionRequiredMixin):
    permission_required = 'news.update_post'
    form_class = PostForm
    model = Post
    template_name = 'article_edit.html'
   

class ArticleDelete(DeleteView, PermissionRequiredMixin):
    permission_required = 'news.delete_post'
    model = Post
    template_name = 'article_delete.html'
    success_url = reverse_lazy('news')


class CategoryListView(ListView):
    model = Post
    template_name = 'category_list.html'
    context_object_name = 'category_news_list'

    def get_queryset(self):
        self.categories = get_object_or_404(Category, id=self.kwargs['pk'])
        queryset = Post.objects.filter(categories=self.categories).order_by('-time_in')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_subscriber'] = self.request.user not in self.categories.subscribers.all()
        context['is_subscriber'] = self.request.user in self.categories.subscribers.all()
        context['categories'] = self.categories
        return context

@login_required()
def subscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.add(user)
    message = 'You subscribed to the category: '
    return render(request, 'subscribe.html', {'category': category, 'message': message})

@login_required()
def unsubscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.remove(user)
    message = 'You unsubscribed from category: '
    return render(request, 'subscribe.html', {'category': category, 'message': message})