import requests
import json
import time  # Importujeme pro měření času

def list_ollama_models():
    """
    Ručně zadaný seznam dostupných modelů.
    """
    return ["takenusername/tinyllm-2:latest", "hollis9/czellama3:latest"]

def query_ollama(prompt, model_name):
    """
    Pošle požadavek na Ollama server a vrátí odpověď jako celek.
    """
    url = "http://localhost:11434/api/generate"
    headers = {"Content-Type": "application/json"}
    data = {"model": model_name, "prompt": prompt}

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
    print("\033[34mNačítám seznam dostupných modelů...\033[0m")
    models = list_ollama_models()
    if not models:
        print("\033[31mŽádné modely nebyly nalezeny. Ujisti se, že Ollama server běží a má nainstalované modely.\033[0m")
        return

    print("\033[34mDostupné modely:\033[0m")
    for idx, model in enumerate(models, 1):
        print(f"{idx}. {model}")

    # Zvol model
    while True:
        try:
            choice = int(input("\033[33mZadej číslo modelu, který chceš použít:\033[0m "))
            if 1 <= choice <= len(models):
                selected_model = models[choice - 1]
                break
            else:
                print("\033[31mNeplatná volba. Zkus to znovu.\033[0m")
        except ValueError:
            print("\033[31mNeplatný vstup. Zadej číslo.\033[0m")

    print(f"\033[34mPoužíváš model: {selected_model}\033[0m")

    # Chatovací smyčka
    print("\033[34mOllama Chat\nZadej 'exit' pro ukončení.\033[0m")
    while True:
        user_input = input("\033[32mTy:\033[0m ")
        if user_input.lower() == "exit":
            print("\033[34mChat ukončen. Nashledanou!\033[0m")
            break

        # Odeslat dotaz modelu
        print("\033[33mOllama přemýšlí...\033[0m")
        start_time = time.time()
        response = query_ollama(user_input, selected_model)
        end_time = time.time()

        # Zobraz odpověď
        if response:
            print(f"\033[35mOllama:\033[0m {response}")
            elapsed_time = end_time - start_time
            minutes, seconds = divmod(int(elapsed_time), 60)
            print(f"\033[36mOdpověď vygenerována za: {elapsed_time:.2f} sekundy ({minutes} minuty a {seconds} sekundy)\033[0m")
        else:
            print("\033[31mChyba: Žádná odpověď od modelu.\033[0m")

if __name__ == "__main__":
    chat_with_ollama()
