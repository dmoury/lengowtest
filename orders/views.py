from django.shortcuts import render, redirect  
from orders.forms import OrderForm  
from orders.models import Order  
from xml.dom import minidom, Node
from django.http import HttpResponse
from django.contrib import messages
import requests
import os

filename = "tmp_data.xml"

def create(request):  
    if request.method == "POST":  
        form = OrderForm(request.POST)  
        if form.is_valid():  
            try:  
                form.save()
                messages.success(request, "Order created successfully")
                return redirect('/list')  
            except:  
                pass  
    else:  
        form = OrderForm()  
    return render(request,'new.html',{'form':form})  

def show(request):  
    orders = Order.objects.all()  
    return render(request,"index.html",{'orders':orders})

def edit(request, id):  
    order = Order.objects.get(id=id)  
    return render(request,'edit.html', {'order':order})  

def update(request, id):  
    order = Order.objects.get(id=id)  
    form = OrderForm(request.POST, instance = order)  
    if form.is_valid():
        form.save()
        messages.success(request, "Order modified successfully")
        return redirect("/list")  
    return render(request, 'edit.html', {'order': order})  

def destroy(request, id):  
    order = Order.objects.get(id=id)  
    order.delete()
    messages.success(request, "Order deleted successfully")
    return redirect("/list")

# Get orders from remote XML file.
def getOrders():
    data = requests.get("http://test.lengow.io/orders-test.xml").text
    f = open(filename, "w")
    f.write(data)
    f.close()
    parsedData = minidom.parse(filename)
    ordersDom = parsedData.getElementsByTagName("orders").item(0)
    return ordersDom.getElementsByTagName("order")

# Get field value from XML file.
def getField(container, xmlField):
    orderField = container.getElementsByTagName(xmlField).item(0)
    if(orderField.firstChild):
        return orderField.firstChild.data
    return ''

# Return XML file as Array of object.
def upload(request):
    orders = getOrders()
    for order in orders:
        orderId = getField(order, 'order_id')
        try:
            newOrder = Order.objects.get(order_id=orderId)
        except:
            marketplace = getField(order, 'marketplace')
            # Status fields
            status = order.getElementsByTagName("order_status").item(0)
            marketplaceStatus = getField(status, 'marketplace')
            lengowStatus = getField(status, 'lengow')

            orderDate = getField(order, 'order_purchase_date')
            formatedDate = orderDate if orderDate != '' else None
            amount = getField(order, 'order_amount')
            currency = getField(order, 'order_currency')
            newOrder = Order(None, orderId, marketplace, amount, currency, marketplaceStatus, lengowStatus, formatedDate)

            newOrder.save()
    #delete temporary file
    os.remove(filename)
    messages.success(request, "Orders uploaded successfuly !")
    return redirect("/list")