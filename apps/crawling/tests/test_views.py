from django.test import TestCase, Client
from rest_framework import status
from ..models import Url, Post



class BoardViewTest(TestCase):
    @classmethod
    def setUp(cls):        
        cls.url_arr = [
         "https://school.iamservice.net/organization/1674/group/2001892",
         "https://school.iamservice.net/organization/19710/group/2091428",
         "https://blog.naver.com/PostList.nhn?blogId=sntjdska123&from=postList&categoryNo=51",
         "https://blog.naver.com/PostList.nhn?blogId=hellopolicy&from=postList&categoryNo=168",
         "http://feeds.bbci.co.uk/news/rss.xml"
        ]

        cls.name_arr = [
            'iam_school_1',
            'iam_school_2',
            'blog_1',
            'blog_2',
            'bbc'
        ]

        for i in range(len(cls.url_arr)):
            Url.objects.create(url=cls.url_arr[i], name=cls.name_arr[i])        

    def test_sunae(self):
        api = "/api/crawl"
        target_url = "https://school.iamservice.net/organization/1674/group/2001892",
        data = {
            "url": target_url
        }
        response = Client().post(api, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("title", response.data[0])
        self.assertIn("published_datetime", response.data[0])
        self.assertIn("body", response.data[0])
        self.assertIn("attachment_list", response.data[0])
        
        self.assertEqual("2023학년도 교과서 목록", response.data[0]['title'])
        self.assertEqual('<p class="desc">2023학년도 교과서 목록입니다.</p>', response.data[0]['body'])
        self.assertEqual(["2023학년도 교과서목록.xls"], response.data[0]['attachment_list'])        
        self.assertEqual("https://school.iamservice.net/organization/1674/group/2001892", response.data[0]['url']['url'])

        self.assertEqual("2023학년도 서울여자대학교 정보보호영재교육원 교육생 모집", response.data[9]['title'])
        self.assertEqual('<p class="desc">서울여자대학교 정보보호영재교육원은 바른 윤리의식과 인성을 갖춘 미래의 화이트 해커 양성을 목표로 교육부에서 지정 및 설치한 영재교육기관으로, 2023학년도 서울, 경기, 인천, 강원 및 제주 지역 중고생을 대상으로 교육생을 모집하오니 관심있는 학생들은 지원 바랍니다.<br/><br/>가. 모집대상: 2023학년도 중·고등학교 1~3학년 진급 예정자(성별무관)<br/><br/>※ 2022학년도기준 초등학교 6학년~고등학교 2학년에 해당<br/><br/>나. 2023학년도 서울여자대학교 정보보호영재교육원 모집일정<br/><br/> <br/><br/><br/><br/>※ 위 일정은 영재원 향후 사정으로 변경될 수 있습니다</p>', response.data[9]['body'])
        self.assertEqual(["2023학년도 서울여자대학교 정보보호 영재교육원 모집요강.hwp",
                        "서울여자대학교 정보보호영재교육원 소개 자료.pdf"], response.data[9]['attachment_list'])        
        self.assertEqual("https://school.iamservice.net/organization/1674/group/2001892", response.data[9]['url']['url'])
        print("sunae test cases are passed!")

    def test_yongin(self):
        api = "/api/crawl"
        target_url = "https://school.iamservice.net/organization/19710/group/2091428",
        data = {
            "url": target_url
        }

        response = Client().post(api, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("title", response.data[0])
        self.assertIn("published_datetime", response.data[0])
        self.assertIn("body", response.data[0])
        self.assertIn("attachment_list", response.data[0])

        self.assertEqual("2022년 겨울철 교육시설물 안전점검 실시 결과",  response.data[0]['title'])        
        self.assertEqual("<p class=\"desc\">2022년 겨울철 학교시설물 안전점검 결과를 붙임과 같이 공개합니다.<br/><br/>붙임 2022년 겨울철 교육시설물 안전점검 실시 결과 1부.</p>", response.data[0]['body'])
        self.assertEqual(["교육시설 안전점검 실시 결과(2022 겨울철).pdf"],  response.data[0]['attachment_list'])
        self.assertEqual("https://school.iamservice.net/organization/19710/group/2091428", response.data[0]['url']['url'])

        self.assertEqual("2023학년도 방과후학교 외부강사 모집 2차 공고",  response.data[9]['title'])
        self.assertEqual('<p class="desc">방과후학교 개인위탁 외부강사 공모<br/><br/>용인초등학교에서는 2023학년도 방과후학교 운영과 관련하여 아래와 같이 방과후학교 프로그램 위탁강사를 모집하오니, 관심 있는 분들의 많은 지원 바랍니다.<br/><br/>     1.모집 분야 : 해당분야 각 1명 모집(5개 부서) ※첨부된 프로그램 참고<br/><br/><br/><br/>1. 모집 세부 사항<br/><br/><br/>(1) 공고 기간 : 2022년 11월 16일(수) ~ 2022년 11월 18일(금)<br/><br/>(2) 서류 접수 : 2022년 11월 17일(목) ~ 2022년 11월 21일(월) 16:00까지<br/><br/>(3) 접수 장소 : 용인초등학교 교무실</p>', response.data[9]['body'])
        self.assertEqual(["2023학년도 용인초 방과후 강사모집 공고문 2차.hwp",
                            "2023학년도 용인초 방과후 강사 제출서류최종.hwp",
                            "2023학년도 용인초 방과후 강사모집 시간표 예시안.hwp"],  response.data[9]['attachment_list'])
        self.assertEqual("https://school.iamservice.net/organization/19710/group/2091428", response.data[9]['url']['url'])
        print("yongin test cases are passed!")


    def test_seong_nam(self):
        api = "/api/crawl"
        target_url = "https://blog.naver.com/PostList.nhn?blogId=sntjdska123&from=postList&categoryNo=51",
        data = {
            "url": target_url
        }
        response = self.client.post(api, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("title", response.data[0])
        self.assertIn("published_datetime", response.data[0])
        self.assertIn("body", response.data[0])
        self.assertIn("attachment_list", response.data[0])

        self.assertEqual("시민 차량 무상점검 행사 등",  response.data[9]['title'])        
        self.assertEqual("https://blog.naver.com/PostList.nhn?blogId=sntjdska123&from=postList&categoryNo=51", response.data[9]['url']['url'])
        print("seong_nam test cases are passed!")

    def test_gov(self):
        api = "/api/crawl"
        target_url = "https://blog.naver.com/PostList.nhn?blogId=hellopolicy&from=postList&categoryNo=168",
        data = {
            "url": target_url
        }
        response = self.client.post(api, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("title", response.data[0])
        self.assertIn("published_datetime", response.data[0])
        self.assertIn("body", response.data[0])
        self.assertIn("attachment_list", response.data[0])

        self.assertEqual("[정책사용설명서] 2023년도부터 자립준비청년에 대한 지원을 강화합니다",  response.data[9]['title'])        
        self.assertEqual("https://blog.naver.com/PostList.nhn?blogId=hellopolicy&from=postList&categoryNo=168", response.data[9]['url']['url'])
        print("government test cases are passed!")


    def test_bbc(self):
        api = "/api/crawl"
        target_url = "http://feeds.bbci.co.uk/news/rss.xml",
        data = {
            "url": target_url
        }
        response = self.client.post(api, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("title", response.data[0])
        self.assertIn("published_datetime", response.data[0])
        self.assertIn("body", response.data[0])
        self.assertIn("attachment_list", response.data[0])

        self.assertEqual("http://feeds.bbci.co.uk/news/rss.xml", response.data[9]['url']['url'])
        print("bbc test cases are passed!")

    def tearDown(self):
        Post.objects.all().delete()
        Url.objects.all().delete()