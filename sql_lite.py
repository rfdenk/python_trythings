import sqlite3


def ppp(f):
    def wrap(*args, **kwargs):
        new_kwargs = {'end': '\r\n', 'flush': True}
        new_kwargs.update(kwargs)
        f(*args, **new_kwargs)
    return wrap


print = ppp(print)

conn = sqlite3.connect(':memory:')
c = conn.cursor()


cities = [
        (1, 'Hobbiton'),
        (2, 'Bree'),
        (3, 'Rivendell')
    ]

try:
    c.execute("CREATE TABLE cities (id int primary key, name text)")
except sqlite3.OperationalError:
    pass


c.executemany("INSERT INTO cities VALUES (?,?)", cities)

try:
    c.execute('CREATE TABLE characters (id integer primary key autoincrement, name text, city integer, age integer, moved integer, movedon DATE)')
#except sqlite3.OperationalError as e:
    #print(e)
except Exception as e:
    print(e)

characters = [
        ('Bilbo', 1, 65, 1),
        ('Innkeeper', 2, 65, 0),
        ('Aragorn', 2, 137, 3),
    ]

c.executemany('INSERT INTO characters (name, city, age, moved) VALUES (?, ?, ?, ?)', characters)

conn.commit()

c.execute('SELECT * from characters')
print(c.fetchall())

c.execute('SELECT * from characters WHERE city=? ORDER BY moved', ('2',))
print(c.fetchall())

c.execute('SELECT * from characters WHERE city=:city ORDER BY moved DESC', {'city': 2})
print(c.fetchall())

c.execute('SELECT * from characters ORDER BY name')
print(c.fetchall())

print()
print()

c.execute('SELECT city FROM characters')
print("NON-DISTINCT RESIDENCE =", c.fetchall())
c.execute('SELECT DISTINCT city FROM characters')
print("DISTINCT RESIDENCE =", c.fetchall())
c.execute('SELECT min(age), max(age) FROM characters')
print('AGE RANGE =', c.fetchall())

c.execute('SELECT COUNT(DISTINCT age) FROM characters')
print('AGE CT =', c.description, c.fetchall())
c.execute('SELECT COUNT(DISTINCT age) AS num_ages FROM characters')
print('AGE CT =', c.description, c.fetchall())
c.execute('SELECT count(*) AS DistinctAges FROM (SELECT DISTINCT age FROM characters)')
print('AGE COUNT =', c.description, c.fetchall())
c.execute('UPDATE characters SET age=64 WHERE name="Innkeeper"')
c.execute('SELECT count(*) AS DistinctAges FROM (SELECT DISTINCT age FROM characters)')
print('AGE COUNT =', c.description, c.fetchall())

c.execute('SELECT avg(age) AS avg_age FROM characters')
print('AVG AGE =', c.fetchall())


c.execute('SELECT * FROM characters WHERE name LIKE "%n%"')
print("Names with n =", c.fetchall())

c.execute('SELECT * FROM characters WHERE name NOT LIKE "%n%"')
print("Names without n =", c.fetchall())

c.execute('SELECT * FROM characters WHERE name LIKE "%[rn]%"')
print("Names with r or n =", c.fetchall())          # doesn't work in sqlite?

c.execute('SELECT * FROM characters WHERE age IN (65, 137)')
print("with age in 65, 137 =", c.fetchall())

c.execute('SELECT * FROM characters WHERE city IN (SELECT id FROM cities WHERE name="Bree")')
print("lives in Bree =", c.fetchall())


c.execute('SELECT name, age + city AS agecity FROM characters')
print(c.fetchall())


c.execute('SELECT name FROM characters UNION SELECT id FROM cities')
print("UNION name,id =", c.description, c.fetchall())


c.execute('SELECT COUNT(characters.name), cities.name FROM characters JOIN cities ON characters.city = cities.id')
print("in each city NO GROUP =", c.fetchall())


c.execute('SELECT COUNT(characters.name), cities.name FROM characters JOIN cities ON characters.city = cities.id GROUP BY cities.name')
print("in each city =", c.fetchall())
print()
print()


#
# JOIN
#

c.execute('SELECT * FROM characters CROSS JOIN cities')
cross_join = c.fetchall()
print('CROSS JOIN')
for row in cross_join:
    print('.', row)
print()
print()

c.execute('SELECT * FROM characters INNER JOIN cities')
cross_join = c.fetchall()
print('INNER JOIN *', flush=True)
for row in cross_join:
    print('.', row)
print()
print()


c.execute('SELECT * FROM characters JOIN cities')
cross_join = c.fetchall()
print('JOIN *', flush=True)
for row in cross_join:
    print(".", row)
print()
print()


c.execute('SELECT * FROM characters, cities where characters.city = cities.id')
cross_join = c.fetchall()
print('IMPLICIT JOIN *', flush=True)
for row in cross_join:
    print(".", row)
print()
print()


c.execute('SELECT characters.name, cities.name FROM characters INNER JOIN cities')
cross_join = c.fetchall()
print('INNER JOIN', flush=True)
for row in cross_join:
    print(".", row)
print()
print()


c.execute('SELECT characters.name, cities.name FROM characters JOIN cities ON cities.id = characters.city')
cross_join = c.fetchall()
print('JOIN WITH ON', flush=True)
for row in cross_join:
    print(".", row)
print()
print()


c.execute('SELECT * FROM characters JOIN cities ON cities.id = characters.city')
cross_join = c.fetchall()
print('JOIN * WITH ON', flush=True)
for row in cross_join:
    print(".", row)
print()
print()


c.execute(
    'SELECT characters.name, cities.name '
    'FROM characters '
    'JOIN cities ON cities.id = characters.city GROUP BY cities.name'
    )
cross_join = c.fetchall()
print('JOIN AND GROUP BY', flush=True)
for row in cross_join:
    print(".", row)
print()
print()


c.execute('SELECT characters.name, cities.name FROM cities JOIN characters ON cities.id = characters.city')
cross_join = c.fetchall()
print('JOIN AND GROUP BY REV', flush=True)
for row in cross_join:
    print(".", row)
print()
print()


#
# TRIGGER
#
create_addr_change_trigger = (
        'CREATE TRIGGER address_change '
        'BEFORE UPDATE OF city ON characters '
        'BEGIN '
        'UPDATE characters SET moved=moved+1 WHERE name=NEW.name AND OLD.city <> NEW.city;'
        'END;'
        )
c.execute(create_addr_change_trigger)

create_addr_change_trigger2 = (
        'CREATE TRIGGER address_change2 '
        'BEFORE UPDATE OF city ON characters '
        'BEGIN '
        'UPDATE characters SET movedon=date("now") WHERE name=NEW.name AND OLD.city <> NEW.city;'
        'END;'
        )
c.execute(create_addr_change_trigger2)

c.execute('UPDATE characters SET city=3 WHERE name="Bilbo"')
c.execute('SELECT moved, movedon FROM characters WHERE name="Bilbo"')
print(c.fetchall())  # should be 2, today


c.execute('UPDATE characters SET city=3 WHERE name="Bilbo"')
c.execute('SELECT moved, movedon FROM characters WHERE name="Bilbo"')
print(c.fetchone())     # should still be 2, today, character's new city is same as old city

c.execute('UPDATE characters SET city=1 WHERE name="Bilbo"')
c.execute('SELECT moved, movedon FROM characters WHERE name="Bilbo"')
print(c.fetchall())  # should now be 3, today; character moved from city 3 to city 1


#
# VIEW
#
create_residence_view = (
        'CREATE VIEW residence AS '
        'SELECT characters.name, cities.name FROM characters JOIN cities '
        'ON cities.id = characters.city'
    )
c.execute(create_residence_view)

c.execute('SELECT * from residence')
print(c.fetchall())


#
# CLEANUP
#
c.execute('DROP TABLE characters')
c.execute('DROP TABLE cities')
c.execute('DROP VIEW residence')
conn.commit()


c.close()
conn.close()
