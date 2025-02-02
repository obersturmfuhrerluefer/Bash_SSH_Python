import paramiko1
import time

# Конфигурация для подключения
host = "192.168.1.58"
username = "username"
password = "P@ssw0rd!"
script_path = "/home/username/ssh_connect/script.sh"

# Создаем SSH клиент
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    # Подключаемся к серверу
    client.connect(host, username=username, password=password)
    print("[+] Успешное подключение к серверу")

    # Открывает интерактивную оболочку
    shell = client.invoke_shell()
    time.sleep(1)  # Ждем открытия shell

    # Запускает .sh-скрипт
    shell.send(f"bash {script_path}\n")

    # Читаем вывод скрипта
    time.sleep(2)  # Даем время на выполнение скрипта (оптимальное значение от 2-х сек)
    output = shell.recv(1024).decode("utf-8")
    print(output, end="")

    # Ожидаем ввод пользователя
    user_input = input("Введите значение для скрипта: ")
    shell.send(user_input + "\n")

    # Читаем оставшийся вывод
    time.sleep(2)
    output = shell.recv(4096).decode("utf-8")
    print(output, end="")

    # Теперь оставляем пользователя в интерактивной оболочке
    print("[+] Теперь вы в интерактивной SSH-сессии. Введите команды:")
    
    while True:
        command = input("$ ")
        if command.lower() == "exit":
            break
        shell.send(command + "\n")
        time.sleep(1)
        output = shell.recv(4096).decode("utf-8")
        print(output, end="")

except Exception as e:
    print(f"[!] Ошибка: {e}")
finally:
    client.close()
