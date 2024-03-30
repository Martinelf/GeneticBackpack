from Algorithms import *
from tkinter import *
from tkinter import ttk


# массив состоит из двух массивов которые используются в отображении
def report_to_file(filename, massiv):
    try:
        with open(filename, 'a') as file:
            array_string = ' '.join(map(str, massiv))
            file.write(array_string+'\n')
    except Exception as e:
        print(f"Произошла ошибка при записи данных в файл: {e}")


def show_result(array_gen=None, array_brut=None):
    label_shtorka1 = ttk.Label(frame, background='#DCDAD5')
    label_shtorka2 = ttk.Label(frame, background='#DCDAD5')
    label_shtorka1.grid(row=12, column=0, columnspan=2, pady=10, sticky='we')
    label_shtorka2.grid(row=14, column=0, columnspan=2, pady=10, sticky='we')

    if len(array_gen[0]) <= 10:
        result_gen = ttk.Label(frame, text=f'solution: {array_gen[0]} value: {array_gen[1]} time: {round(array_gen[2],5)}')
        result_brute = ttk.Label(frame, text=f'solution: {array_brut[0]} value: {array_brut[1]} time: {round(array_brut[2],5)}')
    else:
        result_gen = ttk.Label(frame, text=f'value: {array_gen[1]} time: {round(array_gen[2], 5)}')
        result_brute = ttk.Label(frame, text=f'value: {array_brut[1]} time: {round(array_brut[2], 5)}')

    label_genetic = ttk.Label(frame, text='Генетический алгоритм')
    label_brute = ttk.Label(frame, text='Полный перебор')

    label_genetic.grid(row=11, column=0, columnspan=2, pady=10)
    result_gen.grid(row=12, column=0, columnspan=2, pady=10)

    label_brute.grid(row=13, column=0, columnspan=2, pady=10)
    result_brute.grid(row=14, column=0, columnspan=2, pady=10)


def read_and_solve():
    knapsack_capacity = int(capacityEntry.get())
    amount_of_items = int(amountEntry.get())
    weights, values = [], []
    if var.get() == 0:
        weights_and_values = itemsEntry.get().split()
        for elem in weights_and_values:
            elem = elem.split('-')
            weights.append(elem[0])
            values.append(elem[1])

        weights = list(map(int, weights))
        values = list(map(int, values))
    else:
        weights = [random.randint(1, knapsack_capacity+1) for _ in range(amount_of_items)]
        values = [random.randint(1, knapsack_capacity+1) for _ in range(amount_of_items)]

    print("Формулировка задачи:")
    print(f"веса предметов: {weights}")
    print(f"ценности предметов: {values}")
    population_size = int(populEntry.get())
    mutation_probability = float(mutatEntry.get())
    num_generations = int(numgenEntry.get())

    print(
        f"размер популяции = {population_size}, вероятность мутации = {mutation_probability}, поколений {num_generations}")
    print("само решение:")

    genetic_solve = GeneticAlgorithm(knapsack_capacity, weights,
                                     values, population_size,
                                     mutation_probability, num_generations)
    best_individual_gen, genetic_solution, genetic_time = genetic_solve.solve()

    array_gen = [best_individual_gen, genetic_solution, genetic_time]

    # полный перебор
    knapsack_brute = BruteForce(knapsack_capacity, weights, values)
    best_combination, brute_solution, brute_time = knapsack_brute.solve()
    print("Лучшая комбинация:", best_combination)
    print("Суммарная стоимость выбранных предметов:", brute_solution, '\n')
    print(f'Правильность решения генетического алгоритма: {genetic_solution/brute_solution}')
    array_brute = [best_combination, brute_solution, brute_time]

    show_result(array_gen, array_brute)
    arr_stats = [knapsack_capacity, amount_of_items, population_size, mutation_probability, num_generations,
                 genetic_time, genetic_solution, brute_time, brute_solution]
    report_to_file("stats.txt", arr_stats)


def set_by_hand_radiobutton():
    itemsEntry.grid_forget()
    by_hand.grid(row=3, column=1, sticky="w", pady=5)
    instruct.grid_forget()


def set_entry_items():
    by_hand.grid_forget()
    itemsEntry.grid(row=3, column=1, sticky="w", pady=5)
    randomly.grid(row=4, column=1, sticky="w", pady=5)
    instruct.grid(row=4, column=0, sticky="w")


main_win = Tk()
main_win.resizable(False, False)
main_win.title("Генетический алгоритм")

style = ttk.Style()
style.theme_use('clam')  # тема из tkinter (для красоты)

frame = ttk.Frame(main_win, padding="10")
frame.grid(row=0, column=0, padx=10, pady=10)

var = IntVar()
var.set(0)
by_hand = ttk.Radiobutton(frame, text="Ввести вручную", variable=var, value=0, command=set_entry_items)
randomly = ttk.Radiobutton(frame, text="Сгенерировать случайно", variable=var, value=1, command=set_by_hand_radiobutton)

instruct = ttk.Label(frame, text="вбивать в виде:\nвес1-цена1 вес2-цена2...")
instruct.grid(row=4, column=0, sticky="w")


itemsEntry = ttk.Entry(frame)
itemsEntry.grid(row=3, column=1, sticky="w", pady=5)

randomly.grid(row=4, column=1, sticky="w", pady=5)

knapsackLabel = ttk.Label(frame, text='Характеристики рюкзака')
capacityLabel = ttk.Label(frame, text='Вместимость рюкзака:')
amountLabel = ttk.Label(frame, text='Количество предметов:')
typeLabel = ttk.Label(frame, text='Набор предметов:')
geneticLabel = ttk.Label(frame, text='Характеристики алгоритма')
populLabel = ttk.Label(frame, text='Размер популяции:')
mutatLabel = ttk.Label(frame, text='Вероятность мутации:')
numgenLabel = ttk.Label(frame, text='Количество поколений:')

capacityEntry = ttk.Entry(frame)
amountEntry = ttk.Entry(frame)
populEntry = ttk.Entry(frame)
mutatEntry = ttk.Entry(frame)
numgenEntry = ttk.Entry(frame)

solve_button = ttk.Button(frame, text='Решить задачу', command=read_and_solve)
solve_button.grid(row=10, column=0, columnspan=2, pady=10)

chk_state = BooleanVar()
chk_state.set(True)
# chk = ttk.Checkbutton(frame, text='Проверить правильность результата', variable=chk_state)
# chk.grid(row=9, column=0, columnspan=2, pady=10)

knapsackLabel.grid(row=0, column=0, padx=20, pady=20, columnspan=2)
capacityLabel.grid(row=1, column=0, sticky="e")
amountLabel.grid(row=2, column=0, sticky="e")
typeLabel.grid(row=3, column=0, sticky="e")
geneticLabel.grid(row=5, column=0, padx=20, pady=20, columnspan=2)
populLabel.grid(row=6, column=0, sticky="e")
mutatLabel.grid(row=7, column=0, sticky="e")
numgenLabel.grid(row=8, column=0, sticky="e")

capacityEntry.grid(row=1, column=1, sticky="w")
amountEntry.grid(row=2, column=1, sticky="w")
populEntry.grid(row=6, column=1, sticky="w")
mutatEntry.grid(row=7, column=1, sticky="w")
numgenEntry.grid(row=8, column=1, sticky="w")

main_win.mainloop()



