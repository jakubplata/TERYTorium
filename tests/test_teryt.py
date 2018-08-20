#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from app.teryt import DaneTeryt


class TestTeryt(unittest.TestCase):
    def setUp(self):
        self.t = DaneTeryt('../dane/TERC.xml')

    def test_teryt_exists(self):
        assert self.t is not None

    def test_element(self):
        wynik = self.t.element('POW')
        exp = [None, '01']
        self.assertEqual(exp, wynik[0:2])

    def test_numer_teryt(self):
        nr, n = self.t.numer_nazwa_teryt(('02', None, None, None,
                                          u'DOLNOŚLĄSKIE', u'województwo'))
        self.assertEqual('02', nr)
        self.assertEqual(u'DOLNOŚLĄSKIE', n)
        nr2, n2 = self.t.numer_nazwa_teryt(('02', '01', None, None,
                                           u'bolesławiecki', 'powiat'))
        self.assertEqual('0201', nr2)
        self.assertEqual(u'bolesławiecki', n2)
        nr3, n3 = self.t.numer_nazwa_teryt(('02', '01', '01', '1',
                                           u'Bolesławiec', 'gmina miejska'))
        self.assertEqual('020101_1', nr3)
        self.assertEqual(u'gmina miejska Bolesławiec', n3)

    def test_wczytaj_dane(self):
        lista, w_p, p_g = self.t.wczytaj_dane()
        exp = [u'14 MAZOWIECKIE', u'0201 bolesławiecki',
               u'020101_1 gmina miejska Bolesławiec']
        self.assertEqual(lista[6], exp[0])
        self.assertTrue(exp[1] in w_p[u'02'])
        self.assertTrue(exp[2] in p_g[u'0201'])



if __name__ == '__main__':
    unittest.main()
