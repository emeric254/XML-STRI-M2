import requests
from lxml import etree

films = []
persons = []
temp_persons = {}

film_codes = [
    '241697',
    '246693',
    '237510',
    '246693',
    '245360',
    '237879',
    '241700',
    '228834',
    '228189',
    '239210',
    '243226',
    '231299'
]

jury_codes = {
    '9685',
    '14398',
    '6414',
    '88478',
    '731082',
    '11882',
    '675127',
    '561'
}

for code_film in film_codes:
    r = requests.get('http://api.allocine.fr/rest/v3/movie'
                     '?partner=YW5kcm9pZC12Mg&profile=large&format=json&filter=movie'
                     '&code=' + code_film)
    if r.status_code is 200 and 'movie' in r.json():
        film_rp = r.json()['movie']
        film = {
            'title': film_rp['title'],
            'code': film_rp['code'],
            'movie_type': film_rp['movieType']['$'],
            'production_year': film_rp['productionYear'],
            'release_date': film_rp['release']['releaseDate'],
            'synopsis': film_rp['synopsis'],
            'duration': film_rp['runtime'],  # TODO verify this shit !
            'nationalities': [],
            'languages': [],
            'genres': [],
            'cast_members': []
        }
        for nation in film_rp['nationality']:
            film['nationalities'].append(nation['$'])
        for lang in film_rp['language']:
            film['languages'].append(lang['$'])
        for genre in film_rp['genre']:
            film['genres'].append(genre['$'])
        for person in film_rp['castMember']:
            film['cast_members'].append({
                'code': person['person']['code'],
                'role': person['activity']['$']
            })
            temp_persons[person['person']['code']] = ''
        films.append(film)

for code in jury_codes:
    temp_persons[code] = ''
for code_person in temp_persons:
    r = requests.get('http://api.allocine.fr/rest/v3/person'
                     '?partner=YW5kcm9pZC12Mg&profile=large&format=json'
                     '&code=' + str(code_person))
    if r.status_code is 200 and 'person' in r.json():
        person_rp = r.json()['person']
        person = {
            'code': person_rp['code'],
            'name': (person_rp['name']['family'] if 'family' in person_rp['name'] else '')
                    + ' ' + person_rp['name']['given'] if 'given' in person_rp['name'] else '',
            'biography': person_rp['biography'] if 'biography' in person_rp else '',
            'gender': '',
            'nationalities': []
        }
        if 'gender' in person_rp:
            person['gender'] = 'male' if person_rp['gender'] is 1 else 'female'
        else:
            person['gender'] = 'other'
        if 'nationality' in person_rp:
            for nation in person_rp['nationality']:
                person['nationalities'].append(nation['$'])
        persons.append(person)

# gen xml
x_root = etree.Element('Cannes')
x_root.set('year', '2016')

x_movies = etree.SubElement(x_root, 'movies')
for film in films:
    x_film = etree.SubElement(x_movies, 'movie')
    etree.SubElement(x_film, 'code').text = str(film['code'])
    etree.SubElement(x_film, 'title').text = film['title']
    etree.SubElement(x_film, 'movie_type').text = film['movie_type']
    etree.SubElement(x_film, 'production_year').text = str(film['production_year'])
    etree.SubElement(x_film, 'release_date').text = film['release_date']
    etree.SubElement(x_film, 'duration').text = str(film['duration'])
    etree.SubElement(x_film, 'synopsis').text = film['synopsis']
    x_nationalities = etree.SubElement(x_film, 'nationalities')
    for nation in film['nationalities']:
        x_nation = etree.SubElement(x_nationalities, 'nationality')
        etree.SubElement(x_nation, 'name').text = nation
    x_languages = etree.SubElement(x_film, 'languages')
    for lang in film['languages']:
        x_lang = etree.SubElement(x_languages, 'language')
        etree.SubElement(x_lang, 'name').text = lang
    x_genres = etree.SubElement(x_film, 'genres')
    for genre in film['genres']:
        x_genre = etree.SubElement(x_genres, 'genre')
        etree.SubElement(x_genre, 'name').text = genre
    x_cast_members = etree.SubElement(x_film, 'cast_members')
    for person in film['cast_members']:
        x_person = etree.SubElement(x_cast_members, 'person')
        x_person.set('code', str(person['code']))
        etree.SubElement(x_person, 'role').set('name', str(person['role']))

x_jury = etree.SubElement(x_root, 'jury')
for code in jury_codes:
    x_person = etree.SubElement(x_jury, 'person')
    x_person.set('code', str(code))

x_persons = etree.SubElement(x_root, 'persons')
for person in persons:
    x_person = etree.SubElement(x_persons, 'person')
    etree.SubElement(x_person, 'code').text = str(person['code'])
    etree.SubElement(x_person, 'name').text = person['name']
    etree.SubElement(x_person, 'gender').text = person['gender']
    etree.SubElement(x_person, 'biograhy').text = person['biography']
    x_nationalities = etree.SubElement(x_person, 'nationalities')
    for nation in person['nationalities']:
        x_nation = etree.SubElement(x_nationalities, 'nationality')
        x_nation.set('name', nation)

x_palmares = etree.SubElement(x_root, 'palmares')
x_prix = etree.SubElement(x_palmares, 'prix')
x_prix.set('name', 'Palme d\'or')
etree.SubElement(x_prix, 'film').set('code', str(241697))
x_prix = etree.SubElement(x_palmares, 'prix')
x_prix.set('name', 'Grand prix')
etree.SubElement(x_prix, 'film').set('code', str(237510))
x_prix = etree.SubElement(x_palmares, 'prix')
x_prix.set('name', 'Prix de la mise en scène')
etree.SubElement(x_prix, 'film').set('code', str(241700))
x_prix = etree.SubElement(x_palmares, 'prix')
x_prix.set('name', 'Prix de la mise en scène')
etree.SubElement(x_prix, 'film').set('code', str(237879))
x_prix = etree.SubElement(x_palmares, 'prix')
x_prix.set('name', 'Prix du scénario')
etree.SubElement(x_prix, 'film').set('code', str(245360))
x_prix = etree.SubElement(x_palmares, 'prix')
x_prix.set('name', 'Prix du jury')
etree.SubElement(x_prix, 'film').set('code', str(228834))
x_prix = etree.SubElement(x_palmares, 'prix')
x_prix.set('name', 'Prix d\'interprétation féminine')
etree.SubElement(x_prix, 'film').set('code', str(246693))
x_prix = etree.SubElement(x_palmares, 'prix')
x_prix.set('name', 'Prix d\'interprétation masculine')
etree.SubElement(x_prix, 'film').set('code', str(245360))
x_prix = etree.SubElement(x_palmares, 'prix')
x_prix.set('name', 'Prix vulcain de l\'artiste technicien, décerné par la C.S.T')
etree.SubElement(x_prix, 'film').set('code', str(231299))

# export xml with pretty printing
with open('cannes.xml', mode='w', encoding='UTF-8') as file:
    file.write(etree.tostring(x_root, pretty_print=True).decode('utf-8'))
