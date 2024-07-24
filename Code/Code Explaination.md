# Producer.py

> ## Purpose
  This script scrapes news headlines from the BBC website and sends them to a Kafka topic for real-time processing.
  <br><br>

> ## Breakdown

  1. Import Libraries
      - `requests` : Used to make a request to the BBC website to get the web page content.
      - `BeautifulSoup` : Helps to parse and extract data from the HTML content of the web page.
      - `datetime` : Used to get the current date and time.
      - `Producer` from confluent_kafka : Used to send messages to a Kafka topic.
  <br>

  2. Kafka Settings

      - `bootstrap_servers` : The address of the Kafka server. In this case, it’s set to localhost:9092, which means Kafka is running on the same computer on port 9092.
      - `topic_name` : The name of the Kafka topic where the news data will be sent.
      - `username` and `password` : Credentials for Kafka authentication.
  <br>

  3. Function: \`publish_to_kafka(title, summary, timestamp)\`

      - This function sends the news data to the Kafka topic.
      - *__Configuration__* : Sets up the Kafka producer with the server address and security settings.
      - *__Produce Message__* : Sends the news headline (title) as the key and the news summary (summary) as the value to the Kafka topic.
      - *__Flush Messages__* : Ensures all messages are sent to Kafka before ending the script.
  <br>
        
  4. Function: scrape_bbc_news()

      - *__Request Data__* : Makes a request to the BBC News website to fetch the web page content.
      - *__Parse HTML__* : Uses BeautifulSoup to read and parse the HTML content of the page.
      - *__Find Articles__* : Looks for the section containing news articles and extracts each article's details.
        - __Title__ : Gets the headline of the news article.
        - __Summary__ : Gets a brief summary of the news article.
        - __Timestamp__ : Records the current time when the article was scraped.
      - *__Publish to Kafka__* : Sends the news headline, summary, and timestamp to the Kafka topic.
  <br>

  5. Main Execution

  - When the script runs, it calls the scrape_bbc_news() function to start scraping and publishing news.
  - *__Exception Handling__* : If the script is interrupted (e.g., by pressing Ctrl+C), it will print a message and exit gracefully.
  <br>
    
> ## Summary
This script automates the process of fetching the latest news headlines from BBC, processing them, and sending them to a Kafka topic.


---


# Consumer.py

> ## Purpose
  \`bbc_c.py\` is a Kafka consumer script that connects to a Kafka broker to receive and process news articles from the bbc_news_topic. It retrieves messages published by the producer script, which contains news headlines and summaries scraped from the BBC News website. The consumer script then prints these messages to the console.
  <br><br>

> ## Breakdown
  1. Imports

      ```
      from confluent_kafka import Consumer, KafkaException
      import sys
      ```
      
      - `confluent_kafka` : This is a Python library for working with Kafka. It includes classes for creating Kafka consumers and producers.
      - `sys` : This module provides access to system-specific parameters and functions. Although not used directly in this script, it's often included for potential system interactions.
<br>

  2. Kafka Broker Settings

      ```
      bootstrap_servers = 'localhost:9092'
      topic_name = 'bbc_news_topic'
      group_id = 'my_group'
      username = 'Helois'
      password = 'Hello1@2'
      ```
      
      - `bootstrap_servers` : Specifies the address of the Kafka broker. It’s set to localhost:9092, meaning it’s running on your local machine on port 9092.
      - `topic_name` : The Kafka topic to which the consumer subscribes. Here it’s bbc_news_topic, which is the topic where the producer publishes news articles.
      - `group_id` : A unique identifier for the consumer group. This helps Kafka manage the offset of messages consumed across different instances of consumers.
      - `username` and `password` : These are used for authenticating with the Kafka broker.
<br>

  3. Function to Consume Messages

     ```
     def consume_from_kafka():
      conf = {
          'bootstrap.servers': bootstrap_servers,
          'group.id': group_id,
          'auto.offset.reset': 'earliest',
          'security.protocol': 'SASL_PLAINTEXT',  # Use SASL/PLAIN
          'sasl.mechanism': 'PLAIN',
          'sasl.username': username,
          'sasl.password': password
      }
     ```
     
      - `conf` : A dictionary containing configuration settings for the Kafka consumer:
          - `bootstrap.servers` : Address of the Kafka broker.
          - `group.id` : The ID for the consumer group.
          - `auto.offset.reset` : Determines where to start reading messages if no previous offset exists. 'earliest' means starting from the oldest available message.
          - `security.protocol` : Specifies the security protocol to use. 'SASL_PLAINTEXT' indicates a plain text protocol with SASL for authentication.
          - `sasl.mechanism` : Specifies the SASL mechanism for authentication, which is PLAIN in this case.
          - `sasl.username` and `sasl.password` : Credentials for authentication.

            <br>
      ---
      ```
      consumer = Consumer(conf)
      consumer.subscribe([topic_name])
      ```
      
      - `consumer = Consumer(conf)` : Creates a Kafka consumer instance using the provided configuration.
      - `consumer.subscribe([topic_name])` : Subscribes the consumer to the bbc_news_topic to start receiving messages from this topic.
<br>

  4. Message Consumption Loop

     ```
     try:
       while True:
         msg = consumer.poll(1.0)
     ```
     
     - `while True` : An infinite loop that keeps the consumer running to continuously listen for new messages.

     ---
     ```
     if msg is None:
       continue
     if msg.error():
       if msg.error().code() == KafkaException._PARTITION_EOF:
         continue
       else:
         print(msg.error())
         break
     ```

     - `msg = consumer.poll(1.0)` : Polls the Kafka broker for messages. The 1.0 specifies a timeout of 1 second.
     - `if msg is None` : If no message is received, the loop continues to the next iteration.
     - `if msg.error()` : Checks if there is an error with the received message:
        - `KafkaException._PARTITION_EOF` : Indicates that the end of a partition has been reached. It’s normal and just means there are no more messages at that moment.
        - `print(msg.error())` : Prints any other errors encountered.
        - `break` : Exits the loop if there’s an error other than the end of the partition.

         <br>
     ---
     ```
             print(f"Received message: {msg.value().decode('utf-8')}")
     ```

     - *` print(f"Received message: {msg.value().decode('utf-8')}") `* : Prints the content of the received message. The message payload is decoded from bytes to a UTF-8 string for readability.
<br>

  5. Handling Interrupts and Cleanup

     ```
      except KeyboardInterrupt:
        print("Consumer script interrupted. Exiting...")
      finally:
        consumer.close()
      ```
     
      - `except KeyboardInterrupt` : Catches interruptions (such as pressing Ctrl+C) and prints a message indicating that the script was interrupted.
      - `finally` : Ensures that the consumer is closed properly to release any resources, even if an error occurs or the script is interrupted.
<br>

  6. Main Entry Point

     ```
     if __name__ == '__main__':
       consume_from_kafka()
     ```

     - ` if __name__ == '__main__' ` : Checks if the script is being executed directly (not imported as a module).
     If it is, it calls the consume_from_kafka() function to start the message consumption process.
<br>
     
    
> ## Summary
In summary, consumer.py is a Kafka consumer script that connects to a Kafka broker to listen for and print messages from the bbc_news_topic. 
It handles real-time message retrieval, manages connection errors, and ensures proper cleanup on exit. 
This script is intended to receive and display news articles published by the producer script.
