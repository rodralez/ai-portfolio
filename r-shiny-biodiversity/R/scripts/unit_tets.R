library(dplyr)
library(arrow)

## APPSILON
rm(list = ls())
setwd("/home/rodralez/my/jobs/appsilon/biodiversity-app/")
data <- read_parquet("./data/data.parquet", as_data_frame = TRUE)

source("./R/functions/app_funtions.R")

# Unit test for filter_species()
filter_species_ut(data)
