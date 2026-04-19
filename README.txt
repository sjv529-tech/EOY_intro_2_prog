Weather Prediction Application

Name: Ella Lou
P-number: 303065797
Course Code: IY499

I confirm that this assignment is my own work. Where I have referred to online sources, I have provided comments detailing the reference and included a link to the source.

Description 
This program fetches real-time and historical weather data using the Open-Meteo API. Users can view, save, and analyse weather trends including temperature, precipitation, and wind speed. The app includes data visualisation and can find the hottest/coldest days from saved data. You can look at temperature, rain, and wind speed over the last 7 days, hour by hour. (This means that when you are searching up a specific date (option 3), you need to pick one day from the last 7 days of running the program.)

I wrote all the main algorithms myself from scratch to prove I actually understand how they work. The app uses merge sort (that's O(n log n) if you care about efficiency) to sort through weather records, and binary search (O(log n)) when you want to find a specific date really fast. For predicting temperatures, I built my own linear regression model using the Ordinary Least Squares method, it figures out the slope and intercept to guess what the temperature will be over the next 24 hours.

I also added some nice-to-have features like retrying failed API calls with exponential backoff (fancy way of saying "wait longer between each retry"), saving data to CSV files in a way that won't corrupt your existing data if something crashes, and making pretty charts with Matplotlib.
You just pick options from a simple text menu , fetch new data, look at saved records, search by date, find the hottest/coldest days, make predictions, or plot graphs. The app saves a cache of API responses for an hour so it doesn't keep hammering the server, and if you lose internet, it'll still show you older cached data instead of just giving up.

Libraries Used
- requests: HTTP API calls
- matplotlib: data visualisation

Installation 
pip install -r requirements.txt

How to Run
Run python main.py, and select ‘fetch data’ first and foremost. After fetching data, all other options can be run in any order.

Example Workflow
1. Select [1] to fetch live weather data (cached for 1 hour)
2. Select [2] to verify data loaded successfully
3. Select [4] to see the hottest and coldest days in the dataset
4. Select [5] to generate a 24-hour temperature forecast
5. Select [6] then [4] to view the full dashboard of all three metrics


Repository
https://github.com/sjv529-tech/EOY_intro_2_prog.git
