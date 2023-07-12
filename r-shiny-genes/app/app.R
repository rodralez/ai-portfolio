library(dplyr)
library(bslib)
library(DT)

# Specify URL where file is stored
# url <- "https://bio-test-data.s3.amazonaws.com/Demo/RShiny/Homo+sapiens.csv"
# # Specify destination where file should be saved
# destfile <- "Homo+sapiens.csv"
# # Download the file
# download.file(url, destfile)
# Read the data from the CSV file
# data <- read.csv("Homo+sapiens.csv", stringsAsFactors = FALSE)

data <- read.csv("../rawdata/Homo+sapiens.csv", stringsAsFactors = FALSE)

# Define the UI
ui <- fluidPage(
  
  # Theme from bslib
  theme = bslib::bs_theme(bootswatch = "cosmo"),
  
  titlePanel("R Dev Exercise by Rodrigo Gonzalez"),
  sidebarLayout(
    sidebarPanel(
      selectizeInput(inputId = "autocomplete_select", 
                   label = "Enter a gene symbol or GO term:",
                   choices = NULL,
                   options = list(placeholder = 'gene symbol or GO term', multiple=TRUE)
      ),
    ),
  
    mainPanel(
      tabsetPanel(
        tabPanel("Gene Info", dataTableOutput("gene_table")),
        tabPanel("GO Term Info", dataTableOutput("go_table"))
      )
    )
  )
)

# Define the server
server <- function(input, output, session) {
  
  # Update the autocomplete field in the server side
  updateSelectizeInput(session, 'autocomplete_select', 
                       choices = c(data$gene_symbol,data$go_term_id), 
                       server = TRUE)
  
  # Define the behavior when a gene symbol or GO term is selected
  observeEvent(input$autocomplete_select, {
    
    selected <- input$autocomplete_select
    
    # Show gene info if a gene symbol is selected
    if (selected %in% data$gene_symbol) {
      
      gene_data <- data %>% filter(gene_symbol == selected)
      
      output$gene_table <- renderDataTable({
        gene_data %>% select(gene_symbol, gene_synonyms, ensembl_transcript_id, go_term_id)
      })
      
      output$go_table <- renderDataTable({})
      
      # Show GO term info if a GO term is selected
    } else if (selected %in% data$go_term_id) {
      
      go_data <- data %>% filter(go_term_id == selected)
      
      gene_data <- data %>% filter(go_term_id == selected) %>% distinct(gene_symbol, .keep_all = TRUE)
      
      output$gene_table <- renderDataTable({
          gene_data %>% select(gene_symbol, gene_synonyms, ensembl_transcript_id, go_term_id)
      })
      
      output$go_table <- renderDataTable({
        go_data %>% select(gene_symbol) %>% distinct()
      })
    }
  })
}

# Run the app
shinyApp(ui = ui, server = server)
