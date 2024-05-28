import re

import customtkinter

customtkinter.set_appearance_mode("dark")

S: int = 3  # число входов в s-блок
N: int = 3  # число s-блоков
Str_len: int = S * N  # длина входного слова
Rounds: int = 2  # кол-во полных раундов шифрования
P_option: bool = False  # операция перестановки в конце


def validate_binary_string(newval):
    reg_exp = '^[01]{0,' + str(Str_len) + '}$'
    if re.match(reg_exp, newval):
        return True
    else:
        return False


def validate_s_box(action, value_if_allowed):
    input_limit = 2 ** S
    if action == "1":  # Проверяем, что происходит ввод символа
        try:
            if len(value_if_allowed) > 1 and value_if_allowed[0] == "0":
                return False
            num = int(value_if_allowed)
            if 0 <= num < input_limit:  # Проверяем, что число находится в диапазоне от 0 до limit
                return True
            else:
                return False
        except ValueError:
            return False
    else:
        return True


class TabView(customtkinter.CTkTabview):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.add("Конфигурация шифратора")
        self.add("Шифратор")
        self.add("Метод встречи по середине")
        self.set("Шифратор")

        self.tab("Шифратор").columnconfigure((0, 1), weight=1)
        self.tab("Шифратор").rowconfigure(1, weight=1)


class InputPlaintextFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.configure(fg_color='gray20')
        self.columnconfigure(0, weight=1)

        self.plaintext_label = customtkinter.CTkLabel(master=self, text='Открытый текст')
        self.plaintext_label.grid(row=0, sticky='w', padx=10, pady=(10, 0))
        self.plaintext_entry = customtkinter.CTkEntry(master=self,
                                                      height=40,
                                                      placeholder_text='010101010',
                                                      font=('', 18),
                                                      validate="key",
                                                      validatecommand=(self.register(validate_binary_string), '%P')
                                                      )
        self.plaintext_entry.grid(row=1, sticky='nsew', padx=10, pady=(5, 10))
        self.error_plaintext_label = customtkinter.CTkLabel(master=self,
                                                            text='',
                                                            text_color='brown2',
                                                            width=240,
                                                            height=35
                                                            )
        self.error_plaintext_label.grid(row=2, sticky='w', padx=10, pady=(2, 10))


class InputСiphertextFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.configure(fg_color='gray20')
        self.columnconfigure(0, weight=1)

        self.key_label = customtkinter.CTkLabel(master=self, text='Ключ зашифрования')
        self.key_label.grid(row=0, sticky='w', padx=10, pady=(10, 0))
        self.key_entry = customtkinter.CTkEntry(master=self,
                                                placeholder_text='010101010',
                                                height=40,
                                                font=('', 18),
                                                validate="key",
                                                validatecommand=(self.register(validate_binary_string), '%P')
                                                )
        self.key_entry.grid(row=1, sticky='ew', padx=10, pady=(5, 10))
        self.error_key_label = customtkinter.CTkLabel(master=self,
                                                      text='',
                                                      text_color='brown2',
                                                      width=240,
                                                      height=35
                                                      )
        self.error_key_label.grid(row=2, sticky='we', padx=10, pady=(2, 10))


class SboxScrollableFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master):
        super().__init__(master, orientation='horizontal')

        self.columnconfigure(0, weight=1)
        self.configure(fg_color='gray20')

        self.s_box_label = customtkinter.CTkLabel(master=self, text='S-блок')
        self.s_box_label.grid(row=0, sticky='w', padx=10, pady=(10, 5))

        self.input_s_box_frame = InputSboxFrame(master=self)
        self.input_s_box_frame.grid(row=1, sticky='nsew', padx=10, pady=(0, 10), ipadx=10)

        self.error_s_box_label = customtkinter.CTkLabel(master=self, text='', text_color='brown2', height=35)
        self.error_s_box_label.grid(row=2, column=0, sticky='w', padx=20, pady=(2, 5))


class InputSboxFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.configure(fg_color='gray30')

        self.in_s_box_label = customtkinter.CTkLabel(master=self, text='ВХОД')
        self.in_s_box_label.grid(row=0, column=0, padx=5)
        self.out_s_box_label = customtkinter.CTkLabel(master=self, text='ВЫХОД')
        self.out_s_box_label.grid(row=1, column=0, padx=5)

        self.sbox_labels = self.create_sbox_labels(master=self)
        self.sbox_entries = self.create_sbox_entries(master=self)

    def create_sbox_labels(self, master):
        label_s_box_list = []
        global S
        limit = 2 ** S
        for i in range(limit):
            ent = customtkinter.CTkEntry(master, width=35, state='normal')
            ent.insert(0, f'{i}')
            ent.grid(row=0, column=i + 1, pady=(5, 2))
            ent.configure(state='disable')
            label_s_box_list.append(ent)
        return label_s_box_list

    def create_sbox_entries(self, master):
        entry_s_box_list = []
        global S
        limit = 2 ** S
        for i in range(limit):
            ent = customtkinter.CTkEntry(master=master,
                                         width=35,
                                         state='normal',
                                         validate="key",
                                         validatecommand=(self.register(validate_s_box), '%d', '%P')
                                         )
            ent.grid(row=1, column=i + 1, pady=(2, 5))
            entry_s_box_list.append(ent)
        return entry_s_box_list


class ConfigurationFrame(customtkinter.CTkFrame):
    def __init__(self, master, root):
        super().__init__(master)

        self.columnconfigure((1, 2), weight=1)
        self.columnconfigure((0, 3), weight=2)

        self.root = root
        self.tab_view = root.tab_view

        customtkinter.CTkLabel(master=self,
                               text="Число входов в S-блок:"
                               ).grid(row=0, column=1, padx=0, pady=0, sticky='e')
        self.S_var = customtkinter.StringVar(value='3')
        self.s_entry = customtkinter.CTkEntry(master=self, textvariable=self.S_var, width=40)
        self.s_entry.grid(row=0, column=2, padx=(0, 20), pady=5)
        customtkinter.CTkLabel(master=self,
                               text='Число S-блоков:'
                               ).grid(row=1, column=1, padx=0, pady=0, sticky='e')
        self.N_var = customtkinter.StringVar(value='3')
        self.n_entry = customtkinter.CTkEntry(master=self, textvariable=self.N_var, width=40)
        self.n_entry.grid(row=1, column=2, padx=(0, 20), pady=5)
        customtkinter.CTkLabel(master=self,
                               text="Количество раундов шифрования: \n(без учёта последнего раунда)"
                               ).grid(row=2, column=1, padx=0, pady=0, sticky='e')
        self.rounds_var = customtkinter.StringVar(value='2')
        self.rounds_entry = customtkinter.CTkEntry(master=self, textvariable=self.rounds_var, width=40)
        self.rounds_entry.grid(row=2, column=2, padx=(0, 20), pady=5)
        customtkinter.CTkLabel(master=self,
                               text="Операция перестановки в последнем раунде:"
                               ).grid(row=3, column=1, padx=0, pady=0, sticky='e')
        self.p_option_var = customtkinter.BooleanVar(value=False)
        self.config_option_checkbox = customtkinter.CTkCheckBox(master=self, variable=self.p_option_var, text='')
        self.config_option_checkbox.grid(row=3, column=2, padx=(20, 0), pady=5, sticky='e')
        self.set_button = customtkinter.CTkButton(master=self,
                                                  text='Установить конфигурацию шифратора',
                                                  height=40,
                                                  command=self.set_config)
        self.set_button.grid(row=0, column=3, padx=0, pady=0, ipadx=10)

    def set_config(self):
        global S, N, Str_len, Rounds, P_option
        S = int(self.S_var.get())
        N = int(self.N_var.get())
        Str_len = S * N
        Rounds = int(self.rounds_var.get())
        P_option = self.p_option_var.get()
        self.root.update_sbox()
        self.tab_view.set("Шифратор")


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("SP-network")
        self.geometry("850x550")

        self.tab_view = TabView(self)
        self.tab_view.pack(expand=True, fill='both', padx=5, pady=(0, 5))

        self.plaintext_frame = InputPlaintextFrame(master=self.tab_view.tab("Шифратор"))
        self.plaintext_frame.grid(row=0, column=0, sticky='ew', padx=20)

        self.key_frame = InputСiphertextFrame(master=self.tab_view.tab("Шифратор"))
        self.key_frame.grid(row=0, column=1, sticky='ew', padx=20)

        self.s_box_frame = SboxScrollableFrame(master=self.tab_view.tab("Шифратор"))
        self.s_box_frame.grid(row=1, sticky='ew', columnspan=2, padx=20, pady=20)

        self.configuration_frame = ConfigurationFrame(master=self.tab_view.tab("Конфигурация шифратора"),
                                                      root=self)
        self.configuration_frame.pack(fill='x', padx=10, pady=20)

    def update_sbox(self):
        self.s_box_frame.destroy()
        self.s_box_frame = SboxScrollableFrame(master=self.tab_view.tab("Шифратор"))
        self.s_box_frame.grid(row=1, sticky='ew', columnspan=2, padx=20, pady=20)

app = App()
app.mainloop()
