#Capstone Proposal
### 2Degrees Investing
**What goal will it achieve?**  
ESG ratings give investors valuable insight into the environmental and social impact of the stocks they choose. Unfortunately, these ratings are not easily accessible for private investors, making it difficult to prioritize ethical business practices in their portfolios. ‘Sustainable Investing’ will aim to visualize ESG ratings, allowing investors to make informed decisions about the companies they support.

**What is the target demographic?**  
Private investors who are looking for insight into the sustainability of organizations to guide investment decisions.

**What data will be involved?**  
The primary resource will be [ESG Enterprise API](https://www.esgenterprise.com/esg-enterprise-data-api-services/), which allows us to query the ESG rating of specific companies.

```
[
	{
		"esg_id": 4720,
		"company_name": "Microsoft Corporation",
		"exchange_symbol": "NASDAQ",
		"stock_symbol": "MSFT",
		"environment_grade": "AA",
		"environment_level": "Excellent",
		"social_grade": "BBB",
		"social_level": "High",
		"governance_grade": "BB",
		"governance_level": "Medium",
		"total_grade": "A",
		"total_level": "High",
		"disclaimer": "ESG Enterprise's ESG Rating data (\"Scores\") are all based on public information and provided for informational purposes only. No member of ESG Enterprise or related parties make any prediction, warranty or representation whatsoever, expressly or impliedly, either as to the suitability of our Scores for any particular purposes or the validity of any derivative analysis or conclusion based on the Scores.",
		"last_processing_date": "27-04-2022",
		"environment_score": 715,
		"social_score": 443,
		"governance_score": 375,
		"total": 1533
	}
]
```

Further company information will be sourced from [Yahoo Finance API](https://syncwith.com/yahoo-finance/yahoo-finance-api).

```
				"assetProfile": {
					"address1": "One Apple Park Way",
					"city": "Cupertino",
					"state": "CA",
					"zip": "95014",
					"country": "United States",
					"phone": "408 996 1010",
					"website": "https://www.apple.com",
					"industry": "Consumer Electronics",
					"sector": "Technology",
```

Company logos will be sourced through [Clearbit Logo API](https://dashboard.clearbit.com/docs#logo-api)




Chart.js
