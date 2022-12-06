# 2Degrees
### Invest in the future.


## Visit the webpage
[Click Here!](http://www.2degrees.info)  

![2Degrees Homepage](https://github.com/johnathan-booy/2Degrees/blob/main/static/images/screenshot-homepage.jpg?raw=true)

## Description

ESG ratings give investors valuable insight into the environmental, social and governance impact of the stocks they choose. Unfortunately, these ratings are not easily accessible for private investors. 2Degrees aims to empower these investors to prioritize ethical business practices in their portfolios by visualizing ESG ratings.

**Users can view ESG ratings for:**  

* Companies
* Sectors
* Countries

![2Degrees Homepage](https://github.com/johnathan-booy/2Degrees/blob/main/static/images/screenshot-list.jpg?raw=true)

**They can explore more detail about specific companies, including:**  

* ESG Ratings
* Information
* Description
* Recent news from Yahoo Finance

![2Degrees Homepage](https://github.com/johnathan-booy/2Degrees/blob/main/static/images/screenshot-company.jpg?raw=true)


**They can create an account and add companies to their list for easy comparison.**  

![2Degrees Homepage](https://github.com/johnathan-booy/2Degrees/blob/main/static/images/screenshot-signup.jpg?raw=true)

## Technology Stack

2Degrees is primarily a python app created with Flask. The frontend is implemented through Jinja and styled with SCSS. The backend uses a Postgres server, and forms are executed with Flask WTF.


## Data

This web application aggregates data from multiple API's. The data is collected and cached daily through the populate.py script.

- [ESG Enterprise API](https://www.esgenterprise.com/esg-enterprise-data-api-services/)
- [Yahoo Finance API](https://syncwith.com/yahoo-finance/yahoo-finance-api)
- [Clearbit Logo API](https://dashboard.clearbit.com/docs#logo-api)


## Future Plans

* Include more companies
* Implement a search feature
* Views for Exchanges, States and Cities
