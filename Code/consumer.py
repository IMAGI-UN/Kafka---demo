from confluent_kafka import Consumer, KafkaException
import sys

# Kafka broker settings
bootstrap_servers = 'localhost:9092'
topic_name = 'bbc_news_topic'
group_id = 'my_group'
username = 'Helois'
password = 'Hello1@2'

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

    consumer = Consumer(conf)
    consumer.subscribe([topic_name])

    try:
        while True:
            msg = consumer.poll(1.0)

            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaException._PARTITION_EOF:
                    continue
                else:
                    print(msg.error())
                    break

            print(f"Received message: {msg.value().decode('utf-8')}")

    except KeyboardInterrupt:
        print("Consumer script interrupted. Exiting...")
    finally:
        consumer.close()

if __name__ == '__main__':
    consume_from_kafka()
