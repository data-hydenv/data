#Data Transformation Script | JSON -> CSV | Postgres
#by: Patrick McClatchy
#Date: 23.01.2022

#-------------------------------------------------------
#This script gathers the available OpenWeather JSON files in the GitHub directory
#and transforms them to tibbles which are exported to .csv and uploaded to
#the PostrgreSQL hydenv server
#-------------------------------------------------------
#Required packages
library(jsonlite)
library(tidyverse)
library(lubridate)
library(rvest)
library(RPostgres)
#--------------
#GitHub base URL for the OpenWeather JSON files 
url <- "https://github.com/data-hydenv/data/tree/master/extra/weather/data" 

#create vector of all available jsonfile-urls
l<-(url %>%                 
      read_html() %>%
      html_nodes(xpath = '//*[@role="rowheader"]') %>%
      html_nodes('span a') %>%
      html_attr('href') %>%
      sub('blob/', '', .) %>%
      paste0('https://raw.githubusercontent.com', .))

allurls <- l[grepl("json", l)]#make sure there are only json files/ no readmes etc.

#read, extract the historic modeled data from the JSON files and join to a tibble; 

all_hourly <- NULL

for (i in 1:length(allurls)) {
  l<-fromJSON(allurls[i])
  hh <- as_tibble(l$historic$hourly)
  rownames(hh) <- c()
  all_hourly <- bind_rows(all_hourly,hh)
} #this might take a while; take a break

#clean and transform data
modeled_data<-all_hourly %>% 
  mutate(dttm= as.POSIXct(as.numeric(as.character(dt)),origin="1970-01-01", tz="GMT")) %>% #transform to ymd- date format 
  mutate(temp = temp- 273.15, feels_like = feels_like -273.15) %>% #kelvin -> celsius
  select(dttm, temp, feels_like, pressure, humidity, dew_point, clouds, visibility, wind_speed, wind_deg) #select wanted variables

#----------------------------------
#Upload to postgreSQL Server hydenv

#create connection object
con <- dbConnect(drv =Postgres(), 
                 user="hydenv", 
                 password="hydenv",
                 host="localhost", 
                 port=5432, 
                 dbname="hydenv")

dbWriteTable(con, name="modeldata_output", value=modeled_data, overwrite=TRUE) #upload data to postgres server
#-------------

#export to csv
wd<-getwd()
write_csv(modeled_data, paste(wd,"modeled_data.csv", sep = "/"))
