from django.test import TestCase
from django.urls import reverse
from .models import Servicio, Pedido
from blog.models import Categoria, Post


class CafeteriaTests(TestCase):
    def setUp(self):
        self.servicio = Servicio.objects.create(
            titulo='Café Espresso',
            contenido='Café corto concentrado',
            tipo='cafe_caliente',
            precio='1.50',
        )
        self.categoria = Categoria.objects.create(
            nombre='Ofertas',
            descripcion='Ofertas de la semana',
        )
        self.post = Post.objects.create(
            titulo='2x1 en Café Espresso',
            subtitulo='Solo por hoy',
            contenido='Promoción especial 2x1',
            etiqueta_oferta='2x1',
        )
        self.post.categorias.add(self.categoria)

    def test_paginas_cargan_correctamente(self):
        self.assertEqual(self.client.get(reverse('servicios:inicio')).status_code, 200)
        self.assertEqual(self.client.get(reverse('servicios:menu_pedidos')).status_code, 200)
        self.assertEqual(self.client.get(reverse('blog:lista')).status_code, 200)
        self.assertEqual(
            self.client.get(reverse('blog:categoria', args=[self.categoria.id])).status_code,
            200,
        )
        self.assertEqual(self.client.get(reverse('servicios:modificar_pagina')).status_code, 200)

    def test_pasarela_crea_pedido_con_created_y_updated(self):
        resp = self.client.post(
            reverse('servicios:menu_pedidos'),
            {
                'cliente_nombre': 'Estudiante UTM',
                'cliente_telefono': '0991112223',
                'modalidad': 'mesa',
                'mesa_o_direccion': 'Mesa 5',
                'metodo_pago': 'efectivo',
                f'cantidad_{self.servicio.id}': '2',
            },
        )
        self.assertEqual(resp.status_code, 302)
        pedido = Pedido.objects.first()
        self.assertIsNotNone(pedido)
        self.assertEqual(float(pedido.total), 3.00)
        self.assertIsNotNone(pedido.created)
        self.assertIsNotNone(pedido.updated)
