# 🎊 Wanted X Wecode PreOnBoarding Backend Course | 무한루프 팀
원티드 1주차 기업 과제 : 프레시코드 Assignment Project
  ✅ 프레시코드 기업 과제입니다.
- [프레시코드 사이트](https://www.freshcode.me/) 
- [wanted 채용공고 링크](https://www.wanted.co.kr/wd/34118) 

<br>
<br>

# 🔖 목차
- Team 소개
- 과제 내용
- 기술 환경 및 tools
- 모델링 ERD
- API 명세서
- 설치 및 실행 방법


<br>
<br>

# 🧑‍🤝‍🧑 Team 소개

| 이름 | 담당 기능 | 블로그 |
| :---: | :---: | :---: | 
| 공통 | 초기환경 설정, DB 모델링, postman api 문서 작성, README.md 작성, 배포 | X |
| [손희정](https://github.com/heejung-gjt) | 상품 관리 기능 |  |
| [송치헌](https://github.com/Oraange) | 로그인 기능 | |
| [유동헌](https://github.com/dhhyy) | 상품 관리 기능 | |
| [하예준](https://github.com/TedJunny) | 상품 관리 기능 | |
| [오지윤(팀장)](https://github.com/Odreystella) | 로그인 기능 | https://bit.ly/3qxEQNu|

<br>
<br>

# 📖 과제 내용
> 아래 요구사항에 맞춰 상품 관리 Restfull API를 개발합니다.
### **[필수 포함 사항]**

- Swagger나 Postman을 이용하여 API 테스트 가능하도록 구현
  - Swagger 대신 Postman 이용시 API 목록을 Export하여 함께 제출해 주세요
- READ.ME 작성
    - 프로젝트 빌드, 자세한 실행 방법 명시
    - 구현 방법과 이유에 대한 간략한 설명
    - 완료된 시스템이 배포된 서버의 주소
    - Swagger를 통한 API 테스트할때 필요한 상세 방법
    - 해당 과제를 진행하면서 회고 내용 블로그 포스팅

### **[개발 요구 사항]**
- DB - RDBMS
- 로그인 기능(JWT 인증 방식)

### **[기능 개발]**
- 로그인 기능
   - JWT 인증 방식 이용
   - Authorization 키의 값이 없거나 인증 실패시 적절한 Error Handling
   - 권한 부여 후, 권한에 따른 상품 관리(추가/수정/삭제)
 - 상품 관리 기능
   - 상품 조회 기능(하나 또는 전체 목록)
   - 전체 목록 조회 시 한 페이지당 5개의 아이템 페이징 처리
   - 관리자 권한만 상품 추가/수정/삭제 가능
   - 적절한 Error Handling

<br>

# ➡️ Build(AWS EC2)
API URL : http://3.36.59.83:8000/

<br>
<br>

# ⚒️ 기술 환경 및 tools
- Back-End: python 3.8.12, Django 3.2.9, MySQL
- Deploy: AWS EC2, RDS
- ETC: Git, Github, Postman

<br>

# 📋 모델링 ERD

<img src="images/fresh_code_erd.png" />

- 추후 서비스 확장을 고려하여 Badge, Size, Tag 테이블을 별도로 두어 Item, Menu 테이블에서 FK로 사용하였습니다.

<br>

# 🔖 API 명세서
[Postman API Document 보러가기](https://documenter.getpostman.com/view/16088238/UVC2J9qZ#a3d9020e-61f3-4e69-aca7-e92e6157d57b)

<br>

### 👉 유저 로그인

1. 유저 로그인 시 이메일/패스워드를 body에 담아 요청합니다.
2. 유저의 이메일과 패스워드를 검증 후 유효하지 않는 경우 에러 메시지를 반환합니다.
3. 유효한 유저인 경우 유저의 token을 반환합니다.

- Method: POST
```
http://3.36.59.83:8000/users/sign-in
```

- parameter : request_body
```
{
    "email"    : "abc123@gmail.com",
    "password" : "qwerty135!@",
}
```

- response
```
{
    "message": "SUCCUESS",
    "token"  : "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MSwicm9sZSI6MSwiZXhwIjoxNjM2MTcxNjAxfQ.bMXiqp9nnhXkNGMxXCJYX6xj5rvdEqUFgCe25JYMsGo"
}
```

### 👉 상품 추가

1. 인증된 유저 중 admin 계정만이 상품을 추가할 수 있습니다.
2. 헤더에 토큰과 상품 이름, 카테고리, 설명, 뱃지, 태그를 body에 담아 요청합니다.
3. 유저의 role을 검증 후 유효하지 않는 경우 에러 메시지를 반환합니다.
4. 유효한 유저인 경우 성공 메시지를 반환합니다.

- Method: POST

```
http://3.36.59.83:8000/products
```

- header : Bearer token

- parameter : request_body
```
{
    "name"        : "망고 샐러드",
    "category"    : "SALAD",
    "description" : "망고 담긴 샐러드",
    "badge"       : "NEW",
    "tag"         : "유제품"
}
```

- response
```
{
    "message": "들기름 메밀면 has successfully posted"
}
```

### 👉 상품 목록 조회

1. offset limit 페이징 처리 후 해당 페이지의 상품을 반환합니다.

- Method: GET

```
http://3.36.59.83:8000/list?limit=5&offset=1
```

- parameter : query_parameter

- response
```
{
   {
    {
  "menus": [
    {
      "id": 5,
      "category": "SALAD",
      "name": "메밀면 샐러드",
      "description": "숯불에 구운 메밀면",
      "is_sold": false,
      "badge": "NEW",
      "items": [
        {
          "id": 13,
          "menu_id": 5,
          "name": "라지",
          "size": "L",
          "price": 10000,
          "is_sold": false
        },
        {
          "id": 14,
          "menu_id": 5,
          "name": "미디움",
          "size": "M",
          "price": 8000,
          "is_sold": false
        },
        {
          "id": 15,
          "menu_id": 5,
          "name": "스몰",
          "size": "S",
          "price": 5000,
          "is_sold": false
        }
      ],
      "tags": [
        {
          "id": 1,
          "menu_id": 5,
          "type": "vegetarianism",
          "name": "페스코베지테리언"
        }
      ]
    },
    
    ...
    
   {
      "id": 1,
      "category": "SALAD",
      "name": "요거트샐러드",
      "description": "맛있는 요거트 샐러드",
      "is_sold": false,
      "badge": "NEW",
      "items": [
        {
          "id": 1,
          "menu_id": 1,
          "name": "미디움",
          "size": "M",
          "price": 3000,
          "is_sold": false
        },
        {
          "id": 2,
          "menu_id": 1,
          "name": "미디움",
          "size": "M",
          "price": 12000,
          "is_sold": false
        },
        {
          "id": 3,
          "menu_id": 1,
          "name": "스몰",
          "size": "S",
          "price": 9000,
          "is_sold": false
        }
      ],
      "tags": [
        {
          "id": 2,
          "menu_id": 1,
          "type": "dairy",
          "name": "유제품"
        }
      ]
    }
}

```

### 👉 상품 조회

1. 선택한 상품의 상세 정보를 조회합니다.

- Method: GET

```
http://3.36.59.83:8000/products/5
```

- parameter : path_parameter

- response
```
{
  "menus": {
    "id": 5,
    "category": "SALAD",
    "name": "메밀면 샐러드",
    "description": "숯불에 구운 메밀면",
    "isSold": false,
    "badge": "NEW",
    "items": [
      {
        "item": 13,
        "memuID": 5,
        "size": "라지",
        "price": 10000,
        "isSold": false
      },
      {
        "item": 14,
        "memuID": 5,
        "size": "미디움",
        "price": 8000,
        "isSold": false
      },
      {
        "item": 15,
        "memuID": 5,
        "size": "스몰",
        "price": 5000,
        "isSold": false
      }
    ],
    "tags": [
      {
        "id": 1,
        "menuID": 5,
        "type": "vegetarianism",
        "name": "페스코베지테리언"
      }
    ]
  }
}
```

### 👉 상품 수정(이름, 설명)

1. 헤더로 받은 토큰으로 관리자 계정인지 확인합니다.
2. 검증 후, 상품의 이름과 설명을 수정합니다.

- Method: PUT

```
http://3.36.59.83:8000/products/1
```

- header : Bearer token

- parameter : request_body
```
{
    "name" : "딸기 샐러드",
    "description": "아주 맛있는 딸기 샐러드"
}
```

- response
```
{
    "menu name": "딸기 샐러드", 
    "menu desc": "아주 맛있는 딸기 샐러드"
    }
```

### 👉 아이템 수정(가격, 사이즈) 

1. 헤더로 받은 토큰으로 관리자 계정인지 확인합니다.
2. 검증 후, 상품의 가격과 사이즈를 수정합니다.

- Method: PUT

```
http://3.36.59.83:8000/item/1
```

- header : Bearer token

- parameter : request_body
```
{
    "price": 3000,
    "size": "M"
}
```

- response
```
{
    "item price": 3000, 
    "item size": "M"
}
```

### 👉 상품 삭제

1. 헤더로 받은 토큰으로 관리자 계정인지 확인합니다.
2. 검증 후, path parameter로 받은 상품을 삭제합니다.

- Method: DELETE

```
http://3.36.59.83:8000/products/1
```

- header : Bearer token

- parameter : path_parameter

- response
```
{
  "message": "망고 샐러드 has successfully deleted",
  "result": "1 rows has affected"
}
```

# 🔖 설치 및 실행 방법

### 로컬 및 테스트용
1. 해당 프로젝트를 clone하고, 프로젝트로 들어간다.
```
git clone https://github.com/wanted-InfinityLoop/fresh-code-InfinityLoop.git .
```
2. 가상환경으로 miniconda를 설치한다. [Go](https://docs.conda.io/en/latest/miniconda.html)
3. 가상환경 생성 후, requirements.txt를 설치한다.
```
conda create -n fresh-code python=3.8
conda actvate fresh-code
pip install -r requirements.txt
```
4. makemigrations 후 로컬 서버 가동
```
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

### 배포 및 테스트용
```
docker build -t <docker 계정명>/<이미지명>:<버전> .
```

<br>

# 🌲 디렉토리 구조
```
.
├── config
│   ├── asgi.py
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── core
│   ├── admin.py
│   ├── apps.py
│   ├── decorators.py
│   ├── __init__.py
│   ├── migrations
│   ├── models.py
│   ├── tests.py
│   ├── validators.py
│   └── views.py
├── products
│   ├── admin.py
│   ├── apps.py
│   ├── __init__.py
│   ├── migrations
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
└── users
|    ├── admin.py
|    ├── apps.py
|    ├── __init__.py
|    ├── managers.py
|    ├── migrations
|    ├── models.py
|    ├── tests.py
|    ├── urls.py
|    └── views.py
├── CONVENTION.md
├── fresh_code.txt
├── images
│   └── fresh_code_erd.png
├── manage.py
├── my_settings.py
├── PULL_REQUEST_TEMPLATE.md
├── README.md
├── requirements.txt
```

<br>
