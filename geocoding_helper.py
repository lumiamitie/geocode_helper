import geocoder
import functools as fn
from collections import Counter

try:
    from tqdm import tqdm
    STATUS_tqdm = True
except ImportError:
    STATUS_tqdm = False
    print('tqdm is not installed')
    print('Please install tqdm to check progress')
    print('run "!pip install tqdm" to install tqdm in jupyter')


class GeocodingError(Exception):
    '''
    Google Geocoding API의 에러를 받아서 raise시킨다.
    https://developers.google.com/maps/documentation/geocoding/intro?hl=ko
    
    ZERO_RESULTS     : 지오코드가 성공했지만 반환된 결과가 없음
    OVER_QUERY_LIMIT : 구글 API의 일일 제한 한도를 초과
    REQUEST_DENIED   : 요청이 거부되었음
    INVALID_REQUEST  : 쿼리(address, components 또는 latlng)가 누락되었음
    UNKNOWN_ERROR    : 서버 오류로 인해 요청을 처리할 수 없음
    '''
    
    def __init__(self, error_type):
        self.error_type = error_type

        
        
class GeocodeByGoogle:
    '''
    geocoder 라이브러리의 geocoder.google 함수를 조금 더 편리하게 사용할 수 있게 한다
    
    methods
    ---
    
    geocode      : 주소 하나의 위경도 값을 받아온다. geocoder.google 과는 달리 에러가 발생하면 오류를 반환한다.
    geocode_list : 주소 리스트가 주어질 경우 주소와 위경도 값을 반환한다. 
                   에러가 발생하면 위경도 값에 None을 반환하고, 오류별 개수를 표시해서 알려준다
    cache_clear  : 캐시를 모두 제거한다
    cache_info   : 캐시 정보를 확인한다
    
    
    params
    ---
    show_progress(default: True) : tqdm이 설치된 상태에서 show_progress=True일 경우, 
                                   geocode_list 메서드를 실행하면 진행상황이 표시된다
    '''
    def __init__(self, show_progress=True):
        self.status_tqdm = STATUS_tqdm and show_progress
    
    @fn.lru_cache(maxsize=2500)
    def geocode(self, addr):
        '''
        GeocodeByGoogle.geocode(주소:str)
        ---
        
        geocoder.google 과 동일한 기능을 한다. 차이점은 다음과 같다
        
        - 주소에 해당하는 결과물이 존재하지 않거나 api 할당량을 초과하는 경우 에러를 발생시킨다
        - functools.lru_cache 를 이용하여 결과를 캐싱한다
        '''
        # print('live geocoding!')
        r = geocoder.google(addr)

        if r.error is not None:
            raise GeocodingError(r.error)

        return r
    
    def geocode_list(self, addr_list):
        '''
        GeocodeByGoogle.geocode_list(주소들:list of str)
        ---
        
        주소가 list 형태로 주어지면 각 주소에 해당하는 위경도 값을 반환한다
        tqdm 라이브러리가 설치되어 있을 경우, 진행상황이 표시된다
        '''
        # 최종적으로 결과물을 저장할 리스트
        result_list = []

        # 에러가 발생할 경우 에러 종류를 저장할 리스트
        error_list = []

        if self.status_tqdm:
            loop = tqdm(addr_list)
        else:
            loop = addr_list

        for addr in loop:
            try:
                # geocoding 시도
                g = self.geocode(addr)
                result_list.append({'addr': addr, 'lat': g.latlng[0], 'lng': g.latlng[1]})
            except GeocodingError as e:
                # 에러가 발생할 경우 None으로 값을 채운다
                result_list.append({'addr': addr, 'lat': None, 'lng': None})
                error_list.append(e.args[0])

        # 에러가 발생했을 경우 에러별로 횟수를 정리해서 공유
        if len(error_list) > 0:
            error_counts = Counter(error_list)
            print('Error Counts : ', error_counts.most_common())

        return result_list
    
    def cache_clear(self):
        self.geocode.cache_clear()
        print('Cache Cleared!')
        
    def cache_info(self):
        return self.geocode.cache_info()