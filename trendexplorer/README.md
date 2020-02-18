###getpublicupgrades.py
Gets every CR upgrade of public companies from 2/10/2019 to 2/10/2020 into a CSV along with the current leverage of the company

###getrelevantstockdata.py
For each stock, get price data as csv for the day of the CR upgrade and each day around it. #-1 for insider trading and trends

###graphstockdata.py
Create a graph for each csv from before with the publish time noted

###analyzecrmarketeffect.py
See how CR upgrade influences avg change (at different times after) and avg change over trend (technical?) and avg change over same time previous day 