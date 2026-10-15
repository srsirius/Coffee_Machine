# CoffeeMachine

Консольная кофемашина на Python с конечным автоматом (FSM). Реализует покупку напитков, пошаговое пополнение запасов, выдачу выручки и просмотр остатков.

## Возможности

- **Покупка напитков**: эспрессо, латте, капучино (выбор по номеру).
- **Пошаговое пополнение**: вода → молоко → зёрна → чашки (машина сама запрашивает каждый ресурс).
- **Просмотр состояния**: команда `remaining` показывает точные текущие запасы без изменения состояния.
- **Выдача денег**: команда `take` снимает всю выручку.
- **Отладка**: удобный `__repr__` для быстрого просмотра всех полей объекта.

## Состояния машины (FSM)

| Состояние | Описание |
| --- | --- |
| `MAIN` | Главное меню, ожидание команды |
| `BUY` | Выбор напитка (1/2/3 или `back`) |
| `FILL_WATER` | Ожидание ввода: сколько мл воды добавить |
| `FILL_MILK` | Ожидание ввода: сколько мл молока добавить |
| `FILL_BEANS` | Ожидание ввода: сколько г зёрен добавить |
| `FILL_CUPS` | Ожидание ввода: сколько чашек добавить |
| `EXIT` | Завершение работы |

## Как запустить

1. Убедитесь, что установлен Python 3.8+.
2. Сохраните код в файл `coffee_machine.py`.
3. Запустите из терминала:
   ```bash
   python coffee_machine.py
4.Вводите команды согласно подсказкам в консоли.
Доступные команды (в состоянии MAIN)
Команда	Описание
buy	Перейти к выбору напитка
fill	Начать пополнение ресурсов (пошагово)
take	Забрать всю выручку
remaining	Показать текущие запасы
exit	Выйти из программы
В режиме покупки доступна команда back — возврат в главное меню.

Примеры использования
Интерактивный запуск
bash
python coffee_machine.py
Примерный вывод при старте:

text
Write action (buy, fill, take, remaining, exit):
Использование в коде (для тестов и отладки)
python
from coffee_machine import CoffeeMachine

machine = CoffeeMachine()
print(repr(machine))  # Быстрый снимок состояния: все поля сразу

response = machine.process_input("remaining")
print(response)
Особенности реализации
__repr__: возвращает компактное, но полное представление объекта. Удобно для логирования и быстрой проверки состояния при отладке.
_status(): только чтение текущих значений, без побочных эффектов. Это гарантирует, что команда remaining не меняет запасы.
Разделение ответственности:
_handle_fill_* — только изменяют состояние.
Форматирование строк вынесено в логику возврата из process_input и в _status().
Пошаговый fill: машина сама переключает состояния и запрашивает следующий ресурс.
Проверка ресурсов: перед приготовлением проверяется наличие воды, молока, зёрен и чашек. При нехватке выводится понятное сообщение.
Пример полного диалога (фрагмент)
text
Write action (buy, fill, take, remaining, exit):
> fill
Write how many ml of water you want to add:
> 200
Write how many ml of milk you want to add:
> 100
Write how many grams of coffee beans you want to add:
> 50
Write how many disposable cups you want to add:
> 3
Write action (buy, fill, take, remaining, exit):
> remaining

The coffee machine has:
600 ml of water
640 ml of milk
170 g of coffee beans
12 disposable cups
$550 money
Тестирование
Простой тест на покупку эспрессо:

python
def test_buy_espresso():
    m = CoffeeMachine()
    assert m.water == 400
    m.process_input("buy")
    response = m.process_input("1")
    assert "making you a coffee" in response
    assert m.water == 150  # 400 - 250
    assert m.money == 554  # 550 + 4
Тест, подтверждающий, что remaining ничего не меняет:

python
def test_remaining_no_side_effects():
    m = CoffeeMachine()
    before = m.water
    m.process_input("remaining")
    after = m.water
    assert before == after
Лицензия
Учебный проект, без лицензии (public domain / MIT — на ваше усмотрение).

Контакты и вопросы
Если нужны дополнительные функции (например, сохранение состояния, логирование, юнит‑тесты на pytest) — создавайте issue или пишите в личку.
