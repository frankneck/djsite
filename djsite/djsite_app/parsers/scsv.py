import csv
from parser import *


with open('lavka_orka.csv', 'w', newline='') as csvfile:
    spamwriter = csv.writer(csvfile)
    spamwriter.writerows(games)

