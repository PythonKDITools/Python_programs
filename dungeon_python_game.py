import random
import time
import os

# Очистка консоли
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

# Замедленный вывод для атмосферы
def slow_print(text, delay=0.03):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()

# Главный герой
player = {
    'hp': 20,
    'max_hp': 20,
    'attack': 4,
    'inventory': [],
    'pos': (0, 0)
}

# Карта подземелья (4x4)
dungeon = [
    ['🟫', '🟫', '🟫', '🚪'],
    ['🟫', '💀', '🟫', '🟫'],
    ['🗝️', '🟫', '👹', '🟫'],
    ['🟫', '🟫', '🟫', '⭐']
]
# ⭐ - выход, 🗝️ - ключ, 💀 - ловушка, 👹 - монстр, 🚪 - дверь (требует ключ)

def show_map():
    print("\nКарта подземелья (вы — 🧙):")
    for y, row in enumerate(dungeon):
        line = ""
        for x, cell in enumerate(row):
            if (y, x) == player['pos']:
                line += "🧙 "
            else:
                line += cell + " "
        print(line)
    print()

def move(dx, dy):
    x, y = player['pos']
    nx, ny = x + dx, y + dy
    if 0 <= nx < 4 and 0 <= ny < 4:
        player['pos'] = (nx, ny)
        return True
    return False

def encounter(cell):
    x, y = player['pos']
    if cell == '💀':
        damage = random.randint(3, 8)
        slow_print(f"🔪 Вы наступили на ловушку! -{damage} HP")
        player['hp'] -= damage
        dungeon[y][x] = '🟫'  # ловушка исчезает
        return True
    elif cell == '👹':
        slow_print("👹 На вас напал огр!")
        choice = input("Бежать (б) или сражаться (с)? ").lower()
        if choice == 'с':
            dmg = random.randint(2, 6) + player['attack']
            slow_print(f"Вы нанесли {dmg} урона. Огр пал!")
            # Огр мог ударить в ответ
            if random.random() < 0.5:
                player['hp'] -= 4
                slow_print("Огр ударил вас перед смертью! -4 HP")
        else:
            slow_print("Вы убежали, но получили удар в спину! -3 HP")
            player['hp'] -= 3
        dungeon[y][x] = '🟫'
        return True
    elif cell == '🗝️':
        slow_print("🔑 Вы нашли Золотой Ключ! Теперь можно открыть дверь.")
        player['inventory'].append('key')
        dungeon[y][x] = '🟫'
        return True
    elif cell == '🚪':
        if 'key' in player['inventory']:
            slow_print("🚪 Дверь открыта! За ней лестница наверх...")
            dungeon[y][x] = '🟫'
            return True
        else:
            slow_print("Дверь заперта. Нужен ключ!")
            return False
    elif cell == '⭐':
        slow_print("✨ Это выход из темницы! Вы свободны! ✨")
        return 'exit'
    return True

def game_loop():
    clear()
    slow_print("Ты в тёмном подземелье. Найди ключ, открой дверь и доберись до выхода (⭐).")
    slow_print("Управление: w/a/s/d (вверх/влево/вниз/вправо).")
    while player['hp'] > 0:
        show_map()
        print(f"❤️ HP: {player['hp']}/{player['max_hp']}   🎒: {player['inventory']}")
        move_key = input("Куда идёшь? ").lower()
        dx, dy = 0, 0
        if move_key == 'w':
            dy = -1
        elif move_key == 's':
            dy = 1
        elif move_key == 'a':
            dx = -1
        elif move_key == 'd':
            dx = 1
        else:
            slow_print("Неверная клавиша. Используй w/a/s/d")
            continue
        
        if move(dx, dy):
            x, y = player['pos']
            cell = dungeon[y][x]
            result = encounter(cell)
            if result == 'exit':
                slow_print("Поздравляю! Ты выжил и сбежал из темницы!")
                print("🎉 ПОБЕДА! 🎉")
                return
            if player['hp'] <= 0:
                slow_print("Ты погиб... Игра окончена.")
                return
        else:
            slow_print("Там стена, идти нельзя.")
    
    slow_print("Игра завершена. Ты пал во тьме.")

if __name__ == "__main__":
    game_loop()