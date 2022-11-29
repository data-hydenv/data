Put your processed 10-minute files here.

Those files shoul be conform to those specifications (explained in exercice 2):
-	one header line, without any quotation marks, like “ or ‘
-	observations from line 2 on
-	4 columns with the following names: id, dttm, temp and lux
-	id: consecutive id starting with 1
-	dttm: a string with date and time information in this exact format (YYYY-MM-DD HH:MM) without any other information like “T”, “Z” or “UTC” or other timezone information, 
- the timezone of the data should be UTC+1 (old: GMT+1)
-	temp: values of air temperature measurements in °C
-	lux: values of light intensity measurements in lux
-	the data resolution should be the same as in the raw file (e.g. 4 digits)
-	the column separator is a comma (,), the decimal separator is a point (.)
-	one line per observation (an observation is a 10-min value from the time series)
-	Your file will have 6 (timesteps per hour) x 24 (hours) = 144 values per day, if no measurement point the file shoul have an “NA” written at this observation point
-	Start and End date and time is given during the exercise lecture
-	The name of your file should be “your_hobo_id.csv” (e.g. 10305099.csv)


Here is an example:
| id   | dttm                | temp |  lux |
|------|---------------------|------|-----:|
| 1    | 2022-11-30 00:00:00 | 5.54 |    0 |
| 2    | 2022-11-30 00:10:00 | 5.64 |   10 |
| 3    | 2022-11-30 00:20:00 | 5.74 |  100 |
| 4    | 2022-11-30 00:30:00 | 5.94 | 1000 |
| ...  | ...                 |      |      |
| 6047 | 2023-01-10 23:40:00 | 2.94 |    0 |
| 6048 | 2023-01-10 23:50:00 | NA   |   NA |
