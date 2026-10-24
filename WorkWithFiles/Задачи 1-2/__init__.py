def parse_recipes_file(file_path):
    cook_book = {}
    
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    
    i = 0
    while i < len(lines):
        if not lines[i].strip():
            i += 1
            continue
        
        dish_name = lines[i].strip()
        i += 1
        
        if i >= len(lines):
            break
        
        try:
            ingredients_count = int(lines[i].strip())
        except ValueError:
            i += 1
            continue
        
        i += 1
        
        ingredients = []
        for _ in range(ingredients_count):
            if i >= len(lines):
                break
            
            ingredient_line = lines[i].strip()
            if ingredient_line:
                parts = ingredient_line.split(' | ')
                if len(parts) == 3:
                    ingredient = {
                        'ingredient_name': parts[0],
                        'quantity': int(parts[1]),
                        'measure': parts[2]
                    }
                    ingredients.append(ingredient)
            i += 1
        
        if ingredients:
            cook_book[dish_name] = ingredients
    
    return cook_book


def get_shop_list_by_dishes(cook_book, dishes, person_count):
    shop_list = {}
    
    for dish in dishes:
        for ingredient in cook_book[dish]:
            ingredient_name = ingredient['ingredient_name']
            quantity = ingredient['quantity'] * person_count
            measure = ingredient['measure']
            
            if ingredient_name in shop_list:
                shop_list[ingredient_name]['quantity'] += quantity
            else:
                shop_list[ingredient_name] = {
                    'measure': measure,
                    'quantity': quantity
                }
    
    return shop_list


def display_available_dishes(cook_book):
    print("\nДоступные блюда в кулинарной книге:")
    print("-" * 40)
    for i, dish_name in enumerate(cook_book.keys(), 1):
        print(f"{i}. {dish_name}")
    print("-" * 40)


def get_user_choices(cook_book):
    display_available_dishes(cook_book)
    
    while True:
        print("\nВведите названия блюд через запятую (например: Омлет, Утка по-пекински):")
        dishes_input = input("> ").strip()
        dishes = [dish.strip() for dish in dishes_input.split(',')] 
        break
    
    persons_input = input("\nВведите количество персон: ").strip()
    person_count = int(persons_input)
    
    return dishes, person_count


def main():
    print("Программа 'Кулинарная книга'")
    print("=" * 50)
    file_path = 'recipes.txt'
        
    cook_book = parse_recipes_file(file_path)
    
    print("\n" + "=" * 50)
    print("Задача №1 - Словарь cook_book:")
    print("-" * 50)
    for dish_name, ingredients in cook_book.items():
        print(f"\n{dish_name}:")
        for ingredient in ingredients:
            print(f"  • {ingredient['ingredient_name']}: {ingredient['quantity']} {ingredient['measure']}")
    
    print("\n" + "=" * 50)
    print("Задача №2 - Расчет необходимых ингредиентов")
    print("-" * 50)
    
    dishes_to_cook, persons = get_user_choices(cook_book)
    
    shop_list = get_shop_list_by_dishes(cook_book, dishes_to_cook, persons)
    
    print("\n" + "=" * 50)
    print(f"Результат для блюд: {', '.join(dishes_to_cook)}")
    print(f"Количество персон: {persons}")
    print("-" * 50)
    print("Список необходимых ингредиентов:")
    
    if shop_list:
        for ingredient_name, info in sorted(shop_list.items()):
            print(f"  • {ingredient_name}: {info['quantity']} {info['measure']}")
    else:
        print("  Не найдено ингредиентов для указанных блюд.")

if __name__ == "__main__":
    # Выберите нужный режим:
    # main() - полная версия с выбором файла и проверками
    # main_simple() - упрощенная версия
    
    main()  # Используем полную версию