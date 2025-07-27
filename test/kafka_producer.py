from kafka import KafkaProducer
import json
from kafka.admin import KafkaAdminClient, NewTopic

# check if topic exists
def check_topic_exists(topic_name):
    admin_client = KafkaAdminClient(
        bootstrap_servers="localhost:9092"
    )
    return topic_name in admin_client.list_topics()

topic_name = 'test_topic'
if not check_topic_exists(topic_name):
    admin_client = KafkaAdminClient(
        bootstrap_servers="localhost:9092"
    )



    topic_list = []
    topic_list.append(NewTopic(name=topic_name, num_partitions=12, replication_factor=1))
    admin_client.create_topics(new_topics=topic_list, validate_only=False)
else:
    print(f"Topic {topic_name} already exists")

    
producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)
message_data = {'id': 1, 'message': 'first_message'}
producer.send(topic_name, message_data)
producer.flush()
print(f"Message sent to topic: {topic_name}")
producer.close()