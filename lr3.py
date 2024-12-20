import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from scipy.integrate import odeint
from matplotlib import use as fix_ui

# Исправление UI для корректного отображения анимации в некоторых средах
fix_ui('TkAgg')

# Параметры системы
m = 1  # масса материальных точек
l1 = 1 # длина первого стержня
l2 = 1  # длина второго стержня
c = 1 # жесткость пружины
g = 9.81  # ускорение свободного падения

# Временные параметры
Steps = 500  # Количество шагов анимации
t_fin = 20  # Время моделирования (в секундах)
t_vals = np.linspace(0, t_fin, Steps)  # Массив временных точек

# Начальные условия (углы и угловые скорости)
phi0 = np.pi / 6  # Начальный угол для первого маятника
psi0 = np.pi / 3  # Начальный угол для второго маятника
dphi0 = 0  # Начальная угловая скорость для первого маятника
dpsi0 = 0  # Начальная угловая скорость для второго маятника
y0 = [phi0, psi0, dphi0, dpsi0]  # Начальные условия для интеграции

# Функция для решения дифференциальных уравнений
def odesys(y, t, m, l1, l2, c, g):
    phi, psi, dphi, dpsi = y
    dydt = np.zeros_like(y)

    # Уравнения движения
    dydt[0] = dphi
    dydt[1] = dpsi
    dydt[2] = (-l2 * dpsi ** 2 * np.sin(phi - psi) - g * np.sin(phi) - (c * l1 / m) * np.cos(phi) * np.sin(phi)) / l1
    dydt[3] = (l1 * dphi ** 2 * np.sin(phi - psi) - g * np.sin(psi)) / l2

    return dydt

# Решение системы
Y = odeint(odesys, y0, t_vals, args=(m, l1, l2, c, g))

# Извлечение решений
phi = Y[:, 0]
psi = Y[:, 1]
dphi = Y[:, 2]
dpsi = Y[:, 3]

# Координаты материальных точек
x_O = 0  # Координата верхней точки крепления маятника
y_O = 0
x1 = l1 * np.sin(phi)  # Координата x первой материальной точки
y1 = -l1 * np.cos(phi)  # Координата y первой материальной точки
x2 = x1 + l2 * np.sin(psi)  # Координата x второй материальной точки
y2 = y1 - l2 * np.cos(psi)  # Координата y второй материальной точки

# Координаты ползуна
x_slider = -2  # Координата ползуна по x
slider_height = 1.5  # Высота ползуна
y_slider_top = 1.0  # Верхняя граница ползуна (подняли выше)
y_slider_bottom = -1.5  # Нижняя граница ползуна (поставим ниже)

# Координата точки на ползуне (движущаяся точка пружины)
# Теперь точка крепления пружины движется вверх и вниз в зависимости от угла маятника
y_spring_attach = -0.5 + 0.2 * np.sin(phi)  # Точка движется вверх и вниз

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
ani = FuncAnimation(fig, update, frames=Steps, init_func=init, interval=40, blit=True)

# Добавление легенды
ax.legend()

# Отображение анимации
plt.show()

# Вычисление кинетической и потенциальной энергии
T = 0.5 * m * (l1 * dphi)**2 + 0.5 * m * (l2 * dpsi)**2
U = m * g * (l1 * (1 - np.cos(phi)) + l2 * (1 - np.cos(psi))) + 0.5 * c * l1**2 * np.sin(phi)**2

# Вычисление полной энергии
E = T + U

# Построение графика зависимости энергии от времени
# Построение графиков зависимостей в одной фигуре с несколькими подграфиками
fig, axes = plt.subplots(3, 1, figsize=(10, 12))  # Создаем фигуру с сеткой 3x1

# График кинетической энергии
axes[0].plot(t_vals, T, label='Кинетическая энергия', color='blue')
axes[0].set_title('Кинетическая энергия')
axes[0].set_xlabel('Время (с)')
axes[0].set_ylabel('Энергия (Дж)')
axes[0].legend()
axes[0].grid(True)

# График потенциальной энергии
axes[1].plot(t_vals, U, label='Потенциальная энергия', color='green')
axes[1].set_title('Потенциальная энергия')
axes[1].set_xlabel('Время (с)')
axes[1].set_ylabel('Энергия (Дж)')
axes[1].legend()
axes[1].grid(True)

# График полной энергии
axes[2].plot(t_vals, E, label='Полная энергия', color='red')
axes[2].set_title('Полная энергия')
axes[2].set_xlabel('Время (с)')
axes[2].set_ylabel('Энергия (Дж)')
axes[2].legend()
axes[2].grid(True)

# Автоматическое выравнивание элементов
plt.tight_layout()
plt.show()