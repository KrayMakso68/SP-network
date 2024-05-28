from spn import SPN, gen_pbox, int_to_byte_str_with_fill
import customtkinter
import re

customtkinter.set_appearance_mode("dark")

app = customtkinter.CTk()
app.title("my app")
app.geometry("850x600")

tabview = customtkinter.CTkTabview(master=app)
tabview.pack(expand=True, fill='both', padx=5, pady=(0, 5))

tabview.add("Конфигурация шифратора")
tabview.add("Шифратор")
tabview.add("Метод встречи по середине")
tabview.set("Шифратор")

S = 3  # число входов в s-блок
N = 3  # число s-блоков
rounds = 2  # кол-во полных раундов шифрования
p_option = False  # операция перестановки в конце


def validate_binary_string(newval, n=N, s=S):
    bits_row_len = n * s
    reg_exp = '^[01]{0,' + str(bits_row_len) + '}$'
    if re.match(reg_exp, newval):
        return True
    else:
        return False


def validate_s_box(newval, s=S):
    input_limit = (2 ** s) - 1
    reg_exp = '^[0-{}]?$'.format(input_limit)
    if re.match(reg_exp, newval):
        return True
    else:
        return False


def check_configuration(s=S, n=N) -> bool:
    entry_limit = s * n
    error = False
    if len(plaintext_entry.get()) != entry_limit:
        error = True
        error_plaintext_label.configure(text='Ошибка ввода открытого текста\nЧисло должно быть девятизначным')
    else:
        error_plaintext_label.configure(text='')
    if len(key_entry.get()) != entry_limit:
        error = True
        error_key_label.configure(text='Ошибка ввода ключа\nЧисло должно быть девятизначным')
    else:
        error_key_label.configure(text='')
    s_box_list = []
    error_s_box_label.configure(text='')
    for entry in entry_s_box_list:
        value = entry.get()
        if len(value) == 0:
            error = True
            error_s_box_label.configure(text='Ошибка ввода значений S-блока\nВведите все значения S-блока')
            break
        if int(value) in s_box_list:
            error = True
            error_s_box_label.configure(text='Ошибка ввода значений S-блока\nЗначения S-блока дублируются')
            break
        s_box_list.append(int(value))
    return error


def start_encryption(r=rounds, s=S, n=N):
    bits_row_len = n * s
    cipher_text_entry.configure(state='normal')
    cipher_text_entry.delete(0, 'end')
    if not check_configuration():
        plaintext = int(plaintext_entry.get(), 2)
        key = int(key_entry.get(), 2)
        s_box = [int(entry.get()) for entry in entry_s_box_list]
        p_box = gen_pbox(s, n)
        sp = SPN(s_box, p_box, key, r)
        encrypted_plaintext = sp.encrypt(plaintext)
        cipher_text_entry.insert(0, int_to_byte_str_with_fill(encrypted_plaintext, S, N))
        cipher_text_entry.configure(state='disable')


def update_encryption_config():
    S = int(S_var.get())
    N = int(N_var.get())
    rounds = int(rounds_var.get())
    p_option = p_option_var.get()
    app.update_idletasks()

    tabview.set("Шифратор")


# окно ввода конфигурации
main_input = customtkinter.CTkFrame(master=tabview.tab("Конфигурация шифратора"))
main_input.columnconfigure((1, 2), weight=1)
main_input.columnconfigure((0, 3), weight=2)
customtkinter.CTkLabel(master=main_input,
                       text="Число входов в S-блок:"
                       ).grid(row=0, column=1, padx=0, pady=0, sticky='e')
S_var = customtkinter.StringVar(value=str(S))
s_entry = customtkinter.CTkEntry(master=main_input,
                                 textvariable=S_var,
                                 width=40)
s_entry.grid(row=0, column=2, padx=(0, 20), pady=5)
customtkinter.CTkLabel(master=main_input,
                       text='Число S-блоков:'
                       ).grid(row=1, column=1, padx=0, pady=0, sticky='e')
N_var = customtkinter.StringVar(value=str(N))
n_entry = customtkinter.CTkEntry(master=main_input,
                                 textvariable=N_var,
                                 width=40)
n_entry.grid(row=1, column=2, padx=(0, 20), pady=5)
customtkinter.CTkLabel(master=main_input,
                       text="Количество раундов шифрования: \n(без учёта последнего раунда)"
                       ).grid(row=2, column=1, padx=0, pady=0, sticky='e')
rounds_var = customtkinter.StringVar(value=str(rounds))
rounds_entry = customtkinter.CTkEntry(master=main_input,
                                      textvariable=rounds_var,
                                      width=40)
rounds_entry.grid(row=2, column=2, padx=(0, 20), pady=5)
customtkinter.CTkLabel(master=main_input,
                       text="Операция перестановки в последнем раунде:"
                       ).grid(row=3, column=1, padx=0, pady=0, sticky='e')
p_option_var = customtkinter.BooleanVar(value=p_option)
config_option_checkbox = customtkinter.CTkCheckBox(master=main_input,
                                                   variable=p_option_var,
                                                   text='')
config_option_checkbox.grid(row=3, column=2, padx=(20, 0), pady=5, sticky='e')

set_button = customtkinter.CTkButton(master=main_input,
                                     text='Установить конфигурацию шифратора',
                                     height=40,
                                     command=update_encryption_config
                                     )
set_button.grid(row=0, column=3, padx=0, pady=0, ipadx=10)

main_input.pack(fill='x', padx=10, pady=20)

# рамка ввода открытого текста
tabview.tab("Шифратор").columnconfigure(0, weight=1)
plaintext_frame = customtkinter.CTkFrame(master=tabview.tab("Шифратор"), fg_color='gray20')
plaintext_frame.columnconfigure(0, weight=1)
plaintext_frame.grid(row=0, column=0, sticky='ew', padx=20)
plaintext_label = customtkinter.CTkLabel(master=plaintext_frame, text='Открытый текст')
plaintext_label.grid(row=0, sticky='w', padx=10, pady=(10, 0))
plaintext_entry = customtkinter.CTkEntry(master=plaintext_frame,
                                         height=40,
                                         placeholder_text='010101010',
                                         font=('', 18),
                                         validate="key",
                                         validatecommand=(app.register(validate_binary_string), '%P')
                                         )
plaintext_entry.grid(row=1, sticky='nsew', padx=10, pady=(5, 10))
error_plaintext_label = customtkinter.CTkLabel(master=plaintext_frame,
                                               text='',
                                               text_color='brown2',
                                               width=240,
                                               height=35
                                               )
error_plaintext_label.grid(row=2, sticky='w', padx=10, pady=(2, 10))

# рамка ввода ключа
tabview.tab("Шифратор").columnconfigure(1, weight=1)
key_frame = customtkinter.CTkFrame(master=tabview.tab("Шифратор"), fg_color='gray20')
key_frame.columnconfigure(0, weight=1)
key_frame.grid(row=0, column=1, sticky='ew', padx=20)
key_label = customtkinter.CTkLabel(master=key_frame, text='Ключ зашифрования')
key_label.grid(row=0, sticky='w', padx=10, pady=(10, 0))
key_entry = customtkinter.CTkEntry(master=key_frame,
                                   placeholder_text='010101010',
                                   height=40,
                                   font=('', 18),
                                   validate="key",
                                   validatecommand=(app.register(validate_binary_string), '%P')
                                   )
key_entry.grid(row=1, sticky='ew', padx=10, pady=(5, 10))
error_key_label = customtkinter.CTkLabel(master=key_frame,
                                         text='',
                                         text_color='brown2',
                                         width=240,
                                         height=35
                                         )
error_key_label.grid(row=2, sticky='we', padx=10, pady=(2, 10))

# рамка ввода S-блока
tabview.tab("Шифратор").rowconfigure(1, weight=1)
s_box_frame = customtkinter.CTkScrollableFrame(master=tabview.tab("Шифратор"), fg_color='gray20',
                                               orientation='horizontal')
s_box_frame.columnconfigure(0, weight=1)
s_box_frame.grid(row=1, sticky='ew', columnspan=2, padx=20, pady=20)
s_box_label = customtkinter.CTkLabel(master=s_box_frame, text='S-блок')
s_box_label.grid(row=0, sticky='w', padx=10, pady=(10, 5))
input_s_box_frame = customtkinter.CTkFrame(master=s_box_frame, fg_color='gray30')
input_s_box_frame.grid(row=1, sticky='nsew', padx=10, pady=(0, 10), ipadx=10)
in_s_box_label = customtkinter.CTkLabel(master=input_s_box_frame, text='ВХОД')
in_s_box_label.grid(row=0, column=0, padx=5)
out_s_box_label = customtkinter.CTkLabel(master=input_s_box_frame, text='ВЫХОД')
out_s_box_label.grid(row=1, column=0, padx=5)

# инпупы для клеток S-блока
label_s_box_list = []
for i in range(S * N - 1):
    ent = customtkinter.CTkEntry(master=input_s_box_frame, width=35, state='normal')
    ent.insert(0, f'{i}')
    ent.grid(row=0, column=i + 1, pady=(5, 2))
    ent.configure(state='disable')
    label_s_box_list.append(ent)

# инпуты для ввода значений S-блока
entry_s_box_list = []
for i in range(S * N - 1):
    ent = customtkinter.CTkEntry(master=input_s_box_frame,
                                 width=35,
                                 state='normal',
                                 validate="key",
                                 validatecommand=(app.register(validate_s_box), '%P')
                                 )
    ent.grid(row=1, column=i + 1, pady=(2, 5))
    entry_s_box_list.append(ent)

error_s_box_label = customtkinter.CTkLabel(master=s_box_frame, text='', text_color='brown2', height=35)
error_s_box_label.grid(row=2, column=0, sticky='w', padx=20, pady=(2, 5))

# рамка вывода зашифрованного текста
cipher_text_frame = customtkinter.CTkFrame(master=tabview.tab("Шифратор"), fg_color='gray20')
cipher_text_frame.columnconfigure(0, weight=1)
cipher_text_frame.grid(row=2, column=0, sticky='ew', padx=20, pady=(0, 20))
cipher_text_label = customtkinter.CTkLabel(master=cipher_text_frame, text='Зашифрованный текст')
cipher_text_label.grid(row=0, sticky='w', padx=10, pady=(10, 0))
cipher_text_entry = customtkinter.CTkEntry(master=cipher_text_frame,
                                           height=40,
                                           font=('', 18)
                                           )
cipher_text_entry.grid(row=1, sticky='nsew', padx=10, pady=(5, 10))
cipher_text_entry.configure(state='disable')
start_encryption_button = customtkinter.CTkButton(master=tabview.tab("Шифратор"),
                                                  text='Зашифровать',
                                                  height=40,
                                                  command=start_encryption
                                                  )
start_encryption_button.grid(row=2, column=1, sticky='ew', padx=20, pady=(0, 20))

app.mainloop()
