from dataclasses import field

from django.shortcuts import render, redirect
from django.urls import reverse
from django.core.paginator import Paginator
import csv
from django.conf import settings


def index(request):
    return redirect(reverse('bus_stations'))


def bus_stations(request):
    # получите текущую страницу и передайте ее в контекст
    # также передайте в контекст список станций на странице

    file_path = settings.BUS_STATION_CSV
    required_fields = ['Name', 'Street', 'District']

    with open(file_path, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        content = []

        for row in reader:
            row_filtered = {field: row[field] for field in required_fields if field in row}
            content.append(row_filtered)

    page_number = int(request.GET.get('page', 1))
    paginator = Paginator(content,10)
    page = paginator.get_page(page_number)

    context = {
         'bus_stations': page.object_list,
         'page': page,
    }
    return render(request, 'stations/index.html', context)
