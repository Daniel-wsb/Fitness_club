from datetime import date

from manager import GymClub
from models import BasicPlan, PremiumPlan, Member, Trainer, YogaClass, StrengthClass


def main() -> None:
    club = GymClub("Iron & Zen Fitness Club")

    trainer_1 = Trainer("T-001", "Anna Kowalska", "anna.kowalska@fitness.pl", "joga")
    trainer_2 = Trainer("T-002", "Marek Nowak", "marek.nowak@fitness.pl", "trening siłowy")

    member_1 = Member("M-001", "Jan Zieliński", "jan.zielinski@example.com", BasicPlan())
    member_2 = Member("M-002", "Ewa Wiśniewska", "ewa.wisniewska@example.com", PremiumPlan())

    yoga = YogaClass("C-001", "Poranna joga", trainer_1, capacity=2, base_price=30.0, difficulty="łatwa")
    strength = StrengthClass("C-002", "Full Body Workout", trainer_2, capacity=2, base_price=45.0, required_level=3)

    club.add_trainer(trainer_1)
    club.add_trainer(trainer_2)
    club.add_member(member_1)
    club.add_member(member_2)
    club.add_class(yoga)
    club.add_class(strength)

    print("=== Osoby w systemie ===")
    for person_description in club.show_people():
        print(person_description)

    print("\n=== Zajęcia przed rezerwacją ===")
    for class_description in club.show_classes():
        print(class_description)

    reservation_1 = club.reserve_class("M-001", "C-001", date(2026, 6, 20))
    reservation_2 = club.reserve_class("M-002", "C-002", date(2026, 6, 21))

    print("\n=== Utworzone rezerwacje ===")
    print(reservation_1.summary())
    print(reservation_2.summary())

    print("\n=== Zajęcia po rezerwacji ===")
    for class_description in club.show_classes():
        print(class_description)

    print("\n=== Polimorfizm: ta sama metoda, różne typy zajęć ===")
    for fitness_class in [yoga, strength]:
        print(fitness_class.description())
        print(f"Cena dla planu Premium: {fitness_class.calculate_price_for(member_2)} zł")

    print("\n=== Anulowanie rezerwacji ===")
    club.cancel_reservation("R-0001")
    for reservation_description in club.show_reservations():
        print(reservation_description)


if __name__ == "__main__":
    main()
