# json_validator

1. Goal: Verify accuracy of data from crawler by matching it to example JSON output

2. Approach: Using JSON schema, check that necessary keys are present, check that value outputs are valid by checking for invalid values and verifying relevancy of data by comparing the structure of new data (data types, lengths, etc) to verified data using regex. 

3. Test cases/plan: 
    - First test that the data is structured in a way that contains all relevant information. This means marking all necessary keys are marked required and values for those 
      keys are not null or irrelevant. 
    - Check for duplicate data entries
    - Check for completeness (all products are scraped)
    - Compare data to past data for significant differences in values/outputs
    - Verify links gathered as well download information is accurate and will enable downloads in the future
    
4. Conclusions and next steps: The script here checks basic structure and relevancy of data collected. By looking at data structure and verifying that values broadly fit expected outcome we can have a high degree of certainty that the data is accurate. Ways to improve verification include analyzing the relation between collected keys and values (for example values are sometimes present in multiple keys, such as the series and models present in the URL) and building a more exact check to verify that the relation between the keys/values is accurate. Another thing to consider is a more robust test of URLs. Checking that a URL is active is a simple check, but there are concerns relating to efficiency and potentially being blocked from the source site, placing these tests outside of the realm of this script. 




