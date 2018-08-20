#!/usr/bin/env python
# -*- coding: utf-8 -*-
from lxml import etree
from collections import defaultdict, OrderedDict

class DaneTeryt():
    def __init__(self, plik):
        self.doc = etree.parse(plik)

    def element(self, nazwa):
        elementy = self.doc.xpath("/teryt/catalog/row/col[@name='%s']" % nazwa)
        return [element.text for element in elementy]

    def numer_nazwa_teryt(self, wiersz):
        nr_teryt = [nr for nr in wiersz[0:4] if nr is not None]
        if len(nr_teryt) == 4:
            nr_teryt.insert(3, '_')
            nazwa = ' '.join((wiersz[5], wiersz[4]))
        else:
            nazwa = wiersz[4]
        return ''.join(nr_teryt), nazwa

    def wczytaj_dane(self):
        lista_wojewodztw = []
        woj_pow = defaultdict(list)
        pow_gmi = defaultdict(list)
        woj = self.element('WOJ')
        pow = self.element('POW')
        gmi = self.element('GMI')
        rodz = self.element('RODZ')
        nazwa = self.element('NAZWA')
        nazwa_dod = self.element('NAZDOD')
        teryt_nazwa = {}
        calosc = zip(woj, pow, gmi, rodz, nazwa, nazwa_dod)
        for i in calosc:
            nr_teryt, nazwa = self.numer_nazwa_teryt(i)
            if len(nr_teryt) == 2:
                lista_wojewodztw.append(' '.join((nr_teryt, nazwa)))
            elif len(nr_teryt) == 4:
                woj_pow[nr_teryt[0:2]].append(' '.join((nr_teryt, nazwa)))
            elif len(nr_teryt) == 8:
                pow_gmi[nr_teryt[0:4]].append(' '.join((nr_teryt, nazwa)))
        return lista_wojewodztw, woj_pow, pow_gmi


if __name__ == "__main__":  # pragma no cover
    t = DaneTeryt('../dane/TERC.xml')
    t_n = t.wczytaj_dane()