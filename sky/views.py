from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from .forms import SignUpForm
from .models import NewsRecord, MagicNode, Interest
from area.models import Subscription
from django.contrib.auth.models import User

from collections import Counter
from operator import itemgetter
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .forms import NameForm
from django.http import JsonResponse
# Create your views here.
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
    node = MagicNode.objects.get(id=node_id)

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
        friends = list(node.friends.all())
        if node.pre_nodes:
            pre_nodes = [list(get_by_name(x))[0] for x in node.pre_nodes]


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

    sub = Subscription.objects.filter(user = request.user)
    sub_in = [s.area for s in sub]

    return render(request,'topic_tree.html',
                    {'node':node,
                     'children':children,
                     'parent':parent,
                     'siblings':siblings,
                     'friends':friends,
                     'pre_nodes':pre_nodes,
                     't1':p1,
                     't2':p2,
                     't3':p3,
                     'sub':sub_in,
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

def index(request):
    nc = 0
    try:
        news = NewsRecord.objects.all()[:1].get()
        nc = NewsRecord.objects.all().count()
    except:
        news = None

    return render(request,'index.html',
        {'news':news,
        'more':(nc>1),
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
