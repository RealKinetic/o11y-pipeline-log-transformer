# o11y-pipeline-log-transformer
Google Cloud Function for transforming logs for ingestion into the observability pipeline

## Deployment

```sh
$ gcloud beta functions deploy pipeline-logs-transform \
    --env-vars-file env.yaml \
    --update-labels obs-pipeline= \
    --runtime python37 \
    --entry-point handle_log \
    --trigger-resource pipeline-logs-transform \
    --trigger-event google.pubsub.topic.publish \
    --retry
```
