import requests
from bs4 import BeautifulSoup

def scrape_etsy_reviews():
    # copy and paste the Etsy URL you want to scrape
    url = "https://www.etsy.com/listing/1463508222/custom-dog-portrait-embroidered?ls=s&ga_order=most_relevant&ga_search_type=all&ga_view_type=gallery&ga_search_query=&ref=sr_gallery-1-23&pro=1&content_source=d1da54c41d38b66043c94189ed074c2753406480%253A1463508222&organic_search_click=1&logging_key=d1da54c41d38b66043c94189ed074c2753406480%3A1463508222"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Referer": "https://www.google.com/"
    }   
    next_page = 0
    response = requests.get(url, headers=headers)
    while response.status_code == 200 and next_page != None:
        soup = BeautifulSoup(response.content, "html.parser")
        
        reviews = soup.find_all("p", class_="wt-text-truncate--multi-line wt-break-word wt-text-body")
        
        # get current page number base on the class: wt-action-group__item wt-btn wt-btn--small wt-pr-xs-2 wt-pl-xs-2 wt-is-selected
        current_page = soup.find("a", class_="wt-action-group__item wt-btn wt-btn--small wt-pr-xs-2 wt-pl-xs-2 wt-is-selected")
        if current_page:
            data_page = current_page.find("span").get_text(strip=True)  # Extract the text from the span inside the current page link
            print("Current Page Number (data-page):", data_page)
        else:
            print("Current page number not found.")
        current_num = int(data_page)+1
        
        # next page: wt-action-group__item wt-btn wt-btn--small wt-btn--icon 
        # next page: && current page number + 1
        next_page = soup.find("a", {"class": "wt-action-group__item wt-btn wt-btn--small wt-btn--icon", "data-page": str(current_num)})
        if(next_page != None):
            url_next = next_page.get("href")
            
        response = requests.get(url_next, headers=headers)
        
        # reviews.txt will be created in the same directory as this script
        for review in reviews:
            with open("reviews.txt", "a", encoding="utf-8") as file:  # Open the file in append mode
                file.write(review.get_text(strip=True) + "\n")  # Write each review to the file
    else:
        print(f"Failed to fetch the page. Status code: {response.status_code}")

if __name__ == "__main__":
    scrape_etsy_reviews()