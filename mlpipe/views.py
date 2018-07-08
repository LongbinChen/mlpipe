from __future__ import unicode_literals
from django.core.files.storage import default_storage

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models.fields.files import FieldFile
from django.views.generic import FormView, UpdateView, ListView
from django.views.generic.base import TemplateView
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.template.defaulttags import register
from django.template.loader import render_to_string

from .forms import ContactForm, FilesForm, ContactFormSet
#from .models import Params
from settings import *
from os import listdir
from os.path import isfile, join, isdir, basename
import yaml
import json

class FakeField(object):
    storage = default_storage


fieldfile = FieldFile(None, FakeField, 'dummy.txt')


class HomePageView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        messages.info(self.request, 'hello http://example.com')
        return context


class DefaultFormsetView(FormView):
    template_name = 'formset.html'
    form_class = ContactFormSet


class DefaultFormView(FormView):
    template_name = 'form.html'
    form_class = ContactForm


class DefaultFormByFieldView(FormView):
    template_name = 'form_by_field.html'
    form_class = ContactForm


class FormHorizontalView(FormView):
    template_name = 'form_horizontal.html'
    form_class = ContactForm


class FormInlineView(FormView):
    template_name = 'form_inline.html'
    form_class = ContactForm


class FormWithFilesView(FormView):
    template_name = 'form_with_files.html'
    form_class = FilesForm

    def get_context_data(self, **kwargs):
        context = super(FormWithFilesView, self).get_context_data(**kwargs)
        context['layout'] = self.request.GET.get('layout', 'vertical')
        return context

    def get_initial(self):
        return {
            'file4': fieldfile,
        }


class PaginationView(TemplateView):
    template_name = 'pagination.html'

    def get_context_data(self, **kwargs):
        context = super(PaginationView, self).get_context_data(**kwargs)
        lines = []
        for i in range(200):
            lines.append('Line %s' % (i + 1))
        paginator = Paginator(lines, 10)
        page = self.request.GET.get('page')
        try:
            show_lines = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            show_lines = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            show_lines = paginator.page(paginator.num_pages)
        context['lines'] = show_lines
        return context


class MiscView(TemplateView):
    template_name = 'misc.html'

def getDataByDirectory(dir):
  result = {}
  result["id"] = dir
  result["text"] = basename(dir)
  result["type"] = "folder"
  children = []
  for f in listdir(join(resource_directory, dir)):
    if isfile(join(resource_directory, dir, f)) and f.endswith(".yaml"):
       print "file", f
       typedef = "data"
       if "pipe" in dir:
           typedef = "pipe"
       elif "module" in dir:
           typedef =  "module"
       children.append({'id':join(dir, f), 'text':f[:-5], 'type':typedef})
    if isdir(join(resource_directory, dir, f)):
       print "dir", f
       children.append(getDataByDirectory(join(dir, f)))
  result["children"] = children
  return result
  
  
def getmodule(request):
  print resource_directory
  print request.GET
  result = getDataByDirectory('')
  print result
  return JsonResponse(result['children'], safe=False)
'''
   print(request.
   try:
       r=['<ul class="jqueryFileTree" style="display: none;">']
       d=urllib.unquote(request.POST.get('dir',''))
       for f in os.listdir(d):
           ff=os.path.join(d,f)
           if os.path.isdir(ff):
               r.append('<li class="directory collapsed"><a href="#" rel="%s/">%s</a></li>' % (ff,f))
           else:
               e=os.path.splitext(f)[1][1:] # get .ext and remove dot
               r.append('<li class="file ext_%s"><a href="#" rel="%s">%s</a></li>' % (e,ff,f))
       r.append('</ul>')
   except Exception,e:
       r.append('Could not load directory: %s' % str(e))
   r.append('</ul>')
   return HttpResponse(''.join(r))
'''

def get_parameters(filename):
    filename = join(resource_directory, filename)

    if filename is None:
        return HttpResponse(status=400)
    with open(filename, 'r') as stream:
        try:
            y = yaml.load(stream)
            return y
            #return render(request, join(BASE_DIR, 'durian/templates/param_form.html'), y)
            #return JsonResponse(y, safe=False)
        except yaml.YAMLError as exc:
            print(exc)

def set_parameters(request):
    if request.method == 'POST':
        print (request)

def save_model(request):
    if request.method == 'POST':
        print (request)

def load_model(request):
    if request.method == 'POST':
        print (request)

def open_modal(request):
    print(request.method)
    if request.method == 'POST':
        req_dict = json.loads(request.body)
        filename = req_dict.get(u"filename")
        parameters = get_parameters(filename)
        node_id = req_dict.get(u"id")
        node_params = req_dict.get(u"params")
        #print(parameters)
        if "input" in parameters:
            if "input" not in node_params:
                node_params["input"] = {}
            for inp in parameters.get("input"):
                if inp not in node_params["input"]:
                    node_params["input"][inp] = {}
                    node_params["input"][inp]["current"] = ""
        if "output" in parameters:
            if "output" not in node_params:
                node_params["output"] = {}
            for outp in parameters.get("output"):
                if outp not in node_params["output"]:
                    node_params["output"][outp] = {}
                    node_params["output"][outp]["current"] = ""
        if "parameters" not in node_params:
            if "parameters" not in node_params:
                node_params["parameters"] = {}
            for param in parameters.get("parameters"):
                if param not in node_params["parameters"]:
                    node_params["parameters"][param] = {}
                    node_params["parameters"][param]["default"] = parameters["parameters"][param].get(u"default")
                    node_params["parameters"][param]["current"] = parameters["parameters"][param].get(u"default")
                    node_params["parameters"][param]["type"] = parameters["parameters"][param].get(u"type")
        print (node_id, node_params)
        return render(request, join(BASE_DIR, 'durian/templates/param_form.html'), {"node_id": node_id, "params": node_params})
