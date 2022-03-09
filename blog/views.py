from django.shortcuts import render,get_object_or_404
from comment.forms import CommentForm
from markdown.extensions.toc import TocExtension
from django.utils.text import slugify
from .models import Tag,Category
from django.utils.html import strip_tags
# Create your views here.
from  django.http import HttpResponse
# def index(request):
#     # return HttpResponse("欢迎访问我的博客首页")
#       return render(request,'blog/index.html',context={
#           'title':'我的博客首页',
#           'welcome':'我的博客首页'
#       })
from .models import Post,Category
import markdown
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def index(request):
    post_list=Post.objects.all().order_by('-created_time')
    paginator = Paginator(post_list, 6)
    page = request.GET.get('page')
    try:
        post_list = paginator.page(page)
    except PageNotAnInteger:
        post_list = paginator.page(1)
    except EmptyPage:
        post_list = paginator.page(paginator.num_pages)
    ms=markdown.Markdown(extensions=['markdown.extensions.extra','markdown.extensions.codehilite',])
    for post in post_list:
       post.excerpt=strip_tags(ms.convert(post.body))[:64]+'......'
    return render(request,'blog/index.html',context={'post_list':post_list})

def detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.increase_views()
    md = markdown.Markdown(extensions=['markdown.extensions.extra',
                                       'markdown.extensions.codehilite',
                                        TocExtension(slugify=slugify),])
    post.body=md.convert(post.body)
    form=CommentForm()
    comment_list=post.comment_set.all()
    context={'post':post,'form':form,'comment_list':comment_list,'toc':md.toc}
    return render(request, 'blog/detail.html', context=context)

def archives(request,year,month):
    post_list=Post.objects.filter(created_time__year=year,
                                  created_time__month=month
                                  ).order_by('-created_time')
    return render(request,'blog/index.html',context={'post_list':post_list})
def category(request,pk):
    cate=get_object_or_404(Category,pk=pk)
    post_list=Post.objects.filter(category=cate).order_by('-created_time')
    return render(request,'blog/index.html',context={'post_list':post_list})

def tag(request,pk):
    tag_name=get_object_or_404(Tag,pk=pk)
    post_list = Post.objects.filter(tags=tag_name).order_by('-created_time')
    return render(request, 'blog/index.html', context={'post_list': post_list})

def search(request):
    q=request.GET.get('q')
    post_list=Post.objects.filter(title__icontains=q)
    error_message=''
    if not post_list:
        error_message='请重新输入搜索内容'
        return render(request, 'blog/index.html', {'error_message': error_message, 'post_list': post_list})
    return render(request,'blog/index.html',{'error_message':error_message,'post_list':post_list})

def blog_list(request):
    post_list=Post.objects.all().order_by('-created_time')
    paginator = Paginator(post_list, 15)
    page = request.GET.get('page')
    try:
        post_list = paginator.page(page)
    except PageNotAnInteger:
        post_list = paginator.page(1)
    except EmptyPage:
        post_list = paginator.page(paginator.num_pages)

    for post in post_list:
        post.excerpt = post.body[:64]
    return render(request,'blog/blog_list.html',context={'post_list':post_list})

def about(request):
    return render(request,'blog/about.html')
def pray(request):
    return render(request,'blog/pray.html')

from django import forms
from django.forms import widgets
from django.core import validators
from .cha_spider import Cha

class chaForm(forms.Form):
    url=forms.CharField(required=True,error_messages={'required': '请输入必须的想法id或链接', 'invalid': '格式错误'})
    type = forms.CharField(required=True, error_messages={'required': '请输入种类', 'invalid': '格式错误'})
    price= forms.IntegerField(required=True,max_value=30,min_value=1,error_messages={'required': '请输入数量', 'invalid': '格式错误'})



def cha(request):
    return render(request,'blog/cha.html')


def get_cha(request):
    if request.method=='POST':
        form_c=chaForm(request.POST)
        if form_c.is_valid():
            try:
                url_or_number=form_c.cleaned_data.get('url')
                type=form_c.cleaned_data.get('type')
                price_number = form_c.cleaned_data.get('price')
              
                little_girl=Cha(url_or_number,type,price_number)
                result=little_girl.get_choice()
                pin_url='https://www.zhihu.com/pin/'+url_or_number if url_or_number.isdigit() else url_or_number

                end_tmp={'result':result,'price_number':price_number,'pin_url':pin_url,'pin_gender':type}
                return render(request,'blog/cha_list.html',end_tmp)
            except Exception as e:
                return  render(request,'blog/cha.html',{'errorss':'你填写的网址信息无法正常识别'+str(e)})
        else:
            return render(request,'blog/cha.html',{'form':form_c})
    else:
        return render(request,'blog/cha.html')

