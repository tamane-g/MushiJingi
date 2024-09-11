#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
テスト用実行ファイル

このファイルを実行することによってゲームのテストを実行する。

"""

from cards import *
from player import *

def test():
    deck_1 = [GinYanma(), GinYanma(), KabutoMushi(), KabutoMushi(), 
              NamiAgeha(), NamiAgeha(), KooniYanma(), KooniYanma(),
              Akiakane(), Akiakane(), IbukiOfMushi(), IbukiOfMushi(),
              MinoKaku(), MinoKaku(), Bakunetsu(), Bakunetsu(),
              MinZemi(), MinZemi(), NamiYou(), NamiYou()]
    
    deck_2 = []

    for _ in range(20):
        deck_2.append(SampleM())
        
    pl_1 = Player("Player_1", deck_1)
    pl_2 = Player("Player_2", deck_2)
    
    while True:
        pl_1.TurnStart(pl_2)
        pl_2.TurnStart(pl_1)
        if pl_1.GameSet or pl_2.GameSet:
            break

if __name__ == "__main__":
    test()
