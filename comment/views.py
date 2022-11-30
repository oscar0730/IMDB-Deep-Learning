from datetime import datetime
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import TemplateView
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage, InvalidPage
from .models import Comment
from trips.models import Post
from users.models import User
from .form import CommentForm
import requests, lxml
from bs4 import BeautifulSoup as bs
from .ml_model import predict, load_in_model

def caculate(pk):

    comment_list = Comment.objects.filter(movie=pk)
    good_comment_list = Comment.objects.filter(movie=pk, score="good")
    if (good_comment_list.count()/comment_list.count()) == 1:
        return 100
    return (good_comment_list.count()/comment_list.count())*100

def recommend(user_name, movie_list):
    user = User.objects.get(username = user_name)
    prefer_array = user.preference.replace("," , "")
    prefer_movie = []
    for i in prefer_array:
        #print(i)
        #print(type(i))
        for movie in movie_list:
            print(movie.movie_type)
            print(type(movie.movie_type))
            if str(movie.movie_type) == i:
                prefer_movie.append(movie)
                #print(movie.title)
    
    return prefer_movie

def rank(request):

    #rank_list = Post.objects.all().order_by("-movie_score")
    rank_num = []
    if request.method == "GET":
        print("rank1111111")
        
        rank_list = Post.objects.all().order_by("-movie_score")
        for i in range(len(rank_list)):
            rank_num.append(i+1)

        x = zip(rank_list, rank_num)

        return render(request, 'rank.html',  {'rank_list': x})

def home(request):
    post_list = Post.objects.all()
    comment_count = []
    view_text = "View All"

    for i in range(len(post_list)):
        comment_list = Comment.objects.filter(movie= i+1)
        if comment_list:           
            Post.objects.filter(pk = i+1).update(movie_score = caculate(i+1))
        
    rank_list = Post.objects.all().order_by("-movie_score")

    prefer_movie = []
    preference = ""
    if request.method == "POST":
        user_name = request.POST["user_name"]
        preference = request.POST["preference"]
        print(user_name)
        print(preference)
        User.objects.filter(username = user_name).update(preference = preference)
        
        post_list = recommend(user_name, rank_list)
        view_text = "You Might Like"
        

    for i in range(len(post_list)):
        #post_list[i]
        #print(post_list[i].title)
        #print(post_list[i].pk)
        num = Comment.objects.filter(movie = post_list[i].pk).count()
        print(num,i)
        comment_count.append(num)

    #x = zip(prefer_movie, comment_count)
    x = zip(post_list, comment_count)
    
    
    #load_in_model()

    return render(request, 'home.html', {'post_list':post_list, 'rank_list':rank_list, 'comment_num':comment_count, 'list':x,
                                         'prefer_movie':prefer_movie, 'view_text':view_text, 'preference':preference})

def post_detail(request, pk):
    post = Post.objects.get(pk = pk)
    comment_list = Comment.objects.filter(movie=pk)

    comment_list_page = paginator_view(comment_list, request)

    #print(comment_list.count())
    if comment_list:
        print(caculate(pk))
        Post.objects.filter(pk = pk).update(movie_score = caculate(pk))
  
    
    return render(request, 'post.html', {'post': post, 'comment_list':comment_list_page['comments'], 'page_range':comment_list_page['page_range'], 'last_page':comment_list_page['last_page'],})

def output_page(request):
    return render(request, 'hello_world.html', {
        'current_time': str(datetime.now()),
    })

def get_name(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = TextForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect('/thanks/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = TextForm()

    return render(request, 'home.html', {'form': form})


def test_post(request):
    ctx ={}
    if request.POST:
        print(request.POST)
        text = request.POST.get('comment_text', "")
        name = request.POST.get('movie_name', "")
        print(text,name)
    return render(request, "post.html", ctx)

def add_comment(request):
    print("this is test")
    print(request.POST)
    
    #post = Post.objects.get(pk = pk)
    ctx ={}
    if request.method == "POST":

        form = CommentForm(request.POST)
        if form.is_valid():
            comment_text = request.POST["comment_text"]
            comment_movie = request.POST["movie_name"]

            predict(comment_text)
            
            if predict(comment_text):
                comment_score = "good"
            else:
                comment_score = "bad"
            #comment_score = "bad"

            pk = request.POST["pk"]
            post = Post.objects.get(pk = pk)
            comment_list = Comment.objects.filter(movie=pk)

            #comment_list = paginator_view(comment_list, request)

            #print(comment_text)
            post = Post.objects.get(title = comment_movie)
            #print(post)
            comment = Comment(comment_text = comment_text, score = comment_score, movie = post, comment_time = str(datetime.now()))
            comment.save()

            
            return render(request, 'new_comment.html',  {'post': post, 'comment':comment_text, 'score':comment_score})
            #return HttpResponseRedirect(reverse('comment:post'))
    else:
        form = CommentForm()

    return render(request, 'new_comment.html', ctx)

class ComentView(TemplateView):
    template_name ='post.html'

    def get(self, request):
        form = CommentForm()
        return render( request, self.template_name, {'form':form})

    def post(self, request):
        form = CommentForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            text = form.cleaned_data['post']
            form = TextForm()
            return redirect('home:home')

        args = {'form':form, 'text': text}
        return render(request, self.template_name, args)


def link_web(request):

    ctx ={}
    if request.method == "GET":

        form = CommentForm(request.POST)
        

        pk = request.GET["pk"]
        post = Post.objects.get(pk = pk)
        comment_list = Comment.objects.filter(movie=pk)
        #comment_list_page = paginator_view(comment_list, request)
            
        #post = Post.objects.get(title = comment_movie)

        imdb_list = crawler(post.location)
        i=0
        for i in range(len(imdb_list)):
            
            if predict(imdb_list[i]):
                comment_score = "good"
            else:
                comment_score = "bad"

            if default_input_comment(imdb_list[i],comment_list) == 0:
                continue
            comment = Comment(comment_text = imdb_list[i], score = comment_score, movie = post, comment_time = str(datetime.now()))
            comment.save()

        return render(request, 'link_comment.html',  {'post': post,})

    else:
        form = CommentForm()

    return render(request, 'link_comment.html', ctx)

def crawler(url_number):

    comment_list = []

    url = "https://www.imdb.com/title/"+url_number+"/reviews?ref_=tt_urv"
    my_page = requests.get(url)
    #print(my_page)
    #print(url)
    my_html = bs(my_page.text)
    #print(my_html.prettify())
    #temp = my_html.find("div","text show-more__control")
    #print(temp)
    #tags = temp.find("div")
    #print(tags.text)

    art = my_html.find_all("div","text show-more__control")
    i=0
    for p in art:
        print(p.text+"\n")
        comment_list.append(p.text)
        i += 1
        if i == 5:
            break

    return comment_list
        

def default_input_comment(text, comment_list):
    for i in range(len(comment_list)):
        if text == comment_list[i]:
            return 0
        return 1
    
def paginator_view(comment_list, request):

    paginator = Paginator(comment_list, 5)
    last_page = paginator.num_pages
    #print(last_page)
    if request.method == "GET":
        # 获取 url 后面的 page 参数的值, 首页不显示 page 参数, 默认值是 1
        
        #page = request.GET.get('page')
        if request.GET.get('page') is None:
            page = 1
        else:
            page = int(request.GET.get('page'))

        try:
            comments = paginator.page(page)

            if paginator.num_pages > 7:
                
                if page - 3 < 1:
                    page_range = range(1, 8)

                elif page + 3 > paginator.num_pages:
                    page_range = range(paginator.num_pages - 6, paginator.num_pages + 1)

                else:
                    page_range = range(page - 3, page + 4)
            else:
                page_range = paginator.page_range

            # todo: 注意捕获异常

        except PageNotAnInteger:
            # 如果请求的页数不是整数, 返回第一页。
            comments = paginator.page(1)
        except InvalidPage:
            # 如果请求的页数不存在, 重定向页面
            return HttpResponse('找不到页面的内容')
        except EmptyPage:
            # 如果请求的页数不在合法的页数范围内，返回结果的最后一页。
            comments = paginator.page(paginator.num_pages)

    comment_list_page = {'comments':comments, 'page_range':page_range, 'last_page':last_page}

    return comment_list_page

