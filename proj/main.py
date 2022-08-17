from selenium import webdriver
from selenium.webdriver.common.by import By
import mysql.connector
import time

start_time = time.time()

path = '/home/rittes/Área de Trabalho/Docs/Cursos/selenium/file/chromedriver'
options = webdriver.ChromeOptions()
options.add_argument("--headless")

connector = mysql.connector.connect(
    host = "localhost",
    user='root',
    password='12345',
    database = 'db_movies_comments'
)

cursor = connector.cursor()
command = 'SELECT * FROM id_movies'
cursor.execute(command)
movies = cursor.fetchall()

cmd = 'SELECT * FROM comments'
cursor.execute(cmd)
commts = cursor.fetchall()
ids = 0

for movie in movies:
    url = f"https://www.adorocinema.com/filmes/filme-{str(movie[1])}/criticas/espectadores/?page="
    for page in range(11):
        try:
            driver = webdriver.Chrome(path, options=options)
            driver.get(f"{url}{str(page)}")

            comments = driver.find_elements(By.CSS_SELECTOR,".content-txt.review-card-content")
            stars = driver.find_elements(By.CSS_SELECTOR,".stareval-note")
            
            
            for commentary in range(len(comments)):
                star = str(stars[commentary].text.replace(',',"."))
                txt = str(comments[commentary].text.replace('"',"'"))
                command = f'INSERT INTO comments (commentary, rating ,movie) VALUES ("{txt}", {float(star)}, {movie[0]})'
                cursor.execute(command)
                connector.commit()
            driver.quit()
        finally:
            driver.quit()
cursor.close()
connector.close()

end_time = time.time()
print(end_time-start_time)