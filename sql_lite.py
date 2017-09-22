import sqlite3

def ppp(f):
    def wrap(*args, **kwargs):
        f(args, kwargs, end='<<\r\n', flush=True)
    return wrap

print = ppp(print)

conn = sqlite3.connect('test4.db')
c = conn.cursor()

try:
    c.execute('CREATE TABLE owners (name text, city text, age real)')
except sqlite3.OperationalError:
    # already exists!
    pass

owners = [
    ('Bilbo', 'Hobbitton', 22),
    ('Innkeeper', 'Bree', 33),
    ('Aragorn', 'Bree', 103),
]

c.executemany('INSERT INTO owners VALUES (?,?,?)', owners)

c.execute('SELECT * from owners')
print(c.fetchall())

c.execute('SELECT * from owners WHERE city=? ORDER BY age', ('Bree',))
print(c.fetchall())

c.execute('SELECT * from owners WHERE city=? ORDER BY age DESC', ('Bree',))
print(c.fetchall())

c.execute('SELECT * from owners ORDER BY name')
print(c.fetchall())

c.execute('DROP TABLE owners')

