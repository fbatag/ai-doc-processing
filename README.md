# Flask GCS Upload App

This is a Flask application designed to run on Google Cloud Run. It allows users to upload PDF files to a Google Cloud Storage (GCS) bucket using Signed URLs and lists the uploaded files.

## Prerequisites

1.  **Google Cloud Project**: You need a GCP project.
2.  **GCS Bucket**: Create a bucket to store the files.
3.  **Permissions**: The service account running this app (or your local credentials) needs:
    *   `Storage Object Admin` or `Storage Object Creator` and `Storage Object Viewer` roles on the bucket.

## CORS Configuration

For the browser to be able to upload directly to GCS using the signed URL, you **must** configure CORS on your GCS bucket.

Create a file named `cors.json`:

```json
[
    {
      "origin": ["*"],
      "method": ["GET", "PUT", "OPTIONS"],
      "responseHeader": ["Content-Type", "x-goog-resumable"],
      "maxAgeSeconds": 3600
    }
]
```

Apply it using `gcloud`:

```bash
gcloud storage buckets update gs://YOUR_BUCKET_NAME --cors-file=cors.json
```

*(Replace `*` with your specific domain in production)*

## Running Locally

1.  Set the environment variable:
    ```bash
    export BUCKET_NAME=your-bucket-name
    export GOOGLE_APPLICATION_CREDENTIALS="path/to/key.json" # If not using gcloud auth application-default login
    ```
2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3.  Run the app:
    ```bash
    python app.py
    ```

## Deploying to Cloud Run

1.  Build and deploy using `gcloud`:
    ```bash
    gcloud run deploy gcs-pdf-uploader \
      --source . \
      --region us-central1 \
      --allow-unauthenticated \
      --set-env-vars BUCKET_NAME=your-bucket-name
    ```
