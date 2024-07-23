import matplotlib.pyplot as plt
from RK import *
#plt.plot(decision_eq())
#plt.show()
decision_eq()
plt.plot(T,U)
plt.xlabel("t", fontsize=18)
plt.ylabel("u", fontsize=18)
plt.show()
