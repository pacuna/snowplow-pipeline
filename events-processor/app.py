from confluent_kafka import Consumer, KafkaError
import snowplow_analytics_sdk.event_transformer
import snowplow_analytics_sdk.snowplow_event_transformation_exception
import json

kafka_consumer = Consumer({
    'bootstrap.servers': "kafka:9092",
    'group.id': 'python-consumer',
    'default.topic.config': {
        'auto.offset.reset': 'smallest'
    }
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
        print(json_data)

    except snowplow_analytics_sdk.snowplow_event_transformation_exception.SnowplowEventTransformationException as e:
        for error_message in e.error_messages:
            print("error: " + error_message)

c.close()
