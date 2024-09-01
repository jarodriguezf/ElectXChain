from confluent_kafka.admin import AdminClient, NewTopic

# CONFIGURATION OF KAFKA CLUSTER
config = {
    'bootstrap.servers': 'kafka_host:9093'   
}

admin_client = AdminClient(config)

# NAMES AND SETTINGS
topic_name = 'vote_passthrough'
num_partitions = 2
replication_factor = 1

topic_name_2 = 'vote_result'
num_partitions_2 = 2
replication_factor_2 = 1

new_topic_1 = NewTopic(topic_name, num_partitions=num_partitions, replication_factor=replication_factor)
new_topic_2 = NewTopic(topic_name_2, num_partitions=num_partitions_2, replication_factor=replication_factor_2)

# CREATE THE TOPIC
try:
    # SEND THE VALIDATION FOR CREATE THE TOPIC
    fs = admin_client.create_topics([new_topic_1, new_topic_2])
    
    for topic, future in fs.items():
        try:
            future.result()
            print(f'Tópico {topic} creado con éxito.')
        except Exception as e:
            print(f'Error al crear el tópico {topic}: {e}')
except Exception as e:
    print(f'Error en la creación del tópico: {e}')