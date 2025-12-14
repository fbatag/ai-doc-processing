import json
from google.cloud import firestore

tasks = [
        {
        "task_name": "SADT_instruction",
        "command": 
"""Você é uma especialista médica brasileira.

Sua tarefa é ler com precisão os documentos fornecidos e extrair as informações solicitadas.
Um arquivo pode ter mais de um tipo de documento agregado. Por exemplo, um pedido de exames com uma carteirinha de plano de saúde ou um pedido de exames com seu resultado associado.
Alguns documentos vão ter o número da guia no prestador, registro ANS e código na operadora, então tome cuidado para não confundi-los com as chaves solicitadas.
As informações que precisam ser extraídas geralmente estão preenchidas à mão com letra cursiva ou de médico.
Sempre que não encontrar alguma chave, preencha como nulo "null".
Se o valor do campo estiver pouco legível, não tente inferir, deixe como "null".
Sua resposta deve conter as seguintes chaves: 
1) content: um array onde com cada linha da tabela será um elemento composto com os campos abaixo, cada um extraído como um valor da coluna daquela linh. Essa tabela vem logo abaixo da secção "DADOS DA SOLICITAÇÃO / PROCEDIMENTOS E EXAMES SOLICITADOS".
  1.1) name: O valor do campo da coluna de número 27 chamado "Descrição" ou "Descrição do Procedimento"; 
  1.2) code: O valor do campo da coluna de numerada como 26 cujo título é "Código do Procedimento" ou "Cód. do Procedimento". O valor extraído deve estar logo abaixo do título. Não usar valores de outros lugares. Esse campo é obrigatoriamente numérico de 8 digitos, pondedo ter zeros a esquerda ou estar vazio. Estando vazio, preencher com "null;
  1.3) qty: O valor do campo da coluna de número 28 normalmente chamado de "Qtde.Solic."
  1.4) prepassword: O campo chamado "Pré-Senha", próxima a "Descrição do Procedimento", campo 27;
2) guideNumber: o número da guia. Ele pode ser o número no campo Nº Guia Principal (geralmente campo 3) ou o número no topo direito da guia;
3) beneficiaryName: o nome da pessoa que está no campo "Nome do Beneficiário" ou simplesmente "Nome" (geralmente campo 11);
4) password: um código com letras e muneros que vem no campo "Senha" (geralmente campo 5).
5) crm: número que vem depois da palavra CRM e geralmente tem de 5 à 6 dígitos numéricos, se fornecido, também pode vir no campo Número no Conselho;
6) doctorName: nome do(a) médico(a) que carimbou e/ou assinou o documento;
7) doctorSpecialty: especialidade do(a) médico(a) que carimbou e/ou assinou o documento;
8) cid: código CID-10 é composto por uma letra seguida de dois números (por exemplo, "R10"), podendo aparecer com ou sem ponto ou hífen entre a letra e os números (por exemplo, "A-95"), pode haver espaços em branco, hífens ou outros caracteres antes ou depois do código. Ele pode aparecer perto do nome do procedimento, geralmente no campo "Descrição";
9) requestNature: O campo "Caráter da Solicitação", campo número 22. O valora se preenchido, deve ser somente "E" ou "U". Dentro do campo pode aparecer a explicação do que é o "E" ou o "U" da seguinte forma: "E - Eletiva U - Urgẽncia;Emergência", quando o valor for efeitvamente "E" deve haver um "E" antes dessa explicação. Se houver somente a "E - Eletiva U - Urgẽncia;Emergência" sem um "E" ou "U" anterior, significa que o campo não está preenchido. Deixar com null.
10) clinical: que deve ser extraída do campo "Indicação Clínica" (geralmente no campo 24). Se não encontrar o campo nomeado, tente achar a indicação ou justificativa clínica no documento todo. Ela pode ser a descrição ao lado do campo cid ou após a abrevição "HD". Traga o conteúdo completo do campo.
""",
    "str_output": {
    "type": "OBJECT",
    "properties": {
        "content": {
            "type": "ARRAY",
            "items": {
                "type": "OBJECT",
                "properties": {
                    "name": {
                        "type": "STRING"
                    },
                    "code": {
                        "type": "STRING"
                    },
                    "qty": {
                        "type": "STRING"
                    },
                    "prepassword": {
                        "type": "STRING"
                    }
                }
            }
        },
        "guideNumber": {
            "type": "STRING"
        },
        "beneficiaryName": {
            "type": "STRING"
        },
        "password": {
            "type": "STRING"
        },
        "crm": {
            "type": "STRING"
        },
        "doctorName": {
            "type": "STRING"
        },
        "doctorSpecialty": {
            "type": "STRING"
        },
        "cid": {
            "type": "STRING"
        },
        "requestNature": {
            "type": "STRING"
        },
        "clinical": {
            "type": "OBJECT",
            "properties": {
                "name": {
                    "type": "STRING"
                },
                "code": {
                    "type": "STRING"
                }
            }
        }
    }
    }
    },
{
        "task_name": "OUTRAS_instruction",
        "command": 
"""Você é uma especialista médica brasileira. 

Sua tarefa é ler com precisão os documentos fornecidos e extrair as informações solicitadas. 

<Instruções> 
As caixas de seleção nos documentos podem estar marcadas com um 'X', um '[x]' ou preenchidas. Os procedimentos geralmente estão listados em formato de tabela ou lista com marcadores, com a caixa de seleção na mesma linha ou na linha imediatamente anterior ao nome do procedimento.

Um arquivo pode ter mais de um tipo de documento agregado. Por exemplo, um pedido de exames com uma carteirinha de plano de saúde ou um pedido de exames com seu resultado associado.

Sempre que não encontrar alguma valor, preencha como nulo "null".
Se o valor do campo estiver pouco legível, não tente inferir, deixe como "null"

Sua resposta deve conter as seguintes chaves: 
1) content: uma array onde cada campo é composto por:
  1.1) name: o nome completo do procedimento, exame médico ou encaminhamento para consulta com profissional de saúde solicitado;
  1.2) code: se estiver presente, o código respectivo do procedimento ou exame acima. Este campo deve ser obrigatoriamente numérico e ter 8 digitos, podendo ter zeros a esquerda);
  1.3) qty: a quantidade de solicitações se estiver especificado. Por exemplo, se forem o número de sessões de algum procedimento ou do procedimento em si;
  1.4) prepasswword: Se existir um campo chamado pré-senha ou senha junto ao procedimento encontrado em 1.1
2) guideNumber: pode preencher esse campo com "null"
3) beneficiaryName: o nome do paciente que vai realizar os procedimentos ou exames solicitados;
4) password: pode preencher esse campo com "null"
5) crm: número que costuma vir depois da palavra "CRM", "CRM-[sigla de estado brasileiro]", através de um carimbo com nome do(a) médico(a), parcialmente oculto por uma assinatura ou no campo "Número do Conselho" e geralmente tem de 5 à 6 dígitos numéricos, por exemplo "CRM-DF 12312" o crm é "12312";
6) doctorName: nome do(a) médico(a) que carimbou e/ou assinou o documento;
7) doctorSpecialty: especialidade do(a) médico(a) que carimbou e/ou assinou o documento;
8) cid: código CID-10 é composto por uma letra seguida de dois números (por exemplo, "R10"), podendo aparecer com ou sem ponto ou hífen entre a letra e os números, pode haver espaços em branco, hífens ou outros caracteres antes ou depois do código. Ele pode aparecer próximo a palavras como "Indicação", "Diagnóstico", "Justificativa Clínica", "CID", "CD", "HD" ou "Classificação Internacional de Doenças", mas não é obrigatório;
9) requestNature: pode preencher esse campo com "null";
10) clinical: que deve ser extraída do campo "Indicação Clínica". Se não encontrar o campo nomeado, tente achar a indicação ou justificativa clínica no documento todo. Ela pode ser a descrição ao lado do campo cid ou após a abrevição "HD". Traga o conteúdo completo do campo.
</Instruções>
""",
    "str_output": {
    "type": "OBJECT",
    "properties": {
        "content": {
            "type": "ARRAY",
            "items": {
                "type": "OBJECT",
                "properties": {
                    "name": {
                        "type": "STRING"
                    },
                    "code": {
                        "type": "STRING"
                    },
                    "qty": {
                        "type": "STRING"
                    },
                    "prepassword": {
                        "type": "STRING"
                    }
                }
            }
        },
        "guideNumber": {
            "type": "STRING"
        },
        "beneficiaryName": {
            "type": "STRING"
        },
        "password": {
            "type": "STRING"
        },
        "crm": {
            "type": "STRING"
        },
        "doctorName": {
            "type": "STRING"
        },
        "doctorSpecialty": {
            "type": "STRING"
        },
        "cid": {
            "type": "STRING"
        },
        "requestNature": {
            "type": "STRING"
        },
        "clinical": {
            "type": "OBJECT",
            "properties": {
                "name": {
                    "type": "STRING"
                },
                "code": {
                    "type": "STRING"
                }
            }
        }
    }
}
    },

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