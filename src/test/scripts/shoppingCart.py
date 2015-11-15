#!/usr/bin/python
'''
Created on Nov 12, 2015
__author__ = "Rashu"
'''
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import argparse
import sys
import time

def getCleanProductName(productName):
    """Strips the mark tags from the input string if exists

    input : Straight Talk Apple <mark>iPhone</mark> 6 LTE 16GB Prepaid Smartphone
    

    Returns: Straight Talk Apple iPhone 6 LTE 16GB Prepaid Smartphone
    
    """
    
    if '<mark>' in productName: 
        productName=productName.replace('<mark>','',1)
        productName=productName.replace('</mark>','')
        
    return productName
    

def main():
        
    parser = argparse.ArgumentParser(description='shopping cart test.')
    parser.add_argument("chromeDriverPath", help='specify the chrome driver path')

    args = vars(parser.parse_args())

    #Set Up Chrome Driver
    driver=webdriver.Chrome(args['chromeDriverPath'])
    #navigate Walmart.com
    driver.get("http://www.walmart.com")
    driver.maximize_window()
    try:
        WebDriverWait(driver, 10).until(EC.title_is(('Walmart.com: Save money. Live better.')))
    except:
        print 'Title Not found'

    # Sign Up Pop Up window Handling
   
    popUpDialogCloseButton=driver.find_element_by_xpath("//div[contains(@class,'Modal-outer js-responsive-modal-outer')]//button")
    if popUpDialogCloseButton.is_displayed():
        popUpDialogCloseButton.click()
   
    
 
    #Logging into customer account
    myAccountLink = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.LINK_TEXT,"My Account")))
    myAccountLink.click()
    driver.implicitly_wait(10)     
    # Entering the user Login Email Address
    driver.find_element_by_css_selector("input[id='login-username']").send_keys("rashutestuser@gmail.com")
    # Enter the Password
    driver.find_element_by_css_selector("input[id='login-password']").send_keys("abc@abc")
    # Click the Sign In Button
    driver.find_element_by_css_selector("button[class='btn login-sign-in-btn js-login-sign-in btn-block-max-s btn-block-max-s']").click()

    
    #Explicit Wait Until User Name appears with Hello message
    #Validate that the User is logged into correct account
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"span[class='js-account-display-name account-display-name']")))

    #Locate Search Box and type iphone
    searchTextField = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"input[id='search']")))
    searchTextField.send_keys("iphone")

    #Click the Search/ Submit Button
    searchButton=driver.find_element_by_css_selector("button[type='submit']")
    searchButton.click()
    
    #Locate the entire list of search items to appear
    header=WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"div[id='tile-container']")))
    
    allProducts = header.find_elements_by_css_selector("div[class='js-tile js-tile-landscape tile-landscape']")
    #Selecting the first product from the list
    productSelected = allProducts[1]
    productImageLink= productSelected.find_element_by_class_name("js-product-title")
    
    #getting the  name of the product
    productName=productImageLink.get_attribute("innerHTML")
   
    newProductName= getCleanProductName(productName)
    
    #Click the Product Image Link
    productImageLink.click() 
    
    #Handling out of stock Item
    #out of stock
    try:
        outOfStockLabel= WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"p[class='price-oos']")))
        print 'out of stock'
        driver.quit()
    
    except :
       print 'In stock' 

    #User Navigated to the first next page and Handling the zipcode pop up if exists
    try:
        zipcodeTextfield=WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"input[name='zipcode']")))
        #Type the Zipcode in zicode text field
        zipcodeTextfield.send_keys("94087")

        #Locating and clicking the Check Button
        checkButton=WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"button[class='btn btn-mini  js-cell-coverage-check-btn']")))
        checkButton.click()
        #Locating and closing  the zipcode popup
    
        closeButton = driver.find_element_by_xpath("//div[contains(@class,'js-flyout-modal flyout-modal flyout-modal-wide')]//button")
    
        closeButton.click()
    except:
        print 'No zipcode'

    #Selecting a color field if exists.
    try:
        
        colorList=driver.find_element_by_css_selector("div[class='variants variants-swatches js-variants-swatches js-variants-collapsed variants-collapsed']")
        colorChild=colorList.find_elements_by_css_selector("span[class='js-variant-swatch-container variant-swatch-container']")
        colorChild[0].click() #Selecting the first color
    except:
        print ' no color option'
    
    #Locating and closing Zipcode pop up window second time
    try:
        zipcodeTextfield=WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"input[name='zipcode']")))
        zipcodeTextfield.send_keys("94087")

    except:
        print 'no second zipcode pop up'
        
    #Locating and clicking Add to Cart Button
    cartButton= driver.find_element_by_id('WMItemAddToCartBtn')
    cartButton.click()

  
    #Closing the popup window after item added to shopping cart
    closePopUpShoppingCart=WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"button[class='Modal-closeButton hide-content display-block-m js-modal-close']")))
    closePopUpShoppingCart.click()


    #Locating and navigating to Shopping cart
    shoppingCartButton= WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"a[href='https://www.walmart.com/cart/']")))
    shoppingCartButton.click()
    

    cart= WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"h3[class='cart-list-title']")))
    cartItemInfo=WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"a[id='CartItemInfo']")))
    
    #Asserting the values
    assert '1 item.' in cart.get_attribute('innerHTML')
    assert newProductName in cartItemInfo.get_attribute('innerHTML')
    
    removeButton=WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"button[class='btn-fake-link font-semibold m-margin-left js-cart-item-remove']")))
    removeButton.click()
    driver.implicitly_wait(15)

    #close the browser instance
    driver.close()

# Main Method Call
if __name__== '__main__': main()
