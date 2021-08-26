from django.shortcuts import render

# Create your views here.
from django.views import View
from django.http import JsonResponse
import json
from .models import BlockItem
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

@method_decorator(csrf_exempt, name='dispatch')
class project(View):
    def post(self, request):
        
        data = json.loads(request.body.decode("utf-8"))

        product_data = {
            'product_name': 1,
            'product_price': 2,
            'product_quantity': 3,
        }

        cart_item = BlockItem.objects.create(**product_data)

        data = {
            "message": f"New item added to Cart with id: {cart_item.id}"
        }
        return JsonResponse(data, status=201)

    def get(self, request):
        items_count = BlockItem.objects.count()
        items = BlockItem.objects.all()

        items_data = []
        for item in items:
            items_data.append({
                'product_name': item.product_name,
                'product_price': item.product_price,
                'product_quantity': item.product_quantity,
            })

        data = {
            'items': items_data,
            'count': items_count,
        }

        return JsonResponse(data)