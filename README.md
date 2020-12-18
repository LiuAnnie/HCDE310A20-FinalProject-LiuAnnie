# HCDE 310 Final Project
This is my final project for HCDE 310. I created a Flask app that accesses the Makeup API
and accepts user input to search for relevant products.

See the Makeup API Documentation [here](http://makeup-api.herokuapp.com/).

# Makeup Search
Upon launching the application, the user is directed to the search form page. On this page,
users can search for makeup products by filling out the form. There are two text boxes
that the user can fill out. 

1. What brand, product type, or product category?
2. Maximum Price of Product

The makeup search will take into consideration both answer responses, however, it only needs
a response from at least one of the two questions to execute a search. There is a table below
the form that displays what brands, product types, or product categories the user can search by.

The output is a page with a list of product descriptions that match the search. These descriptions
contain the product's name, id, price, product type, color options, description, tags, and image.
Users can access the link to purchase the product from clicking on the product's image or clicking
the purchase link.

# Generate a New Makeup Routine
Users that are interested in purchasing an entirely new makeup routine can click the given link
below the form to generate a new routine. This will output a page that lists one product from each
product type. At the top of the page, users can see how much this new routine will cost them.
