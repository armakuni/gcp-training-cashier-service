# Cashier Service

This service allows the cashier to create new transactions by exposing an HTTP endpoint
and then queueing the transactions further processing.

### Requirements

- A Pub/Sub topic for transactions up and running in your Google Cloud account
- Ideally, the Transaction service up and running and subscribed to the topic we will use with service

### Environment variables

The Cashier and Transaction services communicate via a pub sub topic on GCP, so make sure that the same topic name is used for both services.

The service uses the below variables in its configuration. They all have default values as shown below if they are not otherwise specified:

```
CUSTOMER_NAMESPACE=customers(default)
PORT=5004(default)
```

The transactions topic ID is also required for the cashier service to publish to the correct channel and interact with the transactions service.
This must be set into the below variable:

```
TRANSACTIONS_TOPIC_ID
```

### To run linter

```bash
make lint
```

### To run tests

```bash
make tests
```

### To run the service locally

Note: To run this service locally, the GCP Project ID that contains the transaction Pub/Sub topic must be exported.
Set it as the environment variable below:

```bash
export PROJECT_ID=[PROJECT_ID]
```

To run the application use the below command:

```bash
make run
```

### Deployment

This repository contains a cloudbuild.yaml file to deploy this service on to Cloud Run:

```bash
gcloud builds submit --substitutions=_TRANSACTIONS_TOPIC_ID="[TRANSACTIONS_TOPIC_ID]"
```

where [TRANSACTIONS_TOPIC_ID] is the ID of the Pub/Sub topic that serves messages to the Transaction service.

### API documentation

You can access the swagger API documentation by launching the application and visiting the 'cashier/docs' endpoint
