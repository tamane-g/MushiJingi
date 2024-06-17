#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 蟲神器オンライン

import random
from cards import *

ColorName = {'Red':"赤", 'Blue':"青", 'Green':"緑"}

def IntInputLoop(message:str, end:int, start:int=0):
    print()
    while True:
        res = int(input(message))
        print("\n====================================================================\n")
        if start <= res and res <= end:
            break
        else:
            print("入力値が範囲外です(適正入力値: " + str(start) + "~" + str(end) + ")")
            
    return res

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
        
        for i in range(len(Deck)):
            self.__Deck[i] = self.__Deck[i](self)
        
        self._ShuffleDeck()
        
        for i in range(6):
            self.__Nawabari.append(self.__Deck.pop(0))
            self.__Nawabari[i].Ura = True
            
        for i in range(4):
            self._Draw()
        
        self.MyInfo()

    # 表示関連
    
    def MyInfo(self):
        print(self.Name)
        print("場　　: ")
        self.PrintBattleZone(AddNum=20, HideUra=True)
        print("手札　: ")
        self.PrintHands()
        print("縄張り: " + str(len(self.__Nawabari)))
        print("山札　: " + str(len(self.__Deck)))
        print("コスト: " + str(self.Costs) + " / " + str(len(self.__Esaba)))
        print()
        
    def OppInfo(self, AttackableOnly=False):
        print(self.Opp.Name)
        print("場　　: ")
        self.PrintBattleZone(HideUra=True, AttackableOnly=AttackableOnly)
        print("手札　: " + str(len(self.Opp.__Hands)))
        print("縄張り: " + str(len(self.Opp.__Nawabari)))
        print("山札　: " + str(len(self.Opp.__Deck)))
        print("コスト: " + str(self.Opp.Costs) + " / " + str(len(self.Opp.__Esaba)))
        print()

    def PrintHands(self, AddNum:int=0, HideUra=False):
        for i in range(len(self.__Hands)):
            if HideUra:
                message = str(i+AddNum) + ": ???"
            else:
                message = str(i+AddNum) + ": " + self.__Hands[i].Name + "\t\tコスト:" + str(self.__Hands[i].Cost) + "\t種類: "
                if issubclass(type(self.__Hands[i]), Mushi):
                    message += "蟲カード"
                elif issubclass(type(self.__Hands[i]), Jutsu):
                    message += "術カード"
                elif issubclass(type(self.__Hands[i]), Kyoka):
                    message += "強化カード"
                else:
                    message += "不明"
            print(message)

    def PrintNawabari(self, AddNum:int=0):
        for i in range(len(self.__Nawabari)):
            if self.__Nawabari[i].Ura:
                message = str(i+AddNum) + ": ???"
            else:
                message = str(i+AddNum) + ": " + self.__Hands[i].Name + "\t\tコスト:" + str(self.__Hands[i].Cost) + "\t種類: "
                if issubclass(type(self.__Hands[i]), Mushi):
                    message += "蟲カード"
                elif issubclass(type(self.__Hands[i]), Jutsu):
                    message += "術カード"
                elif issubclass(type(self.__Hands[i]), Kyoka):
                    message += "強化カード"
                else:
                    message += "不明"
            print(message)

    def PrintBattleZone(self, AddNum:int=0, HideUra=False, AttackableOnly=False):
        exist_blocker = False
        printed_list  = []
        
        for card in self.__BattleZone:
            if (not card.Ura) and card.Blocker:
                exist_blocker = True
        
        for i in range(len(self.__BattleZone)):
            if (HideUra or AttackableOnly) and self.__BattleZone[i].Ura:
                continue
            elif AttackableOnly and self.__BattleZone[i].Gitai:
                continue
            elif AttackableOnly and exist_blocker and (not self.__BattleZone[i].Blocker):
                continue
            else:
                print(str(i+AddNum) + ": " + self.__BattleZone[i].Name + "\t\tHP: " + str(self.__BattleZone[i].HP_result) + "\t色: " + ColorName[self.__BattleZone[i].Color])
                printed_list.append(i+AddNum)
        
        return printed_list
       
    def _OppRefresh(self, Opp:'Player'):
        self.Opp = Opp
      
    def GetBattleZoneLen(self):
        return len(self.__BattleZone)
      
    # プレイヤー内部動作
      
    def _ShuffleDeck(self):
        random.shuffle(self.__Deck)

    def _CntCost(self):
        self.Costs = len(self.__Esaba)
        return self.Costs
    
    def _Draw(self):
        drawed = self.__Deck.pop(0)
        self.__Hands.append(drawed)
        return drawed
        
    def _PutCost(self, Num:int):
        if Num != -1:
            put = self.__Hands.pop(Num)
            self.__Esaba.append(put)
            print("\n" + put.Name + " をエサ場にセットしました\n")

    def Play(self, Num:int):
        p_card = self.__Hands[Num]
        if p_card.Cost <= self.Costs:
            p_card = self.__Hands.pop(Num)
            self.Costs -= p_card.Cost
        else:
            print("\nコストが足りません\n")
            return
        if issubclass(type(p_card), Mushi):
            self._PlayMushi(p_card)
        elif issubclass(type(p_card), Jutsu):
            self._PlayJutsu(p_card)
        elif issubclass(type(p_card), Kyoka):
            if self.GetBattleZoneLen() != 0:
                self._PlayKyoka(p_card)
            else:
                print("強化対象が存在しません")
                self.__Hands.append(p_card)
                return
        else:
            print("不明なカードです")
            return
        print("\n" + p_card.Name + " をプレイしました\n")

    def _PlayMushi(self, Mushi:'Mushi'):
        Mushi.Play()

    def _PlayJutsu(self, Jutsu:'Jutsu'):
        Jutsu.Play()
            
        if Jutsu.Charge:
            self.__Esaba.append(Jutsu)
        else:
            self.__Bochi.append(Jutsu)

    def _PlayKyoka(self, Kyoka:'Kyoka'):
        self.PrintBattleZone(HideUra=True)
        select_mushi = IntInputLoop("対象を選んでください: ", self.GetBattleZoneLen()-1)
        self.__BattleZone[select_mushi].Kyokas.append(Kyoka)
        
        if Kyoka.Buffer:
            self.__BattleZone[select_mushi].DirectHPBuff(Kyoka.BuffList[0])

    def _AtkMushi(self, Num:int):
        mushi = self.__BattleZone[Num]
        if mushi.Tap:
            print("\n攻撃済みです\n")
        else:
            self._AtkChoice(mushi)

    def _AtkChoice(self, Mushi:'Mushi'):
        print("\n" + Mushi.Name)
        print("攻撃: ")
        for Atk in range(len(Mushi.AtkList)):
            print(str(Atk) + ": " + Mushi.AtkList[Atk]['name'] + " " + str(Mushi.AtkList[Atk]['damage']) + " (+" + str(Mushi.Atk_result) + ")")
        select_atk = IntInputLoop("使用する攻撃を選んでください（攻撃しない場合は-1）: ", len(Mushi.AtkList)-1, -1)
        
        if select_atk == -1:
            return
        if len(self.Opp.__BattleZone) > 0:
            self.OppInfo(MushiShow=True)
            select_mushi = IntInputLoop("対象を選んでください（キャンセルする場合は-1）: ", self.Opp.GetBattleZoneLen()-1, -1)
            if select_mushi != -1:
                if Mushi.AtkList[select_atk]['method'](self.Opp.__BattleZone[select_mushi], Mushi.AtkList[select_atk]['damage'], Mushi.Color):
                    self.Opp._BrokeMushi(select_mushi, True)
            else:
                return
        else:
            Mushi.AtkList[select_atk]['method'](self.Opp, Mushi.AtkList[select_atk]['damage'], Mushi.Color)

    def _BrokeMushi(self, MushiNum:int, Direct:bool):
        self.__Bochi.append(self.__BattleZone.pop(MushiNum))
        if Direct:
            self.P_Damage(False)

    def P_Damage(self, P_Direct:bool):
        if P_Direct:
            print(self.Name + " への直接攻撃！！")
        if len(self.__Nawabari) > 0:
            print(self.Name + " の縄張りが1枚破壊された\n")
            print(self.Name + "\n縄張り:")
            self.PrintNawabari()
            select_num = IntInputLoop("引く縄張りを選んでください: ", len(self.__Nawabari)-1)
            draw_nawabari = self.__Nawabari.pop(select_num)
            draw_nawabari.Ura = False
            self.__Hands.append(draw_nawabari)
        elif P_Direct:
            self.Lose()

    def MoveCard(self, target:'Card', from_, to_):
        if target in from_:
            from_.remove(target)
            to_.append(target)

    # プレイヤー外部動作

    def TurnStart(self, Opp:'Player'):
        self._OppRefresh(Opp)
        if not (self.GameSet or self.Opp.GameSet):
            for MyMushi in self.__BattleZone:
                MyMushi.Refresh()
            self.OppInfo()
            self._Draw()
            self._CntCost()
            self.MyInfo()
            self._PutCost(IntInputLoop("餌に置くカードを選んでください（置かないなら-1）: ", len(self.__Hands)-1, -1))
            self._CntCost()
            
            while not (self.GameSet or self.Opp.GameSet):
                self.OppInfo()
                self.MyInfo()
                select_num = int(input("プレイするカードを選択してください（ターンエンドは-1）: "))
                print("\n====================================================================\n")
                if select_num != -1:
                    if (select_num-20) < 0:
                        self.Play(select_num)
                    elif (select_num-40) < 0:
                        self._AtkMushi(select_num-20)
                else:
                    break
            self.TurnEnd()

    def TurnEnd(self):
        pass

    def Lose(self):
        print("\n" + self.Name + " の負けです")
        self.GameSet = True

def test():
    deck_1 = [GinYanma, GinYanma, KabutoMushi, KabutoMushi, 
              NamiAgeha, NamiAgeha, KooniYanma, KooniYanma,
              Akiakane, Akiakane, IbukiOfMushi, IbukiOfMushi,
              MinoKaku, MinoKaku]
    for i in range(6):
        deck_1.append(SampleM)
    deck_2 = []
    for i in range(20):
        deck_2.append(SampleM)
        
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
