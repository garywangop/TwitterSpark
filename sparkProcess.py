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
