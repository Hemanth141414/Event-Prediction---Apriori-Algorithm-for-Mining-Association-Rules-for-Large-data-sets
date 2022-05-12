To run this program run the command in below format
 
  python3 aprio.py <your_dataset.csv> <support> <confidence>

Ex: python3 aprio.py INTEGRATED-DATASET.csv 0.02 0.5

Here, 0.02 is the support and confidence is 0.5.
 

Dataset details:
  Data I'm using in this is from the official New York City data sets that are available at the NYC Open Data site: https://opendata.cityofnewyork.us/data/
  
  I used the NYC_Parks_Events_Listing___Event_Listing as the main table and joined the data from NYC_Parks_Events_Listing___Event_Categories and NYC_Parks_Events_Listing___Event_Locations by a common column event_id in Microsoft Excel using Vlookup. 
  After that we imported this data to Microsoft SQL Server Management Studio and got about 3000 rows for our Integrated-Dataset.csv. I retained only three columns: event_type from event category dataset, event_location from location dataset and start_time from event-listing dataset. 
  
  The query I used is Sql server management studio is as follows:

  select TOP (3000) * from dbo.data$ where dbo.data$.type in ('Accessible', 'Art', 'Arts & Crafts', 'Best for Kids', 'Education', 'Fitness', 'Nature') and place in ('#N/A') order by place asc;

  From these 3000 rows I exported the data as Integrated-Dataset.csv

  
The Purpose of this data set and Interesting findings:
I want to use this data to provide insights of:
1. The probable event types at locations.
2. The probable event type at start times.
3. The probable event location when we know the type of event.
  

Algorithm: The Apriori algorithm in Section 2.1 in general, and in Section 2.1.1 from Rakesh Agrawal and Ramakrishnan Srikant: Fast Algorithms for Mining Association Rules in Large Databases, VLDB 1994.
  
We can predict the type of event based on location or time and vice versa. For example, we found that from our dataset and algorithm, the Carmine Carro Community Center always holds the events of type Fitness (confidence 100%) and Alice Austen House Museum has Art events with confidence of about 60%.
