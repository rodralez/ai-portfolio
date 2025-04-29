# Rodrigo Gonzalez's generative AI, data science and machine learning portfolio

## Renting Chatbot: An Intelligent Conversational Agent for Property Management

This project is an intelligent conversational agent designed to automate property management interactions for both homeowners and residents. The system uses a state machine architecture with specialized agents that handle different user flows:

1. **Homeowner Onboarding** - Collects property information and schedules inspections
2. **Resident Matching** - Helps renters find suitable properties and schedule tours

The chatbot architecture includes four primary nodes:
1. **Welcome Agent** - Determines if the user is a homeowner or a resident
2. **Homeowner Agent** - Handles property onboarding for homeowners
3. **Resident Agent** - Facilitates property searching and tours for residents
4. **User Node** - Collects user input and routes to appropriate agent nodes

The system integrates several tools for scheduling meetings, property tours, notifying staff, and finding properties that match resident criteria.

Link to the project: [link](https://github.com/rodralez/ai-portfolio/tree/main/renting-chatbot)

Technologies: LangGraph, LangChain, OpenAI API, Python, JSON, REST API, Conversational AI, State Machine Architecture, Property Management Automation.


## JurisGPT: an AI-powered Summarization System for the Supreme Court Rulings of the Mendoza province, Argentina

The project aims to develop an MVP for a summarization system that utilizes the rulings of the Supreme Court of Justice. Users will have the capability to produce summaries based on the court's jurisprudence. The system employs several technologies such as LangChain, a local LLM Vicuna 7B, and Chroma DB, among others, and will be deployed on the AWS cloud. This comprehensive solution will enable efficient and accurate retrieval of information from the court's rulings, enhancing access to legal knowledge.

One of the main challenges of the project are:

1. Processing documents in Spanish: The LLM models will be assessed based on their ability to process documents in Spanish effectively.
2. Fine-tuning the LLM for Spanish legal vocabulary: A crucial task involves adapting the LLM to accurately handle the specific legal terminology in Spanish.

Link to the project: [link](https://github.com/rodralez/JurisGPT/)

### Useful notebooks

Implementing a simple Retrieval QA system using LLM Vinuca 7B locally in Spanish. [Link](https://github.com/rodralez/JurisGPT/blob/main/code/python/notebooks/babasonicos_retrieval_qa.ipynb) 
 
Technologies: Langchain, Huggingface, LLM, Chroma DB, Vicuna LLM 7B, Text Generation Web UI, LoRA Fine-tuning, Summarization, Retrieval QA, Python, Jupyter notebook.


## Data Science Challenge

In this Data Science Challenge, two task were addressed.

### Task 1 

Understand the data and prepare the pipeline to transform the data from the raw format to the requested form. 

### Task 2 

The goal of this task is to solve business case involving the development of the analytical model using the provided data.

Link to the project: [link](https://github.com/rodralez/ds-portfolio/tree/main/data-science-challenge)

Link to the conclusion presentation: [link](https://docs.google.com/presentation/d/1wrVYiHOGo5-GN8PoxldjUjPLqYsCdPgebQEmQnKhIJM/edit?usp=sharing)

Technologies: Python, Jupyter notebook, Numpy, Pandas, Seaborn, Data Wrangling, Exploratory data analysis, Scikit Learn, Supervised learning, Random forest classifier, Linear regression, glnmet regression, Feature selection, Residual analysis.


<!-- ## Defects detection in metal nuts by using vision IA multi-label object detection

How many images per class are needed to efectively train a YOLOv5 network to detect defects in metal nuts?

Link to the project: [link](https://github.com/rodralez/ds-portfolio/tree/main/metal_nut).

Technologies: Python, Label Studio, YOLOv5, Object detection, Cross validation, Docker. -->


## R Shiny Application for Species Observations in European Countries

This project is a dashboard built using R Shiny that allows users to visualize and analyze species observations on a map. The main goals of this project are:

1. **Visualize Species Observations**: The dashboard provides a map that displays the locations of species observations. The observations are represented as circle markers on the map.

2. **Search Species**: Users can search for species by their vernacular name or scientific name. The dashboard provides an autocomplete field where users can enter the species name and select from the available options.

3. **European Country Dataset**: The dataset used in this project includes observations from several European countries. Data is taken from the Global Biodiversity Information Facility ([https://www.gbif.org/](https://www.gbif.org/)). 

4. **CSS Styling**: The dashboard has been styled using CSS to enhance the visual appeal and improve the user experience.

5. **Deployment**: The application has been deployed to [shinyapps.io](https://www.shinyapps.io/), making it accessible online.

Visit [https://rodralez.shinyapps.io/biodiversity/](https://rodralez.shinyapps.io/biodiversity/) to access the application online.

Link to the project: [link](https://github.com/rodralez/ds-portfolio/tree/main/r-shiny-biodiversity)

Technologies: R, R Shiny, ShinyDashboards, Leaflet maps, CSS, JavaScript, Shinyapps.io.


## R Shiny Application for Gene Symbol and GO Term Search

The R Shiny application efficiently addresses the following tasks:

1. Users can enter a gene symbol or a GO term in the input box.
2. Autocomplete results are displayed as the user types.
3. If a gene symbol is selected, the application shows its corresponding gene symbol, gene synonyms, Ensembl ID, and associated GO terms.
4. If a GO term is selected, the application displays the genes associated with it. For each gene, it shows the gene symbol, gene synonyms, Ensembl ID, and relevant GO terms.

You have two options to run this application:

1. Execute the `app.R` file using RStudio.
2. Visit [https://rodralez.shinyapps.io/gene-app/](https://rodralez.shinyapps.io/gene-app/) to access the application online.

Technologies: R, R Shiny, Shinyapps.io.


## The Panini Collector Problem

A probabilistic framework to solve how many packs have to be purchased to complete a Panini album.

Link to the project: [link](https://github.com/rodralez/ds-portfolio/tree/main/panini)

Technologies: statistics, R, Markdown.


## R Shiny Application to estimate how many packs to complete a Panini album

This is a shiny app based on rocker/shiny-verse. 

Link to the project: [link](https://github.com/rodralez/ds-portfolio/tree/main/r-shiny-panini-app)

Technologies: R, R Shiny, Docker.


##  Data Analysis of admitted students to high schools of the National University of Cuyo for the year 2022

Statistical analysis about the distribution of admitted new students to high schools of the National University of Cuyo (Spanish only).

Link to the project: [link](https://github.com/rodralez/ds-portfolio/tree/main/uncuyo-ingreso)

Technologies: statistics, pdf scraping, R, Markdown.
