from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import Post
from .forms import PostForm


def lista_posts(request):
    todos_los_posts = Post.objects.all().order_by('-id')
    paginator = Paginator(todos_los_posts, 3)
    numero_pagina = request.GET.get('page')
    posts = paginator.get_page(numero_pagina)
    rango_paginas = posts.paginator.get_elided_page_range(
        posts.number, on_each_side=1, on_ends=1
    )
    return render(request, 'posts/lista_posts.html', {
        'posts': posts,
        'rango_paginas': rango_paginas
    })


def detalle_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'posts/detalle_post.html', {'post': post})


@login_required
def crear_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.autor = request.user.get_full_name() or request.user.username
            post.save()
            return redirect('lista_posts')
    else:
        form = PostForm()
    return render(request, 'posts/post_form.html', {'form': form})


@login_required
def editar_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('detalle_post', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'posts/post_form.html', {
        'form': form,
        'accion': 'Editar'
    })


@login_required
def eliminar_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        post.delete()
        return redirect('lista_posts')
    return render(request, 'posts/post_confirm_delete.html', {'post': post})


def acerca(request):
    return render(request, 'posts/acerca.html')
