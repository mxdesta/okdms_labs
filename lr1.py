import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import sympy as sp
import matplotlib

matplotlib.use('TkAgg')  # выдавало картинку, а не анимацию


def Rot2D(X, Y, Alpha):
    RotX = X * np.cos(Alpha) - Y * np.sin(Alpha)
    RotY = X * np.sin(Alpha) + Y * np.cos(Alpha)
    return RotX, RotY


t = sp.Symbol('t')
r = 2 + sp.sin(12 * t)
phi = t + 0.2 * sp.cos(12 * t)
x = r * sp.cos(phi)
y = r * sp.sin(phi)
Vx = sp.diff(x, t)
Vy = sp.diff(y, t)
Ax = sp.diff(Vx, t)
Ay = sp.diff(Vy, t)

F_x = sp.lambdify(t, x)
F_y = sp.lambdify(t, y)
F_Vx = sp.lambdify(t, Vx)
F_Vy = sp.lambdify(t, Vy)
F_Ax = sp.lambdify(t, Ax)
F_Ay = sp.lambdify(t, Ay)

t = np.linspace(0, 10, 1001)
x = F_x(t)
y = F_y(t)
Vx = F_Vx(t)
Vy = F_Vy(t)
Ax = F_Ax(t)
Ay = F_Ay(t)

Alpha_V = np.arctan2(Vy, Vx)
Alpha_A = np.arctan2(Ay, Ax)

# масштабируем чтоб не выходили за пределы отображения
k_V = 0.34  # Масштаб скорости
k_A = 0.05  # Масштаб ускорения

fig = plt.figure(figsize=[10, 10])
ax = fig.add_subplot(1, 1, 1)
ax.axis('equal')
ax.grid()
ax.set(xlim=[-12, 12], ylim=[-12, 12])  # Увеличенные границы

ax.set_title('Анимация точки')
ax.plot(x, y, label="Траектория движения")

P = ax.plot(x[0], y[0], marker='o', label="Точка движения")[0]
R_line, = ax.plot([0, x[0]], [0, y[0]], 'g', label="Радиус-вектор")
V_line, = ax.plot([x[0], x[0] + Vx[0]], [y[0], y[0] + Vy[0]], 'r', label="Скорость")
A_line, = ax.plot([x[0], x[0] + Ax[0]], [y[0], y[0] + Ay[0]], 'b', label="Ускорение")

arrow_shape_x = np.array([-0.25, 0, -0.25])
arrow_shape_y = np.array([0.09, 0, -0.09])

RotX_V, RotY_V = Rot2D(arrow_shape_x, arrow_shape_y, Alpha_V[0])
RotX_A, RotY_A = Rot2D(arrow_shape_x, arrow_shape_y, Alpha_A[0])
V_Arrow = ax.plot(x[0] + Vx[0] + RotX_V, y[0] + Vy[0] + RotY_V, 'r')[0]
A_Arrow = ax.plot(x[0] + Ax[0] + RotX_A, y[0] + Ay[0] + RotY_A, 'b')[0]

# легенда
ax.legend()

time_text = ax.text(-11, 11, '', fontsize=12)
velocity_text = ax.text(-11, 10, '', fontsize=12)
acceleration_text = ax.text(-11, 9, '', fontsize=12)


def TheMagicOfThtMovement(i):
    P.set_data([x[i]], [y[i]])
    R_line.set_data([0, x[i]], [0, y[i]])
    V_line.set_data([x[i], x[i] + k_V * Vx[i]], [y[i], y[i] + k_V * Vy[i]])

    RotX_V, RotY_V = Rot2D(arrow_shape_x, arrow_shape_y, Alpha_V[i])
    V_Arrow.set_data(x[i] + k_V * Vx[i] + RotX_V, y[i] + k_V * Vy[i] + RotY_V)
    A_line.set_data([x[i], x[i] + k_A * Ax[i]], [y[i], y[i] + k_A * Ay[i]])

    RotX_A, RotY_A = Rot2D(arrow_shape_x, arrow_shape_y, Alpha_A[i])
    A_Arrow.set_data(x[i] + k_A * Ax[i] + RotX_A, y[i] + k_A * Ay[i] + RotY_A)

    time_text.set_text(f"Время: {t[i]:.2f} с")
    velocity_text.set_text(f"|V|: {np.sqrt(Vx[i] ** 2 + Vy[i] ** 2):.2f} ед.")
    acceleration_text.set_text(f"|A|: {np.sqrt(Ax[i] ** 2 + Ay[i] ** 2):.2f} ед.")

    return P, R_line, V_line, A_line, V_Arrow, A_Arrow, time_text, velocity_text, acceleration_text


# Animate
kino = FuncAnimation(fig, TheMagicOfThtMovement, frames=len(t), interval=1000 / 60, blit=True)
plt.show()
