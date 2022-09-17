library(shiny)
library(foreach)
library(doParallel)
library(ggplot2)
library(tidyverse)
library(vecsets)
library(shinythemes)
library(shiny.i18n)
library(bslib)

i18n <-
  Translator$new(translation_json_path = "./data/translation.json")
i18n$set_translation_language("EN")

source("./R/panini.R", local = TRUE)

# Define UI for app that draws a histogram ----
ui <- fluidPage(
  shiny.i18n::usei18n(i18n),
  
  tags$head(
    tags$meta(name = "author", content = "Rodrigo Gonzalez"),
    tags$meta(name = "url", content = "https://github.com/rodralez/ds-portfolio"),
    tags$meta(name = "creation_date", content = "15/09/2022")
  ),
  
  div(
    style = "float: right;",
    selectInput(
      'selected_language',
      i18n$t("Change language"),
      choices = i18n$get_languages(),
      selected = i18n$get_key_translation()
    )
  ),
  
  # theme = shinytheme("united"),
  theme = bslib::bs_theme(bootswatch = "cosmo"),
  
  # App title ----
  titlePanel(i18n$t("The Panini collector problem")),
  
  h3(
    i18n$t("A web app to estimate how many packs to complete a Panini album")
  ),

  span(i18n$t("by Rodrigo Gonzalez"), style = "font-size: 21px; color: black;"),
  span("(", style = "font-size: 21px; color: black;"),
  tags$a(
    href = "https://github.com/rodralez/ds-portfolio",
    "github.com/rodralez",
    style = "font-size: 21px; color: blue;",
    target = "_blank"
  ),
  span(")", style = "font-size: 21px; color: black;"),
  
  br(),
  
  span(i18n$t("For more information about theory behind this web app, "), 
       style = "font-size: 21px; color: black;"),
  tags$a(
    href = "https://rpubs.com/rodralez/panini",
    i18n$t("please read our report"),
    style = "font-size: 21px; color: blue;",
    target = "_blank"
  ),
  span(".", style = "font-size: 21px; color: black;"),
  
  # Sidebar layout with input and output definitions ----
  sidebarLayout(
    # Sidebar panel for inputs ----
    sidebarPanel(
      numericInput(
        "CS",
        i18n$t("Number of total stickers to collect (max 1000)"),
        638,
        min = 300,
        max = 1000,
      ),
      
      numericInput(
        "US",
        i18n$t("How many different stickers do you already have? (max 1000)"),
        0,
        min = 0,
        max = 1000,
      ),
      
      numericInput(
        "N",
        i18n$t("How many people are you swapping stickers with? (max 15)"),
        0,
        min = 0,
        max = 15
      ),
      
      # numericInput(
      #   "RS",
      #   i18n$t("Number of rare stickers, if any (max 20)"),
      #   0,
      #   min = 0,
      #   max = 20
      # ),
      
      numericInput(
        "PRICE",
        i18n$t("How much a pack of stickers in your country?"),
        1.25,
        min = 0,
        max = 100000
      ),
      
      actionButton("panini_button", label = "Panini!"),
    ),
    
    # Main panel for displaying outputs ----
    mainPanel(
      # Output: Histogram ----
      plotOutput(outputId = "distPlot"),
      h5(textOutput("error_msg"),  style = "color:red"),
      h5(textOutput("pack_mean_str")),
      h5(textOutput("pack_q90_str")),
    )
  )
)

# Define server logic required to draw a histogram ----
server <- function(input, output, session) {
  panini <- reactiveValues(var = NULL)
  load("./data/packs_needed.Rda")
  panini$packs_needed_n <- packs_needed
  
  observeEvent(input$selected_language, {
    # This print is just for demonstration
    # print(paste("Language change!", input$selected_language))
    # Here is where we update language in session
    shiny.i18n::update_lang(session, input$selected_language)
  })
  
  observeEvent(panini$packs_needed_n, {
    panini$packs_m <- round(mean(panini$packs_needed_n))
    q <- quantile(panini$packs_needed_n , probs = seq(0, 1, 0.10))
    panini$packs_q90 <- round(q[10])
  })
  
  output$pack_mean_str <- renderText({
    paste(
      i18n$t("On average, you need to purchase"),
      print(panini$packs_m),
      i18n$t("packs or spend $"),
      format(round(
        as.numeric(input$PRICE * panini$packs_m)
      ), big.mark = i18n$t(",")),
      # print(input$PRICE * panini$packs_m),
      i18n$t(" to complete your Panini album.")
    )
  })
  
  output$pack_q90_str <- renderText({
    paste(
      i18n$t("However, there is a 90% chance that you need at most"),
      print(panini$packs_q90),
      i18n$t("packs or spend $"),
      format(round(
        as.numeric(input$PRICE * panini$packs_q90)
      ), big.mark = i18n$t(",")),
      # print(input$PRICE * panini$packs_q90),
      i18n$t(" to complete your Panini album.")
    )
  })
  
  # ====== Main observer
  observeEvent(input$panini_button, {
    if (req(input$CS, input$US, input$N, input$PRICE)) {
      # Constants
      M <- 5
      MC <- 100
      # a <- input$panini_button
      CS <- input$CS
      US <- input$US
      N <- input$N
      PRICE <- input$PRICE
      
      if (CS > 1000) {
        CS <- 1000
      }
      if (US > 1000) {
        US <- 1000
      }
      if (N > 15) {
        N <- 15
      }
      if (PRICE > 1000000) {
        PRICE <- 1000000
      }
      
      # Setting for paralel computing
      n.cores <- parallel::detectCores() - 1
      my.cluster <- parallel::makeCluster(n.cores, type = "PSOCK")
      # register it to be used by %dopar%
      doParallel::registerDoParallel(cl = my.cluster)
      
      if ((CS - US) > 0 &
          CS > 0  & US >= 0 & N >= 0 & PRICE > 0) {
        # Loop to get distribution
        panini$error_msg <- paste("")
        panini$packs_needed_n <- foreach(
          i = 1:MC,
          .packages = c("vecsets"),
          .combine = 'c'
        ) %dopar% {
          source("./R/panini.R", local = TRUE)
          pcp_swap_mc(CS - US, M, N + 1)
        }
      }
      else{
        panini$error_msg <-
          paste(i18n$t(
            "Please, check the numbers on the left. Something is wrong :-/"
          ))
      }
    }
    else
    {
      panini$error_msg <-
        paste(i18n$t("Some values are missing :-/"))
    }
  })
  
  output$error_msg <- renderText({
    panini$error_msg
  })
  
  output$distPlot <- renderPlot({
    plot_density(panini$packs_needed_n)
  })
}



shinyApp(ui = ui, server = server)