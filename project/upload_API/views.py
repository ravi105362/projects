from django.shortcuts import render

# Create your views here.
from django.views import View
from django.http import JsonResponse
from .models import BlockItem
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json

@method_decorator(csrf_exempt, name='dispatch')
class project(View):

    def post(self, request):
        
        """
        POST method to parse a receipt and store the relevant data in DB
        """
        receipt_data=request.body.decode("utf-8")
        relevant_receipt_data=receipt_data.split("text/plain")

        #Data is now divided in blocks
        data_in_blocks=relevant_receipt_data[1].split("\r\n\r\n")
        
        block=1
        row=1
        col=1
        last_row=1

        for each_block in data_in_blocks :

            #ignoring the irrelevant data
            if(block>8):
                break

            # Counting the number of new lines in each_block
            if(each_block.count('\r\n')>=1):
                row=row+each_block.count('\r\n')

            #checking if the block is empty then ignoring the further processing
            if(len(each_block)==0):
                continue

            #Removing the blocks created due to '-'
            if(each_block.count('-')>=2):
                each_block=each_block.split('--')
            
            #checking if the new block was created due to '-' or not
            if(isinstance(each_block, list)):
                if(len(each_block[-1])==0):
                    continue
                to_be_pushed=each_block[-1]
                k=each_block[-1].split('\n')
                col_end=len(k[-1])
            elif (isinstance(each_block, str)):
                if(len(each_block)==0):
                    continue
                to_be_pushed=each_block
                k=each_block.split('\n')
                col_end=len(k[-1])

            #final block information to be added 
            product_data = {
                'current_block':block,
                'begin_row': last_row,
                'end_row': row,
                'begin_col': col,
                'end_col':col_end,
                'data_string': to_be_pushed,
            }
            cart_item = BlockItem.objects.create(**product_data)

            #updating the block
            block=block+1
            
            #updating row by 2 as each block was containing two new line items
            row=row+2

            #keeping the last_row value to track the begin row for next block
            last_row=row
            
        data = {
            "message": f"New item added to DB with id: {cart_item.id}"
        }
        return JsonResponse(data, status=201)

    def get(self, request):

        """
        GET method to get the relevant information from the DB
        """

        #count of the number of items in DB
        items_count = BlockItem.objects.count()

        #getting the actual items
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

        """
        Delete method to delete the items from DB
        """

        #getting the items in DB
        items = BlockItem.objects.all()

        #deleting the items in DB
        item.delete() for item in items

        data={
            'items': True,
        }
        return JsonResponse(data)