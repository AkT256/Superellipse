import math
import tkinter as tk
from tkinter import ttk

#  Обобщённый суперэллипс (независимые nx и ny)

def superellipse_points(cx, cy, a, b, nx, ny, rot_deg, steps):
    """
    Вычисляет точки обобщённого суперэллипса с разными nx и ny.
    cx, cy – центр фигуры
    a, b – полуоси
    nx, ny – показатели степени по X и Y
    rot_deg – угол поворота (в градусах)
    steps – количество точек по периметру
    """
    nx = max(nx, 0.1)
    ny = max(ny, 0.1)
    phi = math.radians(rot_deg)
    sinp, cosp = math.sin(phi), math.cos(phi)

    pts = []
    for i in range(steps + 1):
        t = 2 * math.pi * i / steps
        ct, st = math.cos(t), math.sin(t)

        # Параметризация с разными nx и ny
        x = a * math.copysign(abs(ct) ** (2 / nx), ct)
        y = b * math.copysign(abs(st) ** (2 / ny), st)

        # Поворот точки на угол phi
        xr = x * cosp - y * sinp
        yr = x * sinp + y * cosp

        pts.extend([cx + xr, cy + yr])
    return pts


class SuperellipseApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Обобщённый суперэллипс (nx ≠ ny)")
        self.geometry("1000x700")

        self.canvas = tk.Canvas(self, bg="white", width=700, height=700)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        panel = ttk.Frame(self, padding=10)
        panel.pack(side=tk.RIGHT, fill=tk.Y)

        # Параметры фигуры
        self.var_a = tk.DoubleVar(value=260)
        self.var_b = tk.DoubleVar(value=220)
        self.var_nx = tk.DoubleVar(value=2)
        self.var_ny = tk.DoubleVar(value=2)
        self.var_rot = tk.DoubleVar(value=0)
        self.var_steps = tk.IntVar(value=600)
        self.var_linewidth = tk.DoubleVar(value=2)          # Толщина линии

        # Слайдеры
        self.add_slider(panel, "Полуось a", self.var_a, 20, 340, "{:.0f}")
        self.add_slider(panel, "Полуось b", self.var_b, 20, 340, "{:.0f}")
        self.add_slider(panel, "Показатель nx (по X)", self.var_nx, 0.2, 10.0, "{:.2f}")
        self.add_slider(panel, "Показатель ny (по Y)", self.var_ny, 0.2, 10.0, "{:.2f}")
        self.add_slider(panel, "Поворот (°)", self.var_rot, -180, 180, "{:.0f}")
        self.add_slider(panel, "Точек по периметру", self.var_steps, 100, 2000, "{:.0f}")

        # Отрисовка при изменении окна
        self.redraw()
        self.canvas.bind("<Configure>", lambda e: self.redraw())

    def add_slider(self, parent, label, var, frm, to, fmt):
        """Добавление слайдера с подписью и текущим значением"""
        frame = ttk.Frame(parent)
        frame.pack(fill=tk.X, pady=4)
        ttk.Label(frame, text=label).pack(anchor="w")
        ttk.Scale(frame, from_=frm, to=to, variable=var, command=lambda _: self.redraw()).pack(fill=tk.X)
        lbl = ttk.Label(frame, text=fmt.format(var.get()))
        lbl.pack(anchor="e")
        var.trace_add("write", lambda *_: lbl.config(text=fmt.format(var.get())))

    def redraw(self):
        """Перерисовка фигуры при изменении параметров"""
        self.canvas.delete("all")
        w, h = self.canvas.winfo_width(), self.canvas.winfo_height()
        cx, cy = w / 2, h / 2
        pts = superellipse_points(cx, cy, self.var_a.get(), self.var_b.get(),
                                  self.var_nx.get(), self.var_ny.get(),
                                  self.var_rot.get(), int(self.var_steps.get()))
        self.canvas.create_line(pts, fill="red", width=self.var_linewidth.get())


if __name__ == "__main__":
    app = SuperellipseApp()
    app.mainloop()



