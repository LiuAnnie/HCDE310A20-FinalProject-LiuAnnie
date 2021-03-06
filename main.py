# This final project builds off of my work in HW5.

from flask import Flask, render_template, request
import urllib.request, urllib.error, urllib.parse, json, logging, random

app = Flask(__name__)

def pretty(obj):
    return json.dumps(obj, sort_keys=True, indent=2)

# Sometimes we need a break.
def takebreak(s):
    print("------------------{}------------------".format(s))

###################################################################
# takebreak("Check if Brand or Product Exist")
# print("Search by brand, product type, and product category")
brandlist = ["almay", "alva", "anna sui", "annabelle", "benefit", "boosh", "burt's bees", "butter london", "c'est moi'", "cargo cosmetics", "china glaze", "clinique", "coastal classic creation", "colourpop", "covergirl", "dalish", "deciem", "dior", "dr. hauschka", "e.l.f.", "essie", "fenty", "glossier", "green people", "iman", "l'oreal", "lotus cosmetics usa", "maia's mineral galaxy", "marcelle", "marienatie", "maybelline", "milani", "mineral fusion", "misa", "mistura", "moov", "nudus", "nyx", "orly", "pacifica", "penny lane organics", "physicians formula", "piggy paint", "pure anada", "rejuva minerals", "revlon", "sally b's skin yummies", "salon perfect", "sante", "sinful colours", "smashbox", "stila", "suncoat", "w3llpeople", "wet n wild", "zorah", "zorah biocosmetiques"]
producttypelist = ["blush", "bronzer", "eyebrow", "eyeliner", "eyeshadow", "foundation", "lip liner", "lipstick", "mascara", "nail polish"]
productcategorylist = ["lipstick", "lip gloss", "liquid", "lip stain", "pencil", "concealer", "contour", "bb cc", "cream", "mineral", "powder", "highlighter", "palette", "gel"]

# Check to see if brand or product exists. If it doesn't exist,
# API returns empty dictionary.

def isbrand(brand):
    if brand in brandlist:
        return True
    else:
        return False

def isproducttype(producttype):
    if producttype in producttypelist:
        return True
    else:
        return False

def isproductcategory(productcategory):
    if productcategory in productcategorylist:
        return True
    else:
        return False

# takebreak('Making the Request URL and Returning Dictionaries')
# print("Search by: brand, product type, product category (subcategory of type), price, and id")
baseurl = "http://makeup-api.herokuapp.com/api/v1/products.json"

# find_brand() returns the given brand's makeup dictionary.
# Parameters:
# brand: makeup brand
def branddict(brand):
    brand = brand.strip().lower()  # brand string must be lowercase
    if isbrand(brand):
        brand = brand.replace(" ", "%20")
        brandrequest = '{}?brand={}'.format(baseurl, brand)
        brandrequeststr = urllib.request.urlopen(brandrequest).read()
        branddata = json.loads(brandrequeststr)
        return branddata
    else:
        return "This brand does not exist in the brand dictionary. Suggestion: Is the brand spelled correctly?".format(brand)

# find_product() returns the product type's makeup dictionary
# Parameters:
# brand : default to None
# producttype : the product type (eg. blush, eyebrow, foundation)
def productdict(producttype, brand = None):
    producttype = producttype.strip().lower()
    if isproducttype(producttype):
        producttype = producttype.replace(" ", "_")
        if brand != None:
            brand = brand.strip().lower()
            if isbrand(brand):
                productrequest = '{}?brand={}&product_type={}'.format(baseurl, brand, producttype)
            else:
                productrequest = '{}?product_type={}'.format(baseurl, producttype)
        else:
            productrequest = '{}?product_type={}'.format(baseurl, producttype)
        productrequeststr = urllib.request.urlopen(productrequest).read()
        productdata = json.loads(productrequeststr)
        return productdata
    else:
        outputstring = "This type does not exist in the product type dictionary. Suggestion: Is the product type spelled correctly?\nHere are the product types you can search by:\n".format(producttype)
        for type in producttypelist:
            outputstring += "\t{}\n".format(type)
        return outputstring

# find_product_category() returns the product category's makeup dictionary
# Parameters:
# brand : default to None
# productcategory : the product category (eg. powder, pencil, palette, highlighter)
def product_category_dict(productcategory, brand = None):
    productcategory = productcategory.strip().lower()
    if isproductcategory(productcategory):
        productcategory = productcategory.replace(" ", "_")
        if brand != None:
            brand = brand.strip().lower()
            if isbrand(brand):
                productrequest = '{}?brand={}&product_category={}'.format(baseurl, brand, productcategory)
            else:
                productrequest = '{}?product_category={}'.format(baseurl, productcategory)
        else:
            productrequest = '{}?product_category={}'.format(baseurl, productcategory)
        productrequeststr = urllib.request.urlopen(productrequest).read()
        productdata = json.loads(productrequeststr)
        return productdata
    else:
        outputstring = "This category does not exist in the product category dictionary. Suggestion: Is the product category spelled correctly?\nHere are the product categories you can search by:\n".format(productcategory)
        for category in productcategorylist:
            outputstring += "\t{}\n".format(category)
        return outputstring

# find_product_price_lt() returns a dictionary of makeup products that are less than
# the given price
# Parameters:
# price : makeup should be less than this price
# brand : default to None
# producttype: default to None
# Note: I recognize there are more possible elif cases I could have presented, but I think
# that the ones I prioritized make the most sense.
def product_price_lt_dict(price, brand = None, producttype = None, productcat = None):
    if price < 0:
        return "Please input a nonnegative price."
    baserequest = '{}?price_less_than={}'.format(baseurl, price)
    if (brand != None) & (producttype != None):
        brand = brand.strip().lower()
        producttype = producttype.strip().lower()
        if isbrand(brand) & isproducttype(producttype):
            productrequest = '{}?brand={}&product_type={}&price_less_than={}'.format(baseurl, brand, producttype, price)
        else:
            print("Something went wrong.\nLooking for {} from {}. There was an issue with the brand and/or product type inputted. Check that both exist in the dictionary.\nNow showing all products under {}.".format(producttype, brand, price))
            productrequest = baserequest
    elif brand != None:
        brand = brand.strip().lower()
        if isbrand(brand):
            productrequest = '{}?brand={}&price_less_than={}'.format(baseurl, brand, price)
        else:
            print("Something went wrong.\nLooking for {}. There was an issue with the brand inputted. Check that brand exists in the dictionary.\nNow showing all products under {}.".format(brand, price))
            productrequest = baserequest
    elif producttype != None:
        producttype = producttype.strip().lower()
        if isproducttype(producttype):
            productrequest = '{}?product_type={}&price_less_than={}'.format(baseurl, producttype, price)
        else:
            print("Something went wrong.\nLooking for {}. There was an issue with the product type inputted. Check that the type exists in the dictionary.\nNow showing all products under {}.".format(producttype, price))
            productrequest = baserequest
    elif productcat != None:
        productcat = productcat.strip().lower()
        if isproductcategory(productcat):
            productrequest = '{}?product_category={}&price_less_than={}'.format(baseurl, productcat, price)
        else:
            print("Something went wrong.\nLooking for {}. There was an issue with the product category inputted. Check that the category exists in the dictionary.\nNow showing all products under {}.".format(producttype, price))
            productrequest = baserequest
    else:
        productrequest = baserequest
    productrequeststr = urllib.request.urlopen(productrequest).read()
    productdata = json.loads(productrequeststr)
    return productdata

# singleproductdict() returns the dictionary for a single product.
# Parameter:
# productid: Each product has an id. This can be found when searching for products.
def singleproductdict(productid):
    base = "http://makeup-api.herokuapp.com/api/v1/products/"
    productrequest = base + str(productid) + ".json"
    productrequeststr = urllib.request.urlopen(productrequest).read()
    productdata = json.loads(productrequeststr)
    return productdata


# Product Class
class Product:
    """A class to represent a makeup product."""
    def __init__(self, dict):
        self.name = dict['name'].strip()
        self.id = dict['id']
        if dict['brand'] != None:
            self.brand = dict['brand'].strip()
        else:
            self.brand = 'No Brand Recorded'
        if dict['price'] != None:
            self.price = dict['price']
        else:
            self.price = 0.0
        self.product_link = dict['product_link']
        if dict['description'] != None:
            self.description = "{}...".format(dict['description'][:350].strip())
        if dict['rating'] != None:
            self.rating = dict['rating']
        else:
            self.rating = 'No Rating Recorded'
        self.image = dict['image_link']
        self.type = dict['product_type'].strip()
        if dict['category'] != None:
            self.category = dict['category']
        else:
            self.category = 'No Category Recorded'
        if dict['website_link'] != None:
            self.website = dict['website_link']
        else:
            self.website = 'No Website Recorded'
        self.tagcount = len(dict['tag_list'])
        tags = ""
        if self.tagcount != 0:
            for i in range(self.tagcount):
                if i == self.tagcount-1:
                    tags += dict['tag_list'][i]
                else:
                    tags += "{}, ".format(dict['tag_list'][i])
        self.tags = tags
        # Product Colors
        if 'product_colors' in dict:
            self.colorcount = len(dict['product_colors'])
            colors = ""
            # hex = []
            for i in range(self.colorcount):
                # hex = hex.append(dict['product_colors'][i]['hex_value'])
                if i == self.colorcount-1:
                    colors += "{}".format(dict['product_colors'][i]['colour_name'])
                elif dict['product_colors'][i]['colour_name'] != None:
                    colors += "{},   ".format(dict['product_colors'][i]['colour_name'])
                else:
                    colors += "This color name is not recorded.   "
            # self.hex = hex
            self.colors = colors
        else:
            self.colorcount = 0
            self.colors = ""

    def __str__(self):
        if (self.rating != None) & (self.colorcount != 0):
            outputstring = "From {} which can be found at {},\n{} (Rated {})  ID: {}\n\tPrice: ${}  Purchase at {}\n\tProduct Type: {}\n\tComes in {} colors: {}\n\tDescription: {}\n\tSee image here: {}".format(self.brand, self.website, self.name, self.rating, self.id, self.price ,self.product_link, self.type,self.colorcount, self.colors,self.description, self.image)
        else:
            outputstring = "From {} which can be found at {},\n{}  ID: {}\n\tPrice: ${}  Purchase at {}\n\tProduct Type: {}\n\tDescription: {}\n\tSee image here: {}".format(self.brand, self.website, self.name, self.id, self.price ,self.product_link, self.type,self.description, self.image)
        return outputstring

# I want users to be able to generate a new makeup routine.
# For this, I will build a dictionary that contains product objects
# from each product type.
def newmakeuproutine():
    searchdict = []
    for type in producttypelist:
        searchresults = productdict(type)
        randomitem = random.choice(searchresults)
        searchdict.append(randomitem)
    products = [Product(item) for item in searchdict]
    return products

@app.route('/')
def main():
    app.logger.info("In MainHandler")
    return render_template('searchform.html', page_title="Makeup Search Form",brandlist=brandlist, producttypelist=producttypelist, productcategorylist=productcategorylist)

@app.route('/newroutine')
def newroutine():
    products = newmakeuproutine()
    price = 0
    for product in products:
        price += float(product.price)
    price = round(price, 2)
    return render_template('routine.html', product= 'A New Routine', products=products, price=price)

@app.route('/gresponse')
def giveresponse():
    product = request.args.get('product')
    product = product.lower()
    # minprice = request.args.get('minprice')
    maxprice = request.args.get('maxprice')
    app.logger.info(product)
    app.logger.info(maxprice)
    if product and maxprice:
        if maxprice.isdigit():
            maxprice = int(maxprice)
            if isproducttype(product):
                requestedproducts = product_price_lt_dict(maxprice, brand=None, producttype=product, productcat=None)
                products = [Product(product) for product in requestedproducts]
                return render_template('searchresponse.html', product="{} Under ${}".format(product,maxprice), products=products)
            elif isbrand(product):
                requestedproducts = product_price_lt_dict(maxprice, brand=product, producttype=None, productcat=None)
                products = [Product(product) for product in requestedproducts]
                return render_template('searchresponse.html', product="{} Under ${}".format(product,maxprice), products=products)
            elif isproductcategory(product):
                requestedproducts = product_price_lt_dict(maxprice, brand= None, producttype=None, productcat=product)
                products = [Product(product) for product in requestedproducts]
                return render_template('searchresponse.html', product="{} Under ${}".format(product,maxprice), products=products)
            else:
                return render_template('searchform.html', page_title="Makeup Search Form - Error", brandlist=brandlist,
                                       producttypelist=producttypelist, productcategorylist=productcategorylist,
                                       prompt="Something went wrong. Did you input a valid brand, product type, or product category?")
        else:
            return render_template('searchform.html', page_title="Makeup Search Form - Error", brandlist=brandlist, producttypelist=producttypelist, productcategorylist=productcategorylist, prompt= "Something went wrong. Did input a number for Maximum Price?")
    elif maxprice:
        if maxprice.isdigit():
            maxprice = int(maxprice)
            requestedproducts = product_price_lt_dict(maxprice)
            products = [Product(product) for product in requestedproducts]
            return render_template('searchresponse.html', product='Products under ${}'.format(maxprice), products=products)
        else:
            return render_template('searchform.html', page_title="Makeup Search Form - Error", brandlist=brandlist,
                                   producttypelist=producttypelist, productcategorylist=productcategorylist,
                                   prompt="Something went wrong. Did input a number for Maximum Price?")
    elif product:  # If the form is filled in, do this.
        if isproducttype(product):
            requestedproducts = productdict(product)
            products = [Product(product) for product in requestedproducts]
            return render_template('searchresponse.html', product=product, products=products)
        elif isbrand(product):
            requestedproducts = branddict(product)
            products = [Product(product) for product in requestedproducts]
            return render_template('searchresponse.html', product=product, products=products)
        elif isproductcategory(product):
            requestedproducts = product_category_dict(product)
            products = [Product(product) for product in requestedproducts]
            return render_template('searchresponse.html', product=product, products=products)
        else:
            return render_template('searchform.html', page_title="Makeup Search Form - Error", brandlist=brandlist, producttypelist=producttypelist, productcategorylist=productcategorylist, prompt= "This isn't a valid search option.")
    else:
        return render_template('searchform.html', page_title="Makeup Search Form - Error", brandlist=brandlist, producttypelist=producttypelist, productcategorylist=productcategorylist, prompt= "Something went wrong. Did you let me know what you wanted to see?")


if __name__ == '__main__':
    app.run(host="localhost", port=4000, debug=True)