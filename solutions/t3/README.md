# AIHackCovid
This is a repository to share the code and results of **Team_3** in AICovidHack 2021.
<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Thanks again! Now go create something AMAZING! :D
-->



<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links-->

## Installation

1. The code is written `Python 3`. So, make sure that you have installed `Python 3` on your system. 
2. Clone the repo

   ```sh
   git clone https://github.com/abst0603/AIHackCovid.git
   ```
3. Change your directory to our directory

   ```sh
   cd AIHackCovid
   ```
4. Install requirements

   ```sh
   pip install -r requirements.txt
   ```


## Run the code
Our code has to main parts and for running each of them you should run different scripts.

### Society-related analysis
For this section we performed a statistical analysis evaluate the impact of society-related characteristics of countries
on the outbreak of COVID-19 using OWID dataset. To run the code:

1. Go to the `CountriesAnalysis` folder

   ```sh
   cd CountriesAnalysis
   ```
2. Open `countries_analysis.ipynb` using Jupyter Notebook.


### Time-series analysis
For this part, we provide a time-series analysis over the OxCGRT dataset using Prophet algorithm. To run the code:   

1. Go to the `country_stats` folder

   ```sh
   cd TimeSeriesPrediction
   ```
2. To see the result and plots for each country, you should run `timeseries_infectionrate_[CountryName].py` using Python 3.
