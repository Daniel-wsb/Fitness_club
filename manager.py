from __future__ import annotations

from datetime import date
from typing import Dict

from models import FitnessClass, Member, Reservation, Trainer


class GymClub:
    """Klasa usługowa odpowiedzialna za obsługę rezerwacji w klubie."""

    def __init__(self, club_name: str) -> None:
        self._club_name = club_name
        self._members: Dict[str, Member] = {}
        self._trainers: Dict[str, Trainer] = {}
        self._classes: Dict[str, FitnessClass] = {}
        self._reservations: Dict[str, Reservation] = {}
        self._next_reservation_number = 1

    @property
    def club_name(self) -> str:
        return self._club_name

    def add_member(self, member: Member) -> None:
        self._members[member.person_id] = member

    def add_trainer(self, trainer: Trainer) -> None:
        self._trainers[trainer.person_id] = trainer

    def add_class(self, fitness_class: FitnessClass) -> None:
        self._classes[fitness_class.class_id] = fitness_class

    def find_member(self, member_id: str) -> Member:
        return self._members[member_id]

    def find_class(self, class_id: str) -> FitnessClass:
        return self._classes[class_id]

    def reserve_class(self, member_id: str, class_id: str, reservation_date: date) -> Reservation:
        member = self.find_member(member_id)
        fitness_class = self.find_class(class_id)

        if not member.can_make_reservation():
            raise ValueError("Klient nie spełnia warunków wykonania rezerwacji.")
        if not fitness_class.has_free_place():
            raise ValueError("Brak wolnych miejsc na wybrane zajęcia.")

        reservation_id = f"R-{self._next_reservation_number:04d}"
        self._next_reservation_number += 1

        reservation = Reservation(reservation_id, member, fitness_class, reservation_date)
        member.add_reservation(reservation)
        fitness_class.add_reservation(reservation)
        self._reservations[reservation_id] = reservation
        return reservation

    def cancel_reservation(self, reservation_id: str) -> None:
        self._reservations[reservation_id].cancel()

    def show_people(self) -> list[str]:
        people = list(self._members.values()) + list(self._trainers.values())
        return [person.description() for person in people]

    def show_classes(self) -> list[str]:
        return [fitness_class.description() for fitness_class in self._classes.values()]

    def show_reservations(self) -> list[str]:
        return [reservation.summary() for reservation in self._reservations.values()]
