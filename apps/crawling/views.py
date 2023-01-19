import logging
from datetime import datetime
from bs4 import BeautifulSoup as BP

from django.db import transaction
from rest_framework import permissions, status, exceptions
from rest_framework.response import Response
from rest_framework.views import APIView

from drf_yasg.utils import swagger_auto_schema
from apps.crawling.utils.resource import driver

from .models import Post, Url, UrlTarget, FuncTarget
from .serializers import PostSerialzer, UrlSerializer
from .utils.errors import UrlNotFound, UrlNotFoundError, FuncNotFound, FuncNotFoundError

class board(APIView):
    """
    게시물

    ---
    """
    permission_classes = [permissions.AllowAny]
    serializer_class = None

    def __init__(self, *args, **kwargs):
        self.driver = driver
        return super().__init__(*args, **kwargs)

    def create_url_match_table(self):
        url_match_table = {}
        url_match_check = {}
        url_target = UrlTarget()
        url_target_attrs = [
            attr
            for attr in dir(UrlTarget)
            if not callable(getattr(UrlTarget, attr)) and not attr.startswith("__")
        ]
        for attr in url_target_attrs:
            if attr == 'IAMSCHOOL_1':
                url_match_table[attr] = 'IAMSCHOOL_1'                
            elif attr == 'IAMSCHOOL_2':
                url_match_table[attr] = 'IAMSCHOOL_2'
            elif attr == 'BLOG_1':
                url_match_table[attr] = 'BLOG_1'
            elif attr == 'BLOG_2':
                url_match_table[attr] = 'BLOG_2'
            elif attr == 'BBC':
                url_match_table[attr] = 'BBC'
            else:
                raise exceptions.ValidationError('Suggested URL is not available in this program.')
            url_match_check[attr] = url_target[attr]                
        return url_match_table, url_match_check

    def match_to_url(self, url_match_table, url): 
        if url == url_match_table[url]:
            return True
        return False
    
    def url_handler(self, url):
        url = None
        url_match_table, url_match_check = self.create_url_match_table()
        bool = self.match_to_url(url_match_table, url)
        if bool:
            try:
                url = Url.objects.get(url=url)
                logging.info('등록된 URL입니다')
            except Url.DoesNotExist:
                url = Url.objects.create(url=url)
                logging.info('URL이 등록되었습니다')
        else:
            raise UrlNotFound
        return url_match_check
    
    def match_to_func(self, url):
        target_func = None
        url_match_check = self.url_handler(url)
        var_func = url_match_check[url]
        func_target = FuncTarget()
        try:
            target_func = func_target[var_func]
        except:
            raise FuncNotFound
        return target_func

    def func_exec(self, func):
        if func == 'iam_school_1':
            self.iam_school_1()
        elif func == 'iam_school_2':
            pass
        elif func == 'blog_1':
            pass
        elif func == 'blog_2':
            pass
        elif func == 'bbc':
            pass
        else:
            raise FuncNotFound

    @transaction.atomic
    def iam_school_1(self, url):
        self.driver.get(url)

        published_date_arr = []
        attachment_list = []
        attach_list_cnt = 0

        req = driver.page_source
        soup = BP(req, 'html.parser')

        titles = soup.find_all('h4', {'class' : 'tit_cont'}, limit=10)
        bodies = soup.find_all('p', {'class': 'desc'}, limit=10)
        published_datetime = soup.find_all('p', {'class': 'txt_date'}, limit=10)
        files = soup.find_all('div', {'class': 'bx_btn'}, limit=12)        

        for p_d in published_datetime:            
            pd = p_d.select_one("p.txt_date > span:nth-of-type(2)")            
            published_date_arr.append(pd)        
        
        for file in files:
            ff = file.find_all('span', {'class': 'name'})                        
            if not(ff == '[]' or ff == []) and attach_list_cnt < 11:
                attachment_list.append(ff)
                attach_list_cnt += 1        

        num = len(titles)        
        for i in range(num):
            temp = []
            for attach in attachment_list[i]:
                temp.append(attach.text)
            
            title=titles[i].text
            body= bodies[i]
            p_d= published_date_arr[i].text
            a_l=temp
            url=url            
            pd = datetime.strptime(p_d, "%Y.%m.%d")                        
            Post.objects.update_or_create(title=title, published_datetime=pd, body=body, attachment_list=a_l, url=url)

    @swagger_auto_schema(        
        operation_summary="게시물 조회",
        request_body=UrlSerializer,
        responses={
            status.HTTP_200_OK: None,
            status.HTTP_200_OK: PostSerialzer,
            f"{UrlNotFoundError.STATUS_CODE}({UrlNotFoundError.SYSTEM_CODE})": UrlNotFoundError().response(),
            f"{FuncNotFoundError.STATUS_CODE}({FuncNotFoundError.SYSTEM_CODE})": FuncNotFoundError().response(),
        },
        security=[]
    )
    @transaction.atomic    
    def post(self, request, *args, **kwargs):        
        serializer = UrlSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        url = serializer.validated_data['url']

        self.func_exec(url)        
        queryset = Post.objects.all().limit(10)
                    
        return Response(data={'data':'data'}, status=status.HTTP_200_OK)