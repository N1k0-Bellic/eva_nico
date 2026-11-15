from django.shortcuts import render
from .models import Categoria, Juego

def inicio(request):
    juegos = Juego.objects.filter(disponible=True).select_related('categoria')
    categorias = Categoria.objects.all()
    busqueda = request.GET.get('buscar', '').strip()
    categoria_id = request.GET.get('categoria', '')

    if busqueda:
        juegos = juegos.filter(nombre__icontains=busqueda)

    if categoria_id.isdigit():
        juegos = juegos.filter(categoria_id=int(categoria_id))

    return render(request,'inicio.html', {
        'juegos': juegos,
        'categorias': categorias,
        'busqueda': busqueda,
        'categoria_seleccionada': categoria_id,
    })
