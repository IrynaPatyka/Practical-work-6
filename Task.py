import customtkinter as ctk
import time
import multiprocessing
from concurrent.futures import ProcessPoolExecutor

def calculate_partial_sum(start, end):
    """Обчислює суму чисел у вказаному діапазоні."""
    partial_sum = 0
    for i in range(start, end):
        partial_sum += i
    return partial_sum

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title(" Parallel Processing Analysis")
        self.geometry("450x500")
        self.size = 100_000_000 
        self.setup_ui()

    def setup_ui(self):
        self.label = ctk.CTkLabel(
            self, 
            text="Аналіз ефективності (100 млн елементів)", 
            font=("Arial", 16, "bold")
        )
        self.label.pack(pady=20)

        self.btn_sequential = ctk.CTkButton(
            self, 
            text="Послідовна обробка", 
            command=self.run_sequential,
            fg_color="#2c3e50"
        )
        self.btn_sequential.pack(pady=10)

        self.btn_parallel = ctk.CTkButton(
            self, 
            text="Паралельна обробка", 
            command=self.run_parallel,
            fg_color="#27ae60",
            hover_color="#2ecc71"
        )
        self.btn_parallel.pack(pady=10)

        self.result_box = ctk.CTkTextbox(self, width=400, height=250)
        self.result_box.pack(pady=20, padx=20)

    def log_result(self, method, result, duration):
        self.result_box.insert("end", f"Метод: {method}\n")
        self.result_box.insert("end", f"Сума: {result}\n")
        self.result_box.insert("end", f"Час: {duration:.4f} сек.\n")
        self.result_box.insert("end", "-"*40 + "\n")
        self.result_box.see("end")

    def run_sequential(self):
        self.result_box.insert("end", "Запуск послідовного обчислення...\n")
        self.update_idletasks()
        start_time = time.perf_counter()
        total_sum = sum(range(self.size))
        end_time = time.perf_counter()
        self.log_result("Послідовно", total_sum, end_time - start_time)

    def run_parallel(self):
        self.result_box.insert("end", "Запуск паралельного обчислення...\n")
        self.update_idletasks()
        start_time = time.perf_counter()
        num_cores = multiprocessing.cpu_count()
        chunk_size = self.size // num_cores

        tasks = []
        for i in range(num_cores):
            start = i * chunk_size
            end = (i + 1) * chunk_size if i != num_cores - 1 else self.size
            tasks.append((start, end))

        try:
            with ProcessPoolExecutor(max_workers=num_cores) as executor:
                results = list(executor.map(self.wrapper, tasks))
            
            total_sum = sum(results)
            end_time = time.perf_counter()
            
            self.log_result(f"Паралельно ({num_cores} ядер)", total_sum, end_time - start_time)
        except Exception as e:
            self.result_box.insert("end", f" Помилка: {str(e)}\n")

    @staticmethod
    def wrapper(args):
        """Статичний метод-обгортка для розпаковки аргументів у процесі."""
        return calculate_partial_sum(*args)

if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    
    app = App()
    app.mainloop()