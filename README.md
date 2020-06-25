[![Build Status](https://travis-ci.org/rayomeara/share-commodity-portal.svg?branch=master)](https://travis-ci.org/rayomeara/share-commodity-portal)



A stock exchange portal that allows users to create accounts and buy selected shares
or commodities. Shares can also be sold for in-app credit and this then can be used in
future purchases. Users can also log into the application to look at performance charts
to see how each share/commodity is doing in price.

---
### UX

This is a project idea that ive had great interest in as I have a lot of interest in
finance and the stock market. I've had great interest in how shares or commodities 
would be transacted using an online application and how the prices of said products
would be influenced by these transactions. I also wanted to take a go at trying to
represent the price changes using charts as I have seen many times on financial 
channels like Bloomberg and CNBC.

So this site should be able to handle various scenarios relating to stocks, such as 
purchasing with credit card or online credit, users who want to look at their own 
profiles and make decisions on if this is a good time to sell or users who are just 
logging in to check current market fluxuations.

The website opens into an index page with top links to allow user logins and for new
users to register on the website. Once logged in or registered, the user is brought to
the index page with links to the user porfolio page, current shares/commodity listing
and performance charts. It also shows the user's credit amount, a link to the current
order and the logout link.

The current list of shares/commodites borrows heavily from the example course app. That
is, options in a tabular format with images and brief details. Each option shows the current price and the change from the last price.

The charts allow for a share/commodity lookup and shows the last 5 prices and their 
line chart representation.

Wireframes from the project can be found in the 'wireframes' folder.

https://github.com/rayomeara/share-commodity-portal/tree/master/wireframes

---
### Technologies

HTML5,
CSS3,
Javascript,
Bootstrap 3.4.1,
JQuery 3.4.1,
Python 3,
Django 1.11.17,
Django-Chartjs 2.1.0,
Stripe 1.70.0,
Postgres,
AWS Storage,
Heroku

---
### Features/Design

The application uses a HTML/CSS/Javascript front end to display information
coming from a Python controller class which is connected to a Postgres database.
The python controller is using Django as a means of handling web requests
from the front end.

As described, the current list page shows each of the shares and commodities in a 
tabular form and a user can puchase any from adding an amount in the text box provided
and clicking add. The current order is displayed, giving the user the option to 
purchase, add more items or amend the item quantity. 

Shares can be purchased by either credit card or store credit. If the user selects
the credit card option, the user is brought into a payment page, showing items 
purchased and asking for credit card details. If the user goes with credit, then its
just deducted from their balance with a confirmation. Whichever option is used, a
record of the transaction is stored as part of the share price history which is used
to generate the chart data.

The charts are done user chartjs, a javascript library. The plugin being used in this project is django-chartjs which is a way of configuring a chartjs chart from Django. 
So when the user accesses the charts page, they are given the option to lookup details
on any share/commodity and the request is sent to Django for the data and other 
configuration details. 

---
### Features to do

In relation to the charts, it would be nice to be able to extend the time period on
them to get a longer picture of performance. So ideally, some kind of dynamic time
period option would be needed. Also, it may be interesting to compare different shares
or commodities over a certain time period.

In the listing, currently its only possible to add one share/commodity purchase at a
time. Would be nice to allow for multiple purchases at once. The payment mechanism at present is only set up to use the default credit card number for stripe. Would be nice
to have a full payment system in place to allow for actual transactions.

The main upgrade would need to be the data itself. At the moment, shares and commodities
are coming from the local database. Would be nice to have to actual data coming from the
Dow Jones SE so that current prices and fluxuations could be taken into account. At the
moment, price changes are being mimicked in the system and are not a true reflection on
what actual price changes would be.

---
### Testing

All testing done was manual. This involved checking that the basic CRUD operations
on users. This was important to test as a user cannot be deleted if they have
outstanding purchases in the system. A user may only be deleted if there are no
shares/commodities in their portfolio.Also some basic UI testing to make sure all 
of the links work in the menu bar. 

Testing was done for the purchasing different shares and commodities, checking for empty
fields on purchase and amending. Also checking that the valid data is captured in order
for the credit card purchase can go through. A lot of testing was done for the credit 
balance, allowing for sales and purchases and making sure that credit could only be
used for purchase if there was enough credit to begin with.

Also, tested the chart so that it worked for any share/commodity. Checked that any new
purchases that are made (or sales) are being saved and are being represented on the 
chart. Also, tests are done to ensure that the app does not fall over if no data (or 
less than 5 history records) exist.

---
### Deployment

The site is currently being hosted at:

https://rom-share-commodity-portal.herokuapp.com/

It is deployed to the site via the github repos. The application was initially
created on the heroku site named 'rom-travel-application' with the config 
variables of 'IP' (0,0,0,0), PORT (5000). Settings for AWS_ACCESS_KEY_ID, 
AWS_SECRET_ACCESS_KEY, DATABASE_URL, STRIPE_PUBLISHABLE, STRIPE_SECRET and the
SECRET_KEY are also set up (for security purposes, not defined in this document). 

Static files and images are all being hosted using AWS Storage. To push any static files
to AWS, type:

python3 manage.py collectstatic

The application is linked to the heroku application using the following command:

git remote add heroku https://git.heroku.com/rom-share-commodity-portal.git

To allow the app to be deployed and recognized as a python app by heroku, a 
requirements.txt file is created using:

pip3 freeze --local > requirements.txt

The deployment will fail if this file is not created. To allow the application to 
run on Heroku, a Procfile needs to be created. This is done using:

echo web: python app.py > Procfile

Now the application can be deployed. To push the code from our app to heroku, run:

git push -u heroku master

To ensure that a web process is running by Heroku, run the following:

heroku ps:scale web=1


To run locally, clone the repository using the command:

git clone https://github.com/rayomeara/share-commodity-portal.git