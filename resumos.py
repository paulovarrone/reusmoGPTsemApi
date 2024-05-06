import PyPDF2
import os
from openai import OpenAI
import fitz

client = OpenAI(api_key='SUA CHAVE AQUI') 

# def extract_text_from_pdf(pdf_file):
#   pdf_text = ""
#   pdf_reader = PyPDF2.PdfReader(pdf_file)
#   for page in pdf_reader.pages:
#     pdf_text += page.extract_text()
#     return pdf_text

def extract_text_from_pdf(pdf_path):
  try:

    text = ""

    with fitz.open(pdf_path) as pdf_file:
      for page in pdf_file: 
        text += page.get_text()

    return text
  
  except Exception:
    print("ERRO AO TENTAR EXTRAIR TEXTO")

def resposta(caminho_pdf, caminho_resumos):
  caminho_pasta = os.path.isdir(caminho_pdf)
  conteudo_pasta = os.listdir(caminho_pdf)

  if caminho_pasta:
    # Criar a pasta "resumos" se ela não existir
    if not os.path.exists(caminho_resumos):
      os.makedirs(caminho_resumos)

    for arquivo in conteudo_pasta:
      caminho_arquivos = os.path.join(caminho_pdf, arquivo)
      file_path = caminho_arquivos
      
      if file_path.endswith('.pdf'):
        text = extract_text_from_pdf(file_path)
        completion = client.chat.completions.create(
          model="gpt-3.5-turbo-0125",
          messages=[
            {"role": "system", "content": "Você é especialista em resumir informações de documentos e extrair minuciosamente as informações pedidas."},
            {"role": "user", "content": "Resuma o arquivo."},
            {"role": "assistant", "content": text}
          ]
        )
                
        resumo = completion.choices[0].message.content

        # Nome do arquivo de texto para salvar o resumo
        txt_file_name = os.path.splitext(arquivo)[0] + "_resumo.txt"

        # Caminho completo para o arquivo de texto na pasta "resumos"
        txt_file_path = os.path.join(caminho_resumos, txt_file_name)

        # Escreve o resumo no arquivo de texto
        with open(txt_file_path, 'w', encoding='utf-8') as txt_file:
          txt_file.write(resumo)

# Caminho PDF
caminho_pdf = r'C:\Users\3470622\Desktop\Workspace\pgm testes\pdfs\DirTrein'

# Caminho resumos
caminho_resumos = r'C:\Users\3470622\Desktop\Workspace\pgm testes\ResumoPDF sem api\resumos'


resposta(caminho_pdf, caminho_resumos)
