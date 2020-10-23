from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv

path = "/Users/macbookpro/Documents/ChromeDriver/chromedriver"
driver = webdriver.Chrome(path)

# Function to scrape informations from movie
def scrape_movie():

    try:
        title = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CLASS_NAME, "title_wrapper"))
        )
        movie_title = title.text

        rating = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CLASS_NAME, "imdbRating"))
        )
        movie_rating = rating.text

        duration = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "//*[@id='title-overview-widget']/div[1]/div[2]/div/div[2]/div[2]/div/time"))
        )
        movie_duration = duration.text

        genre = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "//*[@id='title-overview-widget']/div[1]/div[2]/div/div[2]/div[2]/div/a[1]"))
        )
        movie_genre = genre.text

        summary = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CLASS_NAME, "summary_text"))
        )
        movie_summary = summary.text

        year = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.ID, "titleYear"))
        )
        movie_release = year.text

        credits = WebDriverWait(driver, 30).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "credit_summary_item"))
        )
        director = credits[0].text
        writers = credits[1].text
        stars = credits[2].text

        keywords = WebDriverWait(driver, 30).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "itemprop"))
        )
        keywords_of_movie = []
        for i in keywords:
            keywords_of_movie.append(i.text)

        movie = (movie_title,movie_rating,director,writers,stars,keywords_of_movie,movie_duration,movie_genre,movie_release,movie_summary)
        driver.back()

        return movie

    except:
        driver.quit()


driver.get("https://www.imdb.com/search/title/?groups=top_1000&sort=user_rating,desc&start=0&ref_=adv_nxt")

scraped_movies = []

# Start of every page is increased by 50. So, start of 1st page is 1, 2nd is 51, 3rd is 101,...
start_page = []
start_page.append(0)
number = 1
for i in range(16):
    number += 50
    start_page.append(number)

# page < 19
page = 0
while page < 14:
    for i in range(0,50): #0,50
        try:
            items = WebDriverWait(driver, 30).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "loadlate"))
            )

            items[i].click()
            movie_scraped = scrape_movie()
            scraped_movies.append(movie_scraped)

        except:
            driver.implicitly_wait(5)
    page+=1
    new_link = "https://www.imdb.com/search/title/?groups=top_1000&sort=user_rating,desc&start={}&ref_=adv_nxt".format(start_page[page])
    driver.get(new_link)

with open("imdb_top_800_movies_4.csv", "w", newline='',encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(["Title","Rating","Director","Writers","Stars","Keywords","Movie_Duration","Genre","Release_Year","Description"])
    writer.writerows(scraped_movies)





