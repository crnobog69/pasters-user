import http.client
import json
import os
from datetime import datetime  # Увежи модул datetime

# Дефиниција имена конфигурационе и историјске датотеке
CONFIG_FILE = os.path.join(os.path.dirname(__file__), 'config.json')  # Конфигурациона датотека у истом директоријуму
DEFAULT_HISTORY_FILE = os.path.join(os.path.dirname(__file__), 'history.json')  # Подразумевана локација за history.json

def create_paste(content: str) -> str:
    conn = http.client.HTTPSConnection("paste.rs")
    
    headers = {
        'Content-Type': 'text/plain; charset=utf-8',  # Додајемо charset=utf-8
    }
    
    # Шаљемо POST захтев, кодирано у UTF-8
    conn.request("POST", "/", body=content.encode('utf-8'), headers=headers)
    
    response = conn.getresponse()
    
    # Проверимо статус код
    if response.status in [200, 201]:
        paste_url = response.read().decode('utf-8').strip()
        conn.close()
        return paste_url  # Ово је линк до пасте
    else:
        conn.close()
        raise Exception(f"Failed to create paste. Status code: {response.status}")

def save_to_history(paste_url: str, note: str, history_file: str):
    # Добити тренутни датум и време у формату дан-месец-година
    timestamp = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
    
    # Проверимо да ли фајл постоји
    if os.path.exists(history_file):
        with open(history_file, 'r', encoding='utf-8') as file:
            history = json.load(file)
    else:
        history = []
    
    # Додај нову пасту у историју
    history.append({
        'url': paste_url,
        'timestamp': timestamp,
        'note': note  # Додајемо белешку из корисничког уноса
    })
    
    # Сачувај ажурирану историју назад у JSON фајл
    with open(history_file, 'w', encoding='utf-8') as file:
        json.dump(history, file, ensure_ascii=False, indent=4)  # ensure_ascii=False да би ћирилица остала

def load_config() -> str:
    """Учитава конфигурациону датотеку и враћа локацију history.json."""
    if not os.path.exists(CONFIG_FILE):
        # Ако конфигурациона датотека не постоји, користи подразумевану локацију
        history_path = DEFAULT_HISTORY_FILE
        
        # Сачувамо у конфигурационој датотеци
        config = {'history_file': history_path}
        with open(CONFIG_FILE, 'w', encoding='utf-8') as config_file:
            json.dump(config, config_file, ensure_ascii=False, indent=4)
        
        print(f"Конфигурациона датотека '{CONFIG_FILE}' је креирана са подразумеваном локацијом: {history_path}.")
        return history_path

    # Учитавање постојеће конфигурационе датотеке
    with open(CONFIG_FILE, 'r', encoding='utf-8') as config_file:
        config = json.load(config_file)
        return config.get('history_file', DEFAULT_HISTORY_FILE)  # Враћа локацију за history.json

def main():
    # Учитај конфигурацију
    history_file_path = load_config()
    
    # Унос текста од корисника
    paste_content = input("Унесите текст који желите да објавите: ")

    if paste_content:  # Проверимо да ли је унос празан
        print(f"Ваш унети текст:\n{paste_content}")
        
        # Креирање пасте на paste.rs
        try:
            paste_link = create_paste(paste_content)
            print(f"Ваша паста је доступна на: {paste_link}")
            
            # Чување линка пасте у JSON историји
            save_to_history(paste_link, paste_content, history_file_path)  # Користимо paste_content као белешку
        except Exception as e:
            print(e)
    else:
        print("Нисте унели текст. Молимо вас да покушате поново.")

if __name__ == '__main__':
    main()
