library(shiny)
library(dplyr)
library(arrow)
library(leaflet)
library(ggplot2)
library(shinydashboard)

# Clean all variables
rm(list = ls())

HOST = "SHINYAPP.IO"
# HOST = "LOCALHOST"

if (HOST == "SHINYAPP.IO") {
  
  # Specify URL where data.parquet is stored
  # url <- "https://www.dropbox.com/scl/fi/5w5rz9orltsxzw5vmg0mn/data.parquet?rlkey=dd8inw32n9jr1njr9p6btfv1d&dl=0"
  # command <- paste("wget", url)
  # system(command)
  # command <- paste("mv data.parquet?rlkey=dd8inw32n9jr1njr9p6btfv1d data.parquet")
  # system(command)
  
  source("app_funtions.R")
  data <- arrow::read_parquet("data.parquet", as_data_frame = T)
  
} else {
  
  setwd("/home/rodralez/my/jobs/appsilon/biodiversity-app/")
  source("./R/functions/app_funtions.R")
  data <- arrow::read_parquet("./data/data.parquet", as_data_frame = T)
}

countries <-unique(data$country) %>% sort()

#===============================================================================
# Define UI for the application
#===============================================================================
header <- dashboardHeader(
  title = "Global Biodiversity Dashboard",
  titleWidth = "150px"
)

header$children[[2]]$children <- tags$a(href='https://www.gbif.org/',
                                        tags$img(src = "https://geobon.org/wp-content/uploads/2018/09/cropped-site-icon-300x300.png", 
                                                 height='45px', width='auto', style = "margin-left: 1px;"))

body <- dashboardBody(
  
  tags$script("
      document.title = 'Global Biodiversity Dashboard';
    "),
  
  tags$script(HTML('$(document).ready(function() {
            $("header").find("nav").append(\'<div class="myClass"> Global Biodiversity Dashboard </div>\');
                                            })')),
  tags$head(
    tags$style(HTML("
    # .content {
    #   background-color: #acacbc;
    # }
    .myClass { 
      font-size: 25px;
      line-height: 50px;
      text-align: left;
      font-family: 'Lato', sans-serif;
      color: #acacbc !important;
      padding: 0 15px;
      overflow: hidden;
      color: white;
    }
    .skin-blue .main-header .logo {
      font-family: 'Lato', sans-serif;
      font-weight: normal;
      background-color: #093c68 !important;
      color: #093c68 !important;
      box-shadow: 0 2px 4px rgba(0, 0, 0, 0.5);
    }
    .skin-blue .main-header .navbar {
      font-family: 'Lato', sans-serif;
      font-weight: normal;
      background-color: #093c68 !important;
      color: #093c68 !important;
      box-shadow: 0 2px 4px rgba(0, 0, 0, 0.5);
    }   
    .box {
      font-family: 'Lato', sans-serif;
      border-radius: 8px;
      box-shadow: 0 4px 6px rgba(0, 0, 0, 0.5);
    }
  "))
  ),
  
  fluidRow(
    column(width = 3,
           
           box(width = NULL, status = "info",
               selectizeInput(
                 inputId = "autocomplete_country",
                 label = "Select a country",
                 choices = NULL,
                 selected = NULL,
                 options = list(placeholder = 'Select a country', multiple = FALSE, dropdownParent = "body")
               ),
           ),
           
           box(width = NULL, status = "info",
               selectizeInput(
                 inputId = "autocomplete_species",
                 label = "Select a species",
                 choices = NULL,
                 selected = NULL,
                 options = list(placeholder = 'Select a species', multiple = FALSE, dropdownParent = "body")
               ),
           ),
           
           box(width = NULL, height = "400px", status = "info",
               plotOutput("eventPlot")
           )
    ),
    
    column(width = 9,
           
           box(width = NULL, solidHeader = TRUE,
               leafletOutput(outputId = "map", width = "100%", height = "627px")
           ),
    )
  )
)

ui <- dashboardPage(
  
  header,
  dashboardSidebar(disable = TRUE),
  body
)
#===============================================================================
# Define server logic
#===============================================================================
server <- function(input, output, session) {
  
  # Update the autocomplete field in the server side
  updateSelectizeInput(session, 'autocomplete_country', 
                       choices = countries, 
                       selected = "Poland",
                       options= list(maxOptions = length(countries)),
                       server = TRUE)
  
  # Update the autocomplete field for species based on the filtered species
  observeEvent(input$autocomplete_country,{
    
    # Subset the dataframe based on the target country
    subset_data <- data[data$country == input$autocomplete_country, ]
    
    # Create a list of elements in scientificName and vernacularName
    scientific_names <- subset_data$scientificName
    vernacular_names <- subset_data$vernacularName
    
    # Combine the two lists into a single list
    species <- c(scientific_names, vernacular_names)    
    
    updateSelectizeInput(session, 
                         'autocomplete_species',
                         choices = species,
                         server = TRUE)
  })
  
  # Plot the map
  output$map <- renderLeaflet({
    leaflet::leaflet() %>%
      leaflet::addTiles() %>%
      leaflet::setView(lng = 52.0692, lat =19.4809, zoom = 5) %>%
      addLegend(colors = c("yellow", "#69a44c", "#faa21b"), 
                labels = c("Fungi", "Plantae", "Animalia"), opacity = 0.65) %>%
      leaflet::addProviderTiles(leaflet::providers$Esri.WorldGrayCanvas, 
                                providerTileOptions(detectRetina = TRUE,
                                                    reuseTiles = TRUE))
  })
  
  # Update the map
  observeEvent(input$autocomplete_species, {
    
    pal <- leaflet::colorFactor(palette = c("yellow", "#69a44c", "#faa21b" ),
                                levels = c("Fungi", "Plantae", "Animalia"),
                                na.color="gray")
    
    species <- filter_species(data, input$autocomplete_country, input$autocomplete_species)    
    
    leaflet::leafletProxy("map", session) %>%
      leaflet::addTiles() %>%
      leaflet::setView(lng = mean(species$lon), lat = mean(species$lat), zoom = 5) %>%
      leaflet::addProviderTiles(leaflet::providers$Esri.WorldGrayCanvas) %>%
      leaflet::clearMarkers() %>% 
      leaflet::addCircleMarkers(data = species, 
                                lng = ~lon , lat = ~lat,  
                                radius = 10, 
                                fillOpacity = 0.5 ,
                                fillColor = ~pal(kingdom),
                                stroke = FALSE)
  })
  # Filter the data based on selected inputs and generate the plot
  output$eventPlot <- renderPlot({
    
    # Require both inputs to be selected
    req(input$autocomplete_country, input$autocomplete_species)  
    
    # Subset the dataframe based on the selected country and species
    subset_data <- data %>% dplyr::filter(country == input$autocomplete_country) %>%
      dplyr::filter(scientificName == input$autocomplete_species | vernacularName == input$autocomplete_species)
    
    # Extract the year from the eventDate column
    subset_data$year <- format(as.Date(subset_data$eventDate), "%Y")
    
    # Calculate the count of events per year
    events_per_year <- table(subset_data$year)
    
    if (length(events_per_year) > 0) {
      ggplot(data = subset_data, aes(x = year)) +
        geom_bar(stat = "count", fill = "deepskyblue3", color = "black") +
        labs(x = "Year", y = "Number of Occurrences",  title = "Occurrences per Year") +
        theme_minimal() +
        theme(axis.text.x = element_text(angle = 45, hjust = 1)) +
        theme(text=element_text(size=14, family="Lato"))
    } else {
      # If events_per_year is empty, display an error message
      plot(0, main = "No events found", xlab = "", ylab = "")
    }
  }, height = 380)
}

# Run the application 
shinyApp(ui = ui, server = server)
