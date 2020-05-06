#!/usr/bin/env python
# coding: utf-8

# In[1]:


import findspark
findspark.init()

import pyspark;


# In[2]:


import os
os.environ['PYSPARK_SUBMIT_ARGS'] = '--packages net.snowflake:snowflake-jdbc:3.6.24,net.snowflake:spark-snowflake_2.11:2.4.12-spark_2.3 pyspark-shell'


# In[3]:


from pyspark import SparkConf, SparkContext
from pyspark.sql import SQLContext, SparkSession
from pyspark.sql.types import *
from pyspark import SparkConf, SparkContext 

#ML
from pyspark.ml import Pipeline
from pyspark.ml.clustering import KMeans
from pyspark.ml.classification import GBTClassifier, DecisionTreeClassifier
from pyspark.ml.feature import StringIndexer, VectorIndexer, VectorAssembler, IndexToString
from pyspark.ml.evaluation import MulticlassClassificationEvaluator


# In[4]:


spark = SparkSession.builder.master('local').appName('playground').config('spark.driver.memory', '5G').getOrCreate()
spark.builder.config('spark.executor.memory', '16G')
spark.builder.config("spark.executor.cores", "4")


# In[5]:


SNOWFLAKE_SOURCE_NAME = "net.snowflake.spark.snowflake"
sfOptions = {"sfURL":"*", "sfAccount":"*", "sfUser":"*", "sfPassword":"*", "sfDatabase":"*", "sfSchema":"*", "sfWarehouse":"*"}


# In[6]:


#Importing Data 
df = spark.read.csv('/Users/spurushe/Downloads/iris.csv', header='true', inferSchema='true')
df.show(5)


# In[7]:


type(df)


# In[7]:


#StringIndexer () is an Estimator which returns a Transformer (labelIndexer)
# Converts label String classes to indices --- for e.g. 'good', 'bad', 'ugly' to 0,1,2
labelIndexer = StringIndexer(inputCol="Species", outputCol="indexedLabel").fit(df)


# In[8]:


featureAssembler = VectorAssembler(inputCols= [x for x in df.columns if x != 'Species' and x != 'Id'], outputCol="features")

featureIndexer =VectorIndexer(inputCol="features", outputCol="indexedFeatures", maxCategories=4)


# In[11]:


fa = featureAssembler.transform(df)
featureIndexer.fit(fa).transform(fa).show()


# In[9]:


# Chain indexers and Decision tree in a Pipeline
trans_pipeline = Pipeline(stages=[labelIndexer, featureAssembler, featureIndexer])
transformed_df = trans_pipeline.fit(df).transform(df)


# In[10]:


#*******************************************
# SINGLE TRAIN TEST SPLIT
#*******************************************.
(trainingData, testData) = transformed_df.randomSplit([0.7, 0.3])


# In[11]:


#*******************************************
# TRAINING THE MODEL
#*******************************************.
dec_t = DecisionTreeClassifier(labelCol="indexedLabel", featuresCol="indexedFeatures")


# In[12]:


# Train model.  This also runs the indexers.
# Estimators' .fit() returns a Transformer (model)
model = dec_t.fit(trainingData)


# In[13]:


#*******************************************
# PREDICTION
#*******************************************
predictions = model.transform(testData)


# In[14]:


# Quick view at columns of interest
predictions.select('Id', 'indexedLabel', 'prediction', 'probability').show(5)


# In[15]:


predictions.printSchema()


# In[19]:


# Convert indices back to labels
in_to_label = IndexToString(inputCol='indexedLabel', outputCol='Predicted_label').transform(predictions)
in_to_label.select('Species','indexedLabel', 'Predicted_label').head(30)


# In[16]:


#*******************************************
# EVALUATION
#
# evaluating the performance of our ML model
#*******************************************

eva = MulticlassClassificationEvaluator(labelCol='indexedLabel', predictionCol='prediction', metricName='accuracy')

accuracy = eva.evaluate(predictions)
print("Accuracy of our DT model in predicting flowers is ", accuracy)


# In[21]:


## Getting the entire Decision Tree rules.

print(model.toDebugString)


# #### Splitting the probability column into the respective number of columns 
# (One column per category of the target variable)

# In[17]:


subset = predictions.select('Id', 'indexedLabel', 'prediction', 'probability')


# In[18]:


subset.count()


# In[19]:


subset.show(5)


# In[20]:


subset.printSchema()


# ### Using a udf here (permisson problems with rdd solution)

# In[21]:


from pyspark.sql.functions import udf, col
from pyspark.sql.types import ArrayType, DoubleType

def to_array(col):
    def to_array_(v):
        return v.toArray().tolist()
    return udf(to_array_, ArrayType(DoubleType()))(col)

d = predictions    .withColumn("xs", to_array(col("probability")))    .select(['Id','probability', 'prediction'] + [col("xs")[i] for i in range(3)])


# In[22]:


d.columns


# ### Clustering

# In[23]:


kmeans = KMeans(k = 3, seed=2018, featuresCol="probability", predictionCol='clustered_prediction')


# In[24]:


clustered_df = kmeans.fit(d).transform(d)


# In[25]:


clustered_df.columns


# In[26]:


clustered_df.printSchema()


# In[27]:


selections = [x[0] for x in clustered_df.dtypes if x[1] != 'vector']
selections


# In[28]:


clustered_df.columns


# In[29]:


clustered_df.show(5)


# In[30]:


clustered_df.select(selections)        .write.format(SNOWFLAKE_SOURCE_NAME)        .mode("overwrite")        .options(**sfOptions)        .option("dbtable", "dev.zsp.iris_clustered")        .save()


# In[ ]:





# In[31]:


spark.stop()

