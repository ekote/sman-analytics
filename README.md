# Social Media and News Analytics - Brand Monitoring
Social Media and News Analytics Approach build using Azure Synapse Pipelines, Azure Cognitive Services Text Analytics, Azure Bing News Search, Azure Machine Learning.



## Ingredients

- [Azure Synapse Analytics](https://docs.microsoft.com/en-us/azure/synapse-analytics/overview-what-is) 
- [Azure Machine Learning](https://docs.microsoft.com/en-us/azure/machine-learning/) / or Azure Function (TBD)
- [ADLS](https://docs.microsoft.com/en-us/azure/storage/blobs/data-lake-storage-introduction) connected with Synapse and Machine Learning
- [Facebook Scraper library](https://github.com/kevinzg/facebook-scraper/ ) 
- [Azure Cognitive Services - Text Analytics](https://azure.microsoft.com/en-us/services/cognitive-services/text-analytics/)
  - [Text translation](https://docs.microsoft.com/en-us/azure/cognitive-services/translator/)
  - [Sentiment analysis](https://docs.microsoft.com/en-us/azure/cognitive-services/language-service/sentiment-opinion-mining/overview)



## Recipe

1. Provision resources: Azure Synapse Analytics, Azure Machine Learning (connect with the same storage account as was created for Synapse). 

2. Data Scraper

   1. Azure Machine Learning Notebook with Compute Instance (shortcut)

      1. Go to Azure ML Studio
      1. Create Compute Instance
      1. Run the terminal
      1. Clone the repo
      1. Go to `azureml/fb-scraper.ipynb` and install the required library (`pip install facebook-scraper`)
      1. Provide the cookie file (e.g.  extract cookies from your browser after logging into Facebook with an extension like [EditThisCookie (Chrome)](https://chrome.google.com/webstore/detail/editthiscookie/fngmhnnpilhplaeedifhccceomclgfbg?hl=en) or [Cookie Quick Manager (Firefox)](https://addons.mozilla.org/en-US/firefox/addon/cookie-quick-manager/). Make sure that you include both the c_user cookie and the xs cookie, you will get an InvalidCookies exception if you don't.)
      1. Adjust the parameters from the file `scraper.py`:

      ```python
      pages = ('Microsoft.Polska', 'MicrosoftCEE', 'MicrosoftUKEducation', 'Microsoft')
      project_name = "microsoft"
      date = "08_12_2021"
      pages_no = 100
      coockie_file = "cookie.json"
      ```

      6. Run the cell `!python scraper.py` that will run the scraper script. 
      7. Sample results available in the folder `microsoft`
      8. It will take a couple of minutes (or hours, it depends) to complete it. Once it's done - run the last cells that will upload data to a proper place on ADLS that is also connected with Synapse.  

   2. Azure Machine Learning Notebook with Compute cluster 

      The 'as it should be' way described here`azureml/fb-scraper-pipeline.ipynb` 

   

3. Pipeline

   1. Parameters



### Lessons learnt

- comments/posts/any text - "," comma is not the best delimiter or it can be, but remove commas from the text.
- Facebook bans too active users `raise exceptions.TemporarilyBanned(title.text)
  facebook_scraper.exceptions.TemporarilyBanned: You’re Temporarily Blocked`
- 



## Production deployment - to consider

- [ ] Azure Synapse Pipeline schedule
- [ ] Facebook scraper - scheduling daily/weekly
- [ ] Using Azure Functions for scraping
- [ ] Instead of open-sourced library use professional scraper like [Apify](https://apify.com/pocesar/facebook-pages-scraper)
- [ ] Want to add Twitter as the data source? [Check this little library - twitter-scraper](https://github.com/bisguzar/twitter-scraper)


