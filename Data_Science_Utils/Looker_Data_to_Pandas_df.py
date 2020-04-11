# Goal 
# Main purpose of this script is to fetch data from Looker and continue with further analysis 
# It is not to interact with Looker from Python 
# There are advantages to using Looker as a BI tool, but for downstream data science, I often pull data into Python 

# Begin with saving the data you need as a "Look" in Looker, creates a look with a "look_id"
# We use this id to pull data from the look into Python
# might not be the best way, was the quickest for me.




#from looker_sdk import client, models, error --OLD

import looker_sdk
import pandas as pd
from io import StringIO

#https://github.com/looker-open-source/sdk-codegen/blob/master/python/README.rst
# be prepared for changes since this is in beta version. 

# need to get your API client id and client secret from Looker admin
# and put it in your looker.ini file 



sdk = looker_sdk.init31()  # or init40() for v4.0 API
# Older way of doing it
#sdk = client.setup("looker.ini") 



looker_api_user = sdk.me()




my_look_id = 410


try:
    csv_string = sdk.run_look(look_id = my_look_id, result_format="csv") # the result returned from looker 
    csvio = StringIO(csv_string) #casting string 
    
    #final dataframe for further analysis
    df = pd.read_csv(csvio)
except e:
    print(e)
finally:
    sdk.logout() #deletes the access token once data has been  retrieved.
    csvio.close() # close String io buffer
    
    
    