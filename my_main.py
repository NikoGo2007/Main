import tkinter as tk
import math


class PolarRose:
    def __init__(self, root):
        self.root = root
        self.root.title("Полярная роза")

        # Параметры по умолчанию
        self.n = 6.4
        self.d = 1
        self.scale = 100

        self.create_sliders()

        self.canvas = tk.Canvas(root, width=400, height=400, bg='white')
        self.canvas.pack()

        self.draw_rose()

    def create_sliders(self):
        slider_frame = tk.Frame(self.root)
        slider_frame.pack(pady=10)

        tk.Label(slider_frame, text="n:").grid(row=0, column=0)
        self.n_slider = tk.Scale(slider_frame, from_=1, to=10, resolution=0.1,
                                 orient=tk.HORIZONTAL, command=self.on_slider_change)
        self.n_slider.set(self.n)
        self.n_slider.grid(row=0, column=1)

        tk.Label(slider_frame, text="d:").grid(row=1, column=0)
        self.d_slider = tk.Scale(slider_frame, from_=1, to=10, resolution=0.1,
                                 orient=tk.HORIZONTAL, command=self.on_slider_change)
        self.d_slider.set(self.d)
        self.d_slider.grid(row=1, column=1)

    def on_slider_change(self, event=None):
        self.n = self.n_slider.get()
        self.d = self.d_slider.get()
        self.draw_rose()

    def draw_rose(self):
        self.canvas.delete("all")

        # Центр холста
        center_x, center_y = 200, 200

        points = []
        for i in range(1000):
            theta = i * 2 * math.pi / 1000
            k = self.n / self.d

            r = math.cos(k * theta) * self.scale

            x = center_x + r * math.cos(theta)
            y = center_y + r * math.sin(theta)
            points.append((x, y))

        if len(points) > 1:
            self.canvas.create_line(points, fill='red', smooth=True)


if __name__ == "__main__":
    root = tk.Tk()
    app = PolarRose(root)
    root.mainloop()