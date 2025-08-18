from contextlib import nullcontext

from django.http import Http404
from django.shortcuts import render

from main.models import Car, Client, Sale


def cars_list_view(request):
    # получите список авто
    cars = Car.objects.all()

    contex = {
        'cars': cars
    }

    template_name = 'main/list.html'
    return render(request, template_name, contex)  # передайте необходимый контекст


def car_details_view(request, car_id):
    # получите авто, если же его нет, выбросьте ошибку 404
    try:
        car = Car.objects.get(id=car_id)
    except Car.DoesNotExist:
        raise Http404('Car not found')

    template_name = 'main/details.html'
    return render(request, template_name, {'car': car})  # передайте необходимый контекст


def sales_by_car(request, car_id):
    try:
        # получите авто и его продажи
        sales = Sale.objects.filter(car=car_id)
        car = Car.objects.get(id=car_id)
    except Car.DoesNotExist:
        raise Http404('Car not found')

    contex = {
        'car': car,
        'sales': sales
    }

    template_name = 'main/sales.html'
    return render(request, template_name, contex)  # передайте необходимый контекст

