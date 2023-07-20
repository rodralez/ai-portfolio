# R Shiny Application - Species Observations Dashboard


## Raw data folder


The Species Observations Dashboard requires the `biodiversity-data.tar.gz` dataset to be available in the `rawdata` folder. To obtain the dataset, you can follow these steps:

```
# Define file paths and URLs
file <- "./rawdata/biodiversity-data.tar.gz"
url <- "https://drive.google.com/u/0/uc?id=1l1ymMg-K_xLriFv1b8MgddH851d6n2sU&export=download&confirm=t&uuid=6a4071f6-2c66-46df-b318-1dfa63c6b43d&at=ALt4Tm30LYXRPVK09RJDhdYYZbXv:1689260633786"

# Download and extract data
download.file(url, file)
untar("./rawdata/biodiversity-data.tar.gz", exdir = "./rawdata/")
```
