import numpy
from biosig import *
D=biosig.data('09121_DAkkS-Prüfraum-Datenlogger30.07.2021-01.09.2021.edf2')
numpy.savetxt("09121_DAkkS-Prüfraum-Datenlogger30.07.2021-01.09.2021.csv", D, delimiter=",")