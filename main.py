import random
from time import sleep

import teksty_historia_i_swiat
import instrukcje_gry
import postacie
import przedmioty
import questy



class Gra:

    def __init__(self) -> None:
        self.gracz = None
        self.przedmioty_bron: list = []
        self.przedmioty_zbroje: list = []
        self.przedmioty_jedzenie: list = []
        self.przedmioty_specjalne: list = []
        self.przedmioty_startowe: list = []
        self.lista_wrogow: list = []
        self.lista_questow: list = []

    def generuj_przedmioty(self):

        for kategoria in przedmioty.nazwy_i_opisy_przedmiotow:
            for nazwa, opis in przedmioty.nazwy_i_opisy_przedmiotow[kategoria]:
                if kategoria == 'przedmiot specjalny':
                    wartosc_statystyki = None
                else:
                    wartosc_statystyki = random.randint(1, 10)

                # formatka-slownik z opisem cech przedmiotu
                przedmiot = {
                    "nazwa": nazwa,
                    "opis": opis,
                    "cena": random.randint(105, 200),
                    "wartosc_statystyki": wartosc_statystyki,
                    "kategoria": kategoria,
                    "rzadkosc": 'zwykle',
                }
                if kategoria == 'zbroja':
                    self.przedmioty_zbroje.append(przedmioty.Zbroja(**przedmiot))
                elif kategoria == 'broń':
                    self.przedmioty_bron.append(przedmioty.Bron(**przedmiot))
                elif kategoria == 'jedzenie':
                    # modyfikacja "formatki" dla przypadku jedzenia - tanszy 
                    # przedmiot z większą statystyką który ma leczyć (zużywalny)
                    przedmiot["cena"] = round(przedmiot["cena"] / 8) + 3
                    przedmiot["wartosc_statystyki"] *= 4 + 9
                    self.przedmioty_jedzenie.append(przedmioty.Jedzenie(**przedmiot))
                elif kategoria == 'przedmiot specjalny':
                    self.przedmioty_specjalne.append(przedmioty.PrzedmiotSpecjalny(**przedmiot))

        for nazwa, opis in przedmioty.przedmioty_startowe:
            # formatka-slownik z opisem cech przedmiotu
            przedmiot = {
                "nazwa": nazwa,
                "opis": opis,
                "cena": random.randint(5, 100),
                "wartosc_statystyki": None,
                "kategoria": 'przedmiot specjalny',
                "rzadkosc": 'rzadki',
            }
            # -> rozpakowanie formatki do klasy PrzedmiotSpecjalny za pomocą -> **
            self.przedmioty_startowe.append(przedmioty.PrzedmiotSpecjalny(**przedmiot))

    def generuj_wrogow(self):
        for nazwa, opis, poziom in postacie.wrogowie:
            wrog = {
                "nazwa": nazwa,
                "opis": opis,
                "poziom": poziom
            }
            self.lista_wrogow.append(postacie.Wrog(**wrog))

    def generuj_questy(self):
        for nazwa, opis, nagroda, indeks_potwora_z_listy, ilosc_wymagana in questy.questy:
            quest = {
               "nazwa": nazwa,
               "opis": opis,
               "nagroda_w_sel": nagroda,
               "potwor_do_pokonania": self.lista_wrogow[indeks_potwora_z_listy].nazwa,
               "warunek_ukonczenia": ilosc_wymagana,
            }
            self.lista_questow.append(questy.Quest(**quest))

    def ustawienia_poczatkowe_gracza(self):
        print(instrukcje_gry.instrukcja_kreator_postaci)
        imie_postaci = input(instrukcje_gry.instrukcja_kreator_postaci_wybor_imienia)
        if len(imie_postaci) > 40:
            imie_postaci = imie_postaci[:40]

        print(instrukcje_gry.instrukcja_kreator_postaci_wybor_pochodzenia)
        while True:
            decyzja = input(" -> ")
            if decyzja in ['p1', 'p2', 'p3']:
                if decyzja == 'p1':
                    print(teksty_historia_i_swiat.player_backstory_trading)
                if decyzja == 'p2':
                    print(teksty_historia_i_swiat.player_backstory_diplomat)
                if decyzja == 'p3':
                    print(teksty_historia_i_swiat.player_backstory_military)
            elif decyzja in ['1', '2', '3']:
                if decyzja == "1":
                    poziom_poczatkowy = 4
                    poczatkowe_pieniadze = 300
                    poczatkowy_ekwipunek = [self.przedmioty_startowe[0]]
                elif decyzja == "2":
                    poziom_poczatkowy = 2
                    poczatkowe_pieniadze = 100
                    poczatkowy_ekwipunek = [self.przedmioty_startowe[1]]
                else:
                    poziom_poczatkowy = 1
                    poczatkowe_pieniadze = 150
                    poczatkowy_ekwipunek = [self.przedmioty_startowe[2], self.przedmioty_startowe[3]]

                skonfigurowany_gracz = postacie.Gracz(
                    poziom=poziom_poczatkowy,
                    pochodzenie=decyzja,
                    imie_postaci=imie_postaci,
                    kredyty_poczatkowe=poczatkowe_pieniadze,
                    poczatkowy_ekwipunek=poczatkowy_ekwipunek
                )
                print('dokonano wyboru')
                break
            elif decyzja == "h":
                print(instrukcje_gry.instrukcja_kreator_postaci_wybor_pochodzenia)
            else:
                print(instrukcje_gry.instrukcja_niezrozumiale_polecenie)

        return skonfigurowany_gracz

    def rozpocznij_gre(self):
        start_game = False
        while True:
            print("Czy chcesz rozpocząć nową grę?")
            decyzja = input("t/T/tak -> rozpoczyna grę, n/N/nie -> kończy rozgrywke\n -> ")
            if decyzja in ["n", "N", "nie"]:
                break
            elif decyzja in ["t", "T", "tak"]:
                start_game = True
                break
            else:
                print(instrukcje_gry.instrukcja_niezrozumiale_polecenie)

        return start_game

    def handel(self, gracz: postacie.Gracz):
        print(instrukcje_gry.instrukcja_przywitanie_handlarza)
        print(instrukcje_gry.instrukcja_handlarz.format(gracz.kredyty))
        handlarz = postacie.Sprzedawca(kredyty=10000)
        handlarz.losuj_inwentarz(
            dostepne_bronie=self.przedmioty_bron,
            dostepne_jedzenie=self.przedmioty_jedzenie,
            dostepne_p_specjalne=self.przedmioty_specjalne,
            dostepne_zbroje=self.przedmioty_zbroje
        )
        handlarz.wyswietl_ekwipunek()
        zakoncz_handel = False
        
        while not zakoncz_handel:
            decyzja_gracza = input("wybierz przedmiot lub dzialanie -> ")
            
            if decyzja_gracza in [str(i+1) for i in range(len(handlarz.ekwipunek))]:
                # gracz - użytkownik programu - jako "decyzja gracza" wpisuje numer przedmiotu ktory decyduje sie kupic
                # i + 1 -> tak wyświetlamy dla gracza i tak odbieramy ego decyzję z konsoli przez "input()"
                # i - 1 -> tak przeszukujemy tablicę "ekwipunek handlarza", bo python ma liczenie od "0" a nie od "1"
                # musimy też odjąć "-1" bo przetwarzamy decyzję gracza która była "+1"
                wybrany_przedmiot_od_handlarza = handlarz.ekwipunek[int(decyzja_gracza)-1]
                if wybrany_przedmiot_od_handlarza.cena <= gracz.kredyty:
                    # moge kupic - proces kupna przedmiotu
                    gracz.kredyty = gracz.kredyty - wybrany_przedmiot_od_handlarza.cena
                    gracz.ekwipunek.append(wybrany_przedmiot_od_handlarza)
                    handlarz.ekwipunek.pop(int(decyzja_gracza)-1)
                    handlarz.kredyty += wybrany_przedmiot_od_handlarza.cena
                    print(f"\nkupiłeś: {wybrany_przedmiot_od_handlarza}")
                    print(f"twoje pozostałe kredyty: {gracz.kredyty}")
                    handlarz.wyswietl_ekwipunek()
                else:
                    # nie moge kupic - wyswietl wiadomosc i kontynuuj
                    print("\nNie możesz kupić tego przedmiotu, jest zbyt drogi")
            elif decyzja_gracza == "h":
                print(instrukcje_gry.instrukcja_handlarz.format(gracz.kredyty))
            elif decyzja_gracza in ["e", "ekwipunek"]:
                handlarz.wyswietl_ekwipunek()
            elif decyzja_gracza == "exit":
                zakoncz_handel = True
                print("Miło było z tobą porozmawiać!")
                print("Wracasz do centrum miasta...")
            else:
                print(instrukcje_gry.instrukcja_niezrozumiale_polecenie)

    def niebezpieczne_miejsce(self, gracz: postacie.Gracz):
        print(teksty_historia_i_swiat.backstory_niebezpieczne_miejsce)
        print(instrukcje_gry.instrukcja_niebezpieczne_miejsce)

        potwor: postacie.Wrog = random.choice(self.lista_wrogow)
        print(f"Napotykasz {potwor.nazwa}")

        if gracz.poziom < potwor.poziom:
            print(f"Twój poziom ({gracz.poziom}) jest niższy od wroga ({potwor.poziom}) ")
        decyzja = input("Czy chcesz uciec? ('t/T/Tak' jeżeli chcesz) -> ")
        if decyzja.lower() in ['t', 'tak']:
            print("Uciekasz z niebezp. miejsca")
            return

        sila_gracza = 5 + 0.5 * gracz.poziom + gracz.policz_sile_ataku()
        # w sile potwora, nie może być ujemnych punktów bo wtedy będziemy leczyć gracza! (-- = +!)
        # dlatego robimy max(0, modyfikator), żeby tego uniknąć
        sila_potwora = 2 + max(0, potwor.moc_ataku - gracz.policz_sile_obrony())
        # petla while -> odejmowanie życia od wroga, odejmowanie życia od gracza, 
        # wyświetlanie wyniku "gracz zadał {X} obr {nazwa potwora}" i to samo z perspektywy wroga
        while (potwor.punkty_zycia > 0) and (gracz.zycie > 0):
            potwor.punkty_zycia -= sila_gracza
            gracz.zycie -= sila_potwora
            sleep(0.7)
            print(f"gracz zadal {sila_gracza} obrarzen {potwor.nazwa}, (pozostało: {potwor.punkty_zycia})")
            sleep(0.7)
            print(f"potwor zadal ci {sila_potwora} obrarzen , (pozostało: {gracz.zycie})")
    
        if gracz.zycie <= 0:
            print("Zostałes pokonany!")
            return

        if potwor.punkty_zycia <=0:
            print("Wygrałeś nierówną walkę z potworem!")
            gracz.dodaj_doswiadczenie(potwor.poziom * 3)
            # "przeszukanie pokonanego potwora"
            gracz.kredyty += potwor.kredyty
            potwor.kredyty = 0

        # sprawdzenie questa, jeżeli gracz go ma:
        if gracz.aktywny_quest:
            # jak pokonany potwor jest tym na ktorego polowalismy -> dodaj postep
            if potwor.nazwa == gracz.aktywny_quest.nazwa_potwora_ze_zlecenia:
                gracz.aktywny_quest.aktualny_postep += 1

            if gracz.aktywny_quest.czy_skonczony():
                # quest ukonczony
                gracz.kredyty += gracz.aktywny_quest.nagroda_w_sel
                print(f"Ukończono zadanie: {gracz.aktywny_quest.nazwa} i otrzymano nagrody ({gracz.aktywny_quest.nagroda_w_sel} SEL)")
                gracz.aktywny_quest = None  # quest już skonczony -> None (brak questa mozna nowy) 

                # zresetuj tablice zadan z powodu ukonczenia jednego z nich
                self.lista_questow = []
                self.generuj_questy()

        # "regeneracja lokacji" na przyszłość -> inaczej wrog zostanie "martwy" w liscie i cały czas będzie wybierany jako 
        # mający 0 punktów życia (nie regenerujemy obiektu w liście po walce)
        self.lista_wrogow = []
        self.generuj_wrogow()

    def zdobadz_questa(self, gracz: postacie.Gracz):
        nowy_quest: questy.Quest = random.choice(self.lista_questow)
        print("Próbujesz podjąć się następującego zadania:")
        nowy_quest.wyswietl_zadanie()
        nowy_quest.wyswietl_postep()
        gracz.przypisz_quest(nowy_quest)

    def leczenie_gracza(self, gracz: postacie.Gracz):
        print(instrukcje_gry.instrukcja_leczenie_postaci)
        gracz.ulecz_gracza()

    def glowna_petla_gry(self):
        print("Moonword")
        print(teksty_historia_i_swiat.backstory)
        decyzja_start_gry = self.rozpocznij_gre()
        if not decyzja_start_gry:
            return
        self.generuj_przedmioty()
        self.generuj_wrogow()
        self.generuj_questy()
        nowy_gracz = self.ustawienia_poczatkowe_gracza()

        # 1. zdobądz informacje od tubylcow, podejmij zadanie
        # 2. pojdz do handlarza
        # 3. podejmij się walki z potworem
        # 4. ulecz sie
        # 5. wyswietl informacje o graczu
        # 6. wyjdz z gry
        end_game = False
        print(instrukcje_gry.instrukcja_glowna_petla_gry)
        while not end_game:
            # przetestowanie czy ta petla ma sens:
            decyzja = input("wybierz gdzie się udać z centrum miasta (1 - 5) (6 - koniec gry) -> ")
            if decyzja in ["1", "zadanie", "quest"]:
                self.zdobadz_questa(nowy_gracz)
            elif decyzja in ["2", "handlarz"]:
                # jezeli blad -> skopiuj tu z konsoli co wyjdzie
                self.handel(nowy_gracz)
            elif decyzja in ["3", "potwor", "walka"]:
                self.niebezpieczne_miejsce(nowy_gracz)
                if nowy_gracz.zycie <= 0:
                    print("Koniec gry, spróbuj ponownie inną postacią, bądź zmień taktykę")
                    end_game = True
            elif decyzja in ["4", "leczenie"]:
                self.leczenie_gracza(nowy_gracz)
            elif decyzja in ["5", "gracz", "info", "e"]:  # e-> 
                nowy_gracz.wyswietl_pochodzenie()
                print("twój ekwipunek:")
                nowy_gracz.wyswietl_ekwipunek()
                nowy_gracz.wyswietl_statystyki()
                if nowy_gracz.aktywny_quest:
                    print(f"Posiadasz aktywne zadanie: {nowy_gracz.aktywny_quest.nazwa}")
                    nowy_gracz.aktywny_quest.wyswietl_postep()
            elif decyzja in ["6", "exit", "zakoncz gre", "wyjdz z gry"]:
                end_game = True
                break
            elif decyzja == "h":
                print(instrukcje_gry.instrukcja_glowna_petla_gry)
            else:
                print(instrukcje_gry.instrukcja_niezrozumiale_polecenie)

        print("zakończono grę")

if __name__ == '__main__':
    gra = Gra()
    gra.glowna_petla_gry()
