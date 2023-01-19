from datetime import datetime
from bs4 import BeautifulSoup as BP

from django.db import transaction
from rest_framework import permissions, status, exceptions
from rest_framework.response import Response
from rest_framework.views import APIView

from drf_yasg.utils import swagger_auto_schema
from apps.crawling.utils.resource import driver

from .models import Post, Url
from .serializers import UrlTarget, PostSerialzer, UrlSerializer

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
        url_target = UrlTarget()
        url_target_attrs = [
            attr
            for attr in dir(UrlTarget)
            if not callable(getattr(UrlTarget, attr)) and not attr.startswith("__")
        ]

        for attr in url_target_attrs:
            if attr == 'iamSCHOOL_1':
                url_match_table[attr] = url_target['iamSCHOOL_1']
            elif attr == 'iamSCHOOL_2':
                url_match_table[attr] = url_target['iamSCHOOL_2']
            elif attr == 'BLOG_1':
                url_match_table[attr] = url_target['BLOG_1']
            elif attr == 'BLOG_2':
                url_match_table[attr] = url_target['BLOG_2']
            elif attr == 'BBC':
                url_match_table[attr] = url_target['BBC']
            else:
                raise exceptions.ValidationError('Suggested URL is not available in this program.')
        return url_match_table

    def match_to_url(self, url_match_table, url):
        if url == url_match_table[url]:
            return True
        return False
    
    
    @transaction.atomic
    def iam_school_1(self):
        self.driver.get(self.url_1)

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

        url = Url.objects.create(url=self.url_1)

        num = len(titles)
        
        for i in range(num):
            temp = []
            for attach in attachment_list[i]:
                temp.append(attach.text)
            
            title=titles[i].text
            body= str(bodies[i])
            p_d= published_date_arr[i].text
            a_l=temp
            url=url            
            pd = datetime.strptime(p_d, "%Y.%m.%d")                  
                        
            Post.objects.update_or_create(title=title, published_datetime=pd, body=body, attachment_list=a_l, url=url)

    @swagger_auto_schema(        
        operation_summary="게시물 조회",
        request_body=UrlSerializer,
        responses={status.HTTP_200_OK: PostSerialzer},
        security=[]
    )
    @transaction.atomic    
    def post(self, request, *args, **kwargs):        
        serializer = UrlSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        url = serializer.validated_data['url']

        self.iam_school_1()
        queryset = Post.objects.all().limit(10)
            
        return Response(data={'data':'data'}, status=status.HTTP_200_OK)