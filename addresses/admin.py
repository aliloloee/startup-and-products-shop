from django.contrib import admin
from django.template.response import TemplateResponse
from django.urls import path
from django.shortcuts import redirect
from django.contrib import messages

import json

from .models import Province, City
from .forms import BulkAdd


@admin.register(City)
class CityAdmin(admin.ModelAdmin) :
    list_display = ('city', 'province', 'pk',)
    list_filter = ('province__province', )
    list_per_page = 10


@admin.register(Province)
class ProvinceAdmin(admin.ModelAdmin) :
    change_list_template = 'admin/addresses/change_list.html'


    list_display = ('province', 'pk',)

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('bulk_add/', self.bulk_add, name='bulk_add'),
        ]
        return my_urls + urls

    def bulk_add(self, request) :
        context = dict(
            self.admin_site.each_context(request),
        )
        if request.method == 'GET' :
            bulk_form = BulkAdd()

        if request.method == 'POST' :
            cities = []
            bulk_form = BulkAdd(request.POST, request.FILES)
            if bulk_form.is_valid() :

                f = json.load(request.FILES['file'])
                for prov, city_list in f.items() :
                    province = Province.objects.create(province=prov)
                    for city in city_list :
                        cities.append(City(province=province, city=city))
                City.objects.bulk_create(cities)  

                messages.add_message(request, messages.SUCCESS, 'Bulk creation of provinces and cities was successful')
                return redirect('admin:addresses_province_changelist')

        context['form'] = bulk_form
        return TemplateResponse(request, "admin/addresses/bulk_add.html", context)

