import os
import logging
import datetime
from flask import Flask, render_template, request, jsonify, redirect, url_for
from google.cloud import storage
from google.cloud import firestore
from google import auth
credentials, project_id = auth.default()
from google.oauth2 import service_account
from google import genai
from google.genai import types


storage_client = storage.Client()
db = firestore.Client()
local_cred_file = os.environ.get("HOME") +"/.config/gcloud/gemini-app-sa.json"

genai_client = genai.Client(
      vertexai=True,
      project=storage_client.project,
      location="global"
)
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

@app.route("/", methods=["GET", "POST"])
def index():
    print("** MAIN ** ")
    try:
        clicked_button = request.form.get('clicked_button', "NOT_FOUND")
        print("clicked_button: " + clicked_button)
        selected_doc = None
        selected_item = request.form.get("selected_item","")
        if clicked_button == "select_doc_btn": 
            return render_template('index.html', ai_tasks=getAiTasks(), selected_doc=geSelectedDoc(selected_item))
        elif clicked_button == "execute_task_btn":
            model_name, task_name, selected_doc = selected_item.split(";")
            task_result = executeAITask(model_name, task_name, selected_doc)
            return render_template('index.html', ai_tasks=getAiTasks(), selected_doc=selected_doc, task_result=task_result, mode_name=model_name)
        elif clicked_button == "delete_doc_btn":
            deleteDocFromBucket(selected_item)
        elif clicked_button == "delete_task_btn": 
            deleteTaskAI(selected_item)
        return render_template('index.html', docs_files=getDocFiles(), ai_tasks=getAiTasks(), selected_doc=selected_doc)
    except Exception as e:
        logging.error(f"Error listing blobs: {e}")
        return f"Error listing files: {e}", 500

def geSelectedDoc(selected_doc_name):
    print("METHOD: getDocFiles: " + selected_doc_name)
    if selected_doc_name == "": return
    sel_blob = docs_bucket.get_blob(selected_doc_name)
    if sel_blob:
        selected_doc = {
                'name': sel_blob.name,
                'content_type': sel_blob.content_type,
                'url': getSignedDownloadUrl(sel_blob)
            }
    return selected_doc

def getAiTasks():
    print("METHOD: getAiTasks")
    tasks_ref = db.collection(u'ai_tasks')
    docs = tasks_ref.stream()
    tasks = []
    for doc in docs:
        task = doc.to_dict()
        task['task_name'] = doc.id
        tasks.append(task)
    return tasks

def getDocFiles():
    print("METHOD: getDocFiles")
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
    print("METHOD: deleteDocFromBucket: " + doc_to_delete)
    if doc_to_delete == "": return
    try:
        blob = docs_bucket.blob(doc_to_delete)
        print("Deleting " + doc_to_delete)
        blob.delete()
    except Exception as e:
        print(f"Error deleting object '{doc_to_delete}': {e}")

def deleteTaskAI(task_to_delete):
    print("METHOD: deleteTaskAI: " + task_to_delete)
    if  task_to_delete == "": return
    try:
        db.collection(u'ai_tasks').document(task_to_delete).delete()
        print("Deleting " + task_to_delete)
    except Exception as e:
        print(f"Error deleting task '{task_to_delete}': {e}")

def getSignedDownloadUrl(blob):
    print("METHOD: getSignedDownloadUrl: " + blob.name)
    expiration = datetime.timedelta(minutes=15)
    if request.url_root == 'http://127.0.0.1:8080/':
        print("RUNNING LOCAL: getSignedDownloadUrl")
        local_credentials = service_account.Credentials.from_service_account_file(local_cred_file)
        return blob.generate_signed_url(method='GET', version="v4", expiration=expiration, credentials=local_credentials)
    else:
        credentials.refresh(auth.transport.requests.Request())
        return blob.generate_signed_url(method='GET', version="v4", expiration=expiration, service_account_email=credentials.service_account_email, access_token=credentials.token)

@app.route("/getSignedUrl", methods=["GET"])
def getSignedUrl():
    object_destination = request.args.get("object_destination")
    print("METHOD: getSignedUrl: " + object_destination)
    filetype = request.args.get("filetype")
    return getSignedUrlParam(docs_bucket, object_destination, filetype)

def getSignedUrlParam(dest_bucket, object_destination, filetype):
    blob = dest_bucket.blob(object_destination)
    expiration=datetime.timedelta(minutes=15)

    print('Content-Type: '+  filetype)
    if request.url_root == 'http://127.0.0.1:8080/':
        print("RUNNING LOCAL: getSignedUrlParam")
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


def executeAITask(model_name, task_name, selected_doc):
    print(f"METHOD: executeAITask: {model_name} - {task_name} - {selected_doc}")   
    blob = docs_bucket.blob(selected_doc)
    ai_task = db.collection(u'ai_tasks').document(task_name).get()
    command = ""
    str_output = ""
    if ai_task.exists:
        data = ai_task.to_dict()
        command = data.get('command')
        str_output = data.get('str_output')
        print(f"Command: {command}")
        print(f"str_output: {str_output}")

    return call_gemini(model_name, command, [blob], "application/json", str_output)


def call_gemini(
      model: str,
      system_instructions: str,
      blob_docs: list = None,
      response_mime_type: str = None,
      response_schema: dict = None
) -> str:

  parts = [types.Part.from_text(text="Conteúdo:")]
  if blob_docs:
    # pdfs is expected to be a list of tuples: [(mime_type, data), ...]
    doc_parts = [types.Part.from_uri(mime_type=blob_doc.mime, file_uri=blob_doc.y) for blob_doc, data in blob_docs]
    parts.extend(doc_parts)
  parts.append(types.Part.from_text(text="Resultado:"))

  contents = [
    types.Content(
      role="user",
      parts=parts
    )
  ]
  generate_content_config = types.GenerateContentConfig(
    temperature = 0.1,
    top_p = 0.95,
    max_output_tokens = 65535,
    response_modalities = ["TEXT"],
    response_mime_type = response_mime_type,
    response_schema = response_schema,
    system_instruction=[types.Part.from_text(text=system_instructions)],
  )

  response = genai_client.models.generate_content(
     model = model,
     contents = contents,
     config = generate_content_config)

  return response.text

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
