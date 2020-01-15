from django.shortcuts import render, redirect
from .models import Producto
from .forms import ProductoForm
from django.contrib.auth.decorators import login_required, permission_required

def home(request):
    return render(request,'core/home.html')

@login_required
def listado_producto(request):
    productos = Producto.objects.all()
    data = {
        'productos': productos
    }
    return render(request,'core/lista_producto.html', data)

@permission_required('core.add_producto')
def nuevo_producto(request):
    data = {
        'form': ProductoForm()
   
    }

    if request.method == "POST":
        form = ProductoForm(request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            data['mensaje'] = "Guardado correctamente"

    return render(request,'core/nuevo_producto.html', data)


def modificar_producto(request, id):
    producto = Producto.objects.get(id=id)
    data = {
        'form': ProductoForm(instance=producto)
   
    }


    if request.method == "POST":
        form = ProductoForm(data=request.POST, instance=producto, files=request.FILES)
        if form.is_valid():
            form.save()
            data['mensaje'] = "Modificado correctamente"
        data['form'] = ProductoForm(instance=Producto.objects.get(id=id))

    return render(request, 'core/modificar_producto.html', data)


def eliminar_producto(request, id):
    producto = Producto.objects.get(id=id)
    producto.delete()

    return redirect(to='listado_producto')

