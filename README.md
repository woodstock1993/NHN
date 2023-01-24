# NHN

<div align="center"><img src="https://image.rocketpunch.com/company/518/imcompany_logo_1531806392.png?s=400x400&t=inside"/></div>

## Chrome Version
```
$ chrome://settings/help -> 로컬 머신에 깔려 있는 크롬 버전 확인
```

## Chrome Driver
```
https://chromedriver.chromium.org/downloads -> 로컬 머신의 크롬 버전과 OS에 맞는 크롬 드라이버 다운로드

NHN/chromedriver -> 크롬 드라이버 다운 시 설치 경로

pip install -r requirements.txt 설치 전 윗 단계 반드시 선행 -> 크롬드라이버 미설치 후 진행 시 에러 발생
```

# 목차

- [Install](#Install)
- [Test](#Test)
- [API 명세](#api-명세)


## Install
#### MAC OS
```
$ git clone https://github.com/woodstock1993/NHN.git
$ python -m venv venv
$ source venv/bin/activate
$ pip install --upgrade pip
$ python install -r requirements.txt
$ python manage.py runserver
```

## Test
```
$ python manage.py test apps.crawling
```

<img width="514" alt="image" src="https://user-images.githubusercontent.com/67543838/214263249-8c73bbe3-c65e-431d-8462-6956d11fd0f2.png">

## API 명세
```
아래 순서로 API를 호출
```

### url
<img width="1431" alt="image" src="https://user-images.githubusercontent.com/67543838/213925814-d6db7e9c-dd84-4b67-92bb-4c87f7a21474.png">

```
http://0.0.0.0:8000/swagger
```

<img width="1424" alt="image" src="https://user-images.githubusercontent.com/67543838/213926593-589c8aba-a21e-42d9-8646-bb1b97869406.png">

```
Click Execute button
```


<img width="1402" alt="image" src="https://user-images.githubusercontent.com/67543838/213926645-81e745f7-5b9f-42eb-8c30-dcf20ee0373a.png">

```
You can see url objects are created in database
```

### crawl
<img width="1413" alt="image" src="https://user-images.githubusercontent.com/67543838/213927068-20ec78ca-dc90-4a91-9fbf-611d86425c55.png">

<img width="1413" alt="image" src="https://user-images.githubusercontent.com/67543838/213927038-e83f1620-e80b-43c8-8a7f-43b088f641c3.png">

```
Click Execute button with data

sending data looks like below

{
  "url": "https://school.iamservice.net/organization/1674/group/2001892"
}
```

<img width="1403" alt="image" src="https://user-images.githubusercontent.com/67543838/213927225-75719f3c-6207-465b-875c-547fc6d2f8d5.png">

```
수서초등학교에 해당하는 url에 대하여 crawling 한 결과 값을 REST API 형태로 Response
```

```
위와 같은 방법으로 나머지 4개 URL에 대하여 실시
```

<img width="1405" alt="image" src="https://user-images.githubusercontent.com/67543838/213927400-b6b1f0a1-f3bb-4dab-b2bf-9cb5de392c82.png">
<img width="1397" alt="image" src="https://user-images.githubusercontent.com/67543838/213927425-a16c112f-1eb4-455b-80e7-9bcd98cf393f.png">
<img width="1394" alt="image" src="https://user-images.githubusercontent.com/67543838/213927444-d0055562-4493-49b5-ba80-ce7a1ae8654b.png">
<img width="1389" alt="image" src="https://user-images.githubusercontent.com/67543838/213927459-67ba9c95-67b8-477a-bbfd-56bd0bd58008.png">


### sunae
<img width="1428" alt="image" src="https://user-images.githubusercontent.com/67543838/213925857-52ba2e6a-fa02-4ee0-a12d-fd727fd1f857.png">

```
해당 url은 수내초등학교에서 크롤링 된 결과물에 적은 숫자에 해당하는 객체를 반환
```

### yongin
<img width="1431" alt="image" src="https://user-images.githubusercontent.com/67543838/213925888-e96636b4-c46c-4f46-9652-0f539648c9b6.png">

```
해당 url은 용인초등학교에서 크롤링 된 결과물에 적은 숫자에 해당하는 객체를 반환
```

### seoong-nam
<img width="1430" alt="image" src="https://user-images.githubusercontent.com/67543838/213925912-0276c8c8-0314-4740-93e1-d30823fc72b2.png">

```
해당 url은 성남시 블로그에서 크롤링 된 결과물에 적은 숫자에 해당하는 객체를 반환
```

### gov
<img width="1432" alt="image" src="https://user-images.githubusercontent.com/67543838/213925939-3bc9f904-555e-4b18-92d3-9ad2e3895495.png">

```
해당 url은 정부 블로그에서 크롤링 된 결과물에 적은 숫자에 해당하는 객체를 반환
```

### bbc
<img width="1428" alt="image" src="https://user-images.githubusercontent.com/67543838/213925969-a6af82c4-4f8f-4ffd-b9d5-20c6f952877a.png">

```
해당 url은 bbc에서 크롤링 된 결과물에 적은 숫자에 해당하는 객체를 반환
```

## 기술 스택
<img src="https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=Python&logoColor=white"/> <img src="https://img.shields.io/badge/Django-092E20?style=flat-square&logo=Django&logoColor=white"/> <img src="https://img.shields.io/badge/SQLite-003B57?style=flat-square&logo=SQLite&logoColor=white"/> <img src="https://img.shields.io/badge/PyCharm-000000?style=flat-square&logo=PyCharm&logoColor=white"/> <img src="https://img.shields.io/badge/VSCode-007ACC?style=flat-square&logo=Visual Studio Code&logoColor=white"/>
