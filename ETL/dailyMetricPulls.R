# Title     : TODO
# Objective : TODO
# Created by: gkaberere
# Created on: 12/17/18

### Just one time work to install the R pacakges
install.packages(c("googlesheets", "tidyverse", "data.table"))

##############################################################################################################################
####### Pull actual adau, dau, and adi upto previous day using Saptarshi's code  #############################################
##############################################################################################################################
# load package
library(googlesheets)
library(tidyverse)
library(data.table)

BD <- '2017-07-01'
adau.src.url <- "https://sql.telemetry.mozilla.org/api/queries/59728/results.csv?api_key=3x8i4LX9eVR171DfkSck1MxVaalCKDnjEhLJB2pj"
adau <- fread(adau.src.url)[, date := as.Date(as.character(date),"%Y%m%d")]
## See query: https://sql.telemetry.mozilla.org/queries/59575/source for ADI Data (runs once every 24hrs)
adi.src.url <- "Sou?api_key=0M9ISHsK2U8ZrwqHp6EzobHWISRhahlZB94DojZa"
adi <- fread(adi.src.url)[, date := as.Date(date)]
current_data <- merge(adau, adi, by="date",all.y=TRUE) # the global daily data
last_current_date <- max(current_data$date)
last_current_date

## the following is country based adau
#cadau.src.url <- "https://sql.telemetry.mozilla.org/api/queries/59733/results.csv?api_key=5Umuqmdmdk2wO8z23uzo2fCBezrSm0MQxgfWnMD9"
#cadau <- fread(cadau.src.url)[, date := as.Date(as.character(date),"%Y%m%d")] # country level daily data

########################################################################################################################
#### Pull the existing adau, dau, and adi from the google sheet
########################################################################################################################
# get the google sheet
daily_metrics <- gs_title("Daily dau, adau, adi")

# download one of the sheets using gs_read()
existing_data <- gs_read(ss=daily_metrics, ws ="daily")
last_existing_date <- max(existing_data$date)
last_existing_date

if(last_current_date > last_existing_date) {
  # obtain the newly added data (which are beyond the date in the existing data)
  new_added <- current_data %>% filter(date > last_existing_date)
  # append the newly added data to the bottom of the existing data of "daily" tab in the google sheet
  gs_add_row(ss=daily_metrics, ws = "daily", input = new_added)
}
########################################################################################################################
########################################################################################################################
