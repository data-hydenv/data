# Weather Data

This sub-module uses the OpenWeatherMap API to collect data. The collection is done via a Python script, that is called via Github Action on a daily basis.
There are two api-calls: first the historc data of the previous day. Second a weather forecast is requested for the next 5 days. The data is saved, as it comes in, into a JSON file.

## License

The data is fromOpenWeather (TM) and licensed under [ODbL license](https://opendatacommons.org/licenses/odbl/)

## And now?

* Check out the data format
* We need a routine to merge data
* we need a routine to create *clean* timeseries

Possible questions to answer:

* how well do the 1-day forecasts perform? 
* is the forecast improving?
* which products are best forecasted and when? 
