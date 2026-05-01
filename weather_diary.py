import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime

class WeatherDiaryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Дневник погоды")
        self.data_file = "data.json"
        self.records = self.load_data()

        # --- Создание интерфейса ---
        self.create_widgets()

    def create_widgets(self):
        # Поля ввода
        tk.Label(self.root, text="Дата (ГГГГ-ММ-ДД):").grid(row=0, column=0, padx=5, pady=5)
        self.date_entry = tk.Entry(self.root)
        self.date_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.root, text="Температура (°C):").grid(row=1, column=0, padx=5, pady=5)
        self.temp_entry = tk.Entry(self.root)
        self.temp_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(self.root, text="Описание:").grid(row=2, column=0, padx=5, pady=5)
        self.desc_entry = tk.Entry(self.root)
        self.desc_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(self.root, text="Осадки:").grid(row=3, column=0, padx=5, pady=5)
        self.rain_var = tk.StringVar(value="Нет")
        ttk.Combobox(self.root, textvariable=self.rain_var,
                     values=["Да", "Нет"]).grid(row=3, column=1, padx=5, pady=5)

        # Кнопка добавления записи
        tk.Button(self.root, text="Добавить запись", command=self.add_record).grid(
            row=4, column=0, columnspan=2, pady=10)

        # Фильтры
        tk.Label(self.root, text="Фильтр по дате:").grid(row=5, column=0, padx=5)
        self.filter_date = tk.Entry(self.root)
        self.filter_date.grid(row=5, column=1, padx=5)

        tk.Label(self.root, text="Фильтр по температуре (>°C):").grid(row=6, column=0, padx=5)
        self.filter_temp = tk.Entry(self.root)
        self.filter_temp.grid(row=6, column=1, padx=5)

        tk.Button(self.root, text="Применить фильтр", command=self.apply_filter).grid(
            row=7, column=0, columnspan=2, pady=10)

        # Таблица для отображения записей
        self.tree = ttk.Treeview(self.root, columns=(0, 1, 2, 3), show='headings')
        self.tree.heading(0, text="Дата")
        self.tree.heading(1, text="Температура")
        self.tree.heading(2, text="Описание")
        self.tree.heading(3, text="Осадки")
        self.tree.grid(row=8, column=0, columnspan=2, padx=5, pady=5)

    def add_record(self):
        date = self.date_entry.get()
        temp = self.temp_entry.get()
        desc = self.desc_entry.get()
        rain = self.rain_var.get()

        # Валидация ввода
        try:
            datetime.strptime(date, "%Y-%m-%d")
            temp = float(temp)
            if not desc:
                raise ValueError("Описание не может быть пустым!")
            if rain not in ["Да", "Нет"]:
                raise ValueError("Осадки должны быть 'Да' или 'Нет'")
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))
            return

        record = {"date": date, "temp": temp, "desc": desc, "rain": rain}
        self.records.append(record)
        self.save_data()
        self.update_table()

    def apply_filter(self):
        filter_date = self.filter_date.get()
        filter_temp = self.filter_temp.get()

        filtered = self.records.copy()

        if filter_date:
            try:
                datetime.strptime(filter_date, "%Y-%m-%d")
                filtered = [r for r in filtered if r["date"] == filter_date]
            except:
                messagebox.showerror("Ошибка", "Некорректный формат даты!")
                return

        if filter_temp:
            try:
                temp_val = float(filter_temp)
                filtered = [r for r in filtered if r["temp"] > temp_val]
            except:
                messagebox.showerror("Ошибка", "Температура должна быть числом!")
                return

        self.update_table(filtered)

    def update_table(self, records=None):
        for i in self.tree.get_children():
            self.tree.delete(i)

        if records is None:
            records = self.records

        for r in records:
            self.tree.insert("", "end", values=(r["date"], r["temp"], r["desc"], r["rain"]))

    def load_data(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, "r", encoding="utf-8") as f:
                return json.load(f)
        return []

    def save_data(self):
        with open(self.data_file, "w", encoding="utf-8") as f:
            json.dump(self.records, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherDiaryApp(root)
    app.update_table()  # Загрузка данных при старте
    root.mainloop()
