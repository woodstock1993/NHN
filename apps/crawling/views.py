import logging
from datetime import datetime
from bs4 import BeautifulSoup as BP

from django.db import transaction
from rest_framework import permissions, status, exceptions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import mixins, generics

from drf_yasg.utils import swagger_auto_schema
from apps.crawling.utils.resource import driver

from .models import Post, Url, UrlTarget, FuncTarget
from .serializers import PostSerialzer, OriginUrlSerializer, UrlSerializer
from .utils.errors import (
    UrlNotFound, UrlNotFoundError, 
    FuncNotFound, FuncNotFoundError,    
)

class Board(APIView):
    """
    입력 URL 크롤링 후 데이터 생성 및 데이터 조회

    ---
    """
    permission_classes = [permissions.AllowAny]
    serializer_class = None

    def __init__(self, *args, **kwargs):
        self.driver = driver
        return super().__init__(*args, **kwargs)

    def url_exists(self, url):
        try:
            url = Url.objects.get(url=url)
            logging.info('등록된 URL입니다')
        except Url.DoesNotExist:            
            raise UrlNotFound
        return url
    
    def url_match_to_func(self, url):        
        url_obj = self.url_exists(url)
        return url_obj.name
        
    @transaction.atomic
    def iam_school(self, url):
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
            body= str(bodies[i])            
            p_d= published_date_arr[i].text
            a_l=temp
            url_obj=Url.objects.get(url=url)          
            pd = datetime.strptime(p_d, "%Y.%m.%d")                        
            Post.objects.update_or_create(title=title, published_datetime=pd, body=body, attachment_list=a_l, url=url_obj)
        logging.info("Elementary Crawling Succeed")

    @transaction.atomic
    def blog(self, url):
        self.driver.get(url)

        req = driver.page_source
        soup = BP(req, 'html.parser')

        titles = soup.find_all('strong', {'class':'ell'}, limit=10)
        published_datetime = soup.find_all('span', {'class':'date'}, limit=10)

        url_obj = Url.objects.get(url=url)

        for i in range(len(titles)):
            title = titles[i].text
            p_d = published_datetime[i].text.replace(" ", "").rstrip('.')
            pd = datetime.strptime(p_d, "%Y.%m.%d")
            Post.objects.update_or_create(title=title, published_datetime=pd, url=url_obj)

        logging.info('Blog Crawling Succeed')

    @transaction.atomic
    def bbc(self, url):        
        self.driver.get(url)

        req = driver.page_source
        soup = BP(req, 'html.parser')

        titles = soup.find_all('a', {'class':'item'}, limit=10)
        bodies = soup.find_all('div', {'id':'item'}, limit=10)

        url_obj = Url.objects.get(url=url)
        
        for i in range(len(bodies)):
            body = str(bodies[i].select_one("div"))
            title = titles[i].text
            Post.objects.update_or_create(title=title, body=body, url=url_obj)

        logging.info("BBC Crawling Succeed")        


    def func_exec(self, url):
        check = False
        func_name = self.url_match_to_func(url)        
        if func_name==FuncTarget.IAMSCHOOL_1.value or func_name==FuncTarget.IAMSCHOOL_2.value:
            self.iam_school(url)
            check = True
        elif func_name==FuncTarget.BLOG_1.value or func_name==FuncTarget.BLOG_2.value:
            self.blog(url)
            check = True
        elif func_name==FuncTarget.BBC.value:
            self.bbc(url)
            check = True
        if check is True:
            return
        raise FuncNotFound
    
    @swagger_auto_schema(
        operation_summary="크롤링",
        operation_description="크롤링 한 모든 결과 값 조회",
        responses={status.HTTP_200_OK: PostSerialzer}
    )    
    def get(self, request, *args, **kwargs):
        queryset = Post.objects.all()
        res = PostSerialzer(queryset, many=True)
        return Response(res.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(        
        operation_summary="크롤링",
        operation_description="""
        ## <font size=5> 크롤링 후 해당 결과값이 DB에 없을 시 새로운 데이터 생성 </font>
        ### <font size=4> URL 목록 </font>
         - ### 수내초등학교: https://school.iamservice.net/organization/1674/group/2001892
         - ### 용인초등학교: https://school.iamservice.net/organization/19710/group/2091428
         - ### 성남시: https://blog.naver.com/PostList.nhn?blogId=sntjdska123&from=postList&categoryNo=51
         - ### 정부: https://blog.naver.com/PostList.nhn?blogId=hellopolicy&from=postList&categoryNo=168
         - ### bbc: http://feeds.bbci.co.uk/news/rss.xml
        ---        
        """,
        request_body=UrlSerializer,
        responses={
            status.HTTP_200_OK: None,
            status.HTTP_201_CREATED: PostSerialzer,
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
        url_obj = Url.objects.get(url=url)
        queryset = Post.objects.filter(url=url_obj)[:10]
        res = PostSerialzer(queryset, many=True)
        return Response(data=res.data, status=status.HTTP_201_CREATED)


class UrlCreateDeleteAPIView(APIView):
    """
    크롤링 대상 URL 등록 및 삭제

    ---
    """    

    @swagger_auto_schema(
        operation_summary="과제에서 주어진 URL",
        operation_description="""
            과제에서 주어진 URL 생성
            """,
        responses={
            status.HTTP_200_OK: None,
            status.HTTP_201_CREATED : OriginUrlSerializer,
        }
    )
    def post(self, request, *args, **kwargs):
        url_arr = []
        
        for key, value in UrlTarget.__members__.items():
            url_arr.append({key: value})
        
        for dic in url_arr:
            for k, v in dic.items():
                Url.objects.update_or_create(name=k, url=v)            
        queryset = Url.objects.all()
        res = OriginUrlSerializer(queryset, many=True)
        return Response(res.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
    operation_summary="과제에서 주어진 URL",
    operation_description="""
        과제에서 주어진 URL 모두 삭제
        """,        
    )
    def delete(self, request, *args, **kwargs):
        Url.objects.all().delete()
        return Response({"All Url Objects are deleted"}, status=status.HTTP_200_OK)


class SunaeGetAPIView(APIView):
    @swagger_auto_schema(
    operation_summary="수내초등학교",
    operation_description="""
        수내초등학교 크로링 결과 데이터 조회
        """,        
    )
    def get(self, request, *args, **kwargs):
        num = kwargs.get('num')
        queryset = Post.objects.filter(url=UrlTarget.iam_school_1.value)[:num]
        res = PostSerialzer(queryset, many=True)
        return Response(res.data, status=status.HTTP_200_OK)


class YonginGetAPIView(APIView):
    @swagger_auto_schema(
    operation_summary="용인초등학교",
    operation_description="""
        용인초등학교 크로링 결과 데이터 조회
        """,
        responses={status.HTTP_201_CREATED : PostSerialzer,}
    )
    def get(self, request, *args, **kwargs):
        num = kwargs.get('num')
        queryset = Post.objects.filter(url=UrlTarget.iam_school_2.value)[:num]
        res = PostSerialzer(queryset, many=True)
        return Response(res.data, status=status.HTTP_200_OK)


class SeongNamGetAPIView(APIView):
    @swagger_auto_schema(
    operation_summary="성남시",
    operation_description="""
        성남시 크로링 결과 데이터 조회
        """,
        responses={status.HTTP_201_CREATED : PostSerialzer,}
    )
    def get(self, request, *args, **kwargs):
        num = kwargs.get('num')
        queryset = Post.objects.filter(url=UrlTarget.blog_1.value)[:num]
        res = PostSerialzer(queryset, many=True)
        return Response(res.data, status=status.HTTP_200_OK)


class GovernmentGetAPIView(APIView):
    @swagger_auto_schema(
    operation_summary="정부",
    operation_description="""
        정부 크로링 결과 데이터 조회
        """,
        responses={status.HTTP_201_CREATED : PostSerialzer,}
    )
    def get(self, request, *args, **kwargs):
        num = kwargs.get('num')
        queryset = Post.objects.filter(url=UrlTarget.blog_2.value)[:num]
        res = PostSerialzer(queryset, many=True)
        return Response(res.data, status=status.HTTP_200_OK)


class BBCGetAPIView(APIView):
    @swagger_auto_schema(
    operation_summary="BBC",
    operation_description="""
        BBC 크로링 결과 데이터 조회
        """,
        responses={status.HTTP_201_CREATED : PostSerialzer,}
    )
    def get(self, request, *args, **kwargs):
        num = kwargs.get('num')
        queryset = Post.objects.filter(url=UrlTarget.bbc.value)[:num]
        res = PostSerialzer(queryset, many=True)
        return Response(res.data, status=status.HTTP_200_OK)