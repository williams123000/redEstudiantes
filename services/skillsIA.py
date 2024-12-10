import requests
import json

def getAISkillCategory(skill):
    function_url = "https://foha3sddjbmtcipwmxsp2qwzyq0coccy.lambda-url.us-east-1.on.aws/"

    prompt = f"Estoy analizando habilidades (Skills) para clasificarlas en Disciplinares y Transversales. ¿'{skill}' en cual clasificación entraria? Responde solo la clasificación, es decir, solo Transversal o Disciplinaria, sin agregar caracteres de más."
    # Datos que quieres enviar
    payload = {
        "prompt": prompt,
    }

    headers = {
        "Content-Type": "application/json"
    }

    response = requests.post(function_url, headers=headers, data=json.dumps(payload))

    # Manejo de la respuesta
    if response.status_code == 200:
        print("Respuesta exitosa:")
        print(response.json())
        response = response.json()
        determinedCategory = response['response']['content'][0]['text']
        return determinedCategory
    else:
        print(f"Error ({response.status_code}):")
        print(response.text)
        return None