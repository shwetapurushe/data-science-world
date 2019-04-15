#!/usr/bin/env python
# coding: utf-8
#*********************************IMP ENV VARIABLES IN ~bash_profile#*********************************




# export PATH="/Users/spurushe/Documents/apache-maven-3.3.9/bin:$PATH"
# export SPARK_HOME="/Users/spurushe/spark/spark-2.3.1-bin-hadoop2.7"

# # FOR Pyspark
# export PYSPARK_PYTHON="/Users/spurushe/spark/spark-2.3.1-bin-hadoop2.7/python" #causes permission error 13 issues

#USE THIS 
export PYSPARK_PYTHON="/Library/Frameworks/Python.framework/Versions/3.6/bin/python3"


# #JAVA home
# JAVA_HOME=$(/usr/libexec/java_home)
# export JAVA_HOME;
# #For R
# export LD_LIBRARY_PATH=$JAVA_HOME/jre/lib/server;



# # Setting PATH for Python 3.6
# # The original version is saved in .bash_profile.pysave
# PATH="/Library/Frameworks/Python.framework/Versions/3.6/bin:${PATH}"
# export PATH
# In[ ]:


import findspark
findspark.init()

import pyspark;
#get_ipython().profile_dir.startup_dir


# In[2]:


import os
os.environ['PYSPARK_SUBMIT_ARGS'] = '--packages net.snowflake:snowflake-jdbc:3.6.24,net.snowflake:spark-snowflake_2.11:2.4.12-spark_2.3 pyspark-shell'


# In[3]:


from pyspark import SparkConf, SparkContext
from pyspark.sql import SQLContext, SparkSession
from pyspark.sql.types import *
from pyspark import SparkConf, SparkContext 

from pyspark.ml import Pipeline
from pyspark.ml.classification import DecisionTreeClassifier
from pyspark.ml.feature import StringIndexer, VectorIndexer
from pyspark.ml.evaluation import MulticlassClassificationEvaluator

# sc_conf = SparkConf()
# sc_conf.setAppName('Subscription_Predictor')
# sc_conf.setMaster("local[*]")
# sc_conf.set('spark.driver.memory', '5G')
# sc_conf.set('spark.executor.memory', '16G')
# sc_conf.set('spark.memory.fraction', '0.6')
# sc_conf.set('spark.executor.cores', '4')


# In[4]:


spark = SparkSession.builder.master('local').appName('test').config('spark.driver.memory', '5G').getOrCreate()


# In[5]:


spark.builder.config('spark.executor.memory', '16G')
spark.builder.config("spark.executor.cores", "4")


# In[6]:


SNOWFLAKE_SOURCE_NAME = "net.snowflake.spark.snowflake"
sfOptions = {"sfURL":"*", "sfAccount":"*", "sfUser":"*", "sfPassword":"*", "sfDatabase":"*", "sfSchema":"*", "sfWarehouse":"*"}
df = spark.read.format(SNOWFLAKE_SOURCE_NAME).options(**sfOptions).option("*", "*").load()


# In[7]:


df.count()


# In[8]:


spark

