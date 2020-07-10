# REST_TEST 코드 명세

## 빌드

```
$ docker-compose up --build
```

## 마이그레이션
```
# 컨테이너로 진입
$ docker exec -it flask_app /bin/bash

# 마이그레이션
$ python db.py db init
$ python db.py db migrate
$ python db.py db upgrade
```

## 테스트
```
# 컨테이너로 진입
$ docker exec -it flask_app /bin/bash

# 테스트 수행
$ cd tests
$ pytest test_main.py -vv (ordering, option)
```

## API 명세
1. 자동완성

    * endpoint: GET /auto_complete
    * parameter: q: 쿼리 텍스트
    * example: /auto_complete?q=wan
    * response
```
      [
          <Company Object>,
          ...
      ]
```

2. 검색

    * endpoint: GET /search
    * parameter: tag: 태그 텍스트
    * example: /search?tag=태그_4
    * response
```
      [
          <Company Object>,
          ...
      ]
```
3. 태그 추가

    * endpoint: PUT /add_tag/\<int:tag>
    * payload: tag-태그 lang-태그 언어
    * example: /add_tag/1 (payload- {"tag":  "태그_99", "lang": "ko"})
    * response
```
      <Company Object>
```
4. 태그 삭제

    * endpoint: PUT /del_tag/\<int:tag>
    * payload: tag-태그 lang-태그 언어
    * example: /del_tag/1 (payload- {"tag":  "태그_99", "lang": "ko"})
    * response
```
      <Company Object>
```