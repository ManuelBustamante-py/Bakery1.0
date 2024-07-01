# Create your views here.
# frontend/views.py
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from .models import Producto
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.core.mail import send_mail
from django.http import JsonResponse, HttpResponseRedirect
import json
from django.core.exceptions import ObjectDoesNotExist
from .models import MensajeContacto
from django.shortcuts import render, redirect
from .models import MensajeContacto
from django.contrib import messages
from django.http import JsonResponse
from .forms import ContactForm 
from django.urls import reverse

def index(request):
    return render(request, 'frontend/index.html')

def about(request):
    return render(request, 'frontend/about.html')

def admin_page(request):
    return render(request, 'frontend/Admin.html')

def contact(request):
    return render(request, 'frontend/contact.html')

def login(request):
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

@api_view(['GET'])
def obtener_stock(request):
    productos = Producto.objects.all()
    data = []
    for producto in productos:
        data.append({
            'nombre': producto.nombre,
            'precio': producto.precio,  # Asegúrate de tener el campo 'precio' en tu modelo Producto
            'stock': producto.stock
        })
    return Response({'productos': data})

(['GET', 'POST'])
def procesar_pago(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            productos = data.get('productos', [])
            email = data.get('email', '')
            
            if not email:
                return JsonResponse({"error": "Correo electrónico requerido"}, status=400)
            
            total = 0
            detalles = ""
            
            for item in productos:
                try:
                    producto = Producto.objects.get(nombre=item['name'])
                    if producto.stock < item['quantity']:
                        return JsonResponse({"error": f"No hay suficiente stock de {producto.nombre}"}, status=400)
                    
                    producto.stock -= item['quantity']
                    producto.save()
                    total += producto.precio * item['quantity']
                    detalles += f"{producto.nombre}: {item['quantity']} x ${producto.precio} = ${producto.precio * item['quantity']}\n"
                
                except ObjectDoesNotExist:
                    return JsonResponse({"error": f"El producto {item['name']} no existe en la base de datos"}, status=400)
            
            send_mail(
                'Resumen de su compra',
                f"Gracias por su compra. Aquí está su resumen:\n\n{detalles}\nTotal: ${total}\n\nDatos de la transferencia: [Datos ficticios aquí]",
                'tuemail@example.com',
                [email],
                fail_silently=False,
            )
            
            return JsonResponse({"message": "Pago procesado exitosamente"})
        
        except json.JSONDecodeError:
            return JsonResponse({"error": "Error en el formato JSON de la solicitud"}, status=400)
        
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    
    elif request.method == 'GET':
        # Aquí podrías implementar la lógica para obtener detalles adicionales o información requerida
        return JsonResponse({"message": "Endpoint para procesar pagos. Envía una solicitud POST para procesar un pago."})

    return JsonResponse({"error": "Método no permitido"}, status=405)

@api_view(['GET', 'POST'])
def enviar_resumen(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get('email')
            productos = data.get('productos', [])
            total = data.get('total')

            # Construir el mensaje del correo electrónico
            mensaje = "Resumen de tu compra:\n\n"
            for item in productos:
                mensaje += f"{item['name']} - Cantidad: {item['quantity']} - Precio: {item['price']}\n"
            mensaje += f"\nTotal: {total}"

            # Enviar el correo electrónico
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
        # Aquí podrías implementar la lógica para devolver detalles adicionales o información requerida
        return JsonResponse({"message": "Endpoint para enviar resúmenes de compra. Envía una solicitud POST para enviar un resumen."})

    return JsonResponse({"error": "Método no permitido"}, status=405)

def registro_usuario(request):
    return render(request, 'RegistroUsuario.html')


@csrf_exempt
def enviar_mensaje_contacto(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        email = request.POST.get('email')
        asunto = request.POST.get('asunto')
        mensaje = request.POST.get('mensaje')
        
        # Guardar en la base de datos
        mensaje_contacto = MensajeContacto(nombre=nombre, email=email, asunto=asunto, mensaje=mensaje)
        mensaje_contacto.save()
        
        # Preparar respuesta JSON
        response_data = {
            'mensaje': 'Mensaje enviado correctamente.'
        }
        return JsonResponse(response_data)
    
    # Si no es POST, renderiza el formulario
    return render(request, 'contact.html')

def contact_view(request):
    if request.method == 'POST':
        # Procesar el formulario enviado
        form = ContactForm(request.POST)
        if form.is_valid():
            # Guardar los datos del formulario en la base de datos
            form.save()
            return redirect('ruta_de_exito')  # Redirigir a una página de éxito o a donde necesites
    else:
        form = ContactForm()  # Instancia del formulario vacío para mostrarlo

    return render(request, 'template.html', {'form': form})


def contact(request):
    if request.method == 'POST':
        # Obtener datos del formulario
        nombre = request.POST.get('nombre')
        email = request.POST.get('email')
        asunto = request.POST.get('asunto')
        mensaje = request.POST.get('mensaje')
        
        # Validar que todos los campos estén llenos y que el correo contenga '@'
        if not nombre or not email or not asunto or not mensaje or '@' not in email:
            return render(request, 'frontend/contact.html', {'error_message': 'Por favor completa todos los campos correctamente.'})
        
        # Guardar en la base de datos usando el modelo MensajeContacto
        mensaje_contacto = MensajeContacto(nombre=nombre, email=email, asunto=asunto, mensaje=mensaje)
        mensaje_contacto.save()
        
        # Redirigir a una nueva URL después de guardar en la base de datos
        return redirect(reverse('contact') + '?success=true')
    
    # Si la solicitud no es POST, renderizar el template de contacto
    return render(request, 'frontend/contact.html')