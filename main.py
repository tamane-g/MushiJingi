#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 蟲神器オンライン

import random
from cards import *

class Player:
    def __init__(self, Name:str, Deck:List[Card]):
        self.__Deck         = Deck.copy()   # 山札
        self.__BattleZone   = []            # 場
        self.__Nawabari     = []            # 縄張り
        self.__Hands        = []            # 手札
        self.__Bochi        = []            # 墓地
        self.__Esaba        = []            # エサ場
        
        self.Opp            = None
        self.Name           = Name
        self.Turn           = 0
        self.Costs          = 0
        self.GameSet        = False
        
        self.ShuffleDeck()
        
        for i in range(6):
            self.__Nawabari.append(self.__Deck.pop(0))
            self.__Nawabari[i].Ura = True
            
        for i in range(4):
            self.Draw()
        
        self.MyInfo()
            
    def MyInfo(self):
        print(self.Name)
        print("場　　: ")
        self.PrintCards(self.__BattleZone, 20)
        print("手札　: ")
        self.PrintCards(self.__Hands)
        print("縄張り: " + str(len(self.__Nawabari)))
        print("山札　: " + str(len(self.__Deck)))
        print("コスト: " + str(self.Costs) + " / " + str(len(self.__Esaba)))
        print()
        
    def OppInfo(self):
        print(self.Opp.Name)
        print("場　　: ")
        self.PrintCards(self.Opp.__BattleZone, UraShow=False)
        print("手札　: " + str(len(self.Opp.__Hands)))
        print("縄張り: " + str(len(self.Opp.__Nawabari)))
        print("山札　: " + str(len(self.Opp.__Deck)))
        print("コスト: " + str(self.Opp.Costs) + " / " + str(len(self.Opp.__Esaba)))
        print()
      
    def OppRefresh(self, Opp:'Player'):
        self.Opp = Opp
      
    def ShuffleDeck(self):
        random.shuffle(self.__Deck)
        # self.PrintCards(self.__Deck)
        
    def PrintCards(self, Cards:List[Card], AddNum=0, UraShow=True):
        for i in range(len(Cards)):
            if Cards[i].Ura:
                if UraShow:
                    print(str(i+AddNum) + ": ???")
            else:
                print(str(i+AddNum) + ": " + Cards[i].Name + "\tC:" + str(Cards[i].Cost))
    
    def CntCost(self):
        self.Costs = len(self.__Esaba)
        return self.Costs
    
    def Draw(self):
        drawed = self.__Deck.pop(0)
        self.__Hands.append(drawed)
        return drawed
        
    def PutCost(self, Num:int):
        if Num != -1:
            put = self.__Hands.pop(Num)
            self.__Esaba.append(put)
            print("\n" + put.Name + " をエサ場にセットしました\n")

    def PlayMushi(self, Mushi:'Mushi'):
        self.__BattleZone.append(Mushi)

    def Play(self, Num:int):
        p_card = self.__Hands[Num]
        if p_card.Cost <= self.Costs:
            p_card = self.__Hands.pop(Num)
            self.Costs -= p_card.Cost
        else:
            print("\nコストが足りません\n")
            return
        if issubclass(type(p_card), Mushi):
            self.PlayMushi(p_card)
        elif issubclass(type(p_card), Jutsu):
            print("術カードです")
        elif issubclass(type(p_card), Kyoka):
            print("強化カードです")
        else:
            print("不明なカードです")
            return
        print("\n" + p_card.Name + " をプレイしました\n")

    def AtkMushi(self, Num:int):
        mushi = self.__BattleZone[Num]
        if mushi.Tap:
            print("\n攻撃済みです\n")
        else:
            self.AtkChoice(mushi)

    def AtkChoice(self, Mushi:'Mushi'):
        print("\n" + Mushi.Name)
        print("攻撃: ")
        for Atk in range(len(Mushi.AtkList)):
            print(str(Atk) + ": " + Mushi.AtkList[Atk]['name'] + " " + str(Mushi.AtkList[Atk]['damage']) + " (+" + str(Mushi.Atk_result) + ")")
        select_num = int(input("\n使用する攻撃を選んでください（攻撃しない場合は-1）: "))
        
        if select_num != -1:
            if len(self.Opp.__BattleZone) > 0:
                self.OppInfo()
                select_num = int(input("\n対象を選んでください（キャンセルする場合は-1）: "))
                if select_num != -1:
                    if Mushi.AtkList[select_num]['method'](self.Opp.__BattleZone[select_num], Mushi.AtkList[select_num]['damage'], Mushi.Color):
                        self.Opp.BrokeMushi(select_num, True)
                else:
                    return
            else:
                Mushi.AtkList[select_num]['method'](self.Opp, Mushi.AtkList[select_num]['damage'], Mushi.Color)
        else:
            return

    def TurnStart(self, Opp:'Player'):
        self.OppRefresh(Opp)
        if not (self.GameSet or self.Opp.GameSet):
            for MyMushi in self.__BattleZone:
                MyMushi.Refresh()
            self.OppInfo()
            self.Draw()
            self.CntCost()
            self.MyInfo()
            self.PutCost(int(input("餌に置くカードを選んでください（置かないなら-1）: ")))
            self.CntCost()
            
            while True:
                self.OppInfo()
                self.MyInfo()
                select_num = int(input("プレイするカードを選択してください（ターンエンドは-1）: "))
                if select_num != -1:
                    if (select_num-20) < 0:
                        self.Play(select_num)
                    elif (select_num-40) < 0:
                        self.AtkMushi(select_num-20)
                else:
                    print()
                    break
            self.TurnEnd()

    def TurnEnd(self):
        pass

    def BrokeMushi(self, MushiNum:int, Direct:bool):
        self.__Bochi.append(self.__BattleZone.pop(MushiNum))
        if Direct:
            self.P_Damage(False)

    def P_Damage(self, Direct:bool):
        if len(self.__Nawabari) > 0:
            print(self.Name + "\n縄張り:")
            self.PrintCards(self.__Nawabari)
            select_num = int(input("\n引く縄張りを選んでください: "))
            print()
            draw_nawabari = self.__Nawabari.pop(select_num)
            draw_nawabari.Ura = False
            self.__Hands.append(draw_nawabari)
        elif Direct:
            self.Lose()

    def Lose(self):
        print("\n" + self.Name + " の負けです")
        self.GameSet = True

def test():
    deck_1 = []
    for i in range(20):
        deck_1.append(SampleM())
    deck_2 = []
    for i in range(20):
        deck_2.append(SampleM())
        
    pl_1 = Player("Player_1", deck_1)
    pl_2 = Player("Player_2", deck_2)
    
    while True:
        pl_1.TurnStart(pl_2)
        pl_2.TurnStart(pl_1)
        if pl_1.GameSet or pl_2.GameSet:
            break
        
    print("ゲームセット！")
    
if __name__ == "__main__":
    test()
