from kafka import KafkaConsumer
import json
topic_name = 'test_topic'
consumer = KafkaConsumer(
    topic_name,
    bootstrap_servers=['localhost:9092'],
    auto_offset_reset='earliest'
)

for message in consumer:
    print(json.loads(message.value.decode('utf-8')))