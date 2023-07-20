# R Shiny Application - Species Observations Dashboard


## Data folder


The Species Observations Dashboard requires the `data.parquet` dataset to be available in the `data` folder. To obtain the dataset, you can follow these steps:

```
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
```
