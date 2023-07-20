# R Shiny Application - Species Observations Dashboard

This project is a dashboard built using R Shiny that allows users to visualize and analyze species observations on a map. The main goals of this project are:

1. **Visualize Species Observations**: The dashboard provides a map that displays the locations of species observations. The observations are represented as circle markers on the map.

2. **Search Species**: Users can search for species by their vernacular name or scientific name. The dashboard provides an autocomplete field where users can enter the species name and select from the available options.

3. **Deployment**: The application has been deployed to [shinyapps.io](https://www.shinyapps.io/), making it accessible online.

4. **CSS Styling**: The dashboard has been styled using CSS to enhance the visual appeal and improve the user experience.

5. **European Country Dataset**: The dataset used in this project includes observations from several European countries, not just Poland. Data is taken from the Global Biodiversity Information Facility ([https://www.gbif.org/](https://www.gbif.org/)). 

6. **JavaScript Enhancements**: JavaScript has been utilized to enhance the visualization.

7. **Unit Testing**: Unit tests have been implemented for the `filter_species()` function, ensuring its accuracy and reliability.

## How to Use the Dashboard

1. Select a Country: Use the autocomplete field labeled "Country" to select the desired country. The available options include multiple European countries.

2. Search for a Species: Use the autocomplete field labeled "Species" to search for a species. You can enter either the vernacular name or scientific name of the species.

3. Map Visualization: The map will display the locations of the selected species observations. The observations are represented as circle markers on the map. The color of the markers indicates the species kingdom: yellow for Fungi, green for Plantae, and orange for Animalia.

4. Number of Events per Year: The bar plot titled "Number of Events per Year" displays the count of species observations per year for the selected species and country.

## Deployment

The application has been deployed to [shinyapps.io](https://www.shinyapps.io/). You can access the live version of the dashboard at [https://rodralez.shinyapps.io/biodiversity/](https://rodralez.shinyapps.io/biodiversity/).

## Styling

The dashboard has been styled using CSS to enhance the visual appeal and improve the user experience. The styling includes appropriate colors, font sizes, and layout adjustments to make the dashboard more visually appealing and user-friendly.

## Dataset

The dataset used in this project includes species observations from multiple European countries, providing a broader perspective on species distributions and occurrences. The dataset is dynamically filtered based on the selected country and species, ensuring that the displayed observations are relevant to the user's selection.

## Dataset Preprocessing

The provided `R/scripts/biodiversity_eda.R` script, is used to preprocess the provided `biodiversity-data.tar.gz` database. This script performs exploratory data analysis (EDA) tasks, such as data reducing to prepare the dataset for the species observations dashboard and data analysis.

## JavaScript Enhancements

JavaScript has been utilized to enhance the visualization of the dashboard.

## Unit Testing

Unit tests have been implemented for the `filter_species()` function at `R/scripts/unit_tets.R`. This test ensure the accuracy and reliability of the function by checking its behavior against expected inputs and outputs.
