#!/usr/bin/env python
# -*- coding: utf-8 -*-

from teryt import DaneTeryt
import codecs
import os
from tkinter import *
from tkinter.messagebox import showerror, showinfo
from tkinter.filedialog import asksaveasfilename

version = '0.1'
helptext = """
    TERYTorium - %s
    Autor: Jakub Plata
"""

FILESAVEOPTIONS = dict(defaultextension='.txt',
                       filetypes=[('Text', '*.txt')])

class TeryTorium:

    def __init__(self, root):
        self.root = root
        self.root.title('TERYTorium')
        self.root.iconbitmap('./ter.ico')
        self.zapis_flag = IntVar(self.root, value=1)
        if os.path.exists('./dane'):
            try:
                self.teryt = DaneTeryt('./dane/TERC.xml')
            except IOError:
                showerror(u'BŁĄD', 'Brak danych!!!')
                self.root.destroy()
            else:
                self.woj, self.woj_pow, self.pow_gmi = self.teryt.wczytaj_dane()
                self.make_widgets()
                self.menu_bar()
        else:
            showerror(u'BŁĄD', 'Brak foleru ./dane')
            self.root.destroy()

    def make_widgets(self):
        ramka_zapis = LabelFrame(self.root, text='Zapis do pliku:', padx=5, pady=5)
        ramka_zapis.grid(row=0, column=0, columnspan=3, sticky='w')
        Radiobutton(ramka_zapis, text='powiaty', variable=self.zapis_flag, value=1).grid(row=0, column=0)
        Radiobutton(ramka_zapis, text='gminy', variable=self.zapis_flag, value=0).grid(row=0, column=1)
        Button(ramka_zapis, text='Zapisz',
               command=lambda: self.saveas(self.zapis_flag.get())).grid(row=0, column=2)
        Label(self.root, text=u'Województwa:').grid(row=1, column=0)
        Label(self.root, text=u'Powiaty:').grid(row=1, column=1)
        Label(self.root, text=u'Gminy:').grid(row=1, column=2)
        frame_woj = Frame(self.root)
        frame_woj.grid(row=2, column=0)
        frame_pow = Frame(self.root)
        frame_pow.grid(row=2, column=1)
        frame_gmi = Frame(self.root)
        frame_gmi.grid(row=2, column=2)

        self.listbox_woj = Listbox(frame_woj, width=30, height=20)
        self.listbox_woj.bind('<<ListboxSelect>>', self.cur_sel_woj)
        self.listbox_woj.pack(side=LEFT, fill=BOTH)
        scrollbar_pow = Scrollbar(frame_pow)
        scrollbar_pow.pack(side=RIGHT, fill=Y)
        self.listbox_pow = Listbox(frame_pow, yscrollcommand=scrollbar_pow.set,
                              width=30, height=20)
        self.listbox_pow.bind('<<ListboxSelect>>', self.cur_sel_pow)
        self.listbox_pow.pack(side=LEFT, fill=BOTH)
        scrollbar_gmi = Scrollbar(frame_gmi)
        scrollbar_gmi.pack(side=RIGHT, fill=Y)
        self.listbox_gmi = Listbox(frame_gmi, yscrollcommand=scrollbar_gmi.set,
                                   width=50, height=20)
        self.listbox_gmi.pack(side=LEFT, fill=BOTH)


        for t in self.woj:
            self.listbox_woj.insert(END, t)

    def menu_bar(self):
        self.pasek_menu = Menu(self.root)
        self.pomoc_menu = Menu(self.pasek_menu, tearoff=0)
        self.pomoc_menu.add_command(label='O programie', command=self.pomoc)
        self.pasek_menu.add_cascade(label='Pomoc', menu=self.pomoc_menu)

        self.root.config(menu=self.pasek_menu)

    def cur_sel_woj(self, event):
        self.listbox_pow.delete(0, END)
        self.listbox_gmi.delete(0, END)
        nazwa = self.listbox_woj.get(self.listbox_woj.curselection())
        numer = nazwa.split(' ')[0] # wyciaga numer z pelnej nazwy wojewodztwa
        for p in self.woj_pow[numer]:
            self.listbox_pow.insert(END, p)

    def cur_sel_pow(self, event):
        self.listbox_gmi.delete(0, END)
        nazwa = self.listbox_pow.get(self.listbox_pow.curselection())
        numer = nazwa.split(' ')[0]  # wyciaga numer z pelnej nazwy powiatu
        for g in self.pow_gmi[numer]:
            self.listbox_gmi.insert(END, g)

    def saveas(self, tryb):
        file_name = asksaveasfilename(initialdir='.', **FILESAVEOPTIONS)
        if tryb:
            data = self.listbox_pow.get(0, END)
        else:
            data = self.listbox_gmi.get(0, END)
        with codecs.open(file_name, 'w', encoding='cp1250') as f:
            for i in data:
                f.writelines(i+'\r\n')
        f.close()
        showinfo('Info', 'Zapisano plik')


    def pomoc(self):
        showinfo('O programie', helptext % (version))

if __name__ == "__main__":

    root = Tk()
    TeryTorium(root)
    root.mainloop()