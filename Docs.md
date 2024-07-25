# 1. Installation
Download and Install Kafka:

Download the latest version of Kafka from the [Apache Kafka downloads page](https://kafka.apache.org/downloads).
Extract the downloaded file.
<br><br>

# 2. Zookpeeper & Kafka

## - Start Zookeeper:
  Kafka requires Zookeeper to run. You can start Zookeeper by running the following command from the Kafka directory:

  `bin/zookeeper-server-start.bat config/zookeeper.properties`

## - Start Kafka Broker:

  Once Zookeeper is running, start the Kafka broker:

  `bin/kafka-server-start.bat config/server.properties`

---

> ***To establish security using username and password for connecting to the Kafka server, you need to make sure that both the Kafka broker and your producer/consumer are configured correctly for SASL/PLAIN authentication.***

> ***Here is a detailed step-by-step guide to achieve this:***

  ## Step 1: Configure Kafka Broker for SASL/PLAIN Authentication
  
  1. Create JAAS Configuration File:
  
      Create a JAAS configuration file (e.g., kafka_server_jaas.conf) with the following content:
  
      ```
      KafkaServer {
        org.apache.kafka.common.security.plain.PlainLoginModule required
        username="Helois"
        password="Hello1@2"
        user_Helois="Hello1@2";
      };
      ```
  
  2. Configure Kafka Broker Properties:
  
      Edit the server.properties file to include the following properties:
  
      ```
      listeners=SASL_PLAINTEXT://localhost:9092
      advertised.listeners=SASL_PLAINTEXT://localhost:9092
      security.inter.broker.protocol=SASL_PLAINTEXT
      sasl.enabled.mechanisms=PLAIN
      sasl.mechanism.inter.broker.protocol=PLAIN
      allow.everyone.if.no.acl.found=true
      super.users=User:admin
      ```
  
  3. Set the JAAS Configuration Property:
  
      Make sure the JAAS configuration file path is set correctly when starting the Kafka server:
  
      ```
      .\bin\windows\kafka-server-start.bat .\config\server.properties -Djava.security.auth.login.config=path\to\kafka\config\kafka_server_jaas.conf
      ```
  
  ## Step 2: Configure Producer and Consumer
  Ensure your producer & consumer is configured to use SASL/PLAIN authentication.
  
  ## Step 3: Restart Zookeeper and Kafka
  - Set the KAFKA_OPTS Environment Variable:
  
      Open a Command Prompt window and set the KAFKA_OPTS environment variable:
  
      ```
      set KAFKA_OPTS=-Djava.security.auth.login.config=path\to\kafka\config\kafka_server_jaas.conf
      ```
  
  - Restart Zookeeper:
  
    ```
    .\bin\windows\zookeeper-server-start.bat .\config\zookeeper.properties
    ```
  
  - Restart Kafka Server:
  
    ```
    .\bin\windows\kafka-server-start.bat .\config\server.properties
    ```
  
  This should start the Kafka server with the specified JAAS configuration for SASL/PLAIN authentication.
  <br><br>

---
# 3. Create a Topic:

Create a topic named bbc_news_topic to which the producer will send messages:

```
bin/kafka-topics.bat --create --topic bbc_news_topic --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1
```

# 4. Run the Producer and Consumer Scripts:

- Ensure you have Python installed along with the confluent-kafka library. If not, install it using:

  `pip install confluent-kafka`

- Run the Producer Script:
  Save the producer code provided into a file, e.g., producer.py, and run it:

  `python producer.py`

- Run the Consumer Script:
  Save the consumer code provided into a file, e.g., consumer.py, and run it:

  `python consumer.py`

<br>

# OUTPUT :

![image](https://github.com/user-attachments/assets/03a43394-76cf-4ced-bb79-cd30eae6ff69)
