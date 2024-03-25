import hashlib
import re
import subprocess
import time
# import tkinter as tk
from datetime import datetime, timedelta
# from tkinter import messagebox, simpledialog
from urllib.request import urlopen

import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import logging
debug_logger = logging.getLogger('debug_logger')


def check_spotify_match(email):
    spotify_url = f'https://spclient.wg.spotify.com/signup/public/v1/account?validate=1&email={email}'
    try:
        response = requests.get(spotify_url)
        response_json = response.json()
        # Check if the email is already registered
        if 'errors' in response_json and 'email' in response_json['errors']:
            error_message = response_json['errors']['email']
            return "That email is already registered to an account." in error_message
        else:
            return False
    except requests.RequestException as e:
        # print(f"Error making the request: {e}")
        return False

def check_ebay_match(username):
    ebay_url_template = "https://www.ebay.com/sch/i.html?_fss=1&_saslop=1&_sasl={}&LH_SpecificSeller=1"
    ebay_url = ebay_url_template.format(username)
    try:
        with urlopen(ebay_url) as response:
            html_content = response.read().decode("utf-8")
            if "Invalid seller name" in html_content:
                return False
            else:
                return True
    except Exception as e:
        return False


def check_netflix_match(email):
    netflix_url = "https://www.netflix.com/"

    # Set up the Selenium WebDriver in headless mode
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(options=options)
    try:
        # Find the email input field and enter the email
        driver.get(netflix_url)
        email_input = driver.find_element("name", "email")
        email_input.send_keys(email)

        # Submit the form
        email_input.send_keys(Keys.RETURN)

        # Wait for the page to load
        time.sleep(5)

        # Check if the URL changes to the registration page
        if "https://www.netflix.com/signup/registration?locale=en-US" in driver.current_url:
            return "No"
        else:
            return "Yes"
    except Exception as e:
        # print(f"Error: {e}")
        return "Error"
    finally:
        # Close the browser window
        driver.quit()

def check_disney_plus_match(email):
    disney_plus_url = "https://www.disneyplus.com/identity/sign-up/enter-email"

    # Set up the Selenium WebDriver in headless mode
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(options=options)

    try:
        # Find the email input field and enter the email
        driver.get(disney_plus_url)

        # Add a delay to allow the page to load before attempting to locate the email input field
        time.sleep(5)

        email_input = driver.find_element("name", "email")
        email_input.send_keys(email)
        # Submit the form
        email_input.send_keys(Keys.RETURN)

        # Wait for the page to load
        time.sleep(5)

        # Check if the URL changes to the password creation page
        if "https://www.disneyplus.com/identity/sign-up/create-password" in driver.current_url:
            return "No"
        else:
            return "Yes"
    except Exception as e:
        # print(f"Error: {e}")
        return "Error"
    finally:
        # Close the browser window
        driver.quit()
        

import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys


def check_wordpress_match(email):
    wordpress_url = "https://wordpress.com/log-in/"

    # Set up the Selenium WebDriver in headless mode
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(options=options)

    try:
        # Find the email input field and enter the email
        driver.get(wordpress_url)
        email_input = driver.find_element("name", "usernameOrEmail")
        email_input.send_keys(email)

        # Submit the form
        email_input.send_keys(Keys.RETURN)

        # Wait for the page to load
        time.sleep(5)

        # Check if the URL changes to the link login page
        if "https://wordpress.com/log-in/link" in driver.current_url:
            return "Yes"
        else:
            return "No"
    except Exception as e:
        # print(f"Error: {e}")
        return "Error"
    finally:
        # Close the browser window
        driver.quit()


def check_gravatar_match(email):
    gravatar_url_template = "https://gravatar.com/{}"
    md5_hash = hashlib.md5(email.encode('utf-8')).hexdigest()
    gravatar_url = gravatar_url_template.format(md5_hash)
    try:
        with urlopen(gravatar_url) as response:
            html_content = response.read().decode("utf-8")
            if "There is no profile associated with this email address." in html_content:
                return "No"
            else:
                return "Yes"
    except Exception as e:
        return f"Error: {e}"

def get_disposable_domains():
    url = 'https://gist.githubusercontent.com/Mad182/5591652/raw/434ecff801313f74f24b7fcea5c6c5495816d10c/temporary-email-address-domains'
    try:
        # Fetch the content of the URL
        response = requests.get(url)
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Split the content into lines and store them in a list
            disposable_domains = response.text.splitlines()
            return disposable_domains
        else:
            pass
            # print(f"Error: Unable to fetch content. Status code: {response.status_code}")
    except requests.RequestException as e:
        # print(f"Error: {e}")
        pass
    return None


def is_disposable_email(email):
    domain_match = re.search(r'@(.+)', email)
    domain = domain_match.group(1) if domain_match else ""
    disposable_domains = get_disposable_domains()
    return domain in disposable_domains


def calculate_months_difference(date_str):
    try:
        # Try to parse with time information
        created_date = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%SZ')
    except ValueError:
        # If parsing with time information fails, try without time
        created_date = datetime.strptime(date_str.split("T")[0], '%Y-%m-%d')
    today = datetime.now()
    delta = today - created_date
    months_difference = delta.days // 30
    return months_difference


def get_domain_info(email):
    username, domain = email.split('@')
    try:
        result_nslookup = subprocess.run(['nslookup', '-q=mx', domain], capture_output=True, text=True)
        nslookup_info = result_nslookup.stdout
        result_whois = subprocess.run(['whois', domain], capture_output=True, text=True)
        whois_info = result_whois.stdout
        tld = domain.split('.')[-1]
        created_match = re.search(r'Creation Date: (.+)', whois_info)
        created = created_match.group(1) if created_match else ""
        updated_match = re.search(r'Updated Date: (.+)', whois_info)
        updated = updated_match.group(1) if updated_match else ""
        expires_match = re.search(r'Registry Expiry Date: (.+)', whois_info)
        expires = expires_match.group(1) if expires_match else ""
        registrar_match = re.search(r'Registrar: (.+)', whois_info)
        registrar_name = registrar_match.group(1) if registrar_match else ""
        registered_match = re.search(r'Registry Registrant ID: (.+)', whois_info)
        registered_to = registered_match.group(1) if registered_match else ""
        ebay_match = check_ebay_match(username)
        gravatar_match = check_gravatar_match(email)
        spotify_match = check_spotify_match(email)
        disney_plus_match = check_disney_plus_match(email)
        website_exists = True if "mail exchanger" in nslookup_info.lower() else False
        output = {
            "email": email,
            "deliverable": "Positive" if "mail exchanger" in nslookup_info.lower() else "Negative",
            "domain": domain,
            "tld": tld,
            "registered": "Yes" if "No match for" not in whois_info else "No",
            "created": created,
            "updated": updated,
            "expires": expires,
            "registrar_name": registrar_name,
            "registered_to": registered_to,
            "website_exists": website_exists,
            "ebay_match": "Yes" if ebay_match else "No",
            "spotify_match": "Yes" if spotify_match else "No",
            "gravatar_match": gravatar_match,
            "disney_plus_match": "Yes" if disney_plus_match == "Yes" else "No"
        }
        return output
    except Exception as e:
        return f"Error: {e}"


def calculate_score(domain_info):
    score = 0
    score_breakdown = []
    # Assign points based on conditions
    if domain_info["deliverable"] == "Positive":
        score += 20
        score_breakdown.append("Deliverable: +20")
    else:
        score_breakdown.append("Deliverable: 0")
    if domain_info["tld"] == "com":
        score += 10
        score_breakdown.append("TLD (com): +10")
    else:
        score_breakdown.append("TLD (com): 0")
    if domain_info["website_exists"] == "Yes":
        score += 20
        score_breakdown.append("Website Exists: +20")
    else:
        score_breakdown.append("Website Exists: 0")
    if domain_info["ebay_match"] == "Yes":
        score += 20
        score_breakdown.append("eBay Match: +20")
    else:
        score_breakdown.append("eBay Match: 0")
    if domain_info["gravatar_match"] == "Yes":
        score += 20
        score_breakdown.append("Gravatar Match: +20")
    else:
        score_breakdown.append("Gravatar Match: 0")
    if domain_info["spotify_match"] == "Yes":
        score += 20
        score_breakdown.append("Spotify Match: +20")
    else:
        score_breakdown.append("Spotify Match: 0")
    if domain_info["disney_plus_match"] == "Yes":
        score += 20
        score_breakdown.append("Disney Plus Match: +20")
    else:
        score_breakdown.append("Disney Plus Match: 0")
    # Deduct points if email is found in disposable email list
    if is_disposable_email(domain_info["email"]):
        score -= 250
        score_breakdown.append("Disposable Email: -250")
    else:
        score_breakdown.append("Disposable Email: 0")
    # Calculate months difference from the created date
    created_date = domain_info["created"]
    if created_date:
        months_difference = calculate_months_difference(created_date)
        if months_difference > 6:
            score += 25
            score_breakdown.append("Created Date > 6 Months: +25")
        else:
            score_breakdown.append("Created Date > 6 Months: 0")
    else:
        score_breakdown.append("Created Date > 6 Months: 0")
    return score, score_breakdown


def validate_phone(phone_number):
    api_key = "8066e13669fe42e093ec3f8797296590"
    phone_validation_url = f"https://phonevalidation.abstractapi.com/v1/?api_key={api_key}&phone={phone_number}"

    try:
        response = requests.get(phone_validation_url)
        return response.status_code, response.content
    except requests.RequestException as e:
        return 500, f"Error: {e}"


def main(email_to_analyze, phone_to_validate,advanced_feature):
    try:
        domain_info = get_domain_info(email_to_analyze)
        # print("domain_info",domain_info)
        # print("\nStructured Domain Information:")
        # for key, value in domain_info.items():
            # print(f"{key}: {value}")

        # Calculate and display the score
        score, score_breakdown = calculate_score(domain_info)
        # print(f"\nScore: {score}")

        # Display the extended score breakdown
        # print("\nScore Breakdown:")
        # for item in score_breakdown:
            # print(item)

        # Validate phone number if provided
        if phone_to_validate.strip():
            phone_status, phone_content = validate_phone(phone_to_validate)
            # print(f"\nPhone Validation Status Code: {phone_status}")
            # print(f"Phone Validation Response: {phone_content}")
        else:
            phone_status, phone_content = None, None

        # Check Netflix match
        netflix_result = check_netflix_match(email_to_analyze)
        # print(f"\nNetflix Match: {netflix_result}")

        # Check WordPress match
        wordpress_result = check_wordpress_match(email_to_analyze)
        # print(f"\nWordPress Match: {wordpress_result}")

        # Run advanced features if enabled
        if advanced_feature == "yes":
            # (Advanced feature: Disney Plus match)
            disney_plus_result = check_disney_plus_match(email_to_analyze)
            # print(f"Disney Plus Match: {disney_plus_result}")
        
        return {
            'status':"Success",
            'exception':None,
            'domain_info':domain_info,
            'domain_score':score,
            'domain_score_breakdown':score_breakdown,
            'phone_status':phone_status,
            'phone_content':phone_content,
            'netflix_result':netflix_result,
            'wordpress_result':wordpress_result,
            'advanced_search_result':{'disney_plus_result':disney_plus_result} if advanced_feature=="yes" else None
            }
    except Exception as e:
        # print(e)
        debug_logger.exception(f"Exception occured {e} during processing API request.")
        return {
         'status':"Failed",
         'exception':str(e)   
        }
    

if __name__ == "__main__":
    email_to_analyze = input("Enter an email address to analyze: ")
    phone_to_validate = input("Enter a phone number to validate (press Enter to skip): ")

    # Ask for advanced features input
    advanced_feature = input("Enable advanced features? (yes/no): ").lower()
    res=main(email_to_analyze,phone_to_validate,advanced_feature)
    print(res)