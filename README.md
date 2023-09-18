# Demand forecasting

So, a couple of months ago, I did a project for a company called [Adminer](https://adminer.pro/) who is a famous platform for _product minning_, specially for _dropshipping_.

The project consisted in forecast the possible demand for products with high amount of sales on the last few days. As it was my first "real-life" project, I can say it was very challenging and I could learn A LOT. So, I decided to share a little about the techniques I developed, however, as I cannot share private data, I'm using a kaggle dataset of product sales in a much smaller sample. Hope you enjoy.

## Overview
Basically, what I'm gonna do is to show 4 models I made: 
* Last day based 
* Moving average
* ARIMA
* Light Gradient Boosting Machine (LGBM)

The first two are just naive models that will serve as bechmarks for our more sofisticated models, being ARIMA and LGBM. 
