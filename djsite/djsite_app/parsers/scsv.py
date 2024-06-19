import csv
from parser_of_lavka_orka import *


with open('lavka_orka.csv', 'w', newline='') as csvfile:
    spamwriter = csv.writer(csvfile)
    spamwriter.writerows(games)

