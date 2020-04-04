import os
from elasticsearch import Elasticsearch,helpers
from datetime import datetime
from xmljson import badgerfish as bf
from xml.etree.ElementTree import fromstring
from hdfs import InsecureClient
from datetime import datetime
result  = []
es = Elasticsearch(['192.168.1.110:9200'])
client = InsecureClient('http://192.168.1.185:9870')


filelist = client.list("/user/root/datasets/VOCdevkit/VOC2007/Annotations")
print(len(filelist))
for idx,filename in enumerate(filelist):
    with client.read("/user/root/datasets/VOCdevkit/VOC2007/Annotations/" + filename, encoding='utf-8') as reader:
        content = reader.read()
    content = content.replace("\n", "").replace("\t", "")
    doc = {
        'researcher': 'commander',
        'dataset': 'PASCALVOC 2007',
        'data': bf.data(fromstring(content)),
        'timestamp': datetime.now(),
    }
    result.append(doc)
helpers.bulk(es, result,index ='pascalvoc')