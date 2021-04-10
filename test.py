from database import *

db = Database(dbtype='sqlite', dbname='LEGO.db')

"""


lego_bricks = db.read(Brick, Brick.name)

for brick in lego_bricks:
    print(brick)

if db.read_by_id(Brick, '302226'):
    # neprošlo testem id není typu INT
    brick = db.read_by_id(Brick, '302226')
    brick.color = '#ABC123'
    db.update()

db.delete(Brick, 242001)

corner_plate = Brick()
corner_plate.id = 242001
corner_plate.name = 'Corner Plate 1 x 2 x 2'
corner_plate.color = '#FFFFFF'
corner_plate.type = 'standard'
corner_plate.image = 'img/Corner Plate 1 x 2 x 2 - White.jpg'

db.create(corner_plate)

print('\nBrick(s) that have "Corner" in name: ')
for brick in db.read_by_name(Brick, "Corner"):
    print(brick)



if db.read_by_id(Set, 31004):
    db.delete(Set, 31004)
else:
    set_fierce_flyer = Set()
    set_fierce_flyer.id = 31004
    set_fierce_flyer.name = 'Fierce Flyer'
    set_fierce_flyer.year = 2013
    set_fierce_flyer.number_of_pieces = 166
    set_fierce_flyer.price = 14.99
    set_fierce_flyer.image = 'img/Fierce-flyer.jpg'
    db.create(set_fierce_flyer)

sets = db.read(Set, Set.year)

if db.read_by_id(Set, '31004'):
    # neprošlo testem id není typu INT
    set = db.read_by_id(Set, '31004')
    set.name = 'Neni set'
    db.update()


"""
if db.read_by_id(Manual, 31004):
    db.delete(Manual, 31004)
else:
    fierce_flyer_manual = Manual()
    fierce_flyer_manual.id = 31004
    fierce_flyer_manual.name = 'Fierce Flyer'
    fierce_flyer_manual.number_of_pages = 55
    fierce_flyer_manual.image = 'img/Fierce-flyer-manual.jpg'
    db.create(fierce_flyer_manual)

manuals = db.read(Manual, Manual.number_of_pages)

#for manual in manuals:
#    print(manual)

if db.read_by_id(Manual, '31004'):
    # neprošlo testem id není typu INT
    manual = db.read_by_id(Manual, '31004')
    manual.name = 'Nejsem uz manaual'
    db.update()

print('\nManual(s) that have "Flyer" in name: ')
for manual in db.read_by_name(Manual, "Flyer"):
    print(manual)
"""
print('\nLEGO set(s) that have "Fierce" in name: ')
for set in db.read_by_name(Set, "Fierce"):
    print(set)
"""


s1 = Set()
s1.id = 31004
s1.name = "set"
s1.manual = fierce_flyer_manual.id
b1 = Brick()
b1.name = "brick"

s1.bricks.append(b1)
db = Database()
db.create(s1)
db.create(b1)

db.update()

fierce_flyer_manual.set.append(s1)
db.update()
