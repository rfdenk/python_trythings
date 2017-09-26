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
    c.execute('CREATE TABLE characters (name text, city int, moved int)')
except sqlite3.OperationalError:
    # already exists!
    pass

owners = [
        ('Bilbo', 1, 1),
        ('Innkeeper', 2, 0),
        ('Aragorn', 2, 3),
    ]

c.executemany('INSERT INTO characters VALUES (?,?,?)', owners)

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

c.execute('UPDATE characters SET city=3 WHERE name="Bilbo"')
c.execute('SELECT moved FROM characters WHERE name="Bilbo"')
print(c.fetchall()[0][0])  # should be 2

c.execute('UPDATE characters SET city=3 WHERE name="Bilbo"')
c.execute('SELECT moved AS moved FROM characters WHERE name="Bilbo"')
print(c.fetchone()[0])     # should still be 2, character's new city is same as old city

c.execute('UPDATE characters SET city=1 WHERE name="Bilbo"')
c.execute('SELECT moved FROM characters WHERE name="Bilbo"')
print(c.fetchall()[0][0])  # should now be 3; character moved from city 3 to city 1


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
