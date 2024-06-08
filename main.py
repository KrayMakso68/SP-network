import random
import re
import time
from decimal import Decimal
from math import log, sqrt

import customtkinter

from spn import SPN, gen_pbox, int_to_str_with_fill

customtkinter.set_appearance_mode("dark")

S: int = 3  # число входов в s-блок
N: int = 3  # число s-блоков
Str_len: int = S * N  # длина входного слова
Sbox_len: int = 2 ** S  # длина s-блока
Rounds: int = 2  # кол-во полных раундов шифрования
P_option: bool = False  # операция перестановки в конце


def validate_binary_string(newval):
    """
    Function to validate binary string taking into account the changing length of the string

    Parameters
    ----------
    newval: str
         String to be validated

    Returns
    -------
    bool
        True if the string is valid otherwise False
    """
    reg_exp = '^[01]{0,' + str(Str_len) + '}$'
    if re.match(reg_exp, newval):
        return True
    else:
        return False


def validate_s_box(action, value_if_allowed):
    """
    Validate input in s_box

    Parameters
    ----------
    value_if_allowed: str
        Allowed input value
    action: str
        Type of operation

    Returns
    -------
    bool
        Release permission value

    """
    if action == "1":
        try:
            if len(value_if_allowed) > 1 and value_if_allowed[0] == "0":
                return False
            num = int(value_if_allowed)
            if 0 <= num < Sbox_len:
                return True
            else:
                return False
        except ValueError:
            return False
    else:
        return True


def generate_binary_string() -> str:
    """
    Generates a string of a given length, consisting of a random combination of 0 and 1.

    Parameters
    ----------

    Returns
    -------
    str
        Returns a new generated string
    """
    binary_digits = ['0', '1']
    length: int = Str_len
    binary_string = ''.join(random.choices(binary_digits, k=length))
    return binary_string


def generating_possible_keys() -> list[str]:
    """
    Generates a list of possible keys

    Returns
    -------
    list of str
        Returns a list of possible keys
    """
    keys = sqrt(2 * (2 ** Str_len) * log(100))
    keys_list = set()
    while len(keys_list) < keys:
        keys_list.add(generate_binary_string())
    keys_list = list(keys_list)

    # global Str_len
    # keys = 2 ** Str_len
    # keys_list = [int_to_str_with_fill(key, str_len=Str_len) for key in range(keys)]
    # random.shuffle(keys_list)

    return keys_list


def generate_sbox_list():
    """
    Generates a list of strings representing a s_box

    Returns
    -------
    list of int
        Returns a new generated sbox list
    """
    seen = set()
    while len(seen) < Sbox_len:
        seen.add(random.randint(0, Sbox_len - 1))
    seen = list(seen)
    random.shuffle(seen)
    return seen


class TabView(customtkinter.CTkTabview):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.add("Конфигурация шифратора")
        self.add("Шифратор")
        self.add("Метод встречи по середине")
        self.set("Шифратор")

        self.tab("Шифратор").columnconfigure((0, 1), weight=1)
        self.tab("Шифратор").rowconfigure(1, weight=1)


class ConfigurationTabFrame(customtkinter.CTkFrame):
    def __init__(self, master, root):
        super().__init__(master)

        self.columnconfigure((1, 2), weight=1)
        self.columnconfigure((0, 3), weight=2)

        self.root = root
        self.tab_view = root.tab_view

        customtkinter.CTkLabel(master=self, text="Число входов в S-блок:"
                               ).grid(row=0, column=1, padx=0, pady=0, sticky='e')
        self.S_var = customtkinter.StringVar(value='3')
        self.s_entry = customtkinter.CTkEntry(master=self, textvariable=self.S_var, width=40)
        self.s_entry.grid(row=0, column=2, padx=20, pady=5, sticky='w')

        customtkinter.CTkLabel(master=self, text='Число S-блоков:'
                               ).grid(row=1, column=1, padx=0, pady=0, sticky='e')
        self.N_var = customtkinter.StringVar(value='3')
        self.n_entry = customtkinter.CTkEntry(master=self, textvariable=self.N_var, width=40)
        self.n_entry.grid(row=1, column=2, padx=20, pady=5, sticky='w')

        customtkinter.CTkLabel(master=self, text="Количество раундов шифрования: \n(без учёта последнего раунда)"
                               ).grid(row=2, column=1, padx=0, pady=0, sticky='e')
        self.rounds_var = customtkinter.StringVar(value='2')
        self.rounds_entry = customtkinter.CTkEntry(master=self, textvariable=self.rounds_var, width=40)
        self.rounds_entry.grid(row=2, column=2, padx=20, pady=5, sticky='w')

        customtkinter.CTkLabel(master=self, text="Операция перестановки в последнем раунде:"
                               ).grid(row=3, column=1, padx=0, pady=0, sticky='e')
        self.p_option_var = customtkinter.BooleanVar(value=False)
        self.config_option_checkbox = customtkinter.CTkCheckBox(master=self, variable=self.p_option_var, text='')
        self.config_option_checkbox.grid(row=3, column=2, padx=20, pady=5, sticky='w')

        self.set_button = customtkinter.CTkButton(master=self)
        self.set_button.configure(text='Установить конфигурацию шифратора', height=40, width=250, command=self.set_config)
        self.set_button.grid(row=0, column=3, padx=0, pady=0, ipadx=10)


        customtkinter.CTkLabel(master=self, text="Генерация множества ключей:"
                               ).grid(row=5, column=1, padx=0, pady=(100, 0), sticky='e')
        self.combobox_var = customtkinter.StringVar(value="сокращённая")
        self.combobox = customtkinter.CTkComboBox(master=self, values=["сокращённая", "полный перебор"],
                                                  variable=self.combobox_var, width=150)
        self.combobox.grid(row=5, column=2, padx=20, pady=(100, 5), sticky='w')

        customtkinter.CTkLabel(master=self, text="Количество текстов для проверки:"
                               ).grid(row=6, column=1, padx=0, pady=0, sticky='e')
        self.S_var = customtkinter.StringVar(value='3')
        self.s_entry = customtkinter.CTkEntry(master=self, textvariable=self.S_var, width=40)
        self.s_entry.grid(row=6, column=2, padx=20, pady=5, sticky='w')

        self.set_button = customtkinter.CTkButton(master=self)
        self.set_button.configure(text='Установить конфигурацию атаки', height=40, width=250, command=self.set_config)
        self.set_button.grid(row=5, column=3, padx=0, pady=(95, 0), ipadx=10)


    def set_config(self):
        global S, N, Str_len, Sbox_len, Rounds, P_option
        S = int(self.S_var.get())
        N = int(self.N_var.get())
        Str_len = S * N
        Sbox_len = 2 ** S
        Rounds = int(self.rounds_var.get())
        P_option = self.p_option_var.get()
        self.root.encoder_frame.update_input()
        self.root.encoder_frame.reset_errors()
        self.root.meet_in_the_middle_frame.update_input()
        self.root.meet_in_the_middle_frame.reset_errors()
        self.tab_view.set("Шифратор")


class EncoderTabFrame(customtkinter.CTkFrame):
    def __init__(self, master, root):
        super().__init__(master)
        self.columnconfigure((0, 1), weight=1)
        self.rowconfigure(0, weight=1)
        self.root = root

        self.plaintext_frame = InputFrame(master=self, label_text='Открытый текст')
        self.plaintext_frame.grid(row=0, column=0, sticky='ew', padx=(20, 10))

        self.key_frame = InputFrame(master=self, label_text='Ключ зашифрования')
        self.key_frame.grid(row=0, column=1, sticky='ew', padx=(10, 20))

        self.s_box_frame = SboxScrollableFrame(master=self)
        self.s_box_frame.grid(row=1, sticky='ew', columnspan=2, padx=20, pady=20)

        self.cipher_text_frame = OutCiphertextFrame(master=self)
        self.cipher_text_frame.grid(row=2, column=0, sticky='ew', padx=(20, 10), pady=(0, 20))

        self.start_encryption_button = StartEncryptionFrame(master=self,
                                                            button_label='Зашифровать',
                                                            start_command=self.start_encryption,
                                                            reset_command=self.clear_input)
        self.start_encryption_button.grid(row=2, column=1, sticky='nsew', padx=(10, 20), pady=(0, 20))

    def update_input(self):
        self.plaintext_frame.entry.destroy()
        self.plaintext_frame.entry = customtkinter.CTkEntry(master=self.plaintext_frame)
        self.plaintext_frame.entry.configure(height=40, placeholder_text=generate_binary_string(),
                                             font=('', 18),
                                             validate="key",
                                             validatecommand=(self.register(validate_binary_string), '%P'))
        self.plaintext_frame.entry.grid(row=1, sticky='nsew', padx=10, pady=(5, 10))

        self.key_frame.entry.destroy()
        self.key_frame.entry = customtkinter.CTkEntry(master=self.key_frame)
        self.key_frame.entry.configure(placeholder_text=generate_binary_string(), height=40, font=('', 18),
                                       validate="key",
                                       validatecommand=(self.register(validate_binary_string), '%P'))
        self.key_frame.entry.grid(row=1, sticky='ew', padx=10, pady=(5, 10))

        self.s_box_frame.input_s_box_frame.destroy()
        self.s_box_frame.input_s_box_frame = InputSboxFrame(master=self.s_box_frame)
        self.s_box_frame.input_s_box_frame.grid(row=1, sticky='nsew', padx=10, pady=(0, 10), ipadx=10)

        self.cipher_text_frame.set_cipher_text('')
        self.start_encryption_button.set_ex_time('')

    def check_sbox(self, autogen_if_empty=True):
        global Sbox_len

        error = False
        self.s_box_frame.set_error('')
        s_box_set = set()
        for entry in self.s_box_frame.input_s_box_frame.get_sbox_entries():
            s_box_set.add(entry.get())
        if '' in s_box_set:
            if len(s_box_set) == 1 and autogen_if_empty:
                gen_sbox = generate_sbox_list()
                sbox_entries = self.s_box_frame.input_s_box_frame.get_sbox_entries()
                for index, entry in enumerate(sbox_entries):
                    entry.insert(0, str(gen_sbox[index]))
                self.s_box_frame.set_error('Автоподстановка значения', text_color='yellow2')
            else:
                error = True
                self.s_box_frame.set_error('Ошибка ввода значений S-блока\n'
                                           'Введите все значения S-блока')
        elif len(s_box_set) < Sbox_len:
            error = True
            self.s_box_frame.set_error('Ошибка ввода значений S-блока\n'
                                       'Значения S-блока дублируются')
        return error

    def check_configuration(self) -> bool:
        global Str_len
        entry_limit = Str_len
        error = False

        if len(self.plaintext_frame.get()) != entry_limit:
            if self.plaintext_frame.get() == '':
                self.plaintext_frame.set_input(generate_binary_string())
                self.plaintext_frame.set_error('Автоподстановка значения', text_color='yellow2')
            else:
                error = True
                self.plaintext_frame.set_error('Ошибка ввода открытого текста\n'
                                               'Число должно быть {}-значным'.format(Str_len))
        else:
            self.plaintext_frame.set_error('')
        if len(self.key_frame.get()) != entry_limit:
            if self.key_frame.get() == '':
                self.key_frame.set_input(generate_binary_string())
                self.key_frame.set_error('Автоподстановка значения', text_color='yellow2')
            else:
                error = True
                self.key_frame.set_error('Ошибка ввода ключа\n'
                                         'Число должно быть {}-значным'.format(Str_len))
        else:
            self.key_frame.set_error('')

        error = self.check_sbox()
        return error

    def start_encryption(self):
        global Str_len, S, N, Rounds, P_option

        if not self.check_configuration():
            plaintext = int(self.plaintext_frame.get(), 2)
            key = int(self.key_frame.get(), 2)
            s_box = [int(entry.get()) for entry in self.s_box_frame.input_s_box_frame.get_sbox_entries()]
            p_box = gen_pbox(S, N)
            implementation = int(P_option)
            sp = SPN(s_box, p_box, key, Rounds, implementation)

            start = time.time()
            encrypted_plaintext = sp.encrypt(plaintext)
            end = time.time()
            ex_time = float(round(Decimal(end - start), 3))
            self.start_encryption_button.set_ex_time(ex_time)

            out_cipher_text = int_to_str_with_fill(encrypted_plaintext, Str_len)
            self.cipher_text_frame.set_cipher_text(out_cipher_text)

    def reset_errors(self):
        self.plaintext_frame.set_error('')
        self.key_frame.set_error('')
        self.s_box_frame.set_error('')

    def clear_input(self):
        self.plaintext_frame.reset_input()
        self.key_frame.reset_input()
        self.s_box_frame.input_s_box_frame.reset_sbox_entries()
        self.cipher_text_frame.reset_cipher_text()
        self.start_encryption_button.set_ex_time('')
        self.reset_errors()


class MeetInTheMiddleTabFrame(customtkinter.CTkFrame):
    def __init__(self, master, root):
        super().__init__(master)
        self.root = root

        self.columnconfigure((0, 1), weight=1)

        self.plaintext_frame = InputFrame(master=self, label_text='Открытый текст')
        self.plaintext_frame.grid(row=0, column=0, sticky='ew', padx=10, pady=(0, 0))

        self.ciphertext_frame = InputFrame(master=self, label_text='Зашифрованный текст')
        self.ciphertext_frame.grid(row=0, column=1, sticky='ew', padx=10)

        self.key_pairs = KeyPairsFrame(master=self, check_command=self.check_key_pairs)
        self.key_pairs.grid(row=2, column=0, sticky='enw', padx=10, pady=(20, 0), rowspan=2)

        self.start_encryption_button = StartEncryptionFrame(master=self,
                                                            button_label='Выполнить атаку',
                                                            start_command=self.start_attack,
                                                            reset_command=self.clear_input)
        self.start_encryption_button.grid(row=2, column=1, sticky='enw', padx=10, pady=(20, 0))

        self.check_pairs_frame = CheckPairsFrame(master=self, command=self.check_key_pairs)
        self.check_pairs_frame.grid(row=3, column=1, sticky='sew', padx=10)

    def update_input(self):
        self.plaintext_frame.entry.destroy()
        self.plaintext_frame.entry = customtkinter.CTkEntry(master=self.plaintext_frame)
        self.plaintext_frame.entry.configure(height=40, placeholder_text=generate_binary_string(),
                                             font=('', 18),
                                             validate="key",
                                             validatecommand=(self.register(validate_binary_string), '%P'))
        self.plaintext_frame.entry.grid(row=1, sticky='nsew', padx=10, pady=(5, 10))

        self.ciphertext_frame.entry.destroy()
        self.ciphertext_frame.entry = customtkinter.CTkEntry(master=self.ciphertext_frame)
        self.ciphertext_frame.entry.configure(placeholder_text=generate_binary_string(), height=40, font=('', 18),
                                              validate="key",
                                              validatecommand=(self.register(validate_binary_string), '%P'))
        self.ciphertext_frame.entry.grid(row=1, sticky='ew', padx=10, pady=(5, 10))

        self.check_pairs_frame.input_key1.destroy()
        self.check_pairs_frame.input_key1 = customtkinter.CTkEntry(master=self.check_pairs_frame)
        self.check_pairs_frame.input_key1.configure(placeholder_text=generate_binary_string(),
                                                    validate="key", validatecommand=(self.register(validate_binary_string), '%P'))
        self.check_pairs_frame.input_key1.grid(row=2, sticky='nsew', padx=10, pady=(0, 5))

        self.check_pairs_frame.input_key2.destroy()
        self.check_pairs_frame.input_key2 = customtkinter.CTkEntry(master=self.check_pairs_frame)
        self.check_pairs_frame.input_key2.configure(placeholder_text=generate_binary_string(),
                                                    validate="key", validatecommand=(self.register(validate_binary_string), '%P'))
        self.check_pairs_frame.input_key2.grid(row=4, sticky='nsew', padx=10, pady=(0, 5))

        self.start_encryption_button.set_ex_time('')

    def check_configuration(self) -> bool:
        global Str_len
        entry_limit = Str_len
        error = False

        if self.root.encoder_frame.check_sbox(autogen_if_empty=False):
            error = True
            self.plaintext_frame.set_error('Ошибка ввода s-блока\n'
                                           'Проверьте s-блок во вкладке "Шифратор"')
            return error

        if len(self.plaintext_frame.get()) != entry_limit:
            error = True
            if self.plaintext_frame.get() == '':
                self.plaintext_frame.set_error('Ошибка ввода открытого текста\n'
                                               'Введите значение открытого текста')
            else:
                self.plaintext_frame.set_error('Ошибка ввода открытого текста\n'
                                               'Число должно быть {}-значным'.format(Str_len))
        else:
            self.plaintext_frame.set_error('')

        if len(self.ciphertext_frame.get()) != entry_limit:
            error = True
            if self.ciphertext_frame.get() == '':
                self.ciphertext_frame.set_error('Ошибка ввода зашифрованного текста\n'
                                                'Введите значение зашифрованного текста')
            else:
                self.ciphertext_frame.set_error('Ошибка ввода ключа\n'
                                                'Число должно быть {}-значным'.format(Str_len))
        else:
            self.ciphertext_frame.set_error('')
        return error

    def start_attack(self):
        global S, N, Rounds, P_option

        self.key_pairs.key_pairs_frame.clear()

        if not self.check_configuration():
            p = int(self.plaintext_frame.get(), 2)
            c = int(self.ciphertext_frame.get(), 2)
            keys = generating_possible_keys()
            half = len(keys) // 2
            k1_list = keys[:half]
            k2_list = keys[half:]
            encode_pairs_dict = []
            possible_keys_list = []

            s_box = [int(entry.get()) for entry in
                     self.root.encoder_frame.s_box_frame.input_s_box_frame.get_sbox_entries()]
            p_box = gen_pbox(S, N)
            implementation = int(P_option)

            start = time.time()

            for k1 in k1_list:
                sp = SPN(s_box, p_box, int(k1, 2), Rounds, implementation)
                middle_text_enc = sp.encrypt(p)
                encode_pairs_dict.append((k1, middle_text_enc))
            for k2 in k2_list:
                sp = SPN(s_box, p_box, int(k2, 2), Rounds, implementation)
                middle_text_dec = sp.decrypt(c)
                for pair in encode_pairs_dict:
                    if pair[1] == middle_text_dec:
                        possible_keys_list.append((pair[0], k2))

            end = time.time()
            ex_time = float(round(Decimal(end - start), 3))
            self.start_encryption_button.set_ex_time(ex_time)

            # k1 = '101111100'
            # sp = SPN(s_box, p_box, int(k1, 2), Rounds, implementation)
            # possible_keys_list.append(int_to_str_with_fill(sp.decrypt(int('111001001', 2)), str_len=9))

            self.key_pairs.key_pairs_frame.set_list(possible_keys_list)
            # print(possible_keys_list)

    def check_key_pairs(self):
        global S, N, Rounds, P_option, Str_len

        print(self.check_pairs_frame.check_input())
        print(not self.check_configuration())

        if self.check_pairs_frame.check_input() and not self.check_configuration():
            key_checkboxes = self.key_pairs.get_checkboxes()
            s_box = [int(entry.get()) for entry in self.root.encoder_frame.s_box_frame.input_s_box_frame.get_sbox_entries()]
            p_box = gen_pbox(S, N)
            implementation = int(P_option)

            plaintext_list = [generate_binary_string() for _ in range(5)]
            ciphertext_list = []
            control_key1, control_key2 = self.check_pairs_frame.get_keys_list()
            for plaintext in plaintext_list:
                sp1 = SPN(s_box, p_box, int(control_key1, 2), Rounds, implementation)
                middle_text = sp1.encrypt(int(plaintext, 2))
                sp2 = SPN(s_box, p_box, int(control_key2, 2), Rounds, implementation)
                ciphertext = sp2.encrypt(middle_text)
                ciphertext_list.append(ciphertext)

            for key_checkbox in key_checkboxes:
                pair = key_checkbox.cget('text')
                k1, k2 = pair[0], pair[1]
                valid = True
                for i, plaintext in enumerate(plaintext_list):
                    sp1 = SPN(s_box, p_box, int(k1, 2), Rounds, implementation)
                    middle_text = sp1.encrypt(int(plaintext, 2))
                    sp2 = SPN(s_box, p_box, int(k2, 2), Rounds, implementation)
                    ciphertext = sp2.encrypt(middle_text)
                    print(i)
                    if not ciphertext == ciphertext_list[i]:
                        valid = False
                        break
                if valid:
                    key_checkbox.select()
                    key_checkbox.configure(state='disable')


        # if not self.check_configuration():
        #     p = int(self.plaintext_frame.get(), 2)
        #     c = int(self.ciphertext_frame.get(), 2)
        #     key_checkboxes = self.key_pairs.get_checkboxes()
        #     s_box = [int(entry.get()) for entry in
        #              self.root.encoder_frame.s_box_frame.input_s_box_frame.get_sbox_entries()]
        #     p_box = gen_pbox(S, N)
        #     implementation = int(P_option)
        #
        #     P = '011000110'
        #     K1 = '101000100'
        #     K2 = '001000101'
        #
        #     SP1 = SPN(s_box, p_box, int(K1, 2), Rounds, implementation)
        #     MD = SP1.encrypt(int(P, 2))
        #     SP2 = SPN(s_box, p_box, int(K2, 2), Rounds, implementation)
        #     C = SP2.encrypt(MD)
        #
        #     for checkbox in key_checkboxes:
        #
        #         pair = checkbox.cget('text')
        #         k1, k2 = pair[0], pair[1]
        #         sp1 = SPN(s_box, p_box, int(k1, 2), Rounds, implementation)
        #         middle_text = sp1.encrypt(p)
        #         sp2 = SPN(s_box, p_box, int(k2, 2), Rounds, implementation)
        #         c_test = sp2.encrypt(middle_text)
        #
        #         sp3 = SPN(s_box, p_box, int(k1, 2), Rounds, implementation)
        #         middle_text3 = sp3.encrypt(int(P, 2))
        #         sp4 = SPN(s_box, p_box, int(k2, 2), Rounds, implementation)
        #         C_test = sp4.encrypt(middle_text3)
        #
        #         if c == c_test and C_test == C:
        #             checkbox.select()
        #             checkbox.configure(state='disable')

    def reset_errors(self):
        self.plaintext_frame.set_error('')
        self.ciphertext_frame.set_error('')
        self.check_pairs_frame.reset_error()

    def clear_input(self):
        self.plaintext_frame.reset_input()
        self.ciphertext_frame.reset_input()
        self.key_pairs.clear_keys()
        self.start_encryption_button.set_ex_time('')
        self.check_pairs_frame.reset_input()
        self.reset_errors()


class InputFrame(customtkinter.CTkFrame):
    def __init__(self, master, label_text: str):
        super().__init__(master)

        self.configure(fg_color='gray20')
        self.columnconfigure(0, weight=1)

        self.label = customtkinter.CTkLabel(master=self, text=label_text)
        self.label.grid(row=0, sticky='w', padx=10, pady=(10, 0))

        self.entry = customtkinter.CTkEntry(master=self)
        self.entry.configure(height=40, placeholder_text=generate_binary_string(), font=('', 18),
                             validate="key", validatecommand=(self.register(validate_binary_string), '%P'))
        self.entry.grid(row=1, sticky='nsew', padx=10, pady=(5, 10))

        self.error_label = customtkinter.CTkLabel(master=self)
        self.error_label.configure(text='', width=300, height=35)
        self.error_label.grid(row=2, sticky='w', padx=10, pady=(2, 10))

    def get(self):
        return self.entry.get()

    def set_input(self, text):
        self.entry.insert(0, text)

    def set_error(self, error, text_color='brown2'):
        self.error_label.configure(text=error, text_color=text_color)

    def reset_input(self):
        self.entry.delete(0, 'end')


class SboxScrollableFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master):
        super().__init__(master, orientation='horizontal')

        self.columnconfigure(0, weight=1)
        self.configure(fg_color='gray20')

        self.s_box_label = customtkinter.CTkLabel(master=self, text='S-блок')
        self.s_box_label.grid(row=0, sticky='w', padx=10, pady=(10, 5))

        self.input_s_box_frame = InputSboxFrame(master=self)
        self.input_s_box_frame.grid(row=1, sticky='nsew', padx=10, pady=(0, 10), ipadx=10)

        self.error_s_box_label = customtkinter.CTkLabel(master=self, text='', height=35)
        self.error_s_box_label.grid(row=2, column=0, sticky='w', padx=20, pady=(2, 5))

    def set_error(self, error, text_color='brown2'):
        self.error_s_box_label.configure(text=error, text_color=text_color)


class InputSboxFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.configure(fg_color='gray30')

        self.in_s_box_label = customtkinter.CTkLabel(master=self, text='ВХОД')
        self.in_s_box_label.grid(row=0, column=0, padx=5)
        self.out_s_box_label = customtkinter.CTkLabel(master=self, text='ВЫХОД')
        self.out_s_box_label.grid(row=1, column=0, padx=5)

        self.sbox_labels_list = self.create_sbox_labels(master=self)
        self.sbox_entries_list = self.create_sbox_entries(master=self)

    def create_sbox_labels(self, master):
        label_s_box_list = []
        global Sbox_len
        for i in range(Sbox_len):
            ent = customtkinter.CTkEntry(master, width=35, state='normal')
            ent.insert(0, f'{i}')
            ent.grid(row=0, column=i + 1, pady=(5, 2))
            ent.configure(state='disable')
            label_s_box_list.append(ent)
        return label_s_box_list

    def create_sbox_entries(self, master):
        entry_s_box_list = []
        global Sbox_len
        for i in range(Sbox_len):
            ent = customtkinter.CTkEntry(master=master)
            ent.configure(width=35, state='normal', validate="key",
                          validatecommand=(self.register(validate_s_box), '%d', '%P'))
            ent.grid(row=1, column=i + 1, pady=(2, 5))
            entry_s_box_list.append(ent)
        return entry_s_box_list

    def get_sbox_entries(self):
        return self.sbox_entries_list

    def reset_sbox_entries(self):
        for entry in self.sbox_entries_list:
            entry.delete(0, 'end')


class OutCiphertextFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.columnconfigure(0, weight=1)
        self.configure(fg_color='gray20')

        customtkinter.CTkLabel(master=self, text='Зашифрованный текст').grid(row=0, sticky='w', padx=10, pady=(10, 0))
        self.cipher_text_entry = customtkinter.CTkEntry(master=self, height=40, font=('', 18))
        self.cipher_text_entry.grid(row=1, sticky='nsew', padx=10, pady=(5, 10))
        self.cipher_text_entry.configure(state='disable')

    def set_cipher_text(self, cipher_text):
        self.cipher_text_entry.configure(state='normal')
        self.cipher_text_entry.delete(0, 'end')
        self.cipher_text_entry.insert(0, cipher_text)
        self.cipher_text_entry.configure(state='disable')

    def reset_cipher_text(self):
        self.cipher_text_entry.configure(state='normal')
        self.cipher_text_entry.delete(0, 'end')
        self.cipher_text_entry.configure(state='disable')


class StartEncryptionFrame(customtkinter.CTkFrame):
    def __init__(self, master, button_label, start_command, reset_command):
        super().__init__(master)

        self.columnconfigure(1, weight=1)
        self.rowconfigure((0, 2, 4), weight=1)
        self.start_command = start_command
        self.reset_command = reset_command

        self.start_encryption_button = customtkinter.CTkButton(master=self)
        self.start_encryption_button.configure(text=button_label, height=50, command=self.start_command)
        self.start_encryption_button.grid(row=1, column=0, sticky='nsew', columnspan=2, padx=10, pady=(5, 5))

        self.execution_time = customtkinter.CTkLabel(master=self)
        self.execution_time.configure(text='Время выполнения: ', width=165)
        self.execution_time.grid(row=3, column=0, sticky='w', padx=(10, 0), pady=(0, 5))

        self.reset_input = customtkinter.CTkButton(master=self)
        self.reset_input.configure(text='Сбросить', width=80, fg_color='firebrick4', hover_color='firebrick',
                                   command=self.reset_command)
        self.reset_input.grid(row=3, column=1, sticky='e', padx=(0, 10), pady=(0, 5))

    def set_ex_time(self, ex_time: float | str):
        if type(ex_time) is float and not ex_time > 0:
            ex_time = 'мгн'
        self.execution_time.configure(text='Время выполнения: {}'.format(ex_time))


class KeyPairsFrame(customtkinter.CTkFrame):
    def __init__(self, master, check_command):
        super().__init__(master)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=0)
        self.configure(fg_color='gray20')
        self.check_command = check_command

        self.label = customtkinter.CTkLabel(master=self, text='Возможные пары ключей')
        self.label.grid(row=0, column=0, sticky='w', padx=10, pady=5)

        self.key_pairs_frame = KeyPairsScrollableFrame(master=self)
        self.key_pairs_frame.grid(row=1, column=0, sticky='nsew', padx=10, pady=(0, 10))

        # self.check_button = customtkinter.CTkButton(master=self)
        # self.check_button.configure(text='Проверить', fg_color='gray26', width=100,
        #                             hover_color='gray32', command=self.check_command)
        # self.check_button.grid(row=1, column=0, sticky='n', pady=10, padx=(5, 10))

    def get_checkboxes(self):
        return self.key_pairs_frame.get_checkboxes()

    def clear_keys(self):
        self.key_pairs_frame.clear()


class KeyPairsScrollableFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master):
        super().__init__(master)
        self.configure(width=40, height=300)
        self.checkboxes = []

    def add(self, value):
        next_index = len(self.checkboxes)
        checkbox = customtkinter.CTkCheckBox(self, text=value)
        checkbox.grid(row=next_index, column=0, padx=10, pady=(10, 0), sticky="w")
        checkbox.configure(state='disable')
        self.checkboxes.append(checkbox)

    def set_list(self, values):
        for i, value in enumerate(values):
            checkbox = customtkinter.CTkCheckBox(self, text=value)
            checkbox.grid(row=i, column=0, padx=10, pady=(10, 0), sticky="w")
            checkbox.configure(state='disable')
            self.checkboxes.append(checkbox)

    def clear(self):
        for checkbox in self.checkboxes:
            checkbox.destroy()
        self.checkboxes = []

    def get_checkboxes(self):
        return self.checkboxes


class CheckPairsFrame(customtkinter.CTkFrame):
    def __init__(self, master, command):
        super().__init__(master)
        self.columnconfigure(0, weight=1)
        self.command = command

        self.label = customtkinter.CTkLabel(master=self)
        self.label.configure(text='Проверка по исходным ключам')
        self.label.grid(row=0, column=0, sticky='w', padx=10, pady=(5, 10))

        self.label_key1 = customtkinter.CTkLabel(master=self, text='Первый ключ')
        self.label_key1.grid(row=1, sticky='w', padx=10, pady=(5, 0))

        self.input_key1 = customtkinter.CTkEntry(master=self)
        self.input_key1.configure(placeholder_text=generate_binary_string(),
                                  validate="key", validatecommand=(self.register(validate_binary_string), '%P'))
        self.input_key1.grid(row=2, sticky='nsew', padx=10, pady=(0, 5))

        self.label_key2 = customtkinter.CTkLabel(master=self, text='Второй ключ')
        self.label_key2.grid(row=3, sticky='w', padx=10, pady=0)

        self.input_key2 = customtkinter.CTkEntry(master=self)
        self.input_key2.configure(placeholder_text=generate_binary_string(),
                                  validate="key", validatecommand=(self.register(validate_binary_string), '%P'))
        self.input_key2.grid(row=4, sticky='nsew', padx=10, pady=(0, 5))

        self.check_button = customtkinter.CTkButton(master=self)
        self.check_button.configure(text='Проверить', fg_color='gray26', width=100,
                                    hover_color='gray32', command=self.command)
        self.check_button.grid(row=5, column=0, sticky='w', pady=(5, 10), padx=(10, 0))

        self.error_label = customtkinter.CTkLabel(master=self)
        self.error_label.configure(text='', text_color='brown2')
        self.error_label.grid(row=5, sticky='e', padx=10)

    def set_error(self):
        self.error_label.configure(text='Ошибка ввода')

    def reset_error(self):
        self.error_label.configure(text='')

    def reset_input(self):
        self.input_key1.delete(0, 'end')
        self.input_key2.delete(0, 'end')

    def get_keys_list(self):
        k1 = self.input_key1.get()
        k2 = self.input_key2.get()
        return [k1, k2]

    def check_input(self):
        if self.input_key1.get() == '' or self.input_key2.get() == '':
            self.set_error()
            return False
        else:
            self.reset_error()
            return True


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("SP-network")
        self.geometry("900x600")

        self.tab_view = TabView(self)
        self.tab_view.pack(expand=True, fill='both', padx=5, pady=(0, 5))

        self.configuration_frame = ConfigurationTabFrame(master=self.tab_view.tab("Конфигурация шифратора"), root=self)
        self.configuration_frame.pack(fill='x', padx=20, pady=20)

        self.encoder_frame = EncoderTabFrame(master=self.tab_view.tab("Шифратор"), root=self)
        self.encoder_frame.pack(expand=True, fill='both')

        self.meet_in_the_middle_frame = MeetInTheMiddleTabFrame(master=self.tab_view.tab("Метод встречи по середине"),
                                                                root=self)
        self.meet_in_the_middle_frame.pack(fill='x', padx=10, pady=10)


app = App()
app.mainloop()
