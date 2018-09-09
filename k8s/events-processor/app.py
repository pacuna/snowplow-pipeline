from confluent_kafka import Producer, Consumer, KafkaError
import snowplow_analytics_sdk.event_transformer
import snowplow_analytics_sdk.snowplow_event_transformation_exception
import json

kafka_consumer = Consumer({
    'bootstrap.servers': "bootstrap.kafka.svc.cluster.local:9092",
    'group.id': 'python-consumer',
    'default.topic.config': {
        'auto.offset.reset': 'smallest'
    }
 })

kafka_producer = Producer({
    'bootstrap.servers': "bootstrap.kafka.svc.cluster.local:9092",
 })

kafka_consumer.subscribe(['snowplow_enriched_good'])

while True:
    msg = kafka_consumer.poll(1.0)

    if msg is None:
        continue
    if msg.error():
        if msg.error().code() == KafkaError._PARTITION_EOF: continue
        else:
            print(msg.error())
            break

    event = msg.value().decode('utf-8')

    try:
        json_data = snowplow_analytics_sdk.event_transformer.transform(event)
        kafka_producer.poll(0)
        kafka_producer.produce('snowplow_json_event', json.dumps(json_data).encode('utf-8'))
        kafka_producer.flush()
        print(json_data)

    except snowplow_analytics_sdk.snowplow_event_transformation_exception.SnowplowEventTransformationException as e:
        for error_message in e.error_messages:
            print("error: " + error_message)

c.close()

