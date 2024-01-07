from datetime import datetime, date

def cd(t):
    miesiace = {
        'stycznia': 1, 'lutego': 2, 'marca': 3, 'kwietnia': 4, 'maja': 5, 'czerwca': 6,
        'lipca': 7, 'sierpnia': 8, 'września': 9, 'października': 10, 'listopada': 11, 'grudnia': 12
    }

    for miesiac in miesiace:
        t = t.replace(miesiac, str(miesiace[miesiac]))

    format_daty = "%d %m, %H:%M"
    data = datetime.strptime(t, format_daty)

    # Ustal bieżący rok
    biezacy_rok = date.today().year

    # Zaktualizuj datę, pozostawiając rok z bieżącego roku
    data = data.replace(year=biezacy_rok)

    return data
