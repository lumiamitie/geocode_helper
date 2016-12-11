
# geocoding_helper

**`geocoder`** 라이브러리의 `geocoder.google` 함수에 일부 기능을 추가하였다.

**`tqdm`** 이 설치되어있을 경우, 진행상황을 표시해준다

`geocoding_helper.py` 파일과 같은 위치에 있는 상태에서 다음과 같이 불러온다


```python
import geocoding_helper
```

---

## GeocoeByGoogle 클래스


```python
gg = geocoding_helper.GeocodeByGoogle()
```

### .geocode()

**`GeocodeByGoogle.geocode`**는 **`geocoder.google`** 과 동일한 기능을 한다.

차이점은 다음과 같다

- 주소에 해당하는 결과물이 존재하지 않거나 api 할당량을 초과하는 경우 에러를 발생시킨다
- functools.lru_cache 를 이용하여 결과를 캐싱한다


```python
g = gg.geocode('서울시 서대문구 신촌동')
```


```python
g.latlng
#> [37.5646027, 126.9390819]
```




    



### .geocode_list()


```python
sample_list = ['서울특별시 서대문구 창천동 31-4', 
               '경기도 성남시 분당구 정자1동',
               '서울시 서대문구 신촌동',
               '서울특별시 서대문구 대현동 21-106',
               '서울특별시 서대문구 대현동 21-106 럭키아파트 ***동 ***호'
              ]
```

에러가 발생할 경우, 에러별로 개수를 알려준다.


```python
sample_result = gg.geocode_list(sample_list)
```


결과물은 다음과 같은 형태로 반환된다


```python
sample_result
#    [{'addr': '서울특별시 서대문구 창천동 31-4', 'lat': 37.5587229, 'lng': 126.9372291},
#     {'addr': '경기도 성남시 분당구 정자1동', 'lat': 37.3614515, 'lng': 127.111435},
#     {'addr': '서울시 서대문구 신촌동', 'lat': 37.5646027, 'lng': 126.9390819},
#     {'addr': '서울특별시 서대문구 대현동 21-106', 'lat': 37.5595283, 'lng': 126.9481818},
#     {'addr': '서울특별시 서대문구 대현동 21-106 럭키아파트 ***동 ***호', 'lat': None, 'lng': None}]
```








### .cache_info()

현재 캐시 정보를 알려준다


```python
gg.cache_info()
#> CacheInfo(hits=1, misses=4, maxsize=2500, currsize=4)
```








### .cache_clear()

캐시를 모두 제거한다


```python
gg.cache_clear()
#> Cache Cleared!

gg.cache_info()
#> CacheInfo(hits=0, misses=0, maxsize=2500, currsize=0)
```
