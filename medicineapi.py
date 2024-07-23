import requests
from env import SERVICE_KEY

url = 'http://apis.data.go.kr/1471000/MdcinGrnIdntfcInfoService01/getMdcinGrnIdntfcInfoList01'
params ={'serviceKey' : SERVICE_KEY.KEY, 
         'item_name' : '스타렌 정', 
         'entp_name' : '', 
         'item_seq' : '', 
         'img_regist_ts' : '', 
         'pageNo' : '1', 
         'numOfRows' : '3', 
         'edi_code' : '', 
         'type' : 'xml' }

response = requests.get(url, params=params)
print(response.content)