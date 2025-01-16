Put your processed 10-minute files here.

Those files shoul be conform to those specifications (explained in exercice 2):
-	one header line, without any quotation marks, like “ or ‘
-	observations from line 2 on
-	3 columns with the following names: id, dttm and temp
-	id: consecutive id starting with 1
-	dttm: a string with date and time information in this exact format (YYYY-MM-DD HH:MM) without any other information like “T”, “Z” or “UTC” or other timezone information, 
-   the timezone of the data should be UTC+1 (old: GMT+1)
-	temp: values of air temperature measurements in °C
-	the data resolution should be 3 desimal digits
-	the column separator is a comma (,), the decimal separator is a point (.)
-	one line per observation (an observation is a 10-min value from the time series)
-	Your file will have 6 (timesteps per hour) x 24 (hours) = 144 values per day, if no measurement point the file should have an “NA” written at this observation point
-	Start and End date and time is given during the exercise lecture
-	The name of your file should be “your_hobo_id.csv” (e.g. 10305099.csv)


Here is an example:
| id   | dttm                | temp |
|------|---------------------|------|
| 1    | 2022-11-30 00:00:00 | 5.54 |
| 2    | 2022-11-30 00:10:00 | 5.64 |
| 3    | 2022-11-30 00:20:00 | 5.74 |
| 4    | 2022-11-30 00:30:00 | 5.94 |
| ...  | ...                 |      |
| 6047 | 2023-01-10 23:40:00 | 2.94 |
| 6048 | 2023-01-10 23:50:00 | NA   |
