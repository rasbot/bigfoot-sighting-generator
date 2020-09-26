# Bigfoot Sightings Generator

This project generates bigfoot sightings using a RNN (recurrent neural network). Bigfoot sightings are reported on the website https://www.bfro.net/, the bigfoot field researchers organization. The pipeline for this project is:

* Check all URLs that have reporting IDs and save valid IDs to a text file

* Web scrape all valid URLs, cleaning the HTML code and save each one to a JSON file

* Take all reports and put them into a bag of words, which will be the training data for the RNN

* Generate new sightings, store them in a JSON file, separate them into sections < 240 characters, and tweet them.


This project is based off a case study I did during the Galvanize Data Science bootcamp, which involved analyzing some data from this site.

# Data Analysis

The data web scraped from the site shows trends for how many sightings are reported for each month.

<p align="center">
    <img src="https://raw.githubusercontent.com/rasbot/bigfoot-sighting-generator/master/images/month.png" width="700" height="auto"/>
</p>

<p style="text-align: center;">
Sighting counts for each month of the year.
</p>