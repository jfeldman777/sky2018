from django.shortcuts import render
from django.db.models import Q
from .models import Area, AreaPlus
from .forms import RenameForm
from sky.models import MagicNode
from sky.views import tree_count, tree_next

def delete_line(request,id, line_id):
    plus = AreaPlus.objects.get(id=line_id)
    plus.delete()
    return bag(request,id)

def col1(request,id, line_id):
    plus = AreaPlus.objects.get(id=line_id)
    plus.alone = not plus.alone
    plus.save()
    return bag(request,id)

def col2(request,id, line_id):
    plus = AreaPlus.objects.get(id=line_id)
    plus.minus = not plus.minus
    plus.save()
    return bag(request,id)


def rename(request, id):
    area = Area.objects.get(id=id)
    if request.method == 'POST':
        form = RenameForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            area.name = name
            area.save()
    else:
        form = RenameForm(initial={'name':area.name})
        return render(request,'area/rename.html',
            {
            'form':form
            })

    return bag(request,id)

def areas_admin(request):
    my_areas = Area.objects.filter(user = request.user)
    node_name = request.session.get('node_name')
    node_id = request.session.get('node_id')
    return render(request,'area/admin.html',
        {
            'node_name':node_name,
            'node_id':node_id,
            'my_areas':my_areas,
        })

def add(request,area_id):
    area = Area.objects.get(id=area_id)
    my_areas = Area.objects.filter(user = request.user)
    node_id = request.session.get('node_id')

    plus = AreaPlus(area = area, node_id = node_id)
    plus.save()

    root = area.root

    xx = my_bag(area)

    return render(request,'area/admin.html',
        {
            'my_areas':my_areas,
            'area':area,
            'bag':xx,
            'root':root,
        })

def using_areas(request):
    my_areas = Area.objects.filter(user = request.user)
    areas = Area.objects.filter(is_published = True).exclude(user = request.user)

    return render(request,'area/using.html',
        {
            'my_areas':my_areas,
            'areas':areas,
        })

def my_bag(area):
    qq = AreaPlus.objects.filter(area = area)

    xx = []
    if qq:
        for q in qq:
            if q.alone:
                x1 = 'minus'
            else:
                x1 = 'plus'

            if q.minus:
                x2 = 'minus'
            else:
                x2 = 'plus'
        xx.append((q.node, x1, x2, q.id))
    return xx

def pub(request,id):
    area = Area.objects.get(id=id)
    area.is_published = True
    area.save()
    return bag(request,id)

def unpub(request,id):
    area = Area.objects.get(id=id)
    area.is_published = False
    area.save()
    return bag(request,id)

def bag(request,id):
    area = Area.objects.get(id=id)
    my_areas = Area.objects.filter(user = request.user)
    areas = Area.objects.filter(is_published = True).exclude(user = request.user)

    xx = my_bag(area)

    node_name = request.session.get('node_name')
    node_id = request.session.get('node_id')
    return render(request,'area/admin.html',
        {
            'node_name':node_name,
            'node_id':node_id,
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

def delete_area(request,id):
    area = Area.objects.get(id=id)
    area.delete()
    my_areas = Area.objects.filter(user = request.user)
    return render(request,'area/admin.html',
        {
            'my_areas':my_areas,
        })

def area_create(request):
    node_id = request.session.get('node_id')
    node = MagicNode.objects.get(id = node_id)
    area = Area(user = request.user, name = node.desc, root = node)
    area.save()
    my_areas = Area.objects.filter(user = request.user)
    areas = Area.objects.filter(is_published = True).exclude(user = request.user)

    return render(request,'area/admin.html',{
        'areas':areas,
        'my_areas':my_areas,
        'root':node
        }

            )
