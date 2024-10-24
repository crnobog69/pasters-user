import http.client
import json
import os
from datetime import datetime  # Увежи модул datetime

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

def read_txt_file(file_path: str) -> str:
    # Проверимо да ли фајл постоји
    if not os.path.exists(file_path):
        # Ако не постоји, креирамо нови .txt фајл
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write("Ово је пример текста. Молим вас измените садржај.")  # Упутство
        print(f"Креиран фајл: {file_path} са подразумеваним садржајем.")
        return ""  # Враћамо празан садржај ако је фајл ново креиран
    
    # Читање садржаја из .txt фајла
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def save_to_history(paste_url: str, note: str, history_file: str = 'history.json'):
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
        'note': note  # Додајемо белешку из txt фајла
    })
    
    # Сачувај ажурирану историју назад у JSON фајл
    with open(history_file, 'w', encoding='utf-8') as file:
        json.dump(history, file, ensure_ascii=False, indent=4)  # ensure_ascii=False да би ћирилица остала

def main():
    txt_file_path = 'input.txt'  # Унеси пут до свог txt фајла
    history_file_path = 'history.json'  # Фајл где ће се чувати историја паста

    # Читање садржаја из .txt фајла
    paste_content = read_txt_file(txt_file_path)

    # Испис садржаја у конзолу
    if paste_content:  # Исписује се само ако фајл већ постоји
        print(f"Садржај вашег txt фајла:\n{paste_content}")
        
        # Креирање пасте на paste.rs
        try:
            paste_link = create_paste(paste_content)
            print(f"Ваша паста је доступна на: {paste_link}")
            
            # Чување линка пасте у JSON историји
            save_to_history(paste_link, paste_content, history_file_path)  # Користимо paste_content као белешку
        except Exception as e:
            print(e)
    else:
        print("Фајл не садржи текст. Молимо вас да измените садржај.")

if __name__ == '__main__':
    main()
