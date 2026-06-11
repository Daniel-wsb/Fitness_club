from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import date
from typing import List


class MembershipPlan(ABC):
    """Abstrakcyjny kontrakt dla planu członkostwa."""

    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def monthly_price(self) -> float:
        pass

    @abstractmethod
    def max_active_reservations(self) -> int:
        pass

    @abstractmethod
    def discount_percent(self) -> float:
        pass


class BasicPlan(MembershipPlan):
    def name(self) -> str:
        return "Basic"

    def monthly_price(self) -> float:
        return 99.0

    def max_active_reservations(self) -> int:
        return 2

    def discount_percent(self) -> float:
        return 0.0


class PremiumPlan(MembershipPlan):
    def name(self) -> str:
        return "Premium"

    def monthly_price(self) -> float:
        return 179.0

    def max_active_reservations(self) -> int:
        return 5

    def discount_percent(self) -> float:
        return 20.0


class Person(ABC):
    """Klasa ogólna dla osób w klubie fitness."""

    def __init__(self, person_id: str, full_name: str, email: str) -> None:
        if not person_id:
            raise ValueError("Identyfikator osoby nie może być pusty.")
        if "@" not in email:
            raise ValueError("Niepoprawny adres e-mail.")
        self._person_id = person_id
        self._full_name = full_name
        self._email = email

    @property
    def person_id(self) -> str:
        return self._person_id

    @property
    def full_name(self) -> str:
        return self._full_name

    @property
    def email(self) -> str:
        return self._email

    @abstractmethod
    def role(self) -> str:
        pass

    def description(self) -> str:
        return f"{self.full_name} ({self.role()})"


class Trainer(Person):
    def __init__(self, person_id: str, full_name: str, email: str, specialization: str) -> None:
        super().__init__(person_id, full_name, email)
        self._specialization = specialization

    @property
    def specialization(self) -> str:
        return self._specialization

    def role(self) -> str:
        return f"Trener: {self.specialization}"


class Member(Person):
    def __init__(self, person_id: str, full_name: str, email: str, plan: MembershipPlan) -> None:
        super().__init__(person_id, full_name, email)
        self._plan = plan
        self._active = True
        self._reservations: List[Reservation] = []

    @property
    def plan(self) -> MembershipPlan:
        return self._plan

    @property
    def is_active(self) -> bool:
        return self._active

    @property
    def reservations(self) -> tuple[Reservation, ...]:
        return tuple(self._reservations)

    def role(self) -> str:
        return f"Klient planu {self.plan.name()}"

    def deactivate(self) -> None:
        self._active = False

    def change_plan(self, new_plan: MembershipPlan) -> None:
        self._plan = new_plan

    def active_reservations_count(self) -> int:
        return sum(1 for reservation in self._reservations if reservation.is_active)

    def can_make_reservation(self) -> bool:
        return self.is_active and self.active_reservations_count() < self.plan.max_active_reservations()

    def add_reservation(self, reservation: Reservation) -> None:
        if not self.can_make_reservation():
            raise ValueError("Klient nie może mieć więcej aktywnych rezerwacji w tym planie.")
        self._reservations.append(reservation)


class FitnessClass(ABC):
    """Abstrakcyjna klasa bazowa dla zajęć fitness."""

    def __init__(self, class_id: str, title: str, trainer: Trainer, capacity: int, base_price: float) -> None:
        if capacity <= 0:
            raise ValueError("Liczba miejsc musi być większa od zera.")
        if base_price < 0:
            raise ValueError("Cena nie może być ujemna.")
        self._class_id = class_id
        self._title = title
        self._trainer = trainer
        self._capacity = capacity
        self._base_price = base_price
        self._reservations: List[Reservation] = []

    @property
    def class_id(self) -> str:
        return self._class_id

    @property
    def title(self) -> str:
        return self._title

    @property
    def trainer(self) -> Trainer:
        return self._trainer

    @property
    def capacity(self) -> int:
        return self._capacity

    @property
    def base_price(self) -> float:
        return self._base_price

    @property
    def reservations(self) -> tuple[Reservation, ...]:
        return tuple(self._reservations)

    def taken_places(self) -> int:
        return sum(1 for reservation in self._reservations if reservation.is_active)

    def has_free_place(self) -> bool:
        return self.taken_places() < self.capacity

    def add_reservation(self, reservation: Reservation) -> None:
        if not self.has_free_place():
            raise ValueError("Brak wolnych miejsc na zajęciach.")
        self._reservations.append(reservation)

    def calculate_price_for(self, member: Member) -> float:
        discount = member.plan.discount_percent() / 100
        return round(self.base_price * (1 - discount), 2)

    @abstractmethod
    def equipment_info(self) -> str:
        pass

    @abstractmethod
    def class_type(self) -> str:
        pass

    def description(self) -> str:
        return (
            f"{self.class_type()}: {self.title}, trener: {self.trainer.full_name}, "
            f"miejsca: {self.taken_places()}/{self.capacity}, sprzęt: {self.equipment_info()}"
        )


class YogaClass(FitnessClass):
    def __init__(self, class_id: str, title: str, trainer: Trainer, capacity: int, base_price: float, difficulty: str) -> None:
        super().__init__(class_id, title, trainer, capacity, base_price)
        self._difficulty = difficulty

    @property
    def difficulty(self) -> str:
        return self._difficulty

    def equipment_info(self) -> str:
        return "mata do jogi"

    def class_type(self) -> str:
        return f"Joga ({self.difficulty})"


class StrengthClass(FitnessClass):
    def __init__(self, class_id: str, title: str, trainer: Trainer, capacity: int, base_price: float, required_level: int) -> None:
        super().__init__(class_id, title, trainer, capacity, base_price)
        if required_level not in range(1, 6):
            raise ValueError("Poziom trudności musi być od 1 do 5.")
        self._required_level = required_level

    @property
    def required_level(self) -> int:
        return self._required_level

    def equipment_info(self) -> str:
        return "hantle i ławka treningowa"

    def class_type(self) -> str:
        return f"Trening siłowy poziom {self.required_level}"

    def calculate_price_for(self, member: Member) -> float:
        # Trening siłowy ma dopłatę za specjalistyczny sprzęt.
        price_with_equipment_fee = self.base_price + 15.0
        discount = member.plan.discount_percent() / 100
        return round(price_with_equipment_fee * (1 - discount), 2)


class Reservation:
    """Klasa łącząca klienta z konkretnymi zajęciami."""

    def __init__(self, reservation_id: str, member: Member, fitness_class: FitnessClass, reservation_date: date) -> None:
        self._reservation_id = reservation_id
        self._member = member
        self._fitness_class = fitness_class
        self._reservation_date = reservation_date
        self._active = True
        self._price = fitness_class.calculate_price_for(member)

    @property
    def reservation_id(self) -> str:
        return self._reservation_id

    @property
    def member(self) -> Member:
        return self._member

    @property
    def fitness_class(self) -> FitnessClass:
        return self._fitness_class

    @property
    def reservation_date(self) -> date:
        return self._reservation_date

    @property
    def price(self) -> float:
        return self._price

    @property
    def is_active(self) -> bool:
        return self._active

    def cancel(self) -> None:
        if not self._active:
            raise ValueError("Rezerwacja jest już anulowana.")
        self._active = False

    def summary(self) -> str:
        status = "aktywna" if self.is_active else "anulowana"
        return (
            f"Rezerwacja {self.reservation_id}: {self.member.full_name} -> "
            f"{self.fitness_class.title}, {self.reservation_date}, {self.price} zł, status: {status}"
        )
