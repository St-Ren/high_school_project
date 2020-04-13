# -*- coding: UTF-8 -*-

from django.shortcuts import render
from django.shortcuts import HttpResponse
from paragraph.models import Article
from django import forms
from django.http import HttpResponseRedirect
from .background import background_all_web as background
#from .background import vb
#from .background import background_web as d
def create(request):
    
    '''from background import background'''
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            new_article = form.save()
            s=form.cleaned_data['content']
            s=s.replace('\n',' ')
            ans,v,l,dl=background.judge(s)
            #ans,v,l=vb.judge(s)
            #a,dl=d.judge(s)
            l=l[0]
            #return render(request, 'answer.html',{'ans':str(ans+1),'sent_list':dl})
            #return render(request, 'answer.html', {'ans': str(ans+1),'lenth': str(l),'vex_list': str(v)})
            return render(request, 'answer.html', {'ans': str(ans+1),'lenth': str(l),'vex_list': str(v),'sent_list':dl})

    form = ArticleForm()
    return render(request, 'create_article.html', {'form': form})

def detail(request, pk):
    article = Article.objects.get(pk=int(pk))
    return render(request, "detail.html", {'article': article})
    
def home(request):
    s = "Hello '/create' to begin~"
    return HttpResponse(s)


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['content' ]
