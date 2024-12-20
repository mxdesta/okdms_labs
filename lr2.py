import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib import use as fix_ui

# Исправление UI для корректного отображения анимации в некоторых средах
fix_ui('TkAgg')

# Параметры системы
m = 1  # масса материальных точек
l1 = 1  # длина первого стержня
l2 = 1  # длина второго стержня
c = 1  # жесткость пружины
g = 9.81  # ускорение свободного падения

# Временные параметры
Steps = 500  # Количество шагов анимации
t_fin = 20  # Время моделирования (в секундах)
t = np.linspace(0, t_fin, Steps)  # Массив временных точек

# Углы отклонения маятников
phi1 = np.pi / 6 * np.cos(t)  # Колебания первого стержня
phi2 = np.pi / 3 * np.cos(t)  # Колебания второго стержня (больший наклон)

# Координаты материальных точек
x_O = 0  # Координата верхней точки крепления маятника
y_O = 0
x1 = l1 * np.sin(phi1)  # Координата x первой материальной точки
y1 = -l1 * np.cos(phi1)  # Координата y первой материальной точки
x2 = x1 + l2 * np.sin(phi2)  # Координата x второй материальной точки
y2 = y1 - l2 * np.cos(phi2)  # Координата y второй материальной точки

# Координаты ползуна
x_slider = -2  # Координата ползуна по x
slider_height = 1.5  # Высота ползуна
y_slider_top = 0.5  # Верхняя граница ползуна
y_slider_bottom = -1.0  # Нижняя граница ползуна

# Координата точки на ползуне (движущаяся точка пружины)
y_spring_attach = -0.5 - 0.1 * np.cos(t)  # Точка движется вниз при растяжении пружины

# Параметры пружины
spring_segments = 15  # Количество сегментов пружины для визуализации
spring_amplitude = 0.05  # Амплитуда колебаний пружины

# Создание фигуры и осей
fig, ax = plt.subplots(figsize=[8, 6])  # Создаем фигуру и оси с заданным размером
ax.set(xlim=[-2.5, 2], ylim=[-2.5, 0.5])  # Устанавливаем пределы осей
ax.axis('equal')  # Устанавливаем одинаковый масштаб по осям x и y

# Инициализация графических объектов
line1, = ax.plot([], [], 'o-', lw=2, label='Стержень 1')  # Первый стержень
line2, = ax.plot([], [], 'o-', lw=2, label='Стержень 2')  # Второй стержень
spring, = ax.plot([], [], 'r-', lw=2, label='Пружина')  # Пружина
slider, = ax.plot([x_slider, x_slider], [y_slider_bottom, y_slider_top], 'k-', lw=4, label='Ползун')  # Ползун
top_plane, = ax.plot([-2.5, 2], [0, 0], 'k-', lw=4)  # Горизонтальная плоскость сверху

# Подписи точек
point_M1 = ax.text(0, 0, 'M1', color='blue', fontsize=12, ha='right')  # Подпись для первой точки
point_M2 = ax.text(0, 0, 'M2', color='red', fontsize=12, ha='right')  # Подпись для второй точки


def init():
    """Инициализация объектов анимации."""
    line1.set_data([], [])  # Очищаем данные для первого стержня
    line2.set_data([], [])  # Очищаем данные для второго стержня
    spring.set_data([], [])  # Очищаем данные для пружины
    point_M1.set_position((0, 0))  # Сбрасываем позицию подписи первой точки
    point_M2.set_position((0, 0))  # Сбрасываем позицию подписи второй точки
    return line1, line2, spring, point_M1, point_M2, slider, top_plane  # Возвращаем объекты для анимации


def update(frame):
    """Обновление координат для каждого кадра."""
    # Обновление координат стержней
    line1.set_data([x_O, x1[frame]], [y_O, y1[frame]])  # Обновляем координаты первого стержня
    line2.set_data([x1[frame], x2[frame]], [y1[frame], y2[frame]])  # Обновляем координаты второго стержня

    # Обновление подписей точек
    point_M1.set_position((x1[frame], y1[frame]))  # Обновляем позицию подписи первой точки
    point_M2.set_position((x2[frame], y2[frame]))  # Обновляем позицию подписи второй точки

    # Координаты пружины
    spring_x = np.linspace(x_slider, x1[frame], spring_segments)  # Создаем координаты x для пружины
    spring_y = np.linspace(y_spring_attach[frame], y1[frame], spring_segments)  # Создаем координаты y для пружины
    for i in range(1, len(spring_x) - 1):
        if i % 2 == 0:
            spring_y[i] += spring_amplitude  # Добавляем колебания пружины
        else:
            spring_y[i] -= spring_amplitude  # Добавляем колебания пружины
    spring.set_data(spring_x, spring_y)  # Обновляем данные для пружины

    return line1, line2, spring, point_M1, point_M2, slider, top_plane  # Возвращаем объекты для анимации


# Создание анимации
ani = FuncAnimation(fig, update, frames=Steps, init_func=init, interval=5, blit=True)

# Добавление легенды
ax.legend()

# Отображение анимации
plt.show()