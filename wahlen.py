import streamlit as st
import matplotlib.pyplot as plt
import math
import random


def calc_total_votes(votes):
    total_votes = sum(votes.values())
    return total_votes


def calc_wahlbeteiligung(votes, wahlberechtigte, anzahl_sitze=4):
    total_votes = calc_total_votes(votes)
    if wahlberechtigte == 0:
        return 1
    wahlbeteiligung = ((total_votes / anzahl_sitze) / wahlberechtigte)
    return wahlbeteiligung


def calculate_percentages(votes):
    total_votes = calc_total_votes(votes)
    if total_votes == 0:
        return {party: 0 for party in votes.keys()}
    percentages = {party: (count / total_votes) *
                   100 for party, count in votes.items()}
    return percentages


def plot_diagram(percentages):
    plt.figure(figsize=(8, 6))
    plt.bar(percentages.keys(), percentages.values())
    plt.xlabel('Pateien')
    plt.ylabel('% der Stimmen')
    plt.title('Stimmverhältnisse')
    plt.xticks(rotation=45)

    for party, percentage in percentages.items():
        plt.text(party, percentage,
                 f'{percentage:.2f}%', ha='center', va='bottom')
    st.pyplot(plt)


def calc_sitze(votes, anz_sitze):
    # erstzuteilung
    anz_parteistimmen = calc_total_votes(votes)
    verteilungszahl = math.ceil(anz_parteistimmen / (anz_sitze+1))
    if (anz_parteistimmen % (anz_sitze+1) == 0):
        verteilungszahl += 1
    erstzuteilung = {party: math.floor(
        count / verteilungszahl) for party, count in votes.items()}
    rest = {party: (count % verteilungszahl) for party, count in votes.items()}

    # print('erstzuteilung', erstzuteilung)
    # print('rest', rest)

    # restmandate
    while (sum(erstzuteilung.values()) < anz_sitze):
        quotient = {party: count /
                    (erstzuteilung[party]+1) for party, count in votes.items()}
        max_quotient = max(quotient.values())
        max_quotient_parties = [key for key,
                                value in votes.items() if value == max_quotient]
        # print('quotient', quotient)
        if (len(max_quotient_parties) == 1):
            erstzuteilung[max_quotient_parties[0]] += 1
        else:
            # verteilung nach rest erstzuteilung
            max_rest = max(rest.values())
            max_rest_parties = [key for key,
                                value in rest.items() if value == max_rest]
            if (len(max_rest_parties) == 1):
                erstzuteilung[max_rest_parties[0]] += 1
            else:
                # zuteilung nach parteistimmen
                max_parteistimmen = max(votes.values())
                max_parteistimmen_parties = [
                    key for key, value in votes.items() if value == max_parteistimmen]
                if (len(max_parteistimmen_parties) == 1):
                    erstzuteilung[max_parteistimmen_parties[0]] += 1
                else:
                   # theoretisch nach eizelstimmenzahl hier aber per los
                    random_key = random.choice(list(erstzuteilung.keys()))
                    erstzuteilung[random_key] += 1
    return erstzuteilung


def sitze_zuteilen(votes, sitze_insgesamt):
    # Calclulate Verteilung Listenverbindungen
    lv = {'rot-grün': votes['SP']+votes['Grüne'], 'bürgerlich': votes['GLP']+votes['FDP'] +
          votes['LDP']+votes['Die Mitte']+votes['EVP'], 'SVP': votes['SVP'], 'Andere': votes['Andere']}
    sitze = calc_sitze(lv, sitze_insgesamt)

    # Calculate Verteilug in Listenverbindungen

    sitze_rot_grün = calc_sitze(
        {'SP': votes['SP'], 'Grüne': votes['Grüne']}, sitze['rot-grün'])
    sitze_bürgerlich = calc_sitze({'GLP': votes['GLP'], 'FDP': votes['FDP'], 'LDP': votes['LDP'],
                                  'Die Mitte': votes['Die Mitte'], 'EVP': votes['EVP']}, sitze['bürgerlich'])
    print('sitze', sitze)
    print('sitze_rot_grün', sitze_rot_grün)
    print('sitze_bürgerlich', sitze_bürgerlich)
    sitze_final = {'SP': sitze_rot_grün['SP'], 'Grüne': sitze_rot_grün['Grüne'], 'GLP': sitze_bürgerlich['GLP'], 'FDP': sitze_bürgerlich['FDP'],
                   'LDP': sitze_bürgerlich['LDP'], 'Die Mitte': sitze_bürgerlich['Die Mitte'], 'EVP': sitze_bürgerlich['EVP'], 'SVP': sitze['SVP'], 'Andere': sitze['Andere']}
    # Plot Sitzverteilung
    # if (False):
    if (sum(sitze_final.values()) != sitze_insgesamt):
        st.warning('Sitzverteilung fehlgeschlagen:')

    else:
        plot_sitze(sitze_final)


def plot_sitze(sitze):
    plt.figure(figsize=(8, 6))
    plt.bar(sitze.keys(), sitze.values())
    plt.xlabel('Pateien')
    plt.ylabel('Sitze')
    plt.title('Sitzzuteilung')
    plt.xticks(rotation=45)

    for party, sitze in sitze.items():
        plt.text(party, sitze,
                 f'{sitze}', ha='center', va='bottom')

    st.pyplot(plt)


def main():
    # title
    st.set_page_config(page_title='Wahlen 2023 Basel')
    # Side title in the main field
    st.title('Nationalratswahlen 2023 Simulation Sitzzuteilung Basel')
    st.write('##### Es wurde die Listenverbindung Zwischen SP und Grünen und zwischen EVP, GLP, Mitte, FDP, LDP berücksichtigt. Unterlisten sind nicht einzeln aufgeführt und werden zu den jeweiligen Mutterparteistimmen gerechnet. Der Einfachheit halber wurden die restlichen vereinzelten Stimmen zusammengefasst, obwohl diese nicht über eine Listenverbindung verfügen. Die Standartwerte sind auf Basis der Wahlen 2019 gesetzt.')
    st.write(
        'Das folgende Tool simuliert die Sitzverteilung für die Nationalratswahlen 2023 in Basel gemäss Bundesgesetz über die politischen Rechte. Das tool wurde von [Hannes Hui](https://hanneshui.ch) entworfen und umgesetzt. Die Korrektheit der Simulation ist nicht garantiert. Bei Fehlern oder Verbesserungsvorschlägen freue ich mich über eure Rückmeldung. Zur Transparenz und vereinfachten Mitwirkung befindet sich der Source Code dieses Projektes frei zugänglich auf Github: [Repository](https://github.com/hanneshui/Wahlen2023)')
    st.sidebar.title('Parteistimmen für Nationalratswahlen 2023 Basel')

    # Input number of votes for each pair of parties in the sidebar standart value is result of 2019 elections
    parties = {'SP': 87475, 'Grüne': 52949, 'GLP': 15267,
               'FDP': 16194, 'LDP': 41077, 'Die Mitte': 13229, 'EVP': 5406,  'SVP': 33845, 'Andere': 2475}
    votes = {}

    votes = {party: st.sidebar.number_input(
        f'Stimmen für {party}:', min_value=0, value=v, step=500) for party, v in parties.items()}
    wahlberechtigte = st.sidebar.number_input(
        'Wahlberechtigte:', min_value=0, step=1000, value=114139)
    sitze_insgesamt = st.sidebar.number_input(
        'Anzahl Sitze', min_value=0, value=4, step=1)

    if (sum(votes.values()) == 0):
        st.warning('Bitte Stimmen eingeben')
        return

    # if button then perform calculations
    if st.button('Berechnungen Starten'):

        # Calculate percentages
        percentages = calculate_percentages(votes)

        # Display total votes and Wahlbeteiligung

        wahlbeteiligung = calc_wahlbeteiligung(
            votes, wahlberechtigte, sitze_insgesamt)

        st.write(f'##### Wahlbeteiligung: {wahlbeteiligung:.2%}')
        st.write('(Gilt nur falls alle Stimmen abgegeben werden)')
        # Display diagram with percentages
        plot_diagram(percentages)

        sitze_zuteilen(votes, sitze_insgesamt)


if __name__ == '__main__':
    main()
