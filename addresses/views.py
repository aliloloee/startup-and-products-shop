from django.core import serializers
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

from . models import City



@login_required
def get_cities(request) :
    if request.is_ajax() :
        province_id = request.GET.get('province')
        cities = serializers.serialize('json',
                                        City.objects.filter(province=province_id),
                                        fields=('city', ))

        return JsonResponse({'cities':cities}, status=200)
