# NBA Standings Webscraper
## Overview
NBA standings web scraper using Python, functional programming, and concurrency. This webscraper allows the user to input which seasons they would like to see the NBA standings from (at least 1 season). The program will then scrape the url page both sequentially and concurrently (as long as the user inputs more than 1 season because 1 season will only be able to do it sequentially). 

The program retrieves and prints NBA standings for both the Eastern and Western Conferences, including each team's rank, wins, losses, winning percentage, and games behind.

The program runs once sequentially with one worker and then again concurrently with up to four workers. Each run prints the standings and its execution time. The program also calculates the speedup between the two approaches.

## How to Use: 
```
chmod +x nba_scraper.py
./nba_scraper.py
```

The program asks the user which NBA seasons they want to retrieve, so you should enter the season-ending years separated by commas (for example type: 2025, 2026, 2027).

## My Scraper's Performance
### One Worker vs. (Max) Four: 

```
./nba_scraper.py
Enter Seasons: 2024, 2025, 2026
```

In this example it is 1 worker compared to 3.

<img width="464" height="780" alt="Screenshot 2026-11-05 at 3 07 29 PM" src="https://github.com/user-attachments/assets/c7d11744-405c-4907-8582-9ae597a2dbb7" />
<img width="450" height="585" alt="Screenshot 2026-11-05 at 3 07 43 PM" src="https://github.com/user-attachments/assets/db5708ef-3c1b-4c46-a332-92107b61b68c" />
<img width="467" height="575" alt="Screenshot 2026-11-05 at 3 07 55 PM" src="https://github.com/user-attachments/assets/a9c7e9b8-59c3-42cc-abc4-e215540898b8" />

## Performance Impact
### Functional Programming
The scraper uses functional programming techniques such as map(), filter(), and list comprehensions to process NBA standings data.

For example, map() applies the fetch_season() function to each season:
```
results = list(map(fetch_season, seasons))
```
This keeps the code concise and allows the same function to be applied to multiple seasons. 

### Concurrency
The scraper uses concurrent.futures.ThreadPoolExecutor and executor.map() to retrieve standings for multiple NBA seasons concurrently.

The program runs once sequentially with one worker and again with up to four workers. With four workers, multiple HTTP requests can overlap while waiting for ESPN's API to respond, potentially reducing the total execution time.

Both approaches retrieve the same seasons and standings, allowing their execution times to be compared fairly.

The program calculates speedup using:
```
speedup = sequential_time / concurrent_time
```
A speedup greater than 1 means concurrent execution was faster. 
