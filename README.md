# Processamento de Documentos com IA (Google Gemini)

Esta aplicação é uma ferramenta web para processamento e análise inteligente de documentos utilizando os modelos generativos do Google (Gemini). Ela demonstra como integrar serviços do Google Cloud para criar fluxos de trabalho de extração de dados e análise de conteúdo.

## 🚀 Funcionalidades

### Gerenciamento de Documentos
*   **Upload de Arquivos**: Suporte para envio de arquivos PDF, Imagens (JPEG, PNG) e Texto Plano diretamente para o Google Cloud Storage.
*   **Visualização**: Pré-visualização integrada de documentos e imagens na interface.
*   **Gestão**: Listagem detalhada e opção de exclusão de arquivos.

### Tarefas de Inteligência Artificial
As "Tarefas de IA" são instruções pré-configuradas (prompts) que definem o que deve ser extraído ou analisado no documento.
*   **Catálogo de Tarefas**: Visualização de tarefas armazenadas no Firestore.
*   **Execução Flexível**: Capacidade de aplicar qualquer tarefa a qualquer documento carregado.

### Inferência e Análise
*   **Múltiplos Modelos**: Suporte para seleção de diferentes versões do modelo Gemini (ex: Flash, Pro, Flash-Lite) para equilibrar custo e performance.
*   **Saída Estruturada**: Os resultados são processados e exibidos, frequentemente em formato JSON estruturado, facilitando a integração ou leitura.

## 🛠️ Arquitetura Técnica

A aplicação é construída em **Python** utilizando o framework **Flask** e utiliza os seguintes serviços do Google Cloud:

*   **Google Cloud Storage (GCS)**: Armazenamento de objetos (Blob Storage) para guardar os documentos enviados pelos usuários.
*   **Google Cloud Firestore**: Banco de dados NoSQL utilizado para persistir as definições das tarefas de IA (prompts e schemas).
*   **Vertex AI / Google GenAI SDK**: Interface para comunicação com os modelos Gemini (Multimodal) para processamento dos documentos.

## 📦 Instalação e Execução

### Pré-requisitos
*   Python 3.8+
*   Conta no Google Cloud Platform com um projeto ativo.
*   APIs habilitadas: Vertex AI, Cloud Storage, Firestore.
*   Credenciais de autenticação (Application Default Credentials).

### Passos
para instalar, todo os comandos do install.sh

## 📝 Como Usar

1.  **Carregar**: Na tela inicial, clique em "Carregar documento" e selecione um arquivo do seu computador.
2.  **Selecionar**: Na lista de documentos carregados, clique no ícone de confirmação (✔️) ao lado do arquivo que deseja analisar.
3.  **Configurar Análise**:
    *   Visualize o documento carregado.
    *   Selecione o modelo Gemini desejado no menu dropdown.
    *   Na lista de "Tarefas IA Cadastradas", escolha a análise que deseja realizar clicando no ícone de confirmação (✔️).
4.  **Resultado**: Aguarde o processamento. O resultado da análise gerada pela IA aparecerá na tela logo abaixo.
