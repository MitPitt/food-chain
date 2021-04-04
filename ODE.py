import numpy as np 
from scipy.integrate import odeint
import math 

def equationroots(a, b, c):
    dis = b**2 - 4*a*c
    sqrt_val = math.sqrt(abs(dis)) 
    if dis >= 0: 
        re1 = (-b + sqrt_val)/(2 * a)
        re2 = (-b - sqrt_val)/(2 * a)
        im1 = 0
        im2 = 0
    else:
        re1 = - b / (2 * a)
        im1 = sqrt_val
        re2 = - b / (2 * a) 
        im2 = -sqrt_val
    return re1, im1, re2, im2

def step(state, t, C, V0, E1, E2, R):
    y1, y2 = state
    return y1*(-E1+V0*(C-y1-y2)-y2/(R+y1)), y2*(-E2+y1/(R+y1))

def thing(ax1, ax2, C, V0, t_stop=2500, dt=0.01, eps=0.1, starting_point=0):
    
    iters = int(t_stop/dt)
    t = np.linspace(0, t_stop, iters)

    E1 = 0.1
    E2 = 0.2
    R = 5

    # особая точка 0
    sp01 = 0.0
    sp02 = 0.0
    state_00 = [sp01 + eps, sp02 + eps]
    # особая точка 1
    sp11 = (R * E2) / (1 - E2)
    sp12 = (-E1 + V0 * (C - sp11)) / (V0 + 1 / (R + sp11))
    state_01 = [sp11 + eps, sp12 + eps]
    # особая точка 2
    sp21 = C - (E1 / V0)
    sp22 = 0.0
    state_02 = [sp21 + eps, sp22 + eps]
    
    if starting_point == 0:
        start_state = state_00
    elif starting_point == 1:
        start_state = state_01
    elif starting_point == 2:
        start_state = state_02
    
    if start_state[0] < 0 or start_state[1] < 0:
        raise Exception('Начальная точка вне области допустимых значений!')

    solution = odeint(step, start_state, t, args=(C, V0, E1, E2, R))
    
    response0 = 'Особая точка 0 ({:.2f}; {:.2f}) — '.format(sp01,sp02)
    if C > (0.1/V0):
        response0 += 'Седло' 
    elif (0.1/V0) > C:
        response0 += 'Устойчивый узел'

    response1 = 'Особая точка 1 ({:.2f}; {:.2f}) — '.format(sp11,sp12)
    a_ = 1
    b_ = -(-E1 + V0*(C-sp11-sp12)-sp12/(R+sp11) + sp11*(-V0 + sp12/((R+sp11)**2)))
    c_ = (sp11*V0 + sp11/(sp11+R)) * (R*sp12/((sp11+R)**2))
    re1, im1, re2, im2 = equationroots(a_, b_, c_)

    #print('lambdas {:.2f} {:.2f}i; {:.2f} {:.2f}i'.format(re1, im1, re2, im2))

    if im1 == 0:
        if re1 > 0 and re2 > 0:
            response1 += 'Неустойчивый узел'
        if re1 > 0 and re2 < 0:
            response1 += ('Седло')
        if re1 < 0 and re2 < 0:
            response1 += ('Устойчивый узел')
    else:
        if abs(re1) < 0.001:
            response1 += ('Центр')
        elif re1 > 0:
            response1 += ('Неустойчивый фокус')
        elif re1 < 0:
            response1 += ('Устойчивый фокус')

    response2 = 'Особая точка 2 ({:.2f}; {:.2f}) — '.format(sp21,sp22)
    if C > (0.1/V0)+1.25:
        response2 +=('Седло') #-+
    elif (0.1/V0)+1.25 > C > (0.1/V0):
        response2 +=('Устойчивый узел')
    elif (0.1/V0) > C > (0.1/V0)-5:
        response2 +=('Седло') #+-
    elif (0.1/V0)-5 > C:
        response2 +=('Неустойчивый узел')
        
    
    ax1.plot(t, solution[:, 0], 'r', label='y1(t)')
    ax1.plot(t, solution[:, 1], 'g', label='y2(t)')
    if sp11 > 0 and sp12 > 0:
        ax1.axhline(y=sp11, color='black', linestyle = ':')
        ax1.axhline(y=sp12, color='black', linestyle = ':')
    if sp21 > 0:
        ax1.axhline(y=sp21, color='black', linestyle = ':')
    ax1.legend()
    ax1.set_ylim(bottom=0)
    ax1.set_xlim(left=0)
    ax1.grid()
    ax1.set(xlabel='t', title='Численности популяций со временем')
    
    
    line = ax2.plot(solution[:, 0], solution[:, 1])[0]
    ax2.set_ylim(bottom=0)
    ax2.set_xlim(left=0)
    ax2.grid(linewidth=1)
    ax2.set(xlabel='y1 (жертвы)', ylabel='y2 (хищники)', title='Фазовая траектория')
    if sp11 > 0 and sp12 > 0:
        ax2.axvline(x=sp11, color='red', linestyle = ':')
        ax2.axhline(y=sp12, color='red', linestyle = ':')
    if sp21 > 0:
        ax2.axvline(x=sp21, color='green', linestyle = ':')
    
    return response0, response1, response2