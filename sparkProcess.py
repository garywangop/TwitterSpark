from pyspark import SparkConf,SparkContext
from pyspark.sql import Row,SQLContext
from pyspark.streaming import StreamingContext
import requests
import sys

conf = SparkConf()
conf.setAppName("TwitterStreamApplication")
sc = SparkContext(conf=conf)
sc.setLogLevel("ERROR")
ssc = StreamingContext(sc, 1)
ssc.checkpoint("checkpoint_TwitterStreamApp")
dataStream = ssc.socketTextStream("localhost",9090)

def sumup_tags_counts(new_values, total_sum):
    return (total_sum or 0) + sum(new_values)

def return_sql_context_instance(spark_context):
    if ('sqlContextSingletonInstance' not in globals()):
        globals()['sqlContextSingletonInstance'] = SQLContext(spark_context)
    return globals()['sqlContextSingletonInstance']

def stream_dataframe_to_flask(df):
    top_tags = [str(t.tag) for t in df.select("tag").collect()]
    tags_count = [p.counts for p in df.select("count").collect()]
    url = 'http://0.0.0.0:5050/updateData'
    request_data = {'words': str(top_tags), 'counts': str(tags_count)}
    response = requests.post(url, data=request_data)
