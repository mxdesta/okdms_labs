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

# Углы отклонения маятников
phi1 = np.pi / 6 * np.cos(t)  # Колебания первого стержня
phi2 = np.pi / 3 * np.cos(t)  # Колебания второго стержня (больший наклон)

# Координаты материальных точек
x_O = 0  # Координата верхней точки крепления маятника
y_O = 0
x1 = l1 * np.sin(phi1)
y1 = -l1 * np.cos(phi1)
x2 = x1 + l2 * np.sin(phi2)
y2 = y1 - l2 * np.cos(phi2)

# Координаты ползуна
x_slider = -2  # Координата ползуна по x
slider_height = 1.5  # Высота ползуна
y_slider_top = 0.5
y_slider_bottom = -1.0

# Координата точки на ползуне (движущаяся точка пружины)
y_spring_attach = -0.5 - 0.1 * np.cos(t)  # Исправлено: точка движется вниз при растяжении пружины

# Параметры пружины
spring_segments = 15  # Количество сегментов пружины
spring_amplitude = 0.05  # Амплитуда колебаний пружины

# Создание фигуры
fig, ax = plt.subplots(figsize=[8, 6])
ax.set(xlim=[-2.5, 2], ylim=[-2.5, 0.5])
ax.axis('equal')

# Инициализация графических объектов
line1, = ax.plot([], [], 'o-', lw=2, label='Стержень 1')  # Первый стержень
line2, = ax.plot([], [], 'o-', lw=2, label='Стержень 2')  # Второй стержень
spring, = ax.plot([], [], 'r-', lw=2, label='Пружина')  # Пружина
slider, = ax.plot([x_slider, x_slider], [y_slider_bottom, y_slider_top], 'k-', lw=4, label='Ползун')  # Ползун
top_plane, = ax.plot([-2.5, 2], [0, 0], 'k-', lw=4)  # Горизонтальная плоскость сверху

# Подписи точек
point_M1 = ax.text(0, 0, 'M1', color='blue', fontsize=12, ha='right')
point_M2 = ax.text(0, 0, 'M2', color='red', fontsize=12, ha='right')


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

    # Координаты пружины
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
ax.legend()

# Отображение анимации
plt.show()
