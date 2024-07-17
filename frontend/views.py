# frontend/views.py
#importación de diversas librerias
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponseRedirect
import json
from .models import Producto, MensajeContacto, Credenciales
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.core.mail import send_mail
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from .forms import ContactForm, CredencialesForm
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
import json
from django.views.decorators.http import require_GET
from .models import DetalleCompra
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import CredencialesForm
from .models import Credenciales
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import CredencialesForm
from django.db import transaction
from .models import Compra, DetalleCompra
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Compra
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import DetalleCompra
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.db import transaction
from django.core.serializers.json import DjangoJSONEncoder

# Vistas para renderizar páginas HTML y las llamadas POST a cada vista
def index(request):
    return render(request, 'frontend/index.html')

def about(request):
    return render(request, 'frontend/about.html')

def admin_page(request):
    return render(request, 'frontend/Admin.html')

def perfil(request):
    return render(request, 'frontend/perfil.html')

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('contact') + '?success=true')
    else:
        form = ContactForm()
    return render(request, 'frontend/contact.html', {'form': form})

def login_view(request):
    return render(request, 'frontend/login.html')

def privacidad(request):
    return render(request, 'frontend/privacidad.html')

def product(request):
    return render(request, 'frontend/product.html')

def service(request):
    return render(request, 'frontend/service.html')

def team(request):
    return render(request, 'frontend/team.html')

def terminos(request):
    return render(request, 'frontend/Terminos.html')

def testimonial(request):
    return render(request, 'frontend/testimonial.html')

def ventas(request):
    return render(request, 'frontend/Ventas.html')

def registro_usuario(request):
    if request.method == 'POST':
        form = CredencialesForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registro exitoso. Ahora puedes iniciar sesión.')
            return redirect('login')
    else:
        form = CredencialesForm()
    return render(request, 'frontend/RegistroUsuario.html', {'form': form})

# API para obtener el stock de productos según backend
@api_view(['GET'])
def obtener_stock(request):
    productos = Producto.objects.all()
    data = [
        {
            'nombre': producto.nombre,
            'precio': producto.precio,
            'stock': producto.stock
        }
        for producto in productos
    ]
    return Response({'productos': data})

# API para procesar pagos
@csrf_exempt
@login_required
def procesar_pago(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            productos = data.get('productos', [])
            
            total = 0

            with transaction.atomic():
                detalles_productos = []

                for item in productos:
                    try:
                        producto = Producto.objects.get(nombre=item['name'])
                        if producto.stock < item['quantity']:
                            raise ValueError(f"No hay suficiente stock de {producto.nombre}")
                        
                        producto.stock -= item['quantity']
                        producto.save()
                        
                        subtotal = producto.precio * item['quantity']
                        total += subtotal
                        
                        # Crear DetalleCompra asociado a la Compra
                        detalle_compra = DetalleCompra(
                            compra=None,  # Aquí asignaremos la Compra más adelante
                            producto=producto,
                            cantidad=item['quantity'],
                            precio_unitario=producto.precio,
                            usuario=request.user
                        )
                        detalles_productos.append(detalle_compra)
                    
                    except Producto.DoesNotExist:
                        raise ValueError(f"El producto {item['name']} no existe en la base de datos")
                
                # Crear la instancia de Compra
                compra = Compra.objects.create(
                    usuario=request.user,
                    total=total,
                    productos=json.dumps(productos, cls=DjangoJSONEncoder)  # Serializar productos a JSON
                )

                # Asignar la Compra a cada DetalleCompra y guardar
                for detalle_compra in detalles_productos:
                    detalle_compra.compra = compra
                    detalle_compra.save()
            
            return JsonResponse({'message': 'Pago procesado con éxito'})
        
        except json.JSONDecodeError:
            return JsonResponse({"error": "Error en el formato JSON de la solicitud"}, status=400)
        
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    
    return JsonResponse({"error": "Método no permitido"}, status=405)

# API para enviar resúmenes de compra
@api_view(['GET', 'POST'])
def enviar_resumen(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get('email')
            productos = data.get('productos', [])
            total = data.get('total')

            mensaje = "Resumen de tu compra:\n\n"
            for item in productos:
                mensaje += f"{item['name']} - Cantidad: {item['quantity']} - Precio: {item['price']}\n"
            mensaje += f"\nTotal: {total}"

            send_mail(
                'Resumen de tu compra',
                mensaje,
                'cojojose666@gmail.com',  # Cambia esto por el email desde el cual enviarás el correo
                [email],
                fail_silently=False,
            )
            return JsonResponse({"success": True})
        
        except json.JSONDecodeError:
            return JsonResponse({"error": "Error en el formato JSON de la solicitud"}, status=400)
        
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    
    elif request.method == 'GET':
        return JsonResponse({"message": "Endpoint para enviar resúmenes de compra. Envía una solicitud POST para enviar un resumen."})

    return JsonResponse({"error": "Método no permitido"}, status=405)

# Vista para enviar mensajes de contacto
@csrf_exempt
def enviar_mensaje_contacto(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        email = request.POST.get('email')
        asunto = request.POST.get('asunto')
        mensaje = request.POST.get('mensaje')
        
        mensaje_contacto = MensajeContacto(nombre=nombre, email=email, asunto=asunto, mensaje=mensaje)
        mensaje_contacto.save()
        
        response_data = {
            'mensaje': 'Mensaje enviado correctamente.'
        }
        return JsonResponse(response_data)
    
    return render(request, 'frontend/contact.html')

# Vista para el inicio de sesión
def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)  # Aquí solo pasas 'request' y 'user' se maneja automáticamente
            # Redirige al usuario a la página deseada después del inicio de sesión
            return redirect('index')
        else:
            # Manejo de errores si el usuario no puede ser autenticado
            messages.error(request, 'Credenciales inválidas')

    # Renderiza el formulario de inicio de sesión en cualquier caso
    return render(request, 'login.html')


#vista para el perfil del usuario logeado y cerrando sesión
@login_required
def perfil_view(request):
    compras = Compra.objects.filter(usuario=request.user).order_by('-fecha')
    return render(request, 'frontend/perfil.html', {'compras': compras})

def logout_view(request):
    logout(request)
    messages.success(request, 'Has cerrado sesión exitosamente.')
    return redirect('login')  # O la página a la que quieras redirigir después del logout


@require_GET
def check_auth(request):
    return JsonResponse({'is_authenticated': request.user.is_authenticated})


#API que procesa el perfil de usuario con su resumen de compra
@login_required
def perfil_usuario(request):
    user = request.user
    compras = Compra.objects.filter(usuario=user).order_by('-fecha')
    
    context = {
        'user': user,
        'compras': compras,
    }
    
    return render(request, 'frontend/perfil.html', context)



@login_required
def historial_compras(request):
    user = request.user
    compras = Compra.objects.filter(usuario=user).order_by('-fecha')
    
    context = {
        'user': user,
        'compras': compras,
    }
    
    return render(request, 'frontend/historialcompras.html', context)