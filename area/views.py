from django.shortcuts import render
from django.db.models import Q
from .models import Area, AreaPlus
from sky.models import MagicNode
from sky.views import tree_count, tree_next

def areas_admin(request):
    my_areas = Area.objects.filter(user = request.user)
    areas = Area.objects.filter(is_published = True).exclude(user = request.user)
    return render(request,'area/admin.html',
        {
            'my_areas':my_areas,
            'areas':areas,
        })

def using_areas(request):
    my_areas = Area.objects.filter(user = request.user)
    areas = Area.objects.filter(is_published = True).exclude(user = request.user)

    return render(request,'area/using.html',
        {
            'my_areas':my_areas,
            'areas':areas,
        })

def bag(request,id):
    area = Area.objects.get(id=id)
    my_areas = Area.objects.filter(user = request.user)
    areas = Area.objects.filter(is_published = True).exclude(user = request.user)
    qq = AreaPlus.objects.filter(area = area)

    xx = []
    for q in qq:
        if q.alone:
            x1 = 'minus'
        else:
            x1 = 'plus'

        if q.minus:
            x2 = 'minus'
        else:
            x2 = 'plus'
        xx.append((q.node, x1, x2))

    return render(request,'area/admin.html',
        {
            'my_areas':my_areas,
            'areas':areas,
            'root': area.root,
            'bag':xx,
            'area':area,
        })


def report2(request,id):
    my_areas = Area.objects.filter(user = request.user)
    areas = Area.objects.filter(is_published = True).exclude(user = request.user)

    area = Area.objects.get(id=id)
    node = area.root

    children = node.get_children()
    siblings = node.get_siblings()

    count = [0]*6
    tree_count(count,node,request.user)
    next = tree_next(node,request.user)

    return render(request,'area/using.html',
        {
            'my_areas':my_areas,
            'areas':areas,
            'area':area,
             'count0':count[0],
             'count1':count[1],
             'count2':count[2],
             'count3':count[3],
             'count4':count[4],
             'count5':count[5],
             'next':next,
             })

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
