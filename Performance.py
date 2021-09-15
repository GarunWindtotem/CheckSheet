from datetime import *

now1 = datetime.now()

for i in range(0, 200_000_000):
    a = 111+5
now2 = datetime.now()
zeit = (now2-now1).total_seconds()
print(zeit)

now1 = datetime.now()
for i in range(0, 100_000_000):
    a = 111+5
now2 = datetime.now()
zeit = (now2-now1).total_seconds()
print(zeit)

now1 = datetime.now()
for i in range(0, 50_000_000):
    a = 111+5
now2 = datetime.now()
zeit = (now2-now1).total_seconds()
print(zeit)

now1 = datetime.now()
for i in range(0, 25_000_000):
    a = 111+5
now2 = datetime.now()
zeit = (now2-now1).total_seconds()
print(zeit)