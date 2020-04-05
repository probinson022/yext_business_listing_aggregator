from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager


file = "lead_data.csv"
df = pd.read_csv(file)

results = pd.DataFrame(columns = ['Company Name', "Listing Inaccuracy", 'Reviews Rating'])


for index, row in df.iterrows():

    # intializes chrome webdriver and returns webpage
    link = "https://www.yext.com/partner/seobandwagon/diagnostic.html"
    driver = webdriver.Chrome("C:/Users/enaidsnave/.wdm/drivers/chromedriver/80.0.3987.106/win32/chromedriver.exe")
    driver.get(link)



    # field info for company name, phone, and address
    company_name = row['Company Name']
    company_phone = row['Phone Number']
    company_street_address = row['Street Address']
    company_city = row['City']
    company_state = row['State/Region']
    company_zip = row['Postal Code']

    # locates html field elements
    company_name_element = driver.find_element_by_id('scan-name')
    company_phone_element = driver.find_element_by_id('scan-phone-fullLine')
    company_street_address_element = driver.find_element_by_id('scan-address')
    company_city_element = driver.find_element_by_id('scan-city')
    company_state_element = driver.find_element_by_id('scan-state')
    company_zip_element = driver.find_element_by_id('scan-zip')

    # enters company info into field on webpage
    company_name_element.send_keys(company_name)
    company_phone_element.send_keys(company_phone)
    company_street_address_element.send_keys(company_street_address)
    company_city_element.send_keys(company_city)
    company_state_element.send_keys(company_state)
    company_zip_element.send_keys(company_zip)

    # submits request
    submit_button = driver.find_element_by_id("scan-submit")
    submit_button.click()

    # locate results

    try:
        listing_inaccuracy = driver.find_element_by_class_name("js-error-rate-percentage").text
    except NoSuchElementException as error:
        listing_inaccuracy = "-"
    try:
        review_rating = driver.find_element_by_class_name("js-reviews-rate-percentage").text.replace("%", "")
    except NoSuchElementException as error:
        review_rating = "-"

    new_row = pd.Series([df["Company Name"][index], listing_inaccuracy, review_rating])
    row_df = pd.DataFrame([new_row])
    results = pd.concat([row_df, results], ignore_index=True)

    driver.quit()
    print("{:.2%}".format((index+1)/len(df["Contact ID"])))
    results.to_csv(r'C:\Users\enaidsnave\Desktop\Programming\Python3\Company_Leads\company_results.csv', index=False)

