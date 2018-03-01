from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from .forms import SignUpForm, AddItemForm, ChangeFigureForm
from .forms import ChangeItemForm, ChangeTxtForm, MoveItemForm
from .models import NewsRecord, MagicNode, Interest, Profile
from area.models import Subscription
from django.contrib.auth.models import User

from sea.models import Boat

from collections import Counter
from operator import itemgetter
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .forms import NameForm
from django.http import JsonResponse

def total():
    return MagicNode.objects.count()

def ready():
    return MagicNode.objects.filter(is_ready = True).count()

def topic_by_name(request, name):
    try:
        node = MagicNode.objects.get(desc = name)
        return topic_tree(request,node.id)
    except:
        return msg(request, 'node not found:'+name+'?')

def change_txt(request,id):
    node = MagicNode.objects.get(id=id)
    if request.method == 'POST':
        form = ChangeTxtForm(request.POST)
        if form.is_valid():
            node.is_ready = form.cleaned_data['is_ready']
            node.desc = form.cleaned_data['desc']
            node.text = form.cleaned_data['text']
            node.next = form.cleaned_data['next']
            node.sites = form.cleaned_data['sites']
            node.videos = form.cleaned_data['videos']
            node.video = form.cleaned_data['video']

            node.pre_nodes = form.cleaned_data['pre_nodes']
            node.post_nodes = form.cleaned_data['post_nodes']

            node.friends = form.cleaned_data['friends']
            node.sib_order = form.cleaned_data['sib_order']

            node.save()
            return msg(request,'change request done')
        else:
            return msg(request,'change request failed')
    # if a GET (or any other method) we'll create a blank form
    else:
        form = ChangeTxtForm(
            initial={
                'is_ready':node.is_ready,
                'next':node.next,
                'desc':node.desc,
                'text':node.text,
                'sites':node.sites,
                'videos':node.videos,
                'video':node.video,
                'pre_nodes':node.pre_nodes,
                'post_nodes':node.post_nodes,
                'friends':node.friends,
                'sib_order':node.sib_order,
                }
                )

        return render(request, 'change_item.html',
            {'form': form,
            })

def change_item(request,id):
    node = MagicNode.objects.get(id=id)
    parent = node.parent
    if request.method == 'POST':
        form = ChangeItemForm(request.POST, request.FILES)
        if form.is_valid():

            node.parent = form.cleaned_data['parent']
            node.desc = form.cleaned_data['desc']
            node.text = form.cleaned_data['text']
            node.next = form.cleaned_data['next']

            node.sites = form.cleaned_data['sites']
            node.videos = form.cleaned_data['videos']

            node.pre_nodes = form.cleaned_data['pre_nodes']
            node.friends = form.cleaned_data['friends']
            node.sib_order = form.cleaned_data['sib_order']

            node.video = form.cleaned_data['video']
            node.figure = form.cleaned_data['figure']

            node.save()
            return msg(request,'change request done')
        else:
            return msg(request,'change request failed')
    # if a GET (or any other method) we'll create a blank form
    else:
        form = ChangeItemForm(
            initial={
                'next':node.next,
                'parent':node.parent,
                'desc':node.desc,
                'text':node.text,
                'sites':node.sites,
                'videos':node.videos,
                'pre_nodes':node.pre_nodes,
                'friends':node.friends,
                'sib_order':node.sib_order,
                'video':node.video,
                'figure':node.figure
                }
                )

        return render(request, 'change_item.html',
            {'form': form,
            })

def change_figure(request,id):
    node = MagicNode.objects.get(id=id)
    if request.method == 'POST':
        form = ChangeFigureForm(request.POST, request.FILES)
        if form.is_valid():
            node.figure = form.cleaned_data['figure']
            node.save()
            return msg(request,'change request done')
        else:
            return msg(request,'change request failed')
    # if a GET (or any other method) we'll create a blank form
    else:
        form = ChangeFigureForm(
            initial={
                'figure':node.figure
                }
                )

        return render(request, 'change_figure.html',
            {'form': form,
            })

def move_item(request,id):
    node = MagicNode.objects.get(id=id)
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = MoveItemForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            base_name = form.cleaned_data['base_name']
            location = int(form.cleaned_data['location'])

            base_node = MagicNode.objects.get(desc=base_name)
            if location == 1:
                node.move(base_node,pos='left')
            elif location == 2:
                node.move(base_node,pos='right')
            else:
                node.move(base_node,pos='first-child')

            return msg(request,'item moved')
        else:
            return msg(request,'cannnot move item')
    # if a GET (or any other method) we'll create a blank form
    else:
        form = MoveItemForm()

        return render(request, 'move_item.html',
            {'form': form,
            })

def add_item(request,id,location):
    old_node = MagicNode.objects.get(id=id)
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = AddItemForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            name = form.cleaned_data['name']
            location = int(form.cleaned_data['location'])

            new_node = MagicNode(desc=name)
            if location == 1:
                old_node.add_sibling('left',instance=new_node)
            elif location == 2:
                old_node.add_sibling('right',instance=new_node)
            else:
                old_node.add_child(instance=new_node)

            return msg(request,'child created')
        else:
            return msg(request,'cannnot create child')
    # if a GET (or any other method) we'll create a blank form
    else:
        form = AddItemForm(initial={'location':location})

        return render(request, 'add_item.html',
            {'form': form,
            'old_node':old_node,
            'location':location,
            })

def tree(request,id):
    node = MagicNode.get_first_root_node()
    if id!=0:
        node = MagicNode.objects.get(id=id)
    annotated_list = MagicNode.get_annotated_list(parent=node)
    return render(request,'tree.html',
                    {'annotated_list':annotated_list,
                     })

def ajax(request, node, you):
    res = 0
    i,created = Interest.objects.get_or_create(topic = node, user = request.user)
    if you == 10:
        i.i_like_the_topic = False
    elif you == 11:
        i.i_like_the_topic = True
    elif you == 20:
        i.i_like_the_content = False
    elif you == 21:
        i.i_like_the_content = True
    elif you == 30:
        i.i_am_an_expert = False
    else:
        i.i_am_an_expert = True

    try:
        i.save()
        res = 1
    except:
        pass

    context = {'result': res}

    print('ajax on the fly')

    return JsonResponse(context)

def tree_next(node,user):
    me = Interest.objects.get(user = user, topic = node)
    if not me.i_am_an_expert:
        return node
    else:
        children = node.get_children()
        if children:
            for x in children:
                res = tree_next(x,user)
                if res:
                    return res
    return  MagicNode.get_first_root_node()

def tree_count(count, node, user):
    me,c = Interest.objects.get_or_create(user = user, topic = node)
    if me.i_like_the_topic:
        count[0]+=1
    else:
        count[1]+=1
    if me.i_like_the_content:
        count[2]+=1
    else:
        count[3]+=1
    if me.i_am_an_expert:
        count[4]+=1
    else:
        count[5]+=1

    children = node.get_children()
    for child in children:
        tree_count(count,child,user)


def report(request,id):
    node = MagicNode.objects.get(id=id)

    children = node.get_children()
    parent = node.get_parent()
    siblings = node.get_siblings()

    count = [0]*6
    tree_count(count,node,request.user)
    next = tree_next(node,request.user)

    return render(request,'report.html',
                    {'node':node,
                     'children':children,
                     'parent':parent,
                     'siblings':siblings,
                     'count0':count[0],
                     'count1':count[1],
                     'count2':count[2],
                     'count3':count[3],
                     'count4':count[4],
                     'count5':count[5],
                     'next':next,
                     })

def topic_tree(request,id):
    more_count = Boat.objects.filter(node_id=id).count()

    current = None
    if not request.user.is_anonymous:
        current,c = Profile.objects.get_or_create(user = request.user)

    pre_nodes = []
    get = lambda node_id: MagicNode.objects.get(pk=node_id)
    get_by_name = lambda name: MagicNode.objects.filter(desc = name)
    t1,t2,t3 = (False,False,False)

    try:
        try:
            node = get(id)
        except:
            node = MagicNode.get_first_root_node()

        if node.is_root():
            node = node.get_first_child()

        try:
            i,created = Interest.objects.get_or_create(user = request.user, topic = node)
            t1,t2,t3 = (i.i_like_the_topic, i.i_like_the_content, i.i_am_an_expert)
        except:
            print(request.user, node, "cannot find interest")

        children = node.get_children()
        parent = node.get_parent()
        siblings = node.get_siblings()

    except:
        children = []
        siblings = []
        parent = None
        node = None
        friends = []

    p1 = 10 if t1 else 11
    p2 = 20 if t2 else 21
    p3 = 30 if t3 else 31

    if node:
        request.session['node_id'] = node.id
        request.session['node_name'] = node.desc
        if current:
            current.node_last_visited = node
            current.save()

    sub_in = []
    if not request.user.is_anonymous:
        sub = Subscription.objects.filter(user = request.user)
        sub_in = [s.area for s in sub]

    return render(request,'topic_tree.html',
                    {'node':node,
                     'children':children,
                     'parent':parent,
                     'siblings':siblings,
                     't1':p1,
                     't2':p2,
                     't3':p3,
                     'sub':sub_in,
                     'more_count':more_count,
                     })

def user2expert(user):
    i = Interest.objects.filter(user = user, i_am_an_expert = True)
    s = set()
    for x in i:
        s.add(x.topic.id)
    return s

def user2like(user):
    i = Interest.objects.filter(user = user, i_like_the_topic = True)
    s = set()
    for x in i:
        s.add(x.topic.id)
    return s

def expert_search(request):
    result = []
    d = {}
    uu = User.objects.all()
    for u in uu:
        d[u] = user2expert(u)

    dd = {}
    su = d[request.user]
    if len(su) > 0:
        for u in uu:
            dd[u] = len(su.intersection(d[u]))/len(su)

        result = sorted(dd.items(), key=lambda item: (-item[1], item[0].username))
    return render(request, 'expert_search.html',
        {
         'result': result,
        })

def interest_search(request):
    result = []
    d = {}
    uu = User.objects.all()
    for u in uu:
        d[u] = user2like(u)

    dd = {}
    su = d[request.user]
    if len(su) > 0:
        for u in uu:
            dd[u] = len(su.intersection(d[u]))/len(su.union(d[u]))

        result = sorted(dd.items(), key=lambda item: (-item[1], item[0].username))
    return render(request, 'interest_search.html',
        {
         'result': result,
        })

def topic_search(request):
    result = None
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = NameForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            name = form.cleaned_data['name']
            result = MagicNode.objects.filter(desc__icontains=name)

    # if a GET (or any other method) we'll create a blank form
    else:
        form = NameForm()

    return render(request, 'topic_search.html',
        {'form': form,
         'result': result,
        })

def msg(request,msg):
    return render(request, 'msg.html', {'msg': msg})

def password_change_done(request):
    return msg(request, 'Your password was changed successfully!')

def password_reset_done(request):
    return msg(request, 'Your password was changed successfully!')

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            try:
                User.objects.get(email = email)
                return msg(request,'This email is in DB, probably you have been registered')
            except:
                form.save()
                username = form.cleaned_data.get('username')
                raw_password = form.cleaned_data.get('password1')
                user = authenticate(username=username, password=raw_password)
                login(request, user)
                return redirect('/')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

from django.contrib.contenttypes.models import ContentType

def upgrade(request):
    ct = ContentType.objects.get(app_label='sky',model='magicnode')
    return render(request, 'upgrade.html',
        {'log_entries': ct.logentry_set.all()[:25]}
        )

def index(request):
    last_visited = None
    if not request.user.is_anonymous:
        profile,c = Profile.objects.get_or_create(user=request.user)
        last_visited = profile.node_last_visited

    n = total()
    r = ready()
    nc = 0
    try:
        news = NewsRecord.objects.all()[:1].get()
        nc = NewsRecord.objects.all().count()
    except:
        news = None

    return render(request,'index.html',
        {'news':news,
        'more':(nc>1),
        'total':n,
        'ready':r,
        'last_visited':last_visited,
        })

def news(request):
    x_list = NewsRecord.objects.all()
    page = request.GET.get('page', 1)

    paginator = Paginator(x_list, 10)
    try:
        qs = paginator.page(page)
    except PageNotAnInteger:
        qs = paginator.page(1)
    except EmptyPage:
        qs = paginator.page(paginator.num_pages)

    return render(request,'news.html',
            {'qs':qs,
            })
