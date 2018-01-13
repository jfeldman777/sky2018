from django.shortcuts import render
from django.db.models import Q
from .models import Area, AreaPlus
from .forms import RenameForm
from sky.models import MagicNode, Interest

def count_me(count,me):
    for i in range(len(count)):
        count[i]+=me[i]
    return

def node2me(user,node):
    nd,create = Interest.objects.get_or_create(user = user, topic = node)
    b3 = [False]*3
    b3[0] = nd.i_like_the_topic
    b3[1] = nd.i_like_the_content
    b3[2] = nd.i_am_an_expert

    me = [0]*6
    if b3[0]:
        me[0]+=1
    else:
        me[1]+=1
    if b3[1]:
        me[2]+=1
    else:
        me[3]+=1
    if b3[2]:
        me[4]+=1
    else:
        me[5]+=1
    return me

def clean_list(s):
    s1 = list(s)
    for i in range(len(s1)):
        for j in range(i,len(s1)):
            if s1[i].is_descendant_of(s1[j]):
                s.remove(s1[i])
            if s1[j].is_descendant_of(s1[i]):
                s.remove(s1[j])
    return

def tree_c(user,count,node,lt_minus,ln_minus):
    if node in lt_minus:
        return

    if node not in ln_minus:
        me = node2me(user,node)
        count_me(count,me)

    for n in node.get_children():
        tree_c(user,count,n,lt_minus,ln_minus)

    pass

def tree_count2(user,count,ln_plus,lt_plus,lt_minus,ln_minus):
    for n in ln_plus:
        me = node2me(user,n)
        count_me(count,me)

    for n in lt_plus:
        tree_c(user,count,n,lt_minus,ln_minus)

    pass
#########################################################
def next_c(user,node,lt_minus,ln_minus):
    if node in lt_minus:
        return

    if node not in ln_minus:
        interest,created = Interest.objects.get_or_create(user = user, topic = node)
        if not interest.i_am_an_expert:
            raise Exception(node)

    for n in node.get_children():
        next_c(user,n,lt_minus,ln_minus)

    pass

def next_count2(user,ln_plus,lt_plus,lt_minus,ln_minus):
    for node in ln_plus:
        interest,created = Interest.objects.get_or_create(user = user, topic = node)
        if not interest.i_am_an_expert:
            raise Exception(node)

    for n in lt_plus:
        next_c(user,n,lt_minus,ln_minus)

    pass


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

    lt_plus = [area.root]
    qq_tree_plus = AreaPlus.objects.filter(area=area,alone=False,minus=False)
    if qq_tree_plus:
        lt_plus += [p.node for p in qq_tree_plus]

    clean_list(lt_plus)

    lt_minus = []
    qq_tree_minus = AreaPlus.objects.filter(area=area,alone=False,minus=True)
    if qq_tree_minus:
        lt_minus += [p.node for p in qq_tree_minus]

    clean_list(lt_minus)
#################################################################################
    ln_plus = []
    qq_node_plus = AreaPlus.objects.filter(area=area,alone=True,minus=False)
    if qq_node_plus:
        ln_plus += [p.node for p in qq_node_plus]

    ln_minus = []
    qq_node_minus = AreaPlus.objects.filter(area=area,alone=True,minus=True)
    if qq_node_minus:
        ln_minus += [p.node for p in qq_node_minus]


    count = [0]*6
    tree_count2(request.user,count,ln_plus,lt_plus,lt_minus,ln_minus)
    try:
        next_count2(request.user,ln_plus,lt_plus,lt_minus,ln_minus)
        next = MagicNode.get_first_root_node()
    except Exception as e:
        next = e.args[0]
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
