import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import pywhatkit
import random
import time
import os
import pyautogui
import psutil
import re
import screeninfo

# Инициализация голосового движка
engine = pyttsx3.init()
engine.setProperty('rate', 180)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
steam_path = "C:\\Program Files (x86)\\Steam\\steam.exe"

# Настройки браузеров
BROWSERS = {
    'yandex': {
        'path': 'C:/Users/LACRIKA/AppData/Local/Yandex/YandexBrowser/Application/browser.exe',
        'process': 'browser.exe',
        'search_url': 'https://yandex.ru/search/?text='
    },
    'chrome': {
        'path': 'C:/Program Files/Google/Chrome/Application/chrome.exe',
        'process': 'chrome.exe',
        'search_url': 'https://www.google.com/search?q='
    },
    'edge': {
        'path': 'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe',
        'process': 'msedge.exe',
        'search_url': 'https://www.bing.com/search?q='
    },
    'firefox': {
        'path': 'C:/Program Files/Mozilla Firefox/firefox.exe',
        'process': 'firefox.exe',
        'search_url': 'https://www.google.com/search?q='
    }
}

# Регистрируем браузеры
for name, data in BROWSERS.items():
    webbrowser.register(name, None, webbrowser.BackgroundBrowser(data['path']))

# Очередь открытых браузеров
opened_browsers = []
current_volume = 50  # Текущая громкость (0-100)

def speak(text, print_only=False):
    print(f"[Ассистент]: {text}")
    if not print_only:
        engine.say(text)
        engine.runAndWait()

def manage_windows(command):
    try:
        if "запусти deadlock" in command.lower() or "запусти дедлок" in command.lower():
            os.startfile(f'steam://rungameid/1422450')  # ID Deadlock
            speak("Запускаю Deadlock через Steam", print_only=True)
            time.sleep(10)  # Даем время на запуск
            pyautogui.hotkey('alt', 'enter')
            return True
        monitors = pyautogui.getAllWindows()
        
        if len(monitors) < 2:
            speak("У вас только один монитор", print_only=True)
            return False

        if "перенеси на второй экран" in command or "перенеси направо" in command:
            for _ in range(2):  # Двойное нажатие для гарантированного переноса
                pyautogui.hotkey('win', 'shift', 'left')
                time.sleep(0.2)
            speak("Окно перенесено на первый экран", print_only=True)
            
        elif "перенеси на первый экран" in command or "перенеси налево" in command:
            # Перемещаем на первый монитор (Win+Shift+Left)
            
            pyautogui.hotkey('win', 'shift', 'left')
            speak("Окно перенесено на первый экран", print_only=True)
            
        elif "сверни окно" in command or "сверни" in command:
            # Сворачиваем активное окно (Win+Down)
            pyautogui.hotkey('win', 'down')
            speak("Окно свернуто", print_only=True)
            
        elif "разверни окно" in command or "разверни" in command:
            # Разворачиваем активное окно (Win+Up)
            pyautogui.hotkey('win', 'up')
            speak("Окно развернуто", print_only=True)

        elif "закрой" in command or "закрой окно" in command:
            pyautogui.hotkey('alt', 'f4')  
            speak('Окно закрыто')
            
        return True
    
    except Exception as e:
        print(f"Ошибка управления окнами: {e}")
        return False

def listen(timeout=3, phrase_time_limit=3):
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=0.5)
        try:
            print("Слушаю...", end='\r', flush=True)
            audio = r.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
            query = r.recognize_google(audio, language="ru-RU").lower()
            print(f"[Вы]: {query}")
            return query
        except (sr.WaitTimeoutError, sr.UnknownValueError):
            return None
        except Exception as e:
            print(f"Ошибка распознавания: {e}", flush=True)
            return None

def open_browser(browser_name=None, url=None):
    try:
        if not browser_name:
            browser_name = 'yandex'
            
        if browser_name in BROWSERS:
            if not url:
                url = BROWSERS[browser_name]['search_url']
            webbrowser.get(browser_name).open(url)
            opened_browsers.append(browser_name)
            speak(f"Открыл {browser_name}", print_only=True)
            return True
        else:
            speak(f"Браузер {browser_name} не поддерживается", print_only=True)
            return False
    except Exception as e:
        print(f"Ошибка открытия браузера: {e}")
        return False

def close_browser(browser_name=None):
    try:
        if not browser_name and opened_browsers:
            browser_name = opened_browsers[-1] if opened_browsers else None
        
        if browser_name in BROWSERS:
            proc_name = BROWSERS[browser_name]['process']
            closed = False
            
            for proc in psutil.process_iter(['pid', 'name']):
                if proc.info['name'].lower() == proc_name:
                    try:
                        proc.kill()
                        closed = True
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        continue
            
            if closed:
                speak(f"Закрыл {browser_name}", print_only=True)
                opened_browsers[:] = [b for b in opened_browsers if b != browser_name]
                return True
            else:
                speak(f"Браузер {browser_name} не найден", print_only=True)
                return False
        else:
            speak("Укажите браузер для закрытия", print_only=True)
            return False
    except Exception as e:
        print(f"Ошибка закрытия браузера: {e}")
        return False

def music(command):
    if "некст" in command or "next" in command:
        pyautogui.press('nexttrack')
        
    elif "остонови" in command or "пауза" in command or "стоп" in command:
        pyautogui.press('playpause')
        speak("Пауза")
        
    elif "назад" in command or "прошлое" in command:
        pyautogui.press('prevtrack')
        pyautogui.press('prevtrack')
        speak("Back")
        
    elif "заново" in command:
        pyautogui.press('prevtrack')
        speak("Заново")
        
def set_volume(level=None, change=None):
    global current_volume
    
    try:
        if level is not None:
            current_volume = max(0, min(100, int(level)))
            pyautogui.press('volumemute')
            for _ in range(50):
                pyautogui.press('volumedown')
            for _ in range(current_volume // 2):
                pyautogui.press('volumeup')
            speak(f"Установил громкость на {current_volume}%", print_only=True)
        elif change is not None:
            new_volume = max(0, min(100, current_volume + int(change)))
            steps = abs(new_volume - current_volume) // 2
            if new_volume > current_volume:
                for _ in range(steps):
                    pyautogui.press('volumeup')
            else:
                for _ in range(steps):
                    pyautogui.press('volumedown')
            current_volume = new_volume
            speak(f"Громкость {'увеличена' if change > 0 else 'уменьшена'} до {current_volume}%", print_only=True)
            return True 
    except Exception as e:
        print(f"Ошибка изменения громкости: {e}")
        return False

def extract_number(command):
    numbers = re.findall(r'\d+', command)
    return int(numbers[0]) if numbers else None


def handle_command(command):
    command = command.lower()
    
    
    # Управление браузерами
    if any(w in command for w in ["открой браузер", "запусти браузер", "открыть браузер"]):
        if "хром" in command or "chrome" in command or "кром" in command:
            open_browser('chrome')
        elif "edge" in command or "эдж" in command:
            open_browser('edge')
        elif "firefox" in command or "файерфокс" in command:
            open_browser('firefox')
        elif "яндекс" in command or "я" in command:
            open_browser('yandex')
        else:
            # Если просто "открой браузер" без уточнения
            if "браузер" in command:
                open_browser('chrome')  # По умолчанию открываем Chrome
            else:
                # Если команда типа "открой chrome"
                for browser in BROWSERS:
                    if browser in command:
                        open_browser(browser)
                        break
                else:
                    open_browser('chrome')  # По умолчанию Chrome
    
    #перенос окон
    if any(w in command for w in ["перенеси окно", "сверни окно", "разверни окно", "разверни ок", "сверни ок","перенеси ок", "разверни", "сверни","перенеси","закрой","закрой окно"]):
        return manage_windows(command)
    elif  "запусти deadlock" in command or "запусти дедлок" in command:
        return manage_windows(command)


    # Закрытие браузеров
    elif any(w in command for w in ["закрой браузер", "закрыть браузер", "выключи браузер"]):
        if "хром" in command or "chrome" in command:
            close_browser('chrome')
        elif "edge" in command or "эдж" in command:
            close_browser('edge')
        elif "firefox" in command or "файерфокс" in command:
            close_browser('firefox')
        elif "яндекс" in command:
            close_browser('yandex')
        elif "все" in command:
            while opened_browsers:
                close_browser(opened_browsers[-1])
        else:
            close_browser()
    
    # Управление звуком
    elif any(w in command for w in ["установи громкость", "поставь громкость", "громкость на"]):
        level = extract_number(command)
        if level is not None:
            set_volume(level=level)
        else:
            speak("Укажите уровень громкости от 0 до 100", print_only=True)
    elif any(w in command for w in ["увеличь громкость на", "добавь громкости на", "повысь громкость на"]):
        change = extract_number(command)
        if change is not None:
            set_volume(change=change)
        else:
            speak("Укажите на сколько увеличить громкость", print_only=True)
    elif any(w in command for w in ["уменьши громкость на", "убавь громкости на"]):
        change = extract_number(command)
        if change is not None:
            set_volume(change=-change)
        else:
            speak("Укажите на сколько уменьшить громкость", print_only=True)
    elif "выключи звук" in command:
        set_volume(level=0)
    elif "включи звук" in command:
        set_volume(level=50)
    elif any(w in command for w in ["увеличь громкость", "увеличь звук", "громче"]):
        set_volume(change=25)
    elif any(w in command for w in ["уменьши громкость", "уменьши звук", "тише"]):
        set_volume(change=-25)
    elif "next" in command or "некст" in command:
        music(command)
    elif "остонови" in command or "пауза" in command or "стоп" in command:
        music(command)
    elif "назад" in command or "прошлое" in command:
        music(command)
    elif "заново" in command:
        music(command)
    
    # Видео и другие команды
    
    # Основные команды
    elif any(w in command for w in ["привет", "здаров", "здравствуй"]):
        speak("Приветствую!")
    elif any(w in command for w in ["как дела", "как ты", "как работаешь"]):
        speak("Работаю в штатном режиме")
    elif any(w in command for w in ["время", "который час", "сколько времени"]):
        current_time = datetime.datetime.now().strftime("%H:%M")
        speak(f"Сейчас {current_time}")
    elif any(w in command for w in ["найди в интернете", "найди", "поищи"]):
        search = command.split("найди")[-1].strip()
        if search:
            speak(f"Ищу {search}", print_only=True)
            webbrowser.get('yandex').open(BROWSERS['yandex']['search_url'] + search)
    elif any(w in command for w in ["открой ютуб", "ютуб", "youtube"]):
        speak("Открываю YouTube", print_only=True)
        webbrowser.get('yandex').open("https://youtube.com")
    elif any(w in command for w in ["выход", "закройся", "отключись"]):
        speak("До свидания!")
        return False
    else:
        print(f"Не распознана команда: {command}", flush=True)
    
    return True

def main():
    trigger_words = ["джарвес", "jarves", "джарвис"]
    active = False
    
    speak("Готов к работе! Скажите мое имя для активации")
    
    while True:
        try:
            query = listen(timeout=1)  # Короткий таймаут для ожидания активации
            
            if query and any(trigger in query for trigger in trigger_words):
                active = True
                speak("Да, слушаю вас!")
                
            while active:
                command = listen(phrase_time_limit=5)  # Увеличенный лимит для команд
                
                if command:
                    if any(trigger in command for trigger in trigger_words):
                        speak("Да, слушаю вас!")
                        continue
                        
                    if not handle_command(command):
                        active = False
                        break
                else:
                    print("...", end='\r', flush=True)  # Индикатор ожидания без спама в консоль
                    
        except KeyboardInterrupt:
            speak("Выключаюсь")
            break

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Ошибка: {e}")
        input("Нажмите Enter для выхода...")
