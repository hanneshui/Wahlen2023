import streamlit as st
import matplotlib.pyplot as plt


def calc_total_votes(votes):
    total_votes = sum(votes.values())
    return total_votes


def calc_wahlbeteiligung(votes, wahlberechtigte):
    total_votes = calc_total_votes(votes)
    if wahlberechtigte == 0:
        return 1
    wahlbeteiligung = ((total_votes / 4.0) / wahlberechtigte)
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


def calc_size(votes):
    #erstzuteilung
    




def plot_sitze(sitze):
    return 0


def main():
    # Side title in the main field
    st.title('Nationalratswahlen 2023 Simulation Sitzzuteilung Basel')
    st.write('##### Es wurde die Listenverbindung Zwischen SP und Grünen und zwischen EVP, GLP, Mitte, FDP, LDP berücksichtigt. Unterlisten sind nicht einzeln aufgeführt und werden zu den jeweiligen Mutterparteistimmen gerechnet. Der Einfachheit halber wurden die restlichen vereinzelten Stimmen zusammengefasst, obwohl diese nicht über eine Listenverbindung verfügen. Die Standartwerte sind auf Basis der Wahlen 2019 gesetzt.')
    st.write(
        'Das folgende Tool simuliert die Sitzverteilung für die Nationalratswahlen 2023 in Basel gemäss Bundesgesetz über die politischen Rechte. Das tool wurde von [Hannes Hui](https://hanneshui.ch) entworfen und umgesetzt. Die Korrektheit der Simulation ist nicht garantiert. Bei Fehlern oder Verbesserungsvorschlägen freue ich mich über eure Rückmeldung. Zur Transparenz und vereinfachten Mitwirkung befindet sich der Source Code dieses Projektes frei zugänglich auf Github: [Repository](https://github.com/hanneshui/Wahlen2023)')
    st.sidebar.title('Parteistimmen für Nationalratswahlen 2023 Basel')

    # Input number of votes for each pair of parties in the sidebar
    parties = ['SP', 'Grüne', 'GLP',
               'FDP', 'LDP', 'Die Mitte', 'EVP',  'SVP', 'Andere']
    votes = {}

    votes = {party: st.sidebar.number_input(
        f'Stimmen für {party}:', min_value=0) for party in parties}
    wahlberechtigte = st.sidebar.number_input('Wahlberechtigte:', min_value=0)

    # Calculate percentages
    percentages = calculate_percentages(votes)

    # Display total votes and Wahlbeteiligung

    wahlbeteiligung = calc_wahlbeteiligung(votes, wahlberechtigte)

    st.write(f'##### Wahlbeteiligung: {wahlbeteiligung:.2%}')
    # Display diagram with percentages
    plot_diagram(percentages)

    # Calclulate Verteilung Listenverbindungen


    # Calculate Verteilug in Listenverbindungen

    #Plot Sitzverteilung


if __name__ == '__main__':
    main()
