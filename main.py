import os
import json
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
collection_name = u'ai_tasks'


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
    print("** MAIN **")
    try:
        clicked_button = request.form.get('clicked_button', "NOT_FOUND")
        #selected_doc = None
        selected_item = request.form.get("selected_item",";;")
        print(f"clicked_button: {clicked_button} selected_item: {selected_item}")
        model_name, task_name, selected_doc = selected_item.split(";")

        #if clicked_button == "select_doc_btn": 
        
        if clicked_button == "return_btn":
            return render_template('index.html', docs_files=getDocFiles(), ai_tasks=getAiTasks())
        elif clicked_button == "delete_doc_btn":
            deleteDocFromBucket(selected_doc)
        elif clicked_button == "delete_task_btn": 
            deleteTaskAI(task_name)

        elif clicked_button == "execute_task_btn":
            msg_processing = f"Executando a inferência da tarefa: <span style='float:right'>{task_name}</span><br><br>Para o documento: <span style='float:right'>{selected_doc}</span><br><br>Usando o modelo: <span style='float:right'>{model_name}</span><br><br><br><span style='display:block; text-align:center'>Aguarde alguns instantes...</span>"
            return render_template('index.html', msg_processing=msg_processing, selected_item=f"{model_name};{task_name};{selected_doc}", selected_doc="")
        
        elif clicked_button == "result_execute_task_btn":
            task_result = executeAITask(model_name, task_name, selected_doc)
            return render_template('index.html', ai_tasks=getAiTasks(), selected_doc=geSelectedDoc(selected_doc), task_result=task_result, choosen_model_name=model_name, executed_task_name=task_name)

        return render_template('index.html', docs_files=getDocFiles(selected_doc), ai_tasks=getAiTasks(), selected_doc=geSelectedDoc(selected_doc))       
    except Exception as e:
        print(e)
        return f"Error: {e}", 500

def geSelectedDoc(selected_doc_name):
    print("METHOD: getDocFiles: " + selected_doc_name)
    if not selected_doc_name or selected_doc_name == "": return
    sel_blob = docs_bucket.get_blob(selected_doc_name)
    if sel_blob:
        selected_doc = {
                'name': sel_blob.name,
                'content_type': sel_blob.content_type,
                'url': getSignedDownloadUrl(sel_blob)
            }
    return selected_doc

def getDocFiles(selected_doc = ""):
    print(f"METHOD: getDocFiles {selected_doc}")
    if selected_doc != "": return
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

def getAiTasks():
    print("METHOD: getAiTasks")
    tasks_ref = db.collection(collection_name)
    docs = tasks_ref.stream()
    tasks = []
    for doc in docs:
        task = doc.to_dict()
        task['task_name'] = doc.id
        tasks.append(task)
    return tasks

@app.route("/getAITask", methods=["GET"])
def getAITask(task_name=None):
    is_internal_call = task_name is not None
    if not task_name: task_name = request.args.get("task_name")
    print("METHOD: getAITask: "+ task_name)
    ai_task = db.collection(collection_name).document(task_name).get()
    data = ai_task.to_dict()
    command = data.get('command')
    str_output = data.get('str_output')
    if isinstance(str_output, (dict, list)):
        str_output = json.dumps(str_output, indent=4)
    
    if is_internal_call:
        return command, str_output
        
    return jsonify({
        "command": command,
        "str_output": str_output
    })

@app.route("/addAITask", methods=["POST"])
def addAITask():
    task_name = request.form["task_name"]
    print(f"METHOD: addAITask: {task_name}")
    try:
        ai_task_ref = db.collection(collection_name).document(task_name)
        if ai_task_ref.get().exists:
            return f"Erro: A tarefa '{task_name}' já existe.", 400

        ai_task_ref.set({
            "command": "",
            "str_output": {}
        })
        return "Sucesso", 200
    except Exception as e:
        print(e)
        return f"Erro ao criar {task_name}: {e}", 500
    
@app.route("/saveAITask", methods=["POST"])
def saveAITask():
    task_name = request.form["task_name"]
    command = request.form["command"]
    str_output = request.form["str_output"]
    print(f"METHOD: saveAITask: T:{task_name} C:{command} S:{str_output}")
    try:
        ai_task_ref = db.collection(collection_name).document(task_name)
        ai_task_ref.set({
            'command': command,
            'str_output': json.loads(str_output)
        })
        return "Sucesso", 200
    except Exception as e:
        print(e)
        return f"Erro ao salvar {task_name}: {e}", 500

def deleteTaskAI(task_to_delete):
    print("METHOD: deleteTaskAI: " + task_to_delete)
    if  task_to_delete == "": return
    try:
        db.collection(collection_name).document(task_to_delete).delete()
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
        print("getSignedDownloadUrl with CREDENTIALS")
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
        print("getSignedUrlParam with CREDENTIALS")
        print(credentials.service_account_email)
        #if credentials.token is None:
        credentials.refresh(auth.transport.requests.Request())
        print(credentials.token)
        signeUrl = blob.generate_signed_url(method='PUT', version="v4", expiration=expiration, content_type=filetype, 
                                    service_account_email=credentials.service_account_email, access_token=credentials.token,
                                    headers={"X-Goog-Content-Length-Range": "1,5000000000", 'Content-Type': filetype})
        #except Exception as e:
        #    print(e)
    return signeUrl

def executeAITask(model_name, task_name, selected_doc):
    print(f"METHOD: executeAITask: {model_name} - {task_name} - {selected_doc}")   
    try:
        blob = docs_bucket.blob(selected_doc)
        ai_task = db.collection(collection_name).document(task_name).get()
        data = ai_task.to_dict()
        command = data.get('command')
        str_output = data.get('str_output')
        result = call_gemini(model_name, command, [blob], "application/json", str_output)
        try:
            parsed_result = json.loads(result)
            return json.dumps(parsed_result, indent=4, ensure_ascii=False)
        except Exception:
            return result
    except Exception as e:
        return f"Erro ao executar Model: {model_name} Tarefa: {task_name} Documento: {selected_doc} Erro: {e}"

def call_gemini(
      model: str,
      system_instructions: str,
      blob_docs: list = None,
      response_mime_type: str = None,
      response_schema: dict = None
) -> str:

    parts = [types.Part.from_text(text="Conteúdo:")]
    if blob_docs:
        doc_parts = [types.Part.from_uri(mime_type=blob_doc.content_type, file_uri=f"gs://{blob_doc.bucket.name}/{blob_doc.name}" ) for blob_doc in blob_docs]
        parts.extend(doc_parts)
    parts.append(types.Part.from_text(text="Resultado:"))

    contents = [
        types.Content(
        role="user",
        parts=doc_parts
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
