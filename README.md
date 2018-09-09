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

## Run in production (Kubernetes)

The configuration files are using endpoints for Kafka provided by [kubernetes-kafka](https://github.com/Yolean/kubernetes-kafka). You can configure your own brokers in the collector and enrich configuration file (configmaps).

Assuming you have configured Kafka for all the components:

1. Deploy the collector: `kubectl apply -f ./k8s/collector`. This will create the configuration, deployment and a service that uses a Load Balancer to access the collector's endpoint. 
2. Deploy the enricher: `kubectl apply -f ./k8s/stream-enrich`. This will create the configurations and deployment.
3. Build a Docker image for the events processor, upload it to some registry and add it to `k8s/events-processor/deploy.yml`. Checkout the files in `k8s/events-processor` before building the image and change the broker configuration in `app.py`.
4. Deploy the events processor application using the previous `k8s/events-processor/deploy.yml` file.
5. Run the webapp example locally and change the collector's address to the load balancer IP address created for the collector. The collector is using the port 80 so remove the port and just leave the IP address.
6. Once everything is running, open the webapp and refresh the page a couple of times. Checkout the logs of the events processor pod to see if the Json events are created correctly.
