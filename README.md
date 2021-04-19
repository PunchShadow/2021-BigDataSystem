# 2021 NTU Big Data System - Crypto Trading Competition 

## Introduction
This is a strategy script used Crypto Arsenal API.
Crypto Arsenal is a platform that enables traders to share their investing strategies and provides variable functions for trading crpytos.
Crypto Arsenal has user-friendly interface and document for beginners to first step to quantumn trading.
For more details about Crypto Arsenal. Please check out the [platform](https://crypto-arsenal.io/zh-tw/dashboard) or the [Github repo](https://github.com/Crypto-Arsenal/public-docs)

## Strategy Explaination

### Assumption
I assume the market is going to be bullmarket for next few months.
Therefore, we should buy in once the price is lower a certain threshold, and vice versa.
In this competition, it is only allowed to trade with BitCoin and USDT in Binance.

### Strategy
Since I'm going to buy in at a low price, the question is what is called a *lower price* ?
By observing the 15 minutes candlestick, I found that the price will rebound when 15 min's change is lower than -4.5\% and amptitude is larger than 7\%.
Once the condition is achieved, we'll buy in a unit of BTC(The amount is also a variable that can be fined tuned).
Further, when the price is too high, we'll sell some BTCs.
The threshold is change > 11\% and amptitude > 8\%(Since we assume the market is bullmarket, we don't easily sell our BTCs.).


## Strategy Improvement
As I mentioned above, the amount of BTCs bought in and sold out is a big issue to solve. 
Further, The threshold seems too high that stuck the trading during the one month competition.
Therefore, the parameters might be getten by using some machine learning model or some technical indicators.


## Conclusion
It's an interesting competition because it's my first trading strategy using Python code.
Thanks a lot for Prof. Liao and Cryto Arensal for providing such meaningful and interesting activity.
It really influences me a lot and makes me think more about how to invest crpytos.
