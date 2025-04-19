import random
from dataclasses import dataclass, field
from typing import List, Dict

@dataclass
class Terrorist:
    name: str
    age: int
    role: str
    traits: List[str]
    location: str
    loyalty: int = field(default_factory=lambda: random.randint(30, 100))
    is_alive: bool = True

@dataclass
class TerrorGroup:
    name: str
    leaders: List[str]
    strength: int
    locations: List[str]
    structure: Dict[str, int] = field(default_factory=lambda: {
        "Боевики": random.randint(50, 200),
        "Снайперы": random.randint(5, 20),
        "Подрывники": random.randint(10, 30),
        "Финансисты": random.randint(3, 10)
    })

@dataclass
class Player:
    name: str
    age: int = 22
    rank: str = "Стажёр"
    reputation: int = 50
    stress: int = 0
    skills: Dict[str, int] = field(default_factory=lambda: {
        "Стрельба": random.randint(20, 40),
        "Аналитика": random.randint(30, 50),
        "Переговоры": random.randint(10, 30),
        "Хакерство": random.randint(5, 20)
    })
    money: int = 5000
    completed_missions: int = 0
    agency: str = "FSB"

TERROR_GROUPS = [
    TerrorGroup(
        name="Освобождение Кашмира",
        leaders=["Абдул Рашид", "Мухаммад Фарук"],
        strength=75,
        locations=["Кашмир", "Исламабад"]
    ),
    TerrorGroup(
        name="Исламский Джихад",
        leaders=["Ахмад Аль-Масих", "Али Аль-Багдади"],
        strength=60,
        locations=["Йемен", "Сомали"]
    )
]

def generate_terrorist(group: TerrorGroup) -> Terrorist:
    names = ["Карим Уллах", "Зия Хан", "Фарук Ахмедзи"]
    traits = ["Шрам на лице", "Хромота", "Татуировка Корана", "Протез руки"]
    roles = ["Боевик", "Снайпер", "Подрывник", "Проповедник", "Финансист"]
    
    return Terrorist(
        name=random.choice(names),
        age=random.randint(20, 50),
        role=random.choice(roles),
        traits=random.sample(traits, random.randint(1, 2)),
        location=random.choice(group.locations)
    )

def random_event(player: Player) -> str:
    events = [
        ("Вы обнаружили склад оружия", {"reputation": 10, "money": 2000}),
        ("Ваш информатор убит", {"stress": 15}),
        ("Теракт предотвращён", {"reputation": 20}),
        ("Скандал в СМИ", {"reputation": -10}),
        ("Повышение зарплаты", {"money": 5000})
    ]
    event, effects = random.choice(events)
    for attr, value in effects.items():
        setattr(player, attr, getattr(player, attr) + value)
    return event

def handle_mission(player: Player, group: TerrorGroup):
    terrorist = generate_terrorist(group)
    print(f"\n🚨 МИССИЯ: {terrorist.role} {terrorist.name}")
    print(f"Группировка: {group.name}")
    print(f"Локация: {terrorist.location}")
    print(f"Приметы: {', '.join(terrorist.traits)}")
    
    options = {
        "1": ("Штурмовать", "Стрельба", 40),
        "2": ("Вербовать информатора", "Переговоры", 30),
        "3": ("Киберразведка", "Хакерство", 20)
    }
    
    for key, (desc, _, _) in options.items():
        print(f"{key}. {desc}")
    
    choice = input("> ")
    if choice in options:
        _, skill, threshold = options[choice]
        success = player.skills.get(skill, 0) > random.randint(threshold - 20, threshold + 20)
        
        if success:
            print(f"✅ Успех! {terrorist.name} нейтрализован.")
            player.reputation += 15
            player.completed_missions += 1
            group.strength -= 10
        else:
            print("❌ Провал! Цель избежала захвата.")
            player.stress += 10
    else:
        print("Неверный выбор!")

def main():
    print("=== АНТИТЕРРОР BITLIFE ===")
    player = Player(name=input("Ваше имя: "), agency=input("Спецслужба (FSB/CIA/MI6): ").upper())
    
    year = 2023
    while year < 2033 and player.reputation > 0 and player.stress < 100:
        print(f"\n--- {year} год ({player.age} лет) ---")
        print(f"Ранг: {player.rank} | Репутация: {player.reputation} | Стресс: {player.stress}")
        print(f"Навыки: {player.skills}")
        
        event_type = random.choices(
            ["mission", "random_event", "promotion"],
            weights=[70, 20, 10]
        )[0]
        
        if event_type == "mission":
            handle_mission(player, random.choice(TERROR_GROUPS))
        elif event_type == "random_event":
            print(f"\n📢 Событие: {random_event(player)}")
        else:
            if player.reputation >= 70 and player.rank == "Стажёр":
                player.rank = "Офицер"
                print("\n🎉 Повышение до Офицера!")
            elif player.reputation >= 90 and player.rank == "Офицер":
                player.rank = "Директор"
                print("\n🔥 Вы стали Директором!")
                break
        
        player.age += 1
        year += 1
        player.stress = max(0, player.stress - 5)
    
    print("\n=== ИГРА ОКОНЧЕНА ===")
    print(f"Финальный ранг: {player.rank}")
    print(f"Выполнено миссий: {player.completed_missions}")
    print(f"Остаток денег: ${player.money}")

if __name__ == "__main__":
    main()