# Load necessary libraries
library(dplyr)
library(arrow)

# Clear workspace
rm(list = ls())

# Set working directory
setwd("~/my/jobs/appsilon/biodiversity-app/")

# Define file paths and URLs
file <- "./rawdata/biodiversity-data.tar.gz"
url <- "https://drive.google.com/u/0/uc?id=1l1ymMg-K_xLriFv1b8MgddH851d6n2sU&export=download&confirm=t&uuid=6a4071f6-2c66-46df-b318-1dfa63c6b43d&at=ALt4Tm30LYXRPVK09RJDhdYYZbXv:1689260633786"

# Download and extract data
download.file(url, file)
untar("./rawdata/biodiversity-data.tar.gz", exdir = "./rawdata/")

# Read the occurrence data in Arrow format
rawdata <- read_csv_arrow(
  "./rawdata/biodiversity-data/occurence.csv",
  as_data_frame = F
)

# Write the rawdata to Parquet format
write_parquet(rawdata, "./data/occurence.parquet")

# Select specific columns from the rawdata
data <- rawdata %>%
  select("scientificName", "kingdom", "vernacularName",
         "longitudeDecimal", "latitudeDecimal", "country", "eventDate") %>%
  rename(lon = longitudeDecimal, lat = latitudeDecimal)

# Filter data from some countries
countries_names <- c("Andorra", "Austria", "Belgium", "Bulgaria",
               "Croatia", "Cyprus", "Czech Republic", "Denmark", "Estonia",
               "Finland", "France", "Georgia", "Germany", "Greece", "Hungary",
               "Iceland", "Ireland", "Italy", "Latvia", "Lithuania", "Luxembourg", 
               "Malta", "Moldova", "Monaco", "Netherlands",  "The Netherlands", 
               "Norway", "Poland", "Portugal", "Romania", "Russia", "Serbia",
               "Slovakia", "Slovenia", "Spain", "Sweden", "Switzerland",
               "Ukraine", "United Kingdom")
data_filtered <- data %>% dplyr::filter(country == countries_names)

# Convert the column to a factor
data_filtered$kingdom <- factor(data_filtered$kingdom)

# Write the selected data to Parquet format
write_parquet(data_filtered, "./data/data.parquet")

# Read the data from the Parquet file
data <- read_parquet("./data/data.parquet", as_data_frame = TRUE)

countries <- unique(data$country) %>% sort() %>% as.data.frame() %>% rename(country = "." )
write_parquet(countries, "./data/countries.parquet")
countries <- read_parquet("./data/countries.parquet", as_data_frame = TRUE)

# Printing the list of countries
print(countries)

# Display the first few rows of the data
head(data)

# Print the structure of the data
str(data)

# Kingdoms
kingdom <- unique(data$kingdom)
kingdom
