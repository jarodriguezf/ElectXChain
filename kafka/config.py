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

new_topic = NewTopic(topic_name, num_partitions=num_partitions, replication_factor=replication_factor)

# CREATE THE TOPIC
try:
    # SEND THE VALIDATION FOR CREATE THE TOPIC
    fs = admin_client.create_topics([new_topic])
    
    for topic, future in fs.items():
        try:
            future.result()
            print(f'Tópico {topic} creado con éxito.')
        except Exception as e:
            print(f'Error al crear el tópico {topic}: {e}')
except Exception as e:
    print(f'Error en la creación del tópico: {e}')