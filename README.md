# System zarządzania klubem fitness

## Temat aplikacji

Projekt przedstawia prostą aplikację konsolową do obsługi klubu fitness. System pozwala dodać trenerów, klientów, plany członkostwa, zajęcia sportowe oraz rezerwacje. Aplikacja pokazuje podstawowy model obiektowy, w którym klasy mają konkretne odpowiedzialności i są połączone relacjami zgodnymi z zasadami OOP.

## Jak uruchomić projekt

Wymagany jest Python 3.10 lub nowszy.

```bash
python main.py
```

## Lista klas

### `MembershipPlan`
- Odpowiedzialność: abstrakcyjny kontrakt dla planów członkostwa.
- Najważniejsze metody: `name()`, `monthly_price()`, `max_active_reservations()`, `discount_percent()`.

### `BasicPlan`
- Odpowiedzialność: konkretny podstawowy plan członkostwa.
- Najważniejsze metody: implementuje metody z `MembershipPlan`.

### `PremiumPlan`
- Odpowiedzialność: konkretny rozszerzony plan członkostwa.
- Najważniejsze metody: implementuje metody z `MembershipPlan`, daje większy limit rezerwacji i zniżkę.

### `Person`
- Odpowiedzialność: abstrakcyjna klasa bazowa dla osób w systemie.
- Najważniejsze właściwości: `person_id`, `full_name`, `email`.
- Najważniejsze metody: `role()`, `description()`.

### `Trainer`
- Odpowiedzialność: reprezentuje trenera prowadzącego zajęcia.
- Najważniejsze właściwości: `person_id`, `full_name`, `email`, `specialization`.
- Najważniejsze metody: `role()`.

### `Member`
- Odpowiedzialność: reprezentuje klienta klubu fitness.
- Najważniejsze właściwości: `person_id`, `full_name`, `email`, `plan`, `is_active`, `reservations`.
- Najważniejsze metody: `change_plan()`, `deactivate()`, `can_make_reservation()`, `add_reservation()`.

### `FitnessClass`
- Odpowiedzialność: abstrakcyjna klasa bazowa dla zajęć fitness.
- Najważniejsze właściwości: `class_id`, `title`, `trainer`, `capacity`, `base_price`, `reservations`.
- Najważniejsze metody: `has_free_place()`, `add_reservation()`, `calculate_price_for()`, `equipment_info()`, `class_type()`, `description()`.

### `YogaClass`
- Odpowiedzialność: reprezentuje zajęcia jogi.
- Najważniejsze właściwości: `difficulty`.
- Najważniejsze metody: `equipment_info()`, `class_type()`.

### `StrengthClass`
- Odpowiedzialność: reprezentuje trening siłowy.
- Najważniejsze właściwości: `required_level`.
- Najważniejsze metody: `equipment_info()`, `class_type()`, `calculate_price_for()`.

### `Reservation`
- Odpowiedzialność: łączy klienta z wybranymi zajęciami i przechowuje informacje o rezerwacji.
- Najważniejsze właściwości: `reservation_id`, `member`, `fitness_class`, `reservation_date`, `price`, `is_active`.
- Najważniejsze metody: `cancel()`, `summary()`.

### `GymClub`
- Odpowiedzialność: obsługuje dodawanie obiektów i tworzenie/anulowanie rezerwacji.
- Najważniejsze właściwości: `club_name` oraz prywatne kolekcje klientów, trenerów, zajęć i rezerwacji.
- Najważniejsze metody: `add_member()`, `add_trainer()`, `add_class()`, `reserve_class()`, `cancel_reservation()`, `show_people()`, `show_classes()`, `show_reservations()`.

## Relacje między klasami

1. Dziedziczenie:
   - `Trainer` i `Member` dziedziczą po klasie `Person`.
   - `YogaClass` i `StrengthClass` dziedziczą po klasie `FitnessClass`.
   - `BasicPlan` i `PremiumPlan` dziedziczą po abstrakcyjnej klasie `MembershipPlan`.

2. Relacja przez właściwość:
   - `FitnessClass` ma właściwość `trainer`, czyli każde zajęcia mają przypisanego trenera.
   - `Member` ma właściwość `plan`, czyli klient posiada wybrany plan członkostwa.

3. Relacja przez kolekcję:
   - `Member` przechowuje listę swoich rezerwacji.
   - `FitnessClass` przechowuje listę rezerwacji na konkretne zajęcia.
   - `GymClub` przechowuje kolekcje klientów, trenerów, zajęć i rezerwacji.

4. Agregacja:
   - `Reservation` łączy obiekt `Member` i obiekt `FitnessClass`, ale nie tworzy ich samodzielnie. Klient i zajęcia mogą istnieć niezależnie od rezerwacji.

5. Przekazanie obiektu przez konstruktor:
   - `Member` otrzymuje obiekt planu członkostwa w konstruktorze.
   - `FitnessClass` otrzymuje obiekt `Trainer` w konstruktorze.
   - `Reservation` otrzymuje obiekty `Member` i `FitnessClass` w konstruktorze.

6. Identyfikatory:
   - `Person` używa `person_id`.
   - `FitnessClass` używa `class_id`.
   - `Reservation` używa `reservation_id`.

## Cztery zasady OOP

### Enkapsulacja

Pola klas są chronione przez podkreślenie, np. `_active`, `_reservations`, `_plan`. Dostęp do nich odbywa się przez właściwości i metody, np. `is_active`, `reservations`, `deactivate()`, `change_plan()`, `add_reservation()`. Dzięki temu nie można swobodnie zmieniać ważnego stanu obiektu bez kontroli.

Przykład: rezerwacja nie powinna być anulowana przez ręczną zmianę pola `_active`, tylko przez metodę `cancel()`, która sprawdza, czy rezerwacja nie została już wcześniej anulowana.

### Dziedziczenie

Dziedziczenie zostało użyte tam, gdzie występuje relacja „jest rodzajem”:

- `Member` jest rodzajem `Person`.
- `Trainer` jest rodzajem `Person`.
- `YogaClass` jest rodzajem `FitnessClass`.
- `StrengthClass` jest rodzajem `FitnessClass`.
- `BasicPlan` i `PremiumPlan` są rodzajami `MembershipPlan`.

### Polimorfizm

Polimorfizm występuje przy wywołaniu tych samych metod na różnych typach obiektów. W pliku `main.py` metoda `description()` jest wywoływana dla różnych zajęć, a metoda `calculate_price_for()` działa inaczej dla `YogaClass` i `StrengthClass`.

`StrengthClass` dolicza dopłatę za specjalistyczny sprzęt, a `YogaClass` korzysta z podstawowego sposobu liczenia ceny.

### Abstrakcja

Abstrakcja została zastosowana przez klasy abstrakcyjne `Person`, `FitnessClass` i `MembershipPlan`. Definiują one wspólny kontrakt dla klas szczegółowych, ale nie opisują wszystkich szczegółów implementacji.

Przykład: `FitnessClass` wymaga metod `equipment_info()` i `class_type()`, ale konkretne klasy, takie jak `YogaClass` i `StrengthClass`, same określają, jaki sprzęt jest potrzebny i jaki typ zajęć reprezentują.

## Przykładowe działanie aplikacji

Aplikacja tworzy przykładowych trenerów, klientów, plany członkostwa i zajęcia. Następnie wykonuje rezerwacje, pokazuje listę osób, listę zajęć, ceny dla różnych planów oraz anulowanie rezerwacji.

## Użycie AI

AI zostało użyte jako wsparcie przy uporządkowaniu struktury klas, relacji między klasami oraz przygotowaniu przykładowych danych testowych.
