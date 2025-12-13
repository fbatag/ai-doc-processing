export PROJECT_ID=$(gcloud config get project)
export REGION=southamerica-east1
export SERVICE_NAME=ai-doc-processing
export BUCKET_NAME=$SERVICE_NAME-$PROJECT_ID
export BUCKET_URL=gs://$BUCKET_NAME
export SERVICE_ACCOUNT_NAME=sa-$SERVICE_NAME
export SERVICE_ACCOUNT=$SERVICE_ACCOUNT_NAME@$PROJECT_ID.iam.gserviceaccount.com

gcloud services enable cloudresourcemanager.googleapis.com
gcloud services enable storage-component.googleapis.com
gcloud services enable aiplatform.googleapis.com
gcloud services enable appengine.googleapis.com
gcloud services enable cloudbuild.googleapis.com # para o Cloud Run
gcloud services enable iap.googleapis.com 

gsutil mb -b on -l $REGION $BUCKET_URL
gsutil lifecycle set bucket_lifecycle.json $BUCKET_URL
gcloud storage buckets update $BUCKET_URL --cors-file=bucket-cors.json
gcloud storage buckets describe $BUCKET_URL --format="default(cors_config)" # Verificar se acatou

gcloud iam service-accounts create $SERVICE_ACCOUNT_NAME \
--display-name "Service Account para processador com IA para documentos" \
--project $PROJECT_ID

gcloud projects add-iam-policy-binding $PROJECT_ID --member serviceAccount:$SERVICE_ACCOUNT --role roles/aiplatform.user
gcloud projects add-iam-policy-binding $PROJECT_ID --member serviceAccount:$SERVICE_ACCOUNT --role roles/aiplatform.user
gcloud storage buckets add-iam-policy-binding $BUCKET_URL --member serviceAccount:$SERVICE_ACCOUNT --role roles/storage.objectUser --project=$PROJECT_ID
