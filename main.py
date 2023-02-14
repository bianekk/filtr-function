# importing module
from pandas import *
import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import asksaveasfile

filter_window = tk.Tk()
filter_window.title('Filter')
filter_window.geometry("400x600")
filter_window.configure(bg='#262c2b')
filter_top_frame = tk.Frame(filter_window)
filter_top_frame.pack(side=tk.TOP)
filter_top_frame.configure(bg='#262c2b')
filter_bottom_frame = tk.Frame(filter_window)
filter_bottom_frame.pack(side=tk.BOTTOM)
filter_bottom_frame.configure(bg='#262c2b')
multiplication_filter = []
band_center = [1, 1.25, 1.6, 2, 2.5, 3.15, 4, 5, 6.3, 8, 10, 12.5, 16, 20, 25, 31.5, 40, 50, 63, 80, 100]


def load_filter_csv():
    temp_filter_name = (tk.filedialog.askopenfile(mode='r', filetypes=[('CSV file', '*.csv')]))

    data = read_csv(str(temp_filter_name.name))
    multiplication_filter.append(data['F'])


filter_csv_button = tk.Button(
    filter_top_frame,
    text="Load CSV",
    width=20,
    fg='white', bg='black',
    command=lambda: load_filter_csv(),
    font='Lato 10 bold')
filter_csv_button.pack(side=tk.TOP, pady=5, padx=5)

if not multiplication_filter:
    multiplication_filter = [1] * len(band_center)

octave_frame = tk.Frame(filter_top_frame)
octave_frame.pack(side=tk.TOP, pady=5, padx=5)
octave_scroll = tk.Scrollbar(octave_frame, orient='vertical')
octave_scroll.pack(side='right', fill='y')

octave_values = ttk.Treeview(octave_frame, yscrollcommand=octave_scroll.set)
octave_values.pack()

octave_scroll.config(command=octave_values.yview)

# column definition
octave_values['columns'] = ('center_band', 'filter_value')

octave_values.column("#0", width=0,  stretch=False)
octave_values.column("center_band", anchor='center', width=120)
octave_values.column("filter_value", anchor='center', width=120)

# headings
octave_values.heading("#0", text="", anchor='center')
octave_values.heading("center_band", text="Band Frequency [Hz]", anchor='center')
octave_values.heading("filter_value", text="Filter value", anchor='center')

for i in range(len(multiplication_filter)):
    octave_values.insert(parent='', index='end', iid=i, text='', values=(band_center[i], multiplication_filter[i]))

# labels
center_band = tk.Label(filter_top_frame, text="center_band", width=10)
center_band.pack(side=tk.LEFT, padx=5, pady=5, anchor=tk.N)

filter_value = tk.Label(filter_top_frame, text="filter_value", width=10)
filter_value.pack(side=tk.LEFT, padx=5, pady=5, anchor=tk.N)

# entry boxes
center_band_entry = tk.Entry(filter_top_frame, width=10)
center_band_entry.pack(side=tk.LEFT, padx=5, pady=5, anchor=tk.S)

filter_value_entry = tk.Entry(filter_top_frame, width=10)
filter_value_entry.pack(side=tk.LEFT, padx=5, pady=5, anchor=tk.S)

# select record


def select_record():
    # clear entry boxes
    center_band_entry.delete(0, 'end')
    filter_value_entry.delete(0, 'end')

    # grab record
    selected = octave_values.focus()
    # grab record values
    record_values = octave_values.item(selected, 'values')
    # temp_label.config(text=selected)

    # output to entry boxes
    center_band_entry.insert(0, record_values[0])
    filter_value_entry.insert(0, record_values[1])


# save record
def update_record():
    selected = octave_values.focus()
    # save new data
    octave_values.item(selected, text="", values=(center_band_entry.get(), filter_value_entry.get()))

    # clear entry boxes
    center_band_entry.delete(0, 'end')
    filter_value_entry.delete(0, 'end')


select_button = tk. Button(filter_window, text="Select Record", command=select_record)
select_button.pack(pady=10)

edit_button = tk.Button(filter_window, text="Edit ", command=update_record)
edit_button.pack(pady=10)

filter_info_label = tk.Label(filter_bottom_frame,
                             text="Filter applied",
                             fg='white', bg='#262c2b',
                             font='Lato 8')
filter_info_label.pack(side=tk.BOTTOM, anchor=tk.S, pady=5, padx=5)
filter_list = [0]*21

# print(filter_list)

filter_ok_button = tk.Button(
    filter_bottom_frame,
    text="OK",
    width=20,
    fg='white', bg='black',
    command=lambda: get_filter_values() ,
    font='Lato 10 bold')
filter_ok_button.pack(side=tk.BOTTOM, pady=5, padx=5)


def get_filter_values():
    for j in range(len(band_center)):
        temp_dict = octave_values.item(j)
        octave_values_list = list(temp_dict.values())
        filter_list[j] = octave_values_list[2][1]
    filter_window.destroy()


filter_window.mainloop()
