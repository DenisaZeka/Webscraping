from selenium import webdriver  # Importing a tool for automating web browser actions.
from bs4 import BeautifulSoup  # Importing a library for parsing HTML and XML documents.
from selenium.common.exceptions import TimeoutException  # Importing an exception raised when a timeout occurs.
import pandas as pd  # Importing a library for data manipulation and analysis.

#Here we have the web scraping of ranking colon of : https://www.timeshighereducation.com/world-university-rankings/2024/world-ranking

# Function to scrape data from a single page
def scrape_page(driver, data):
    """
    Function to scrape data from a single page.

    Parameters:
    - driver: An automated web browser instance.
    - data: A list to store the scraped data.

    This function parses the HTML of the page using BeautifulSoup.
    It finds all universities listed on the page and iterates over each one.
    For each university, it extracts various statistics and appends them to the data list.
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
            # Extract various statistics about the university
            stats_elems = university.find_all('td', class_=lambda x: x and 'stats' in x)
            if len(stats_elems) >= 5:
                students = stats_elems[0].text.strip()
                student_staff_ratio = stats_elems[1].text.strip()
                intl_students_percentage = stats_elems[2].text.strip()
                female_male_ratio = stats_elems[3].text.strip()
                interdisciplinary_research = stats_elems[4].text.strip()
            else:
                students = student_staff_ratio = intl_students_percentage = female_male_ratio = interdisciplinary_research = "N/A"

            # Append the scraped data to the list
            data.append({
                "Rank": rank,
                "Name": name,
                "Location": location,
                "Number of Students": students,
                "Student-Staff Ratio": student_staff_ratio,
                "Percentage of International Students": intl_students_percentage,
                "Female to Male Ratio": female_male_ratio,
                "Percentage of Interdisciplinary Research": interdisciplinary_research,
                "Website": full_url
            })

            # Print the scraped data
            print(f"Rank: {rank}")
            print(f"Name: {name}")
            print(f"Location: {location}")
            print(f"Number of Students: {students}")
            print(f"Student-Staff Ratio: {student_staff_ratio}")
            print(f"Percentage of International Students: {intl_students_percentage}")
            print(f"Female to Male Ratio: {female_male_ratio}")
            print(f"Percentage of Interdisciplinary Research: {interdisciplinary_research}")
            print(f"Website: {full_url}")
            print("-------------------------")

# Function to scrape data from all pages
def scrape_all_pages(url):
    """
    Function to scrape data from all pages.

    Parameters:
    - url: The website address to start scraping from.

    This function initializes a Chrome webdriver and scrapes data from all pages.
    It constructs URLs for each page, loads them, and calls scrape_page function to scrape data from each page.
    After scraping, it saves the collected data into an Excel file.
    """

    # Initialize a Chrome webdriver
    driver = webdriver.Chrome()
    page_number = 1
    data = []

    try:
        total_pages = 107  # Total number of pages to scrape
        while page_number <= total_pages:
            # Load the page with the specified URL and page number
            driver.get(url + f"?page={page_number}#")
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
    df.to_excel("universitiesranking_data.xlsx", index=False)

    print("Data saved to 'universities_data.xlsx'")
    print("Scraping finished.")

# URL of the page to scrape
url = 'https://www.timeshighereducation.com/world-university-rankings/2024/world-ranking'
# Call the scrape_all_pages function to start scraping
scrape_all_pages(url)