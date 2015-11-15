Steps to follow for mac pc and chrome browser only:

[1] brew install python  // to install python on mac

[2] sudo  easy_install pip // to install pip

[3] sudo pip install selenium //to install selenium 

[4] Download chrome Driver - http://chromedriver.storage.googleapis.com/2.20/chromedriver_mac32.zip and unzip the folder and copy and paste the path in the execution step [5]

[5] git clone git@github.com:SeleniumExamples/seleniumShoppingCartExample.git
    [5.a] cd to project directory

[6] To run test use the below command
/usr/bin/python src/test/scripts/shoppingCart.py < path_of_chrome_driver_downloaded_instep_4 >

Notes for the reviewer 
[1] this test is for 'iphone' keyword only
[2] tested for list view only
[3] future enhancement could take care of 'out ot stock' product
[4] In this implementation the script handles zipcode popup and color option, so there is an extra wait before the item is added to the cart.
[5] Also, at the end of the test , I am cleaning up the cart , before quitting the browser.
[6] I  picked  1st product to be added to the cart after the search for 'iphone'
