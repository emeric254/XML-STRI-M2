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
    r = requests.get('http://api.allocine.fr/rest/v3/movie?partner=YW5kcm9pZC12Mg&profile=large&format=json&filter=movie&code=' + code_film)
    if r.status_code is 200:
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
    r = requests.get('http://api.allocine.fr/rest/v3/person?partner=YW5kcm9pZC12Mg&profile=large&format=json&code=' + str(code_person))
    if r.status_code is 200 and 'person' in r.json():
        person_rp = r.json()['person']
        person = {
            'code': person_rp['code'],
            'name': person_rp['name']['family'] if 'family' in person_rp['name'] else '' + ' ' + person_rp['name']['given'] if 'given' in person_rp['name'] else '',
            'biography': person_rp['biography'] if 'biography' in person_rp else '',
            'gender': '',
            'nationalities': []
        }
        if 'gender' in person_rp:
            person['gender'] = 'male' if person_rp['gender'] else 'female'
        if 'nationality' in person_rp:
            for nation in person_rp['nationality']:
                person['nationalities'].append(nation['$'])
        persons.append(person)

# debug
print(len(films))
print(films)
print(len(persons))
print(persons)

# gen xml
x_root = etree.Element('Cannes')
x_root.set('year', '2016')

x_movies = etree.SubElement(x_root, 'movies')
for film in films:
    x_film = etree.SubElement(x_movies, 'movie')
    x_film.set('title', film['title'])
    x_film.set('movie_type', film['movie_type'])
    x_film.set('production_year', str(film['production_year']))
    x_film.set('release_date', film['release_date'])
    x_film.set('duration', str(film['duration']))
    x_sysnopsis = etree.SubElement(x_film, 'synopsis')
    x_sysnopsis.text = film['synopsis']
    x_nationalities = etree.SubElement(x_film, 'nationalities')
    for nation in film['nationalities']:
        x_nation = etree.SubElement(x_nationalities, 'nationality')
        x_nation.set('name', nation)
    x_languages = etree.SubElement(x_film, 'languages')
    for lang in film['languages']:
        x_lang = etree.SubElement(x_languages, 'language')
        x_lang.set('name', lang)
    x_genres = etree.SubElement(x_film, 'genres')
    for genre in film['genres']:
        x_genre = etree.SubElement(x_genres, 'genre')
        x_genre.set('name', genre)
    x_cast_members = etree.SubElement(x_film, 'cast_members')
    for person in film['cast_members']:
        x_person = etree.SubElement(x_cast_members, 'person')
        x_person.set('id', str(person['code']))
        x_person.set('role', str(person['role']))

x_jury = etree.SubElement(x_root, 'jury')
for code in jury_codes:
    x_person = etree.SubElement(x_jury, 'person')
    x_person.set('code', str(code))

x_persons = etree.SubElement(x_root, 'persons')
for person in persons:
    x_person = etree.SubElement(x_persons, 'person')
    x_person.set('code', str(person['code']))
    x_person.set('name', person['name'])
    x_person.set('gender', person['gender'])
    etree.SubElement(x_person, 'biograhy').text = person['biography']
    x_nationalities = etree.SubElement(x_person, 'nationalities')
    for nation in person['nationalities']:
        x_nation = etree.SubElement(x_nationalities, 'nationality')
        x_nation.set('name', nation)

x_palmares = etree.SubElement(x_root, 'palmares')
x_prix = etree.SubElement(x_palmares, 'prix')
x_prix.set('name', 'palme d\'or')
x_prix.set('code', str(241697))
x_prix = etree.SubElement(x_palmares, 'prix')
x_prix.set('name', 'grand prix')
x_prix.set('code', str(237510))
x_prix = etree.SubElement(x_palmares, 'prix')
x_prix.set('name', 'prix de la mise en scene')
x_prix.set('code', str(241700))
x_prix = etree.SubElement(x_palmares, 'prix')
x_prix.set('name', 'prix de la mise en scene')
x_prix.set('code', str(237879))
x_prix = etree.SubElement(x_palmares, 'prix')
x_prix.set('name', 'prix du scenario')
x_prix.set('code', str(245360))
x_prix = etree.SubElement(x_palmares, 'prix')
x_prix.set('name', 'prix du jury')
x_prix.set('code', str(228834))
x_prix = etree.SubElement(x_palmares, 'prix')
x_prix.set('name', 'prix d\'interpretation feminine')
x_prix.set('code', str(246693))
x_prix = etree.SubElement(x_palmares, 'prix')
x_prix.set('name', 'prix d\'interpretation masculine')
x_prix.set('code', str(245360))
x_prix = etree.SubElement(x_palmares, 'prix')
x_prix.set('name', 'prix vulcain de l\'artiste technicien, decerne par la C.S.T')
x_prix.set('code', str(231299))

# export xml with pretty printing
with open('cannes.xml', mode='w', encoding='UTF-8') as file:
    file.write(etree.tostring(x_root, pretty_print=True).decode('utf-8'))
