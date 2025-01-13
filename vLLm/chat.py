import requests
import json

def query_ollama(prompt):
    """
    Pošle požadavek na Ollama server a vrátí odpověď jako celek.
    """
    url = "http://localhost:11434/api/generate"
    headers = {"Content-Type": "application/json"}
    data = {"model": "gemma2:2b", "prompt": prompt}

    response = requests.post(url, json=data, headers=headers, stream=True)
    if response.status_code == 200:
        full_response = ""
        for line in response.iter_lines():
            if line:
                chunk = line.decode('utf-8')
                try:
                    chunk_data = json.loads(chunk)
                    if "response" in chunk_data:
                        full_response += chunk_data["response"]
                    if chunk_data.get("done"):
                        break
                except json.JSONDecodeError as e:
                    print(f"Chyba při dekódování JSON: {e}")
        return full_response.strip()
    else:
        print(f"Chyba při komunikaci s Ollama serverem: {response.status_code}")
        return None

def chat_with_ollama():
    """
    Funkce umožňuje chatovat s Ollama modelem.
    """
    print("\033[34mOllama Chat\nZadej 'exit' pro ukončení.\033[0m")
    while True:
        # Zadej otázku
        user_input = input("\033[32mTy:\033[0m ")
        if user_input.lower() == "exit":
            print("\033[34mChat ukončen. Nashledanou!\033[0m")
            break

        # Odeslat dotaz modelu
        print("\033[33mOllama přemýšlí...\033[0m")
        response = query_ollama(user_input)

        # Zobraz odpověď
        if response:
            print(f"\033[35mOllama:\033[0m {response}")
        else:
            print("\033[31mChyba: Žádná odpověď od modelu.\033[0m")

if __name__ == "__main__":
    chat_with_ollama()
