# Вариант 5

from pydantic import BaseModel, ConfigDict, Field, ValidationError
from typing import Literal

class CakeItem(BaseModel):
    model_config = ConfigDict(extra="forbid")

    cake_id: Literal['honey', 'napoleon', 'carrot', 'chocolate']
    weight_kg: float = Field(ge=0.5, le=5)
    decoration: Literal['simple', 'berries', 'festive']
    inscription: str | None = Field(default=None, max_length=50)

class OrderExtraction(BaseModel):
    model_config = ConfigDict(extra="forbid")

    items: list[CakeItem]
    needs_clarification: bool
    clarification_question: str | None


# Task 2
print('Task 2')

records = [
    {"cake_id": "chocolate", "weight_kg": 1.5, "decoration": "berries", "inscription": "С днём рождения!"},
    {"cake_id": "honey", "weight_kg": 1.0, "decoration": "simple", "inscription": None},
    {"cake_id": "tiramisu", "weight_kg": 1.0, "decoration": "simple", "inscription": None},
    {"cake_id": "napoleon", "weight_kg": 0.2, "decoration": "flowers", "inscription": None}]

valid_records = []
invalid_records = {}

for i in range(len(records)):
    try:
        valid_records.append(CakeItem.model_validate(records[i]))
        print(f'Запись {i + 1}: VALID')

    except ValidationError as error:
        record_errors = {}
        for problem in error.errors():
            record_errors[problem["loc"][0]] = problem["msg"]
        invalid_records[i] = record_errors
        print(f'Запись {i + 1}: INVALID')

for i in invalid_records.keys():
    print(f'Запись {i + 1}  невалидна: {str(invalid_records[i])[1:-1]}')

# Task 3
print('\nTask 3')

cake = CakeItem.model_validate(valid_records[0])

order = OrderExtraction(
    items=[cake],
    needs_clarification=False,
    clarification_question=None,
)

print(type(order).__name__)
print(type(order.items[0]).__name__)
print(order.items[0].cake_id)
print(order.items[0].weight_kg)
print(order.items[0].decoration)
print(order.items[0].inscription)
print(order.model_dump())

# Task 4
print('\nTask 4')

#Сообщение 1: «Медовик 1 кг с простым оформлением без надписи и шоколадный торт 2 кг с праздничным оформлением и надписью “Поздравляем!”».
order_1 = OrderExtraction(
    items=[
        CakeItem(
            cake_id='honey',
            weight_kg=1,
            decoration='simple',
            inscription=None,
        ),
        CakeItem(
            cake_id='chocolate',
            weight_kg=2,
            decoration='festive',
            inscription='Поздравляем!'
        )
    ],
    needs_clarification=False,
    clarification_question=None
)

#Сообщение 2: «Нужен небольшой праздничный торт»
order_2 = OrderExtraction(
    items=[],
    needs_clarification=True,
    clarification_question=(
        'Какой торт вам нужен, какой массы и нужно ли добавить надпись?'
    )
)

print(order_1)
print(order_2)

print('\n')
for item in order_1.items:
    print(item.cake_id)
    print(item.weight_kg)
    print(item.decoration)
    print(item.inscription)
