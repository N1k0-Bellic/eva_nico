from django.shortcuts import render, get_object_or_404
from .models import Categoria, Juego
from .forms import PedidoForm


def inicio(request):
    juegos = Juego.objects.filter(disponible=True)
    categorias = Categoria.objects.all()

    busqueda = request.GET.get('buscar', '').strip()
    categoria_id = request.GET.get('categoria', '')

    if busqueda:
        juegos = juegos.filter(nombre__icontains=busqueda)

    if categoria_id.isdigit():
        juegos = juegos.filter(categoria_id=int(categoria_id))

    contexto = {
        'juegos': juegos,
        'categorias': categorias,
        'busqueda': busqueda,
        'categoria_seleccionada': categoria_id,
    }

    return render(request, 'inicio.html', contexto)


def detalle_juego(request, juego_id):
    juego = get_object_or_404(
        Juego,
        id=juego_id,
        disponible=True
    )

    formulario = PedidoForm()

    contexto = {
        'juego': juego,
        'formulario': formulario
    }

    return render(request, 'detalle.html', contexto)