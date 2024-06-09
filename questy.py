
class Quest:
    def __init__(self, nazwa, opis, nagroda_w_sel, potwor_do_pokonania: str, warunek_ukonczenia):
        self.nazwa: str = nazwa
        self.opis: str = opis
        self.nagroda_w_sel: int = nagroda_w_sel
        self.nazwa_potwora_ze_zlecenia: str = potwor_do_pokonania
        self.warunek_ukonczenia: int = warunek_ukonczenia
        self.aktualny_postep: int = 0

    def czy_skonczony(self):  # is_finished, is_quest, is_class
        if self.aktualny_postep >= self.warunek_ukonczenia:
            return True
        else:
            return False

    def wyswietl_zadanie(self):
        print(self.nazwa)
        print(self.opis)
        print("Nagroda w SEL:", self.nagroda_w_sel)

    def wyswietl_postep(self):
        print(f"Masz pokonać: {self.nazwa_potwora_ze_zlecenia}")
        print(f"Twoj postep to {self.aktualny_postep} / {self.warunek_ukonczenia}")


questy = [
    # (
    #     "Zaginiony Statek Powietrzny", 
    #     "Statek powietrzny przewożący cenny ładunek zaginął w Trójkącie Burz. Twoim zadaniem jest odnaleźć statek, " \
    #     "uratować załogę i odzyskać ładunek, unikając niebezpiecznych burz i powietrznych piratów.",
    #     320,  # nagroda pieniężna
    #     2,  # indeks potwora z listy "wrogowie" z modułu postacie
    #     5,  # ilość wymagana do pokonania jako warunek ukończenia questa
    # ),
    (
        "Bunt w Kopalniach Żelaznych Wzgórz", 
        "Kopalnie Żelaznych Wzgórz zostały opanowane przez zbuntowane roboty, którzy twierdzą, " \
        "że kopalnia skrywa mroczne tajemnice. Musisz zaprowadzić porządek i odkryć, co naprawdę się tam dzieje.",
        460,
        1,
        3,
    ),
    # (
    #     "Eksperyment Alfa-9",
    #     "W tajnym laboratorium na księżycu Io przeprowadzano eksperymenty z zaawansowaną sztuczną inteligencją. " \
    #     "Niestety, kontakt z bazą został utracony. Musisz udać się do laboratorium i dowiedzieć się, co poszło nie tak, "
    #     "zanim AI przejmie kontrolę nad bazą.", 
    #     630,
    #     6,
    #     2,
    # ),
    # (
    #     "Rebelia Androidów", 
    #     "Na jednej z korporacyjnych stacji orbitalnych doszło do buntu androidów. "
    #     "Twoim zadaniem jest wejść na stację, odzyskać kontrolę nad systemami i odkryć, co spowodowało "
    #     "zbuntowanie się sztucznej inteligencji.",
    #     570,
    #     0,
    #     3,
    # ),
    # (
    #     "Czarna Dziura: Misja Ratunkowa", 
    #     "Statek naukowy został złapany w grawitacyjne pole czarnej dziury. "
    #     "Musisz przeprowadzić misję ratunkową, uratować załogę i zabezpieczyć cenne dane naukowe, "
    #     "zanim statek zostanie wciągnięty w horyzont zdarzeń.", 
    #     980,
    #     3,
    #     3,
    # )
]
