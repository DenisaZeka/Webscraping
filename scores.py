import pandas as pd  # A library for data manipulation and analysis.
from selenium import webdriver  # A tool for automating web browser actions.
from bs4 import BeautifulSoup  # A library for parsing HTML and XML documents.
from selenium.common.exceptions import TimeoutException  # An exception raised when a timeout occurs.

#Here we have the web scraping of scores colon of : https://www.timeshighereducation.com/world-university-rankings/2024/world-ranking

def scrape_page(driver, data):
    """
    Function to scrape data from a single page.

    Parameters:
    - driver: An automated web browser instance.
    - data: A list to store the scraped data.

    This function goes through a web page and collects information about universities listed there.
    It then adds this information to a list, which will later be used to create a table or spreadsheet.
    """

    # Parse the HTML of the page using BeautifulSoup
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    # Find all universities listed on the page
    universities = soup.find_all('tr')

    # Iterate over each university
    for university in universities:
        # Extract rank of the university
        rank_elem = university.find('td', class_='rank')
        if rank_elem:
            rank = rank_elem.text.strip()
        else:
            rank = "N/A"

        # Extract name and URL of the university
        name_elem = university.find('a', class_='ranking-institution-title')
        if name_elem:
            name = name_elem.text.strip()
            url = name_elem['href']
            full_url = f"https://www.timeshighereducation.com{url}"
        else:
            name = "N/A"
            full_url = "N/A"

        # Extract location of the university
        location_elem = university.find('div', class_='location')
        if location_elem:
            location = location_elem.text.strip().replace('\n', ' ')
        else:
            location = "N/A"

        # Check if the location is Spain
        if "Spain" in location:
            # Extract various scores of the university
            overall_score_elem = university.find('td', class_='scores overall-score')
            teaching_score_elem = university.find('td', class_='scores teaching-score')
            research_score_elem = university.find('td', class_='scores research-score')
            citations_score_elem = university.find('td', class_='scores citations-score')
            industry_income_score_elem = university.find('td', class_='scores industry_income-score')
            international_outlook_score_elem = university.find('td', class_='scores international_outlook-score')

            # Extract scores or set to "N/A" if not found
            overall_score = overall_score_elem.text.strip() if overall_score_elem else "N/A"
            teaching_score = teaching_score_elem.text.strip() if teaching_score_elem else "N/A"
            research_score = research_score_elem.text.strip() if research_score_elem else "N/A"
            citations_score = citations_score_elem.text.strip() if citations_score_elem else "N/A"
            industry_income_score = industry_income_score_elem.text.strip() if industry_income_score_elem else "N/A"
            international_outlook_score = international_outlook_score_elem.text.strip() if international_outlook_score_elem else "N/A"

            # Append the scraped data to the list
            data.append({
                "Rank": rank,
                "Name": name,
                "Location": location,
                "Overall Score": overall_score,
                "Teaching Score": teaching_score,
                "Research Environment Score": research_score,
                "Research Quality Score": citations_score,
                "Industry Score": industry_income_score,
                "International Outlook Score": international_outlook_score,
                "Website": full_url
            })

            # Print the scraped data
            print(f"Rank: {rank}")
            print(f"Name: {name}")
            print(f"Location: {location}")
            print(f"Overall Score: {overall_score}")
            print(f"Teaching Score: {teaching_score}")
            print(f"Research Environment Score: {research_score}")
            print(f"Research Quality Score: {citations_score}")
            print(f"Industry Score: {industry_income_score}")
            print(f"International Outlook Score: {international_outlook_score}")
            print(f"Website: {full_url}")
            print("-------------------------")

def scrape_all_pages(url):
    """
    Function to scrape data from all pages.

    Parameters:
    - url: The website address to start scraping from.

    This function starts at the provided website address and goes through all its pages.
    It collects data about universities from each page and stores it.
    After scraping all pages, it saves the collected data into a file for future use.
    """

    # Initialize a Chrome webdriver
    driver = webdriver.Chrome()
    page_number = 1
    data = []

    try:
        total_pages = 107  # Total number of pages to scrape
        while page_number <= total_pages:
            # Construct URL for the current page
            page_url = f"{url}?page={page_number}#!/length/25/sort_by/rank/sort_order/asc/cols/scores"
            # Load the page with the constructed URL
            driver.get(page_url)
            # Call scrape_page function to scrape data from the current page
            scrape_page(driver, data)
            page_number += 1
    except TimeoutException:
        print("Scraping finished.")
    finally:
        # Quit the webdriver after scraping
        driver.quit()

    # Convert the scraped data into a DataFrame
    df = pd.DataFrame(data)
    # Save the DataFrame to an Excel file
    df.to_excel("uniscores_data.xlsx", index=False)

    print("Data saved to 'uniscores_data.xlsx'")
    print("Scraping finished.")

# URL of the page to scrape
url = 'https://www.timeshighereducation.com/world-university-rankings/2024/world-ranking'
# Call the function to start scraping
scrape_all_pages(url)
