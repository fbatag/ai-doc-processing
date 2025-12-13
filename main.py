import os
import logging
import datetime
from flask import Flask, render_template, request, jsonify, redirect, url_for
from google.cloud import storage
from google.cloud import firestore
from google import auth
credentials, project_id = auth.default()
from google.oauth2 import service_account

storage_client = storage.Client()
db = firestore.Client()
local_cred_file = os.environ.get("HOME") +"/.config/gcloud/gemini-app-sa.json"

print("(RE)LOADING APPLICATION")
app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)

# Get Bucket Name from environment variable

SERVICE_NAME = os.environ.get("SERVICE_NAME", "ai-doc-processing")
BUCKET_NAME = os.environ.get("BUCKET_NAME", f"{SERVICE_NAME}-{storage_client.project}")
docs_bucket = storage_client.bucket(BUCKET_NAME)
if not docs_bucket:
    raise Exception(f"Erro: {BUCKET_NAME} bucket não encontrado")

docs_files = []

@app.route("/", methods=["GET", "POST"])
def index():
    global docs_files

    print("** MAIN ** ")
    clicked_button = request.form.get('clicked_button', "NOT_FOUND")
    if clicked_button == "delete_doc_btn": 
        deleteDocFromBucket(request.form["item_to_delete"])
    elif clicked_button == "delete_task_btn": 
        deleteTaskAI(request.form["item_to_delete"])
    try:
        docs_files = getDocFilesFromBucket()
        ai_tasks = getAiTasks()
        return render_template('index.html', docs_files=docs_files, ai_tasks=ai_tasks)
    except Exception as e:
        logging.error(f"Error listing blobs: {e}")
        return f"Error listing files: {e}", 500

def getAiTasks():
    tasks_ref = db.collection(u'ai_tasks')
    docs = tasks_ref.stream()
    tasks = []
    for doc in docs:
        task = doc.to_dict()
        task['task_name'] = doc.id
        tasks.append(task)
    return tasks

def getDocFilesFromBucket():
    blobs = docs_bucket.list_blobs()
    files = []
    for blob in blobs:
        files.append({
                'name': blob.name,
                'url': blob.public_url,
                'content_type': blob.content_type,
                'size': blob.size,
                'updated': blob.updated
            })
    return files

def deleteDocFromBucket(doc_to_delete):
    print("METHOD: deleteDocFromBucket")
    try:
        blob = docs_bucket.blob(doc_to_delete)
        print("Deleting " + doc_to_delete)
        blob.delete()
    except Exception as e:
        print(f"Error deleting object '{doc_to_delete}': {e}")

def deleteTaskAI(task_to_delete):
    print("METHOD: deleteTaskAI")
    try:
        db.collection(u'ai_tasks').document(task_to_delete).delete()
        print("Deleting " + task_to_delete)
    except Exception as e:
        print(f"Error deleting task '{task_to_delete}': {e}")

@app.route("/getSignedUrl", methods=["GET"])
def getSignedUrl():
    print("METHOD: getSignedUrl")
    object_destination = request.args.get("object_destination")
    filetype = request.args.get("filetype")
    return getSignedUrlParam(docs_bucket, object_destination, filetype)

def getSignedUrlParam(dest_bucket, object_destination, filetype):
    blob = dest_bucket.blob(object_destination)
    expiration=datetime.timedelta(minutes=15)

    print('Content-Type: '+  filetype)
    if request.url_root == 'http://127.0.0.1:8080/':
        print("RUNNING LOCAL")
        local_credentials=service_account.Credentials.from_service_account_file(local_cred_file)
        signeUrl = blob.generate_signed_url(method='PUT', version="v4", expiration=expiration, content_type=filetype, 
                                    credentials=local_credentials, #credentials=credentials,
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
    print(signeUrl)
    return signeUrl

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
