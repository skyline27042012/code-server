
import findspark
findspark.init()
from pyspark.sql import SparkSession

from pyspark import SparkConf, SparkContext
conf = (SparkConf().setMaster("spark://spark-master:7077").setAppName("recommender").setAll([('spark.executor.memory', '2g'), ('spark.executor.cores', '4'), ('spark.cores.max', '8'), ('spark.driver.memory','8g')]))

from pyspark import SparkContext, SparkConf
from pyspark.sql import SQLContext

"""
if __name__ == "__main__":
    #conf = SparkConf().setAppName("WriteToES")
    sc = SparkContext(conf=conf)
    sqlContext = SQLContext(sc)
    es_conf = {"es.nodes" : "192.168.1.161",
    "es.port" : "9200","es.nodes.client.only" : "true","es.resource" : "sensor_counts/metrics"}
    es_df_p = sqlContext.read.format("com.databricks.spark.csv").option("header", "true").load("output/part-00000-c353bb29-f189-4189-b35b-f7f1af717355.csv")
    es_df_pf= es_df_p.groupBy("network_key")
    es_df_pf.saveAsNewAPIHadoopFile(
    path='-',
    outputFormatClass="org.elasticsearch.hadoop.mr.EsOutputFormat",
    keyClass="org.apache.hadoop.io.NullWritable",
    valueClass="org.elasticsearch.hadoop.mr.LinkedMapWritable",
    conf=es_conf)
"""







