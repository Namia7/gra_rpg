import random


rzadkosci = ['zwykly', 'niepospolity', 'rzadki']


nazwy_i_opisy_przedmiotow = {
    'jedzenie': [
        ("Galaktyczny Burger", "Burger wyhodowany z syntetycznego mięsa, popularny wśród kosmicznych podróżników."),
        ("Astro Nutrient Bar", "Zawiera wszystkie potrzebne składniki odżywcze dla astronauty na misji."),
        ("Plazmowe Żelki", "Żelki pełne energii, uwalnianej podczas trudnych lotów."),
        ("Suplement Omega", "Suplement diety zwiększający odporność na zmiany grawitacyjne."),
        ("Chipsy Selenowe", "Chipsy przyprawione regolitem, z dodatkiem smaku księżycowego sera."),
    ],
    'broń': [
        ("Laser Blaster", "Broń laserowa o wysokiej mocy, idealna do walki w przestrzeni kosmicznej."),
        ("Pistolet Ionyczny", "Wysyła ładunki jonowe, które mogą unieruchomić przeciwnika."),
        ("Promiennik Gamma", "Wystrzeliwuje promienie gamma, zdolne przenikać przez większość metali."),
        ("Falownik Cząsteczkowy", "Broń, która dezintegruje materię na poziomie atomowym."),
        ("Kusza Kwantowa", "Wykorzystuje mechanikę kwantową do teleportowania strzał."),
    ],
    'przedmiot specjalny': [
        ("Tarcza Energii", "Generuje pole ochronne wokół użytkownika."),
        ("Modulator Czasu", "Pozwala na krótkie przeskoki w czasie, użyteczne w krytycznych momentach."),
        ("Dysk Holograficzny", "Projektor tworzący realistyczne hologramy do dezorientacji wroga."),
        ("Implant Cybernetyczny", "Implant zwiększający możliwości percepcyjne i reakcje."),
        ("Detektor Anomalii", "Urządzenie wykrywające rzadkie zjawiska kosmiczne i anomalie."),
    ],
    'zbroja': [
        ("Pancerz Kosmiczny", "Wzmocniony pancerz zapewniający ochronę w warunkach zerowej grawitacji."),
        ("Kombinezon Astro", "Kombinezon przystosowany do długotrwałych misji kosmicznych."),
        ("Hełm Neutronowy", "Hełm chroniący głowę przed promieniowaniem i mikrometeorytami."),
        ("Rękawice Kometarne", "Rękawice zapewniające lepszy chwyt i ochronę w ekstremalnych warunkach."),
        ("Buty Grawitacyjne", "Buty umożliwiające chodzenie po różnych powierzchniach planetarnych bez utraty przyczepności."),
    ]
}

przedmioty_startowe = [
    ('Wielka Księga Handlu', 'Stara, obszerna księga zawierająca tajniki i techniki handlu międzygalaktycznego.'),
    ('Pieczęć Dyplomatyczna', 'Oficjalna pieczęć używana do zatwierdzania międzynarodowych umów i traktatów.'),
    ('Klucz Sterujący statku Aurora', 'Urządzenie do sterowania najnowszym modelem statku kosmicznego, Aurora.'),
    ('Elektroniczny Wytrych', 'Zaawansowany elektroniczny narzędzie do otwierania zamków cyfrowych.'),
]

class Przedmiot:
    def __init__(self, nazwa, opis, cena, wartosc_statystyki, kategoria, rzadkosc) -> None:
        self.nazwa = nazwa
        self.opis = opis
        self.cena = cena
        self.wartosc_statystyki = wartosc_statystyki
        self.kategoria = kategoria
        self.rzadkosc = rzadkosc

    def __str__(self) -> str:
        # dzięki tej funkcji tego już nie będzie -> <przedmioty.PrzedmiotSpecjalny object at 0x000001D8031EDA10>
        # zamiast tego co powyżej wyświetli się tekst, który zapiszemy i zwrócimy -> "return"
        return f"{self.nazwa}\n{self.opis}\nwartość: {self.cena}, " \
            f"statystyka: {self.wartosc_statystyki}, kategoria: {self.kategoria}, rzadkość: {self.rzadkosc}"


class Zbroja(Przedmiot):
    def __init__(self, nazwa, opis, cena, wartosc_statystyki, kategoria, rzadkosc) -> None:
        super().__init__(nazwa, opis, cena, wartosc_statystyki, kategoria, rzadkosc)

    def zmniejsz_obrazenia(self, obrazenia):
        # na ten moment nie jest to wykorzystywane, ale może się przyda później
        return obrazenia - self.wartosc_statystyki



class Bron(Przedmiot):
    def __init__(self, nazwa, opis, cena, wartosc_statystyki, kategoria, rzadkosc) -> None:
        super().__init__(nazwa, opis, cena, wartosc_statystyki, kategoria, rzadkosc)

    def zadaj_obrarzenia(self, wrog):
        wrog.punkty_zycia -= self.wartosc_statystyki


class Jedzenie(Przedmiot):
    def __init__(self, nazwa, opis, cena, wartosc_statystyki, kategoria, rzadkosc) -> None:
        super().__init__(nazwa, opis, cena, wartosc_statystyki, kategoria, rzadkosc)

    def wylecz(self, gracz):
        gracz.zycie += self.wartosc_statystyki


class PrzedmiotSpecjalny(Przedmiot):
     """
     ta klasa przedmiotów nie ma specjalnych właściwości, lecz pozwala kończyć zadania w inny 
     niedostępny normalnie sposób, gdy się je posiada
     """
     def __init__(self, nazwa, opis, cena, wartosc_statystyki, kategoria, rzadkosc) -> None:
        super().__init__(nazwa, opis, cena, wartosc_statystyki, kategoria, rzadkosc)


