import os
import logging
import datetime
from flask import Flask, render_template, request, jsonify, redirect, url_for
from google.cloud import storage
from google import auth
credentials, project_id = auth.default()
from google.oauth2 import service_account

storage_client = storage.Client()
local_cred_file = os.environ.get("HOME") +"/.config/gcloud/gemini-app-sa.json"

print("(RE)LOADING APPLICATION")
app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)

# Get Bucket Name from environment variable

SERVICE_NAME = os.environ.get("SERVICE_NAME", "ai-doc-processing")
BUCKET_NAME = os.environ.get("BUCKET_NAME", f"{SERVICE_NAME}-{storage_client.project}")
bucket = storage_client.bucket(BUCKET_NAME)

@app.route('/')
def index():
    if not bucket:
        return f"Erro: {BUCKET_NAME} bucket  não encontrado", 500

    try:
        blobs = bucket.list_blobs()
        
        files = []
        for blob in blobs:
            files.append({
                'name': blob.name,
                'url': blob.public_url,
                'content_type': blob.content_type,
                'size': blob.size,
                'updated': blob.updated
            })
            
        return render_template('index.html', files=files, bucket_name=BUCKET_NAME)
    except Exception as e:
        logging.error(f"Error listing blobs: {e}")
        return f"Error listing files: {e}", 500

@app.route("/getSignedUrl", methods=["GET"])
def getSignedUrl():
    print("METHOD: getSignedUrl")
    print(request.args)
    dest_bucket = request.args.get("dest_bucket")
    object_destination = request.args.get("object_destination")
    filetype = request.args.get("filetype")
    if dest_bucket == "code":
        return getSignedUrlParam(codeBucket, object_destination, filetype)
    return getSignedUrlParam(contextsBucket, object_destination, filetype)

def getSignedUrlParam(dest_bucket, object_destination, filetype):
    blob = dest_bucket.blob(object_destination)
    expiration=datetime.timedelta(minutes=15)

    print('Content-Type: '+  filetype)
    if request.url_root == 'http://127.0.0.1:5000/':
        print("RUNNING LOCAL")
        signeUrl = blob.generate_signed_url(method='PUT', version="v4", expiration=expiration, content_type=filetype, 
                                    credentials=service_account.Credentials.from_service_account_file(local_cred_file),
                                    #credentials=credentials,
                                    headers={"X-Goog-Content-Length-Range": "1,5000000000", 'Content-Type': filetype})
    else:
        print("CREDENTIALS")
        print(credentials.service_account_email)
        #if credentials.token is None:
        credentials.refresh(auth.transport.requests.Request())
        print(credentials.token)
        signeUrl = blob.generate_signed_url(method='PUT', version="v4", expiration=expiration, content_type=filetype, 
                                    service_account_email=credentials.service_account_email, access_token=credentials.token,
                                    headers={"X-Goog-Content-Length-Range": "1,5000000000", 'Content-Type': filetype})
        #except Exception as e:
        #    print(e)
    #print(signeUrl)
    return signeUrl

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
