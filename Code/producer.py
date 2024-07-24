import requests
from bs4 import BeautifulSoup
import datetime
from confluent_kafka import Producer

# Kafka broker settings
bootstrap_servers = 'localhost:9092'
topic_name = 'bbc_news_topic'
username = 'Helois'
password = 'Hello1@2'

def publish_to_kafka(title, summary, timestamp):
    conf = {'bootstrap.servers': bootstrap_servers,
            'security.protocol': 'SASL_PLAINTEXT',  # Use SASL/PLAIN
            'sasl.mechanism': 'PLAIN',  
            'sasl.username': username,
            'sasl.password': password
            }
    producer = Producer(conf)

    # Produce message to Kafka topic
    producer.produce(topic_name, key=title.encode('utf-8'), value=summary.encode('utf-8'))

    # Flush messages
    producer.flush()

def scrape_bbc_news():
    url = 'https://www.bbc.com/news'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the main section with news articles
    main_section = soup.find('div', {'id': '__next'})
    articles = main_section.find_all('div', class_='sc-f98732b0-2 bNZLNs')

    for article in articles:
        title = article.find('h2', {'data-testid': 'card-headline', 'class': 'sc-4fedabc7-3 dsoipF'}).text.strip()
        summary = article.find('p', {'data-testid': 'card-description', 'class': 'sc-f98732b0-0 iQbkqW'}).text.strip()
        timestamp = datetime.datetime.now().isoformat()

        # Publish to Kafka
        publish_to_kafka(title, summary, timestamp)
        print(f"Published to Kafka: Title={title}, Summary={summary}, Timestamp={timestamp}")

if __name__ == '__main__':
    try:
        scrape_bbc_news()
    except KeyboardInterrupt:
        print("Producer script interrupted. Exiting...")
