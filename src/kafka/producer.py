import os
import argparse
from kafka import KafkaProducer
import json
from kafka.admin import KafkaAdminClient, NewTopic
import sys
import time
import numpy as np




module_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(module_path)


from src.kafka.data_generator import generate_data


def check_topic_exists(topic_name):
    admin_client = KafkaAdminClient(
        bootstrap_servers=kafka_broker_url
    )
    return topic_name in admin_client.list_topics()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--batch_size', type=int, default=1000)
    parser.add_argument('--time_interval', type=int, default=1)
    parser.add_argument('--data_generation_speed', type=int, default=10000)
    parser.add_argument('--iters', type=int, default=20)
    args = parser.parse_args()
    iters = 0

    while iters<args.iters:
        start_time = time.time()
        kafka_broker_url = os.getenv('KAFKA_BROKER_URL')
        topic_name = os.getenv('KAFKA_TOPIC')



        if not check_topic_exists(topic_name):
            admin_client = KafkaAdminClient(
                bootstrap_servers=kafka_broker_url
            )
            topic_list = []
            topic_list.append(NewTopic(name=topic_name, num_partitions=12, replication_factor=1))
            admin_client.create_topics(new_topics=topic_list, validate_only=False)
        else:
            print(f"Topic {topic_name} already exists")

        data = generate_data(batch_size=args.batch_size,time_interval=args.time_interval,data_generation_speed=args.data_generation_speed)

        producer = KafkaProducer(bootstrap_servers=kafka_broker_url)

        for row in data:
            producer.send(topic_name, key=row['user_id'].encode('utf-8'), value=json.dumps(row).encode('utf-8'))
        iters+=1
        producer.flush()
        producer.close()
        end_time = time.time()
        print(f"Time taken: {end_time - start_time} seconds")
        print(f"Throughput: {np.round(args.batch_size/(end_time - start_time),0)} messages/second")
        print('Batch completed. Sleeping for 6 seconds')
        time.sleep(6)