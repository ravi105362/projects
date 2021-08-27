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
        #print(request.read())
        old_data=request.body.decode("utf-8")
        
        print("after splitting the data")
        old_data_1=old_data.split("text/plain")
        new_data=old_data_1[1].split("\r\n\r\n")
        block=1
        row=1
        col=1
        last_row=1
        for i in new_data :

            if(block>8):
                break

            if(i.count('\r\n')>=1):
                row=row+i.count('\r\n')

            if(len(i)==0) :
                continue
            if(i.count('-')>=2):
                i=i.split('--')
            
            if(isinstance(i, list)):
                if(len(i[-1])==0):
                    continue
                to_be_pushed=i[-1]
                k=i[-1].split('\n')
                col_end=len(k[-1])
            elif (isinstance(i, str)):
                if(len(i)==0):
                    continue
                to_be_pushed=i
                k=i.split('\n')
                col_end=len(k[-1])
    
            product_data = {
                'current_block':block,
                'begin_row': last_row,
                'end_row': row,
                'begin_col': col,
                'end_col':col_end,
                'data_string': to_be_pushed,
            }
            cart_item = BlockItem.objects.create(**product_data)
            block=block+1
            row=row+2
            last_row=row
            
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
                'current_block' : item.current_block,
                'begin_row': item.begin_row,
                'end_row': item.end_row,
                'begin_col': item.begin_col,
                'end_col': item.end_col,
                'data_string' : item.data_string,
            })

        data = {
            'items': items_data,
            'count': items_count,
        }

        return JsonResponse(data)
    
    def delete(self,request) :
        items = BlockItem.objects.all()
        for item in items:
            item.delete()

        data={
            'items': True,
        }
        return JsonResponse(data)