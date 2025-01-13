import requests
import json  # Importujeme knihovnu JSON

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
                    # Používáme json.loads místo eval
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

if __name__ == "__main__":
    # Příklad použití
    prompt = "Ahoj, jak se máš?"
    print("Odesílám dotaz modelu Ollama...")
    response = query_ollama(prompt)
    print("\nOdpověď modelu:")
    print(response)
