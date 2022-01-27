import requests
from bs4 import BeautifulSoup
import csv
from itertools import zip_longest

while True:
    username = input("Please enter username in github to extact all his repositories to CSV file: ")
    result = requests.get(f"https://github.com/{username}?tab=repositories")
    if result.status_code != 200:
        print("Invalid username, Please write a correct username")
    else:
        break

soup = BeautifulSoup(result.content, "lxml")

repo_name = []
updated = []
status = []
links = []
stars = []

repo_name_row = soup.find_all("a", {"itemprop":"name codeRepository"})
updated_row = soup.find_all("relative-time")
status_row = soup.find_all("span", {"class":"Label Label--secondary v-align-middle ml-1 mb-1"})

for i in range(len(repo_name_row)):
    text = repo_name_row[i].text
    repo_name.append(text[9:-1])
    updated.append(updated_row[i].text)
    status.append(status_row[i].text)
    links.append("https://github.com"+repo_name_row[i].attrs["href"])

for i,link in enumerate(links):
    result_link = requests.get(link)
    soup_link = BeautifulSoup(result_link.content, "lxml")
    stars_row = soup_link.find("span", {"id":"repo-stars-counter-star"})
    stars.append(stars_row.text)
    print("Done "+str(i+1)+" repositories ...")


file_list = [repo_name, updated, status, stars, links]
exported = zip_longest(*file_list)
with open("/Users/abudr/Documents/courses/web scraping repos github/repos.csv", "w") as myfile:
    wr = csv.writer(myfile)
    wr.writerow(["Repository Name", "Language", "Status","Stars" ,"Link"])
    wr.writerows(exported)

print("*"*40)
print("CSV file was Completed Successflly!")
print("*"*40)
