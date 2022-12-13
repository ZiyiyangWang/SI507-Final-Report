# Ann Arbor House Renting
## Overview
Craigslist is an American classified ads website, with sections for employment, housing, for sale, goods sought, services, volunteer opportunities, gigs, résumés, and discussion forums.

The website not only provides basic service information, such as hiring labor needed for moving, but also community life information, including publishing life-related wishes, as well as information on renting and selling houses, as well as job recruitment information. The posts posted by these individuals can be collected to understand the general needs of people by region.

![Craigslist main page](/img/craigs_index.png)

Use Python crawler, Flask framework, Echarts, WordCloud and other technologies to collect the [Ann Arbor house](https://annarbor.craigslist.org/search/apa) rental information, save it in Excel and database and make a tree data structure, perform data visualization operations, and make web page display.

## Data structure
Set *Ann Arbor* as root, make each *post* as nodes and *location*, *information*, *picture*, *price* as different child nodes. 

## Running method
Open ***craigslist.py***, run the file to get house renting data from craigslist and store the data into ***annarbor_renting.xls*** and ***annarbor_renting_cache.txt***. 

Run **AnnArbor_flask/app.py** and type **http://127.0.0.1:5000/index** in the chrome to reach to the display page.

###### Index Page
![Index page](/img/index1.png)
![Index page](/img/index2.png)

###### Posting Page
![Post page](/img/post.png)

###### House information Page
![information page](/img/info.png)

###### House picture Page
![Pic page](/img/pic.png)
