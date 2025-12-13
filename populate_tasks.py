import json
from google.cloud import firestore

tasks = [
    {
        "task_name": "Convênio-Rede_de_Atendimento",
        "command": 
"""Analise o documento completamente.
Identifique o Anexo que contem dados da Rede de Atendimento.
Para cada Plano com lista de produtos liste:

- Nome da Linha de Produtos
- Codigo da Rede
- Nome do Produto
- Nivel do Produto
""",
    "str_output": { 
      "type": "ARRAY",
      "items": {
        "type": "OBJECT",
        "properties": {
          "Linha de Produtos": {
            "type": "STRING",
            "description": "O nome da linha de produtos."
          },
          "Codigo da Rede": {
            "type": "STRING",
            "description": "O código da rede."
          },
          "Produto": {
            "type": "STRING",
            "description": "O nome do produto."
          },
          "Nivel do Produto": {
            "type": "STRING",
            "description": "O nível do produto."
          }
        }
      }
    }
    },
    {
        "task_name": "Convenio_Regra_Atend_Setor_Alergia_e_Imunologia",
        "command": 
"""Analise o documento completamente. Identifique o Anexo que contem a tabela de procedimentos
contemplados para cada especialidade médica, assim como seu regime de atendimento. O regime de atendimento é determinado pela marcação com a letra X sob cada um dos regimes.
Liste os procedimentos descritos em cada especialidade médica com os seguintes informações:
- Nome da Especialidade Médica
- Codigo do Procedimento
- Nome do Procedimento
- Regime de Atendimento

Considere os regimes de atendimento separados por virgula quando mais de um estiver disponível.
O regime de atendimento é descrito uma vez em cada tabela, sendo o mesmo para todos os procedimentos contidos na mesma tabela.

Retorne somente as informações solicitadas para a especialidade ALERGIA E IMUNOLOGIA.

""",        
    "str_output": {
      "type": "ARRAY",
      "items": {
        "type": "OBJECT",
        "properties": {
          "Código da Especialidade Médica": {
            "type": "STRING",
            "description": "O código da especialidade médica."
          },
          "Especialidade Médica": {
            "type": "STRING",
            "description": "O nome da especialidade médica."
          },
          "Codigo do Procedimento": {
            "type": "STRING",
            "description": "O código do procedimento."
          },
          "Procedimento": {
            "type": "STRING",
            "description": "O nome do procedimento."
          },
          "Regime de Atendimento": {
            "type": "STRING",
            "description": "O tipo do regime de atendimento."
          }

        }
      }
    }
    },
    {
    "task_name": "Convenio_Regra_Atend_Setor_Cardiologia",
    "command": 
"""Analise o documento completamente. Identifique o Anexo que contem a tabela de procedimentos
contemplados para cada especialidade médica, assim como seu regime de atendimento. O regime de atendimento é determinado pela marcação com a letra X sob cada um dos regimes.
Liste os procedimentos descritos em cada especialidade médica com os seguintes informações:
- Nome da Especialidade Médica
- Codigo do Procedimento
- Nome do Procedimento
- Regime de Atendimento

Considere os regimes de atendimento separados por virgula quando mais de um estiver disponível.
O regime de atendimento é descrito uma vez em cada tabela, sendo o mesmo para todos os procedimentos contidos na mesma tabela.

Retorne somente as informações solicitadas para a especialidade CARDIOLOGIA.

"""    ,
    "str_output":  {
      "type": "ARRAY",
      "items": {
        "type": "OBJECT",
        "properties": {
          "Código da Especialidade Médica": {
            "type": "STRING",
            "description": "O código da especialidade médica."
          },
          "Especialidade Médica": {
            "type": "STRING",
            "description": "O nome da especialidade médica."
          },
          "Codigo do Procedimento": {
            "type": "STRING",
            "description": "O código do procedimento."
          },
          "Procedimento": {
            "type": "STRING",
            "description": "O nome do procedimento."
          },
          "Regime de Atendimento": {
            "type": "STRING",
            "description": "O tipo do regime de atendimento."
          }

        }
      }
    }
    },
    {
    "task_name": "Convenio_Regra_Atend_Setor_Cirurgia Geral",
    "command": 
"""Analise o documento completamente. Identifique o Anexo que contem a tabela de procedimentos
contemplados para cada especialidade médica, assim como seu regime de atendimento. O regime de atendimento é determinado pela marcação com a letra X sob cada um dos regimes.
Liste os procedimentos descritos em cada especialidade médica com os seguintes informações:
- Nome da Especialidade Médica
- Codigo do Procedimento
- Nome do Procedimento
- Regime de Atendimento

Considere os regimes de atendimento separados por virgula quando mais de um estiver disponível.
O regime de atendimento é descrito uma vez em cada tabela, sendo o mesmo para todos os procedimentos contidos na mesma tabela.

Retorne somente as informações solicitadas para a especialidade CIRURGIA GERAL.

""",
    "str_output":  {
      "type": "ARRAY",
      "items": {
        "type": "OBJECT",
        "properties": {
          "Código da Especialidade Médica": {
            "type": "STRING",
            "description": "O código da especialidade médica."
          },
          "Especialidade Médica": {
            "type": "STRING",
            "description": "O nome da especialidade médica."
          },
          "Codigo do Procedimento": {
            "type": "STRING",
            "description": "O código do procedimento."
          },
          "Procedimento": {
            "type": "STRING",
            "description": "O nome do procedimento."
          },
          "Regime de Atendimento": {
            "type": "STRING",
            "description": "O tipo do regime de atendimento."
          }

        }
      }
    }
    },
    {
    "task_name": "Convenio_Regra_Atend_Setor_Anestesiologia",
    "command": 
"""Analise o documento completamente. Identifique o Anexo que contem a tabela de procedimentos
contemplados para cada especialidade médica, assim como seu regime de atendimento. O regime de atendimento é determinado pela marcação com a letra X sob cada um dos regimes.
Liste os procedimentos descritos em cada especialidade médica com os seguintes informações:
- Nome da Especialidade Médica
- Codigo do Procedimento
- Nome do Procedimento
- Regime de Atendimento

Considere os regimes de atendimento separados por virgula quando mais de um estiver disponível.
O regime de atendimento é descrito uma vez em cada tabela, sendo o mesmo para todos os procedimentos contidos na mesma tabela.

Retorne somente as informações solicitadas para a especialidade ANESTESIOLOGIA.

""",
    "str_output": {
      "type": "ARRAY",
      "items": {
        "type": "OBJECT",
        "properties": {
          "Código da Especialidade Médica": {
            "type": "STRING",
            "description": "O código da especialidade médica."
          },
          "Especialidade Médica": {
            "type": "STRING",
            "description": "O nome da especialidade médica."
          },
          "Codigo do Procedimento": {
            "type": "STRING",
            "description": "O código do procedimento."
          },
          "Procedimento": {
            "type": "STRING",
            "description": "O nome do procedimento."
          },
          "Regime de Atendimento": {
            "type": "STRING",
            "description": "O tipo do regime de atendimento."
          }

        }
      }
    }
    },
    {
    "task_name": "Pacote_Procedimento",
    "command": 
"""Analise o documento completamente.
Identifique o Anexo que contem a negociação e remuneração. Identifique os PACOTES contemplados.
Para cada pacote identificado liste:
- Codigo do Pacote
- Codigo TUSS do Pacote
- Descrição do Pacote
- Valor do Pacote
- Honorário Médico (Sim ou Não)
- Regime de Atendimento
- Acomodação
- Quantidade de Diarias
- Categoria Principal da Autorização
- Categoria Secundária da Autorização
- Honorário Médico Incluído
- Diárias e Serviços Incluídos
- Gasoterapia Incluída
- Home Care Incluído
- Procedimentos Incluídos
- Materiais Incluídos
- Medicamentso Incluídos
- Remoção Incluída
- SADT Incluídos
- Taxas Incluídas
- Terapias Incluídas
- Honorário Médico Excluído
- Diárias e Serviços Excluído
- Gasoterapia Excluída
- Home Care Excluído
- Procedimentos Excluídos
- Materiais Excluído
- Medicamentso Excluído
- Remoção Excluído
- SADT Excluído
- Taxas Excluído
- Terapias Excluído
""",
    "str_output": {
      "type": "ARRAY",
      "items": {
        "type": "OBJECT",
        "properties": {
          "Código do Pacote": {
            "type": "STRING",
            "description": "O código do Pacote."
          },
          "Código TUSS do Pacote": {
            "type": "STRING",
            "description": "O código TUSS do Pacote."
          },
          "Descrição do Pacote": {
            "type": "STRING",
            "description": "Descrição do Pacote."
          },
          "Valor do Pacote": {
            "type": "STRING",
            "description": "Valor do Pacote."
          },
          "Honorário Médico": {
            "type": "STRING",
            "description": "Honorário Médico."
          },
          "Regime de Atendimento": {
            "type": "STRING",
            "description": "O Regime de Atendimento."
          },
          "Acomodação": {
            "type": "STRING",
            "description": "O tipo de acomodação."
          },
          "Quantidade de Diárias": {
            "type": "STRING",
            "description": "A Quantidade de Diárias."
          },
          "Categoria Principal da Autorização": {
            "type": "STRING",
            "description":"A Categoria Principal da Autorização."
          },
          "Categoria Secundária da Autorização": {
            "type": "STRING",
            "description":"A Categoria Secundária da Autorização."
          },
          "Honorário Médico Incluído": {
            "type": "STRING",
            "description":"Os honorários médicos incluídos."
          },
          "Diárias e Serviços Incluídos": {
            "type": "STRING",
            "description":"As diárias e os serviços incluídos."
          },
          "Gasoterapia Incluída": {
            "type": "STRING",
            "description":"A gasoterapia incluída."
          },
          "Home Care Incluído": {
            "type": "STRING",
            "description":"O Home Care incluído."
          },
          "Procedimentos Incluídos": {
            "type": "STRING",
            "description":"Os procedimentos incluídos."
          },
          "Materiais Incluídos": {
            "type": "STRING",
            "description":"Os materiais incluídos."
          },
          "Medicamentos Incluídos": {
            "type": "STRING",
            "description":"Os medicamentos incluídos."
          },
          "Remoção Incluída": {
            "type": "STRING",
            "description":"A remoção incluída."
          },
          "SADT Incluído": {
            "type": "STRING",
            "description":"O SADT incluído."
          },
          "Taxas Incluídas": {
            "type": "STRING",
            "description":"As taxas incluídas."
          },
          "Terapias Incluídas": {
            "type": "STRING",
            "description":"As terapias incluídas."
          },

            "Honorário Médico Excluído": {
            "type": "STRING",
            "description":"Os honorários médicos excluídos."
          },
          "Diárias e Serviços Excluídos": {
            "type": "STRING",
            "description":"As diárias e os serviços excluídos."
          },
          "Gasoterapia Excluída": {
            "type": "STRING",
            "description":"A gasoterapia excluídas."
          },
          "Home Care Excluído": {
            "type": "STRING",
            "description":"O Home Care excluído."
          },
          "Procedimentos Excluídos": {
            "type": "STRING",
            "description":"Os procedimentos excluídos."
          },
          "Materiais Excluídos": {
            "type": "STRING",
            "description":"Os materiais excluídos."
          },
          "Medicamentos Excluídos": {
            "type": "STRING",
            "description":"Os medicamentos excluídos."
          },
          "Remoção Excluída": {
            "type": "STRING",
            "description":"A remoção excluída."
          },
          "SADT Excluído": {
            "type": "STRING",
            "description":"O SADT excluído."
          },
          "Taxas Excluídas": {
            "type": "STRING",
            "description":"As taxas excluída."
          },
          "Terapias Excluídas": {
            "type": "STRING",
            "description":"As terapias excluídas."
          },


        }
      }
    }
    },
    {
    "task_name": "Tabela_de_Diárias_e_Taxas_Tabela_Própria",
    "command": 
"""Analise o documento completamente.
Identifique o Anexo que contem a tabela de serviços.
Desta tabela, identifique os atributos contidos e os liste de maneira estruturada.
""",
    "str_output": {
      "type": "ARRAY",
      "items": {
        "type": "OBJECT",
        "properties": {
          "Codigo do Produto": {
            "type": "STRING",
            "description": "O código do Produto."
          },
          "Descrição do Produto": {
            "type": "STRING",
            "description": "A descrição do Produto."
          },
          "Valor do Produto": {
            "type": "STRING",
            "description": "O valor do produto."
          }


        }
      }
    }
    },
    {
    "task_name": "Contrato_03_Tabela_de_Preços",
    "command": 
"""Analise o documento completamente.
Identifique o Anexo que contem a tabela de preços.
Desta tabela, identifique os atributos contidos e os liste de maneira estruturada todo seu conteúdo.
""",
    "str_output": {
      "type": "ARRAY",
      "items": {
        "type": "OBJECT",
        "properties": {
          "Tipo do Exame": {
            "type": "STRING",
            "description": "O tipo do Exame."
          },
          "Código CBHPM do Exame": {
            "type": "STRING",
            "description": "Código CBHPM do Exame."
          },
          "Descrição do Exame": {
            "type": "STRING",
            "description": "A descrição do Exame."
          },
          "Valor do Exame": {
            "type": "STRING",
            "description": "O valor do exame."
          }


        }
      }
    }
    }
]
def populate_ai_tasks():
    # Inicializa o cliente Firestore
    db = firestore.Client()
    
    # Referência para a coleção
    collection_name = "ai_tasks"
    
    # Dados de exemplo para popular

    for task in tasks:
        # Extrai o nome para usar como ID do documento
        doc_id = task["task_name"]
        
        # Cria a referência do documento com o ID customizado
        doc_ref = db.collection(collection_name).document(doc_id)
        
        # Dados a serem salvos (excluindo o nome se não quiser duplicar dentro do doc)
        data = {
            "command": task["command"],
            "str_output": task["str_output"] # O Firestore aceita dicts como Maps/JSON
        }
        
        try:
            doc_ref.set(data)
            print(f"Sucesso: Documento '{doc_id}' criado/atualizado.")
        except Exception as e:
            print(f"Erro ao criar '{doc_id}': {e}")

if __name__ == "__main__":
    populate_ai_tasks()