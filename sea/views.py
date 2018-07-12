from django.shortcuts import render
from .models import Boat
from .forms import AddBoatForm
from sky.models import MagicNode
from sky.views import msg

def delete(request,id):
    boat = Boat.objects.get(id=id)
    boat.delete()
    return msg(request,'deleted')

def edit(request,id):
    boat = Boat.objects.get(id=id)
    if request.method == 'POST':
        form = AddBoatForm(request.POST)
        if form.is_valid():
            boat.link = form.cleaned_data['link']
            boat.desc = form.cleaned_data['desc']
            boat.name = form.cleaned_data['name']
            boat.n_sib = form.cleaned_data['n_sib']
            boat.save()
            return msg(request,'add request done')
        else:
            return msg(request,'add request failed')
    # if a GET (or any other method) we'll create a blank form
    else:
        form = AddBoatForm(
                initial={
                'link':boat.link,
                'name':boat.name,
                'desc':boat.desc,
                'n_sib':boat.n_sib,
                }
                )

        return render(request, 'sea/add.html',
            {'form': form,
            })

def more(request,id):
    node = MagicNode.objects.get(pk = id)
    qs = Boat.objects.filter(node_id=id).order_by('n_sib')
    return render(request,'sea/more.html',
        {'boats':qs, 'node':node}
        )

def add(request,id):
    node = MagicNode.objects.get(id=id)
    if request.method == 'POST':
        form = AddBoatForm(request.POST)
        if form.is_valid():
            boat = Boat(node=node)
            boat.link = form.cleaned_data['link']
            boat.desc = form.cleaned_data['desc']
            boat.name = form.cleaned_data['name']
            boat.n_sib = form.cleaned_data['n_sib']
            boat.save()
            return msg(request,'add request done')
        else:
            return msg(request,'add request failed')
    # if a GET (or any other method) we'll create a blank form
    else:
        form = AddBoatForm(
                )

        return render(request, 'sea/add.html',
            {'form': form,'node':node
            })
