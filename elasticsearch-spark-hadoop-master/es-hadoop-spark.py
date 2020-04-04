import findspark
findspark.init()
from pyspark.sql import SparkSession



from pyspark import SparkConf, SparkContext
conf = (SparkConf().setMaster("spark://spark-master:7077").setAppName("recommender").setAll([('spark.executor.memory', '2g'), ('spark.executor.cores', '4'), ('spark.cores.max', '8'), ('spark.driver.memory','8g')]))


from pyspark import SparkContext, SparkConf
from pyspark.sql import SQLContext

import json

errors.map(json.dumps)\
    .map(lambda x: ('key', x))

#conf = SparkConf()
#conf.set("es.nodes1", "192.168.1.156:9200")

sc = SparkContext(conf=conf)
sqlContext = SQLContext(sc)

es_write_conf = {

# specify the node that we are sending data to (this should be the master)
"es.nodes" : '192.168.1.156',

# specify the port in case it is not the default port
"es.port" : '9200',

# specify a resource in the form 'index/doc-type'
"es.resource" : 'testindex/testdoc',

# is the input JSON?
"es.input.json" : "yes",

# is there a field in the mapping that should be used to specify the ES document ID
"es.mapping.id": "doc_id"

}

data = [
{'some_key': 'some_value', 'doc_id': 123},
{'some_key': 'some_value', 'doc_id': 456},
{'some_key': 'some_value', 'doc_id': 789}
]

rdd = sc.parallelize(data)

def format_data(x):
    return (data['doc_id'], json.dumps(data))

rdd = rdd.map(lambda x: format_data(x))
"""
rdd.saveAsNewAPIHadoopFile(
    path='-',
    outputFormatClass="org.elasticsearch.hadoop.mr.EsOutputFormat",
    keyClass="org.apache.hadoop.io.NullWritable",
    valueClass="org.elasticsearch.hadoop.mr.LinkedMapWritable",
    conf=es_write_conf)
"""
