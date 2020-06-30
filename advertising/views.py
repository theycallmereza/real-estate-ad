from django.shortcuts import render, HttpResponseRedirect
from django.views.generic import ListView, DetailView
from django.forms import modelformset_factory
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from .models import Image, Property, Category, Advertising, PropAd
from .forms import NewAdForm, ImageForm, AddPropsForm


# Create your views here.
class HomepageView(ListView):
    queryset = Advertising.objects.all()
    context_object_name = 'advertisements'
    template_name = 'index.html'


class AdDetailView(DetailView):
    model = Advertising
    template_name = 'advertising/detail.html'
    context_object_name = 'ad'

@login_required
def create_ad(request):
    image_formset = modelformset_factory(Image, form=ImageForm, extra=5)
    categories = Category.objects.all()

    if request.method == 'POST':
        form = NewAdForm(request.POST)
        formset = image_formset(request.POST, request.FILES, queryset=Image.objects.none())

        if form.is_valid() and formset.is_valid():
            ad_form = form.save(commit=False)
            ad_form.user = request.user
            category_id = form.cleaned_data['category'].id
            ad_form.save()
            ad_id = ad_form.id

            for form in formset.cleaned_data:
                if form:
                    image = form['image']
                    photo = Image(advertisement=ad_form, image=image)
                    photo.save()

            return HttpResponseRedirect(reverse('add-props', args=(category_id, ad_id)))
    else:
        form = NewAdForm()
        formset = image_formset(queryset=Image.objects.none())

    return render(request, 'advertising/new_ad.html', {'form': form, 'formset': formset, 'categories': categories})

@login_required
def add_props_to_advertisement(request, category_id, ad_id):
    cat = Category.objects.get(id=category_id)
    props = cat.properties.all()
    props_list = []
    if cat.parent:
        catparent = Category.objects.get(id=cat.parent.id)
        props2 = catparent.properties.all()
        for p in props2:
            props_list.append(p.title)
    for p in props:
        props_list.append(p.title)
    if request.method == 'POST':
        form = AddPropsForm(request.POST, extra=props_list)
        if form.is_valid():
            for (title, value) in form.get_values():
                prop = Property.objects.get(title=title)
                ad = Advertising.objects.get(id=ad_id)
                ad.property.add(prop)
                PropAd.objects.create(property=prop, advertisement=ad, value=value)
        return HttpResponseRedirect('/')
    else:
        form = AddPropsForm(extra=props_list)
    return render(request, 'advertising/add_props.html', {'form': form})
