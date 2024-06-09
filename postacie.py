import random

import teksty_historia_i_swiat
import przedmioty


wrogowie = [
    ("Festus", "Potężny smok, który strzeże ukrytego skarbu na szczytach gór.",7),
    ("Wilk Szalejących Lasów","Wilk zmutowany przez szalonych naukowców, który poluje na podróżnych w okolicznych drogach.",4),
    ("Podstępne Gobliny ","Gromada goblinów, która zamieszkuje opuszczone ruiny starożytnego miasta, grasując i rabując podróżnych.",6),
    ("Nekromanta Zguby","Ciemny czarownik, który przywołuje zmarłych z grobów, aby służyli mu jako armia.",5),
    ("Gigantyczna Żmija "," Potwór z legend pustynnych, który czyha w piaskach, by zaatakować nieostrożnych podróżnych.",10),
    ("Gnomy Mechaniczni z Metalowej Doliny","Inżynierowie, którzy stworzyli armię mechanicznych golemów, by podbić sąsiednie królestwa.",1),
    ("Cienioki", "Te potwory to istoty stworzone z czystej ciemności. Zazwyczaj atakują z ukrycia, korzystając z ciemności do swojej przewagi.",2),
    ("Harpia", "Bestie o ciele ptaka i twarzy kobiety, które polują na podróżnych w górach i lasach. Zdolne do szybkiego lotu i potężnych ataków.",3),
    ("Wąż Morskiej Otchłani", "Bestie morskie, których długość może sięgać dziesiątek metrów. Zwinne i śmiertelnie niebezpieczne, żyjące w najgłębszych wodach oceanów.", 8)
]

class Postac:
    def __init__(self, kredyty=None, ekwipunek=None):
        if ekwipunek is None:
            self.ekwipunek: list = []
        else:
            self.ekwipunek = ekwipunek
        self.kredyty: int | None = kredyty

    def wyswietl_ekwipunek(self):
        """wyświetl domyślnie posiadane przedmioty i pieniądze postaci"""
        print(f"\nPieniądze postaci: {self.kredyty}")
        for indeks, przedmiot in enumerate(self.ekwipunek):
            print(f"przedmiot {indeks+1}: ", przedmiot)


class Gracz(Postac):
    def __init__(self, poziom, pochodzenie, imie_postaci, kredyty_poczatkowe, poczatkowy_ekwipunek):
        self.poziom = poziom
        self.maksymalny_poziom_zycia = 100 + 10 * poziom
        self.zycie = self.maksymalny_poziom_zycia
        self.pochodzenie = pochodzenie
        self.imie_postaci = imie_postaci
        self.aktywny_quest = None
        self.punkty_doswiadczenia = 0
        Postac.__init__(self, kredyty=kredyty_poczatkowe, ekwipunek=poczatkowy_ekwipunek)

    def wyswietl_pochodzenie(self):
        print(f"Nazywasz się {self.imie_postaci}.")
        if self.pochodzenie == "1":
            print("pochodzisz z rodu zajmującego się handlem")
            print(teksty_historia_i_swiat.player_backstory_trading)
        if self.pochodzenie == "2":
            print("pochodzisz z rodu zajmującego się dyplomacją")
            print(teksty_historia_i_swiat.player_backstory_diplomat)
        if self.pochodzenie == "3":
            print("pochodzisz z rodu, w którym każdy służył ojczyźnie")
            print(teksty_historia_i_swiat.player_backstory_military)

    def wyswietl_ekwipunek(self):
        """dla obiektu klasy "Gracz", wyświetl budżet gracza oraz przedmioty które ma w ekwipunku"""
        print(f"\nTwój budżet: {self.kredyty}")
        for indeks, przedmiot in enumerate(self.ekwipunek):
            print(f"przedmiot {indeks+1}: ", przedmiot)

    def wyswietl_statystyki(self):
        print(f"\nTwoje doświadzcenie: poziom {self.poziom}, {self.punkty_doswiadczenia}/{self.poziom*10} do następnego")
        print(f"Masz {self.zycie}/{self.maksymalny_poziom_zycia} zycia.")

    def przypisz_quest(self, quest):
        if self.aktywny_quest:  # if self.aktywny_quest is not None:
            print("Już masz przypisane aktywne zadanie! Nie możesz wziąć drugiego póki nie skończysz obecnego.")
        else:
            print("Podjąłeś zadanie!")
            self.aktywny_quest = quest

    def dodaj_doswiadczenie(self, punkty):
        self.punkty_doswiadczenia += punkty
        if self.punkty_doswiadczenia >= 10 * self.poziom:
            self.punkty_doswiadczenia -= 10 * self.poziom
            self.poziom += 1
            # zazwyczaj w grach hack-n-slash, po uzyskaniu poziomu postać leczy się do maksimum poziomu zdrowia (Diablo)
            self.maksymalny_poziom_zycia = 100 + 10 * self.poziom
            self.zycie = self.maksymalny_poziom_zycia
            print(f"Awansowałeś na kolejny ({self.poziom}) poziom!")

    def ulecz_gracza(self):
        if self.zycie < self.maksymalny_poziom_zycia:
            indeks_jedzony_przedmiot = -1
            # Szukamy w ekwipunku jedzenia, zapisujemy indeks pozycji z listy gdy na jakieś trafimy. 
            # Następnie "jemy przedmiot" przy pomocy pop(), gdy znaleźliśmy go u siebie w ekwip.
            for indeks, przedmiot in enumerate(self.ekwipunek):
                if type(przedmiot) == przedmioty.Jedzenie:
                    indeks_jedzony_przedmiot = indeks
                    break
            if indeks_jedzony_przedmiot >= 0:
                jedzenie = self.ekwipunek.pop(indeks_jedzony_przedmiot)
                print(f"Zjadasz {jedzenie.nazwa}")
                print(f"Odzyskujesz {jedzenie.wartosc_statystyki} zdrowia!")
                self.zycie += jedzenie.wartosc_statystyki
        else:
            print("Masz maksymalny poziom życia!")

    def policz_sile_ataku(self):
        """zsumuj efektywny atak wszystkich przedmiotów ofensywnych w ekwipunku"""
        sila = 0
        for przedmiot in self.ekwipunek:
            if type(przedmiot) == przedmioty.Bron:
                sila += przedmiot.wartosc_statystyki
        return sila

    def policz_sile_obrony(self):
        """zsumuj efektywną obronę wszystkich przedmiotów defensywnych w ekwipunku"""
        obrona = 0
        for przedmiot in self.ekwipunek:
            # dla każdego przedmiotu o klasie "Zbroja":
            if type(przedmiot) == przedmioty.Zbroja:
                obrona += przedmiot.wartosc_statystyki
        return obrona
    


class Sprzedawca(Postac):
    def __init__(self, kredyty=None, ekwipunek=None) -> None:
        self.punkty_zycia = 100000000
        Postac.__init__(self, kredyty=kredyty, ekwipunek=ekwipunek)

    def losuj_inwentarz(self, dostepne_zbroje, dostepne_bronie, dostepne_jedzenie, dostepne_p_specjalne):
        """
        przekzujemy do funkcji wszystkie listy przedmiotów dostępnych w całej grze kategoriami
        następnie, na każdą grupę przedmiotów którą przekazaliśmy, rozszerzamy (ekwipunek.extend) 
        wyposażenie handlarza o jeden lub dwa (k=random.randint(1, 2))
        przedmioty z każdej kategorii, losując je z danej grupy (random.choices(grupa, k=ilosc_losowanych_przedmitow)).
        W ten sposób będziemy mieli losowy zbiór przedmiotów u handlarza, kiedykolwiek go odwiedzimy.
        """
        self.ekwipunek = []
        for grupa_przedmiotow in [dostepne_zbroje, dostepne_bronie, dostepne_jedzenie, dostepne_p_specjalne]:
            ilosc_losowanych_przedmitow = random.randint(1, 2)
            wybrane_przedmioty = random.choices(grupa_przedmiotow, k=ilosc_losowanych_przedmitow)
            self.ekwipunek.extend(wybrane_przedmioty)

    def wyswietl_ekwipunek(self):
        """dla obiektu klasy "Sprzedawca", wyświetl budżet sprzedawcy oraz przedmioty które ma na stanie"""
        print(f"\nBudżet sprzedawcy: {self.kredyty}")
        print("przedmioty handlarza:")
        for indeks, przedmiot in enumerate(self.ekwipunek):
            print(f"przedmiot {indeks+1}: ", przedmiot)


class Wrog(Postac):
    def __init__(self, nazwa, opis, poziom) -> None:
        self.nazwa = nazwa
        self.opis = opis
        self.punkty_zycia = 100
        self.poziom = poziom
        self.moc_ataku = 2 * self.poziom
        super().__init__(kredyty=self.poziom * 60)

    def zadaj_obrazenia(self, gracz: Gracz):
        gracz.zycie -= self.moc_ataku


if __name__ == "__main__":
    # krótkie sprawdzenie czy handlarz ma faktycznie losowy inwentaż za każdym uruchomieniem
    for i in range(5):
        s = Sprzedawca(kredyty=10000)
        s.losuj_inwentarz(["a1", "b1", "c1"], ["a2", "b2", "c2"], ["a3", "b3", "c3"], ["a4", "b4", "c4"])
        print(s.ekwipunek)
