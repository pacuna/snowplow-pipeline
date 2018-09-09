# Snowplow Analytics Pipeline

This is an example of an end-to-end Snowplow pipeline to track events using a Kafka broker.

The pipeline works in the following way:

1. A request is sent to the Scala Collector
2. The raw event (thift event) is put into the `snowplow_raw_good` (or bad) topic
3. The enricher grabs the raw events, parses them and put them into the `snowplow_parsed_good` (or bad) topic
4. A custom events processor grabs the parsed event, which is in a tab-delimited/json hybrid format and turns it into a proper
Json event using the python analytics SDK from Snowplow. This event is then put into a final topic called `snowplow_json_event`.
5. (WIP) A custom script grabs the final Json events and loads them into some storage solution (such as BigQuery or Redshift)


## Run the pipeline

Execute:

```sh
docker-compose up -d
```
After that, make sure all the containers are up with `docker-compose ps`. If not, try to run the command again.

This command will create all the components and also a simple web application that sends pageviews and other events to the collector.
Please checkout the `docker-compose.yml` file for more details.
