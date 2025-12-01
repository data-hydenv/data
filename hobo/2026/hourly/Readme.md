Put your processed and fileld hourly timeseries files here.

The files should be in the format explained in exercice 4.

The file must contain three columns:
1.  **dttm**: Date and time in the format "YYYY-MM-DD HH" in UTC+1 (old name GMT+1)
2.  **th** : Temperature** values (in °C)
3.  **origin**: A flag indicating whether the value is from your HOBO station (H) or filled by regression (R)

Column separator should be a comma (`.csv`). 

Here is an example:
| dttm                | th    | origin |
|---------------------|-------|--------|
| 2018.11.30 00:00:00 | 2.388 | R      |
| 2018.11.30 01:00:00 | 2.428 | H      |
| 2018.11.30 02:00:00 | 2.101 | R      |
| 2018.11.30 03:00:00 | 2.275 | H      |
| ...                 | ...   | ...    |
