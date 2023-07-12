# get shiny serves plus tidyverse packages image
FROM rocker/shiny-verse:latest
# system libraries of general use
RUN apt-get update && apt-get install -y \
    sudo \
    pandoc \
    pandoc-citeproc \
    libcurl4-gnutls-dev \
    libcairo2-dev \
    libxt-dev \
    libssl-dev \
    libssh2-1-dev 
# install R packages required 
# (change it dependeing on the packages you need)
RUN R -e "install.packages('ggplot2', repos='http://cran.rstudio.com/')"
RUN R -e "install.packages('foreach', repos='http://cran.rstudio.com/')"
RUN R -e "install.packages('doParallel', repos='http://cran.rstudio.com/')"
RUN R -e "install.packages('vecsets', repos='http://cran.rstudio.com/')"
RUN R -e "install.packages('shinythemes', repos='http://cran.rstudio.com/')"
RUN R -e "install.packages('shiny.i18n', repos='http://cran.rstudio.com/')"
RUN R -e "install.packages('bslib', repos='http://cran.rstudio.com/')"
#RUN R -e "devtools::install_github('andrewsali/shinycssloaders')"
# copy the app to the image
COPY panini-app /srv/shiny-server/panini-app
# COPY R /srv/shiny-server/R
# COPY data /srv/shiny-server/data
# select port
EXPOSE 3838
# allow permission
RUN sudo chown -R shiny:shiny /srv/shiny-server
# run app
# CMD ["/usr/bin/shiny-server.sh"]
