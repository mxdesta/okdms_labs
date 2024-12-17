import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib import use as fix_ui

fix_ui('TkAgg')

# Параметры системы
m = 1  # масса материальных точек
l1 = 1  # длина первого стержня
l2 = 1  # длина второго стержня
c = 1  # жесткость пружины
g = 9.81  # ускорение свободного падения

# Временные параметры
Steps = 500  # Количество шагов
t_fin = 20  # Время моделирования
t = np.linspace(0, t_fin, Steps)

# Угол отклонения (одинаковый для обоих стержней)
phi = np.pi / 6 * np.cos(t)

# Координаты материальных точек
x_O = 0  # Координата верхней точки крепления маятника
y_O = 0
x1 = l1 * np.sin(phi)
y1 = -l1 * np.cos(phi)
x2 = x1 + l2 * np.sin(phi)
y2 = y1 - l2 * np.cos(phi)

# Координаты ползуна
x_slider = -2  # Координата ползуна по x
slider_height = 1.5  # Высота ползуна
y_slider_top = 0.5
y_slider_bottom = -1.0

# Координата точки на ползуне (движущаяся точка пружины)
y_spring_attach = -0.5 - 0.1 * np.cos(t)  # Точка пружины движется вниз

# Параметры пружины
spring_segments = 15  # Количество сегментов пружины
spring_amplitude = 0.05  # Амплитуда колебаний пружины

# Создание фигуры с графиками
fig, axs = plt.subplots(2, 1, figsize=[8, 8])
fig.suptitle("Графики N(t), phi(t), анимация маятников")

# Верхний график - нормальные реакции и углы
ax1 = axs[0]
N = m * g * np.cos(phi)  # Нормальная реакция
ax1.plot(t, N, label='N(t)', color='green')
ax1.plot(t, phi, label='phi(t)', color='blue')
ax1.set_title("Графики N(t) и phi(t)")
ax1.legend()

# Анимация маятников
ax2 = axs[1]
ax2.set_xlim(-2.5, 2)
ax2.set_ylim(-2.5, 0.5)
ax2.axis('equal')

# Графические элементы
line1, = ax2.plot([], [], 'o-', lw=2, label='Стержень 1')  # Первый стержень
line2, = ax2.plot([], [], 'o-', lw=2, label='Стержень 2')  # Второй стержень
spring, = ax2.plot([], [], 'r-', lw=2, label='Пружина')  # Пружина
slider, = ax2.plot([x_slider, x_slider], [y_slider_bottom, y_slider_top], 'k-', lw=4, label='Ползун')
top_plane, = ax2.plot([-2.5, 2], [0, 0], 'k-', lw=4)

# Подписи точек
point_M1 = ax2.text(0, 0, 'M1', color='blue', fontsize=12, ha='right')
point_M2 = ax2.text(0, 0, 'M2', color='red', fontsize=12, ha='right')

def init():
    """Инициализация объектов анимации."""
    line1.set_data([], [])
    line2.set_data([], [])
    spring.set_data([], [])
    point_M1.set_position((0, 0))
    point_M2.set_position((0, 0))
    return line1, line2, spring, point_M1, point_M2, slider, top_plane

def update(frame):
    """Обновление координат для каждого кадра."""
    # Обновление координат стержней
    line1.set_data([x_O, x1[frame]], [y_O, y1[frame]])
    line2.set_data([x1[frame], x2[frame]], [y1[frame], y2[frame]])

    # Обновление подписей точек
    point_M1.set_position((x1[frame], y1[frame]))
    point_M2.set_position((x2[frame], y2[frame]))

    # Обновление пружины
    spring_x = np.linspace(x_slider, x1[frame], spring_segments)
    spring_y = np.linspace(y_spring_attach[frame], y1[frame], spring_segments)
    for i in range(1, len(spring_x) - 1):
        if i % 2 == 0:
            spring_y[i] += spring_amplitude
        else:
            spring_y[i] -= spring_amplitude
    spring.set_data(spring_x, spring_y)

    return line1, line2, spring, point_M1, point_M2, slider, top_plane

# Создание анимации
ani = FuncAnimation(fig, update, frames=Steps, init_func=init, interval=40, blit=True)

# Добавление легенды
ax2.legend()

# Отображение анимации
plt.tight_layout()
plt.show()
