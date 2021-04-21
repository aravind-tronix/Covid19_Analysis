# Covid19_Analysis
## Covid19-tracking-project data visualization
"The COVID Tracking Project collects realtime data for India. It displays statewise and districtwise cases".
This app uses two API's which updates everyday. The data are loaded dynamically from the api.

## Installation

clone the repo and install requirements by  
``pip install -r requirements.txt``

## Usage
Run the app by  
``streamlit run app.py``  
note down the ip address and port its running on and open it in the browser.

## Deploy it on heroku
1. Clone the repo and deploy it to heroku via heroku CLI or deploy the app.
2. commit the repo to your git account, create an app in heroku and use deploy option to sync your github account with heroku and deploy it with a click.

## Live version of the app
This app is runing on heroku **https://app-covid19-analysis.herokuapp.com**

## Data visualization

### DATE VS ACTIVE CASES

![covid-tracking](https://github.com/aravind-tronix/Covid19_Analysis/blob/main/images/Covid1900.PNG)

### DATE VS DEATH RATES

![covid-tracking](https://github.com/aravind-tronix/Covid19_Analysis/blob/main/images/Covid1901.PNG)

### DEATH VS ACTIVE CASES VS RECOVERED

![covid-tracking](https://github.com/aravind-tronix/Covid19_Analysis/blob/main/images/Covid1902.PNG)

### Statewise data
here you can select a particular State to see the death,active,confirmed and recovered cases till date

![covid-tracking](https://github.com/aravind-tronix/Covid19_Analysis/blob/main/images/Covid1903.PNG)

### Districtwise data
here you can select a particular District for selected State to see the death,active,confirmed and recovered cases till date

![covid-tracking](https://github.com/aravind-tronix/Covid19_Analysis/blob/main/images/Covid1903.PNG)

# Reference API
1. Statewise data **https://api.covid19india.org/data.json**
2. Districtwise data **https://api.covid19india.org/state_district_wise.json**

