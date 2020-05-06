import boto3
from botocore.exceptions import ClientError



s3 = boto3.client('s3')


BUCKET_NAME = 'aws-shweta-poc'

PATH = 'blah'

# fetches items at the required path in the S3 bucket
# returns a list of dictionaries each dictionary is one item
items = s3.list_objects(Bucket = BUCKET_NAME
                , Delimiter='/'
                , Prefix=f'/{PATH}/')['Contents']



# you can filter files for a certain type, size etc. 
# for example 
# pick up only csv files 
csv_items = [di for di in items if '.csv' in di['Key']]


#Sort the csv items by the latest month
x = sorted(csv_items, key = lambda i: i['LastModified'])

# use the latest one -- this will give us the latest csv file dumped 
x.pop() 