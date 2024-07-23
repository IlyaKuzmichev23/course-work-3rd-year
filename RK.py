from queue import Queue

q = Queue()
d = 0
k = 3
r = 2.5826
n = 10
h = 1 #запаздывание
delta_x = 1 / n
delta_t = delta_x ** 3
x = 0
t = 0
t_final = 100
U = []
T = []



def get_eq_value(u_prev, u_cur, u_next, u_cur_del, i):
    return d*(u_prev-2*u_cur+u_next)/(delta_x**2) - r*u_cur_del*(1+u_cur)

def get_k1_values(u, u_del):
    k1 = []
    for i in range(0,len(u)):
        if i == 0:
            k1.append(get_eq_value(u[i+1]-2*k*delta_x*u[i], u[i], u[i+1], u_del[i], i)*delta_t)
        elif i == len(u)-1:
            k1.append(get_eq_value(u[i-1], u[i], u[i-1], u_del[i], i)*delta_t)
        else:
            k1.append(get_eq_value(u[i-1], u[i], u[i+1], u_del[i], i)*delta_t)
    return k1

def get_k2_values(u, u_del, k1):
    k2 = []
    for i in range (0,len(u)):
        if i == 0:
            k2.append(get_eq_value(u[i+1]-2*k*delta_x*u[i]+k1[i]/2, u[i]+k1[i]/2, u[i+1]+k1[i]/2, u_del[i], i)*delta_t)
        elif i == len(u)-1:
            k2.append(get_eq_value(u[i-1]+k1[i]/2, u[i]+k1[i]/2, u[i-1]+k1[i]/2, u_del[i], i)*delta_t)
        else:
            k2.append(get_eq_value(u[i-1]+k1[i]/2, u[i]+k1[i]/2, u[i+1]+k1[i]/2, u_del[i], i)*delta_t)
    return k2

def get_k3_values(u,u_del, k1, k2):
    k3 = []

    for i in range(0,len(u)):
        if i == 0:
            k3.append(get_eq_value(u[i+1] - 2 * k * delta_x* u[i]-k1[i]+2*k2[i], u[i]-k1[i]+2*k2[i], u[i+1]-k1[i]+2*k2[i], u_del[i], i) * delta_t)
        elif i == len(u)-1:
            k3.append(get_eq_value(u[i-1]-k1[i]+2*k2[i], u[i]-k1[i]+2*k2[i],u[i-1]-k1[i]+2*k2[i], u_del[i], i) * delta_t)
        else:
            k3.append(get_eq_value(u[i-1]-k1[i]+2*k2[i], u[i]-k1[i]+2*k2[i], u[i+1]-k1[i]+2*k2[i], u_del[i], i)*delta_t)
    return k3

def new_u(u,k1_arr,k2_arr,k3_arr):
    u_next = []
    for i in range(0, len(u)):
        u_next.append(u[i]+(k1_arr[i]+4*k2_arr[i]+k3_arr[i])/6)
    return u_next

def test_f(u,u_del):
    u_next = []
    for i in range(0,len(u)):
        if i == 0:
            u_next.append(u[i]+delta_t*get_eq_value(u[i+1]-2*k*delta_x*u[i], u[i], u[i+1], u_del[i], i))
        elif i == len(u)-1:
            u_next.append(u[i]+delta_t*get_eq_value(u[i-1], u[i], u[i-1], u_del[i], i))
        else:
            u_next.append(u[i]+delta_t*get_eq_value(u[i-1], u[i], u[i+1], u_del[i], i))
    return u_next

def decision_eq():
    u = [0.1 for _ in range(n+1)]
    u_del = [0.1 for _ in range(n+1)]
    global t, t_final
    while t < h:
        q.put(u)
        U.append(u[0])
        T.append(t)
        k1_arr = get_k1_values(u,u_del)
        k2_arr = get_k2_values(u,u_del,k1_arr)
        k3_arr = get_k3_values(u,u_del,k1_arr,k2_arr)
        u = new_u(u,k1_arr,k2_arr,k3_arr)
        t+=delta_t
    while t<=t_final:
        q.put(u)
        U.append(u[0])
        T.append(t)
        del_var = q.get()
        k1_arr = get_k1_values(u, del_var)
        k2_arr = get_k2_values(u, del_var, k1_arr)
        k3_arr = get_k3_values(u, del_var, k1_arr, k2_arr)
        u = new_u(u,k1_arr,k2_arr,k3_arr)
        t+=delta_t
    return U

