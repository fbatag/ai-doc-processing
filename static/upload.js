async function getAITask(taskName) {
    const response = await fetch("/getAITask?" + new URLSearchParams({
        task_name: taskName
    }));
    if (response.ok) {
        const data = await response.json();
        return data;
    } else {
        console.error("Erro ao obter a tarefa '" + taskName + "': " + response.statusText);
        alert("Erro ao obter a tarefa '" + taskName + "': " + response.statusText);
        return null;
    }
}

async function addAITask(taskName) {
    const formData = new URLSearchParams();
    formData.append("task_name", taskName);
    const response = await fetch("/addAITask", {
        method: "POST",
        body: formData
    });
    if (!response.ok) {
        const errorText = await response.text();
        console.error("Erro criando tarefa IA: ", response.statusText, errorText);
        alert("Erro criando tarefa IA: '" + taskName + "'\n" + errorText);
        return false;
    }
    await response.text();
    return true;
}

async function saveAITask(taskName, command, str_output) {
    console.log("saveAITask")
    console.log(taskName)
    console.log(command)
    console.log(str_output)
    const formData = new URLSearchParams();
    formData.append("task_name", taskName);
    formData.append("command", command);
    formData.append("str_output", str_output);

    const response = await fetch("/saveAITask", {
        method: "POST",
        body: formData
    });
    if (!response.ok) {
        const errorText = await response.text();
        console.error("Erro salvando tarefa IA: ", response.statusText);
        alert("Erro salvando tarefa IA: " + taskName + "\n"+ response.statusText);
        return false;
    }
    await response.text();
    alert("Tarefa '"+ taskName + "' salva!!!");
    return true;
}

function UploadWithSignedUrl(file, callback) {
    if (file.size <= 5) 
    {
        callback("Por definição, o arquivo deve conter pelo menos 5 bytes de informação.");
        return;
    }
    getSignedUrl(file.name, file.type, (error, signedUrl) => {
        if (error) {
            callback(error);
          } else {
            uploadFileToGCS(signedUrl, file, callback);
          }
    });
}

function getSignedUrl(object_destination, filetype, callback) {
    const xhr = new XMLHttpRequest();
    const url = `/getSignedUrl?${new URLSearchParams({
        object_destination: object_destination,
        filetype: filetype
    }).toString()}`;

    xhr.open("GET", url, true);
    xhr.onload = function () {
        if (xhr.status === 200) {
            callback(null, xhr.responseText);
        } else {
            callback(xhr.status + " : Erro ao tentar obter a URL assinada para o arquivo " + object_destination + ". Resposta: " + xhr.responseText, null);
        }
    };
    xhr.onerror = function (event) {
        callback("Erro (onerror) ao tentar obter a URL assinada para o arquivo " + object_destination + ". Resposta: " + xhr.responseText);
    };
    xhr.send();
}

function uploadFileToGCS(signedUrl, file, callback) {
    const xhr = new XMLHttpRequest();
    xhr.open("PUT", signedUrl, true);
    xhr.onload = () => {
        const status = xhr.status;
        if (status === 200) {
            callback(null);
        } else {
            callback(xhr.status + " : Erro ao tentar carregar o arquivo " + file.name + " usando URL assinada. Resposta: " + xhr.responseText);
        }
    };
    xhr.onerror = (event) => {
        callback("Erro ao tentar carregar o arquivo " + file.name + " usando URL assinada. Resposta: " + xhr.responseText);
    };
    xhr.setRequestHeader('Content-Type', file.type);
    xhr.setRequestHeader('X-Goog-Content-Length-Range', '1,5000000000');
    xhr.send(file);
}

async function TestSignedUrl() {
    const response = await fetch("/getSignedUrl?" + new URLSearchParams({
        project: "Agendamento",
        filename: "teste.txt",
        content_type: "text/plain"
    }).toString(), {
        method: "GET"
    })
    const signedUrl = await response.text();
    alert(signedUrl);
}

async function executeAITask(model_name, task_name, selected_doc, callback) {
    const response = await fetch("/executeAITask", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            model_name: model_name,
            task_name: task_name,
            selected_doc: selected_doc
        })
    });

    if (response.ok) {
        const result = await response.text();
        callback(null, result);
    } else {
        const error = await response.text();
        callback(error, null);
    }
}
