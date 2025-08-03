



1. This project is using Python and the source data will get from data.gov.sg via API provided below from the origin source:
"""
import requests
          
dataset_id = "d_8b84c4ee58e3cfc0ece0d773c8ca6abc"
url = "https://data.gov.sg/api/action/datastore_search?resource_id="  + dataset_id
        
response = requests.get(url)
print(response.json())
"""

2. Install Environment.yml

3. Run Streamlit following url


Notes:
1. The approximate floor area includes any recess area purchased, space adding item under HDB’s upgrading programmes, roof terrace, etc.
2. The transactions exclude resale transactions that may not reflect the full market price such as resale between relatives and resale of part shares.
3. Resale prices should be taken as indicative only as the resale prices agreed between buyers and sellers are dependent on many factors.



1. create new project using python to connect api below data set https://data.gov.sg/api/action/datastore_search?resource_id=d_8b84c4ee58e3cfc0ece0d773c8ca6abc
see the option if the peformance better to save the data to CSV or directly to the data.gov.sg to manipulate the data

2. Create Evironment.yml to create all the packages Python, Streamlit, etc

3. Create new file with New_Readme.md  

4. Create comprehensive analysis and report in Streamlit