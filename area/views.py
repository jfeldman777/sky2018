from django.shortcuts import render
from django.db.models import Q
from .models import Area
from sky.models import MagicNode

# Create your views here.
def index(request):
    return render(request,'area/index3.html',
        {})

def areas_admin(request):
    node_id = request.session.get('node_id')
    node_name = request.session.get('node_name')
    print(node_id, node_name)

    my_areas = Area.objects.filter(user = request.user)
    areas = Area.objects.filter(is_published = True).exclude(user = request.user)
    area_id = request.session.get('selected_area')
    area_selected = Area.objects.get(id = area_id)

    return render(request,'area/admin.html',
        {
            'my_areas':my_areas,
            'areas':areas,
            'node_name':node_name,
            'area_selected':area_selected
        })

def using_areas(request):
    return render(request,'area/using.html',
        {})

def area_create(request):
    node_id = request.session.get('node_id')
    print(node_id)
    node = MagicNode.objects.get(id = node_id)
    print(node)
    area = Area.objects.create(user = request.user, name = node.desc, root = node)
    request.session['selected_area']=area.id

    my_areas = Area.objects.filter(user = request.user).exclude(id = area.id)
    areas = Area.objects.filter(is_published = True).exclude(user = request.user)

    return render(request,'area/admin.html',{
        'selected_area':area,
        'areas':areas,
        'my_areas':my_areas,
        'root':node
        }

            )
