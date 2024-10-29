import random

# Глобальные переменные
inventory = ["Зелье исцеления"]
current_level = 1
solved_puzzles = set()
enemies_defeated = set()
player_health = 15

# Словарь уровней
levels = {
    1: {
        "description": "Ты стоишь в тёмном коридоре. Впереди видны две двери, а на полу блестит ключ.",
        "keys": ["Ключ"],
        "puzzles": [],
        "enemies": [],
        "door_code": ["Ключ"]
    },
    2: {
        "description": "Ты в зале, где стоит страшный гоблин. Он охраняет сундук с сокровищами.",
        "keys": ["Меч"],
        "puzzles": [],
        "enemies": ["Гоблин"],
        "door_code": ["Ключ"]
    },
    3: {
        "description": "Ты в библиотеке. На полке лежат книги с загадочными символами. Загадка: 'Что имеет корни, но не может расти, имеет лист, но не имеет ветвей, имеет кожу, но не имеет плоти?",
        "keys": [],
        "puzzles": ["Загадка"],
        "enemies": [],
        "door_code": ["Ответ"]
    }
}

# Словари для врага
enemies = {
    "Гоблин": {"health": random.randint(25, 30), "attack": 5, "weakness": "Меч"}
}
enemy_forms = {
    "Гоблин": {
        "accusative": "Гоблина",  
        "creative": "Гоблином",  
    }
}

# Словари для предметов
items = {
    "Меч": {
        "damage": 10, "uses": 1
    },   
    "Топор":{
        "damage": 7, "uses": 2
    },
    "Зелье исцеления":{
        "heal": 5
    }
}
items_forms = {
    "Меч":{
        "creative": "Мечом",
        "nominative": "Меч"
    },
    "Топор":{
        "creative": "Топором",
        "nominative": "Топор"
    }
}


# Функция для отображения описания уровня
def show_level_description():
    if current_level == 2 and "Гоблин" in enemies_defeated:
        print("Ты в зале, где лежит мертвый гоблин. Он охранял сундук с сокровищами.")
    else:
        print(levels[current_level]["description"])

# Функция для отображения доступных действий
def show_actions():

    # Создаем пустой список для хранения доступных действий
    actions = []

    # Проверяем наличие ключа, меча, загадки и врагов на текущем уровне
    if "Ключ" in levels[current_level]["keys"]:
        actions.append("Взять ключ")
    if "Меч" in levels[current_level]["keys"]:
        actions.append("Взять меч")
    if "Загадка" in levels[current_level]["puzzles"]:
        actions.append("Решить загадку")
    if levels[current_level]["enemies"]:
        actions.append("Сразиться с врагом")

    # Добавляем действие "Перейти на следующий этаж"
    actions.append("Перейти на следующий этаж")

    print("Доступные действия:")

    # Выводим список доступных действий
    for action in actions:
        print("  " + action)

# Функция для обработки действий игрока
def handle_action(action):
    global inventory, current_level, solved_puzzles, enemies_defeated

    # Проверяем наличие ключа в текущем уровне
    if action == "Взять ключ":

        # Добавляем ключ в инвентарь и удаляем его из уровня
        if "Ключ" in levels[current_level]["keys"]:
            inventory.append("Ключ")
            levels[current_level]["keys"].remove("Ключ")
            print("  Ты взял ключ.")
        else:
            print("  Здесь нет ключа.")

    # Проверяем наличие меча
    elif action == "Взять меч":

        # Добавляем меч в инвентарь и удаляем его из уровня
        if "Меч" in levels[current_level]["keys"]:
            inventory.append("Меч")
            levels[current_level]["keys"].remove("Меч")
            print("  Ты взял меч.")
        else:
            print("  Здесь нет меча.")

    # Проверяем наличие загадки и правильность ответа
    elif action == "Решить загадку":
        if "Загадка" in levels[current_level]["puzzles"]:
            answer = input("  Введите ответ на загадку: ")
            if answer == "Корень":

                # Добавляем загадку в решенные и удаляем ее из уровня
                solved_puzzles.add("Загадка")
                levels[current_level]["puzzles"].remove("Загадка")
                inventory.append("Ответ")
                print("Правильно! Ты разгадал загадку.")
            else:
                print("  Неверный ответ.")
        else:
            print("  Здесь нет загадки.")

    # Проверяем наличие врагов и запускаем бой
    elif action == "Сразиться с врагом":
        if levels[current_level]["enemies"]:

            # Выбираем случайного врага из списка
            enemy = random.choice(levels[current_level]["enemies"])
            fight(enemy)
        else:
            print("  Здесь нет врагов.")

    # Проверяем наличие необходимых предметов для перехода на следующий уровень
    elif action == "Перейти на следующий этаж":
        if all(item in inventory for item in levels[current_level]["door_code"]):

            # Проверяем, не последний ли это уровень
            if current_level < 3:
                current_level += 1
                print("  Ты перешел на следующий этаж.")
            else:
                print("  Ты победил!(Выходишь из замка).")
                exit()
        else:
            print(" Тебе не хватает чего-то, чтобы пройти дальше.")

    else:
        print("Некорректное действие.")

# Функция для боя с врагом
def fight(enemy_type):
    global inventory, enemies_defeated, player_health, current_level

    enemy = enemies[enemy_type]

    # Проверяем, побежден ли Гоблин 
    if "Гоблин" in enemies_defeated:
        print("  Гоблин уже побежден")
    else:
        print("  Ты сражаешься с", enemy_forms[enemy_type]['creative'],"!")

    # Цикл боя, продолжается пока у врага и игрока есть здоровье
    while enemy["health"] > 0 and player_health > 0:

        # Выводим текущее здоровье игрока и врага
        print("У", enemy_forms[enemy_type]['accusative'], "осталось", enemy['health'], "здоровья.")
        print("У тебя осталось", player_health, "здоровья.")

        action = input("  Что ты хочешь сделать? (атаковать/бежать(можно один раз восстановить хп)): ")

        # Если игрок выбрал "атаковать"
        if action == "атаковать":
            
            # Если у игрока есть Меч в инвентаре
            if "Меч" in inventory:

                if items["Меч"]["uses"] > 0:

                    enemy["health"] -= items["Меч"]["damage"]
                    print(f" Ты ударил {enemy_forms[enemy_type]['accusative']} {items_forms['Меч']['creative']}, нанеся {items['Меч']['damage']} единиц урона!")

                    if enemy["health"] > 0:
                        damage = random.randint(1, enemy["attack"])
                        player_health -= damage
                        print(" " + enemy_type, "нанес тебе", damage, "урона!")
                        
                    print("У", enemy_forms[enemy_type]['accusative'], "осталось", enemy['health'], "здоровья.")
                    print("У тебя осталось", player_health, "здоровья.")
                    
                    #Уменьшение прочности Меча
                    items["Меч"]["uses"] -= 1

                    #Меч ломается
                    if items["Меч"]["uses"] == 0:
                        print(items_forms["Меч"]["nominative"], "сломался!")
                        inventory.remove("Меч")

                    print("На полу валяется топор. Хочешь взять его? Если да, то ты пропустишь один удара")
                    choice = input("  Да/Нет: ")
                        
                    #Пропуск урона, если берешь топор
                    if choice == "Да":
                        inventory.append("Топор")
                        print("Ты взял топор!")

                        damage = random.randint(1, enemy["attack"])  
                        player_health -= damage
                        print(" " + enemy_type, "нанес тебе", damage, "урона!")
                    else:
                        print("Ты решаешь оставить топор лежать.")

            # Если у игрока есть Топор в инвентаре
            elif "Топор" in inventory:
                
                #Проверка на прочность топора
                if items["Топор"]["uses"] > 0:

                    enemy["health"] -= items["Топор"]["damage"]
                    print(f" Ты ударил {enemy_forms[enemy_type]['accusative']} {items_forms['Топор']['creative']}, нанеся {items['Топор']['damage']} единиц урона!")

                    if enemy["health"] > 0:
                        damage = random.randint(1, enemy["attack"])
                        player_health -= damage
                        print(" " + enemy_type, "нанес тебе", damage, "урона!")

                #Уменьшение прочности топора
                items["Топор"]["uses"] -= 1  

                #Топор сломался
                if items["Топор"]["uses"] == 0:  
                    print(items_forms["Топор"]["nominative"], "сломался!")
                    inventory.remove("Топор")
                            
            else:

                #удар кулаком
                damage = random.randint(1, 5)
                enemy["health"] -= damage
                print(" Ты ударил", enemy_forms[enemy_type]['accusative'], "кулаком, нанеся", damage, "урона!") 

                if enemy["health"] > 0:
                    damage = random.randint(1, enemy["attack"])
                    player_health -= damage
                    print(" " + enemy_type, "нанес тебе", damage, "урона!") 

        elif action == "бежать":

            #Проверка на наличие зелья в инвентаре
            if "Зелье исцеления" in inventory:
                player_health += items["Зелье исцеления"]["heal"]  
                print(" Ты сбежал от боя, выпил зелье исцеления и восстановил", items["Зелье исцеления"]["heal"], "ХП!")
                
                inventory.remove("Зелье исцеления")
                return
            else:
                print(" У тебя нет зелья исцеления! Ты сбегаешь от боя...")
                return
        else:
            print("Некорректное действие.")
            continue
        
        #Проверка, если у врага меньше 0 хп
        if enemy["health"] <= 0:
            print("Ты победил", enemy_forms[enemy_type]['accusative'],"!") 
            enemies_defeated.add(enemy_type)

            inventory.append("Ключ")
            
            print("Ты нашел ключ!\nПеред тобой сундук с сокровищами. Хочешь открыть его?")
            choice = input("  Да/Нет: ")

            if choice == "Да":
                print("Ты открыл сундук...\nВнутри ты нашел старинное кольцо, испускающее зловещее сияние.\nЭто кольцо проклято. Если ты умрешь, то воскреснешь в определенную точку времени до смерти.")
            else:
                print("Ты решаешь оставить сундук нетронутым.")

        #Проверка, если у персонажа меньше 0 хп
        if player_health <= 0:  
            print("Ты проиграл")
            exit()
    
# Основной цикл игры
while True:
    show_level_description()
    show_actions()
    action = input("Что ты хочешь сделать?: ")
    handle_action(action)