#' Filter species based on country and species name
#'
#' This function filters a dataset based on the specified country and species name.
#'
#' @param data The input dataset containing species data
#' @param autocomplete_country The country to filter by
#' @param autocomplete_species The species name to filter by
#'
#' @return A filtered dataset containing species that match the specified country and species name
#' @export
filter_species <- function(data, autocomplete_country, autocomplete_species) {
  filtered_data <- data %>%
    dplyr::filter(country == autocomplete_country) %>%
    dplyr::filter(scientificName == autocomplete_species | vernacularName == autocomplete_species)
  
  return(filtered_data)
}

#' Unit test for the filter_species() function
#'
#' This function filters a dataset based on the specified country and species name.
#'
#' @param data The input dataset containing species data
#'
#' @return A filtered dataset containing species that match the specified country and species name
#' @export
filter_species_ut <- function(data) {

  print(paste("Testing filter_species()..."))
  
  # Get unique values for country, scientificName, and vernacularName
  unique_countries <- unique(data$country) %>% sort()
  
  # Initialize a variable to track test results
  all_tests_pass <- TRUE
  
  # Perform the unit test for each combination of values
  for (country in unique_countries) {
    
    # Subset the dataframe based on the target country
    subset_data <- data[data$country == country, ]
    
    # Create a list of elements in scientificName and vernacularName
    scientific_names <- subset_data$scientificName
    vernacular_names <- subset_data$vernacularName
    
    # Combine the two lists into a single list
    unique_species <- c(scientific_names, vernacular_names) %>% unique() %>% sort()
    
    for (species in unique_species) {
      
      filtered_data <- filter_species(data, country, species)
      
      # Subset the dataframe based on the target country
      subset_data <- data[data$country == country, ]
      
      expected_result <- subset_data %>% 
        dplyr::filter(scientificName == species | vernacularName == species)

      # Check if the filtered data matches the expected result
      if (!identical(filtered_data, expected_result)) {
        all_tests_pass <- FALSE
        print(paste("Test for country:", country, "and species:", species, "FAILED"))
      }else{
        print(paste("Test for country:", country, "and species:", species, "PASS"))
      }
    }
  }
  
  # Print final test result
  if (all_tests_pass) {
    print("All unit tests passed!")
  } else {
    print("Some unit tests failed!")
  }
}


