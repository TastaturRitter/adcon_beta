import requests
import os
import json

BASE_URL = "http://127.0.0.1:8000"
LOGIN_URL = f"{BASE_URL}/api/auth/login/"
UPLOAD_URL = f"{BASE_URL}/api/documents/"

# Credenciales (Admin)
auth_data = {
    "username": "admin",
    "password": "admin"
}

def run_test():
    print(f"--- Iniciando Verificación de Endpoints Adcon ---")
    
    # 1. Login para obtener JWT
    print(f"1. Solicitando JWT a {LOGIN_URL}...")
    try:
        response = requests.post(LOGIN_URL, json=auth_data)
        response.raise_for_status()
        tokens = response.json()
        access_token = tokens['access']
        print(f"   [OK] JWT obtenido exitosamente.")
        print(f"   [DEBUG] Role en respuesta: {tokens['user']['role']}")
    except Exception as e:
        print(f"   [ERROR] Falló el login: {e}")
        if 'response' in locals():
            print(f"   [DEBUG] Detalle: {response.text}")
        return

    # 2. Crear archivo dummy
    dummy_file_path = "dummy_contrato.pdf"
    with open(dummy_file_path, "w") as f:
        f.write("%PDF-1.4\n% Dummy PDF for Adcon Testing\n%%EOF")
    print(f"2. Archivo dummy creado: {dummy_file_path}")

    # 3. Subir archivo vía POST
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    payload = {
        "title": "Verificación Técnica: Contrato de Prueba v1"
    }
    files = {
        "file": open(dummy_file_path, "rb")
    }

    print(f"3. Enviando POST a {UPLOAD_URL} (multipart/form-data)...")
    try:
        upload_resp = requests.post(UPLOAD_URL, data=payload, files=files, headers=headers)
        upload_resp.raise_for_status()
        result = upload_resp.json()
        print(f"   [OK] Archivo subido exitosamente.")
        print(f"   [RESULTADO JSON]:")
        print(json.dumps(result, indent=4))
        
        # Verificaciones solicitadas
        print(f"\n--- Verificaciones de Integridad ---")
        print(f"Role/User ID en 'uploaded_by': {result.get('uploaded_by')}")
        print(f"Ubicación del archivo (file): {result.get('file')}")
        
    except Exception as e:
        print(f"   [ERROR] Falló la subida: {e}")
        if 'upload_resp' in locals():
            print(f"   [DEBUG] Detalle: {upload_resp.text}")
    finally:
        files['file'].close()
        if os.path.exists(dummy_file_path):
            os.remove(dummy_file_path)

if __name__ == "__main__":
    run_test()
