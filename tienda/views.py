from django.shortcuts import render, get_object_or_404, redirect
from django.db import transaction
from django.db.models import F
from .models import Categoria, Juego, Pedido
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

    if request.method == 'POST':
        formulario = PedidoForm(request.POST)

        if juego.stock == 0:
            formulario.add_error(
                None,
                'Este juego está agotado.'
            )

        elif formulario.is_valid():
            cantidad = formulario.cleaned_data['cantidad']

            if cantidad > juego.stock:
                formulario.add_error(
                    'cantidad',
                    f'Solo quedan {juego.stock} unidades disponibles.'
                )
            else:
                with transaction.atomic():
                    actualizados = Juego.objects.filter(
                        id=juego.id,
                        stock__gte=cantidad
                    ).update(stock=F('stock') - cantidad)

                    if actualizados:
                        pedido = formulario.save(commit=False)
                        pedido.juego = juego
                        pedido.save()

                if actualizados:
                    return redirect(
                        'tienda:comprobante',
                        codigo=pedido.codigo
                    )

                juego.refresh_from_db()
                formulario.add_error(
                    'cantidad',
                    f'Solo quedan {juego.stock} unidades disponibles.'
                )

    else:
        formulario = PedidoForm()

    contexto = {
        'juego': juego,
        'formulario': formulario
    }

    return render(request, 'detalle.html', contexto)


def comprobante(request, codigo):
    pedido = get_object_or_404(Pedido, codigo=codigo)
    total = pedido.juego.precio * pedido.cantidad

    contexto = {
        'pedido': pedido,
        'total': total
    }

    return render(request, 'comprobante.html', contexto)
