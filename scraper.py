import requests
import json
import time
from concurrent.futures import ThreadPoolExecutor

def fetch_page(i):
    url_json = f"https://bff-service.rtbf.be/oaos/v1.5/pages/en-continu?_page={i}&_limit=100"
    response = requests.get(url_json)
    articles_data = []
    
    if response.status_code == 200:
        page_json = response.text
        articles = json.loads(page_json)["data"]["articles"]
        for article in articles:
            article_data = {
                "type": article.get("type"),
                "title": article.get("title"),
                "summary": article.get("summary"),
                "topic": article.get("dossierLabel"),
                "publishedFrom": article.get("publishedFrom"),
                "majorUpdatedAt": article.get("majorUpdatedAt"),
                "readingTime": article.get("readingTime"),
                "dossierLabel": article.get("dossierLabel"),
                "url": "https://www.rtbf.be/article/" + article["slug"] + "-" + str(article["id"]),
                "redactedByTeamRedactionInfo": article.get("redactedByTeamRedactionInfo"),
            }
            articles_data.append(article_data)
    else:
        print(f"Failed to fetch page {i}: {response.status_code}")
    
    return articles_data

def get_articles(total_pages):
    all_articles_data = []
    
    with ThreadPoolExecutor(max_workers=10) as executor:
        results = executor.map(fetch_page, range(1, total_pages + 1))
        
        for result in results:
            all_articles_data.extend(result)
    
    return all_articles_data

start_time = time.time()

articles = get_articles(100)

end_time = time.time()

with open("articles.json", "w", encoding='utf-8') as f:
    json.dump(articles, f, ensure_ascii=False, indent=4)

execution_time = end_time - start_time
print(f"Fetched {len(articles)} articles in {execution_time:.2f} seconds.")