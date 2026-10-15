from django.shortcuts import render, get_object_or_404
from .models import Post, Categoria


def blog_lista(request):
    posts = Post.objects.filter(activo=True).prefetch_related('categorias')
    categorias = Categoria.objects.all()
    return render(
        request,
        'blog/blog_lista.html',
        {
            'posts': posts,
            'categorias': categorias,
            'categoria_actual': None,
        },
    )


def blog_por_categoria(request, categoria_id):
    categoria = get_object_or_404(Categoria, id=categoria_id)
    posts = Post.objects.filter(activo=True, categorias=categoria).prefetch_related('categorias')
    categorias = Categoria.objects.all()
    return render(
        request,
        'blog/blog_lista.html',
        {
            'posts': posts,
            'categorias': categorias,
            'categoria_actual': categoria,
        },
    )
