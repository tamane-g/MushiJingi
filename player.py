#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Playerクラス定義

このモジュールは、ゲームの主体となるPlayerクラスを提供する。
主な機能として、プレイヤーの山札・手札・場・エサ場・捨て札の管理を行う。

"""

import random
from typing import Union
from cards import Card, Mushi, Jutsu, Kyoka


def IntInputLoop(message:str, end: int, start: int=0) -> int:
    """
    指定された範囲内の整数でユーザーに入力させるループを実行する

    この関数は、指定されたメッセージを表示し、ユーザーに整数を入力させる。
    入力が指定された範囲に収まるまで、ユーザーに入力を行わせる。
    範囲内の整数が入力されると、ループを終了してその値が返す。

    Args:
        message (str): 入力を促す際に表示するメッセージ
        end (int): 入力可能な整数の最大値
        start (int, optional): 入力可能な整数の最小値。デフォルトは0

    Returns:
        int: ユーザーが指定された範囲内で入力した整数

    """
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
    """
    Playerを表すクラス

    このクラスは、プレイヤーの持つカードを保持・管理し、
    それらに関連する動作を提供する。

    Methods:
        UI Methods:
            PrintCards(Cards: list[Card], AddNum: int=0, UraShow: bool=True, MushiShow: bool=False) -> None:
                通し番号付きでCardsの情報を表示する。通し番号はAddNumから始まる。
                UraShowがFalseなら、裏向きの場のカードは表示されない。
                MushiShowがTrueなら、虫カードによって攻撃可能な虫カードのみが表示される(擬態中の虫や鳴く・鱗粉と並んでいる虫は表示されない。)。

            ShowMyInfo(): 自プレイヤーの知り得る情報を表示する。
            ShowEnemyPlayerInfo(): 相手プレイヤーの知り得る情報を表示する。
            ShowEnemyAttackableMushiInfo(): 自プレイヤーの虫が攻撃可能な、相手プレイヤーの場の虫を表示する。
            ShorChoosableMushiInfo(): 能力や術、強化カードによって選択可能な、自プレイヤーの場の虫を表示する。
            PlayMushi(): 虫カードをプレイする。
            PlayJutsu(): 術カードをプレイする。対象選択が必要な術なら対象選択を行わせる。
            PlayKyoka(): 強化カードをプレイする。自プレイヤーの虫から対象選択を行わせる。
            AttackMushi(): 入力された番号に対応した場の虫が攻撃可能かどうかを判定する。
            AttackMushiChoice(): 虫の攻撃対象を選択し、攻撃を行う。
            TurnStart(): プレイヤーのターン中の行動を処理する。
            TurnEnd(): プレイヤーのターン終了時の処理を行う（つもり）。
            PlayerDamage(): プレイヤーへのダメージの処理を行う。
            Lose(): 敗北処理を行う。
    
    """

    def __init__(self, Name: str, Deck: list[Card]) -> None:
        self.__Deck         = Deck.copy()   # 山札
        self.__BattleZone   = []            # 場
        self.__Nawabari     = []            # 縄張り
        self.__Hands        = []            # 手札
        self.__Bochi        = []            # 墓地
        self.__Esaba        = []            # エサ場
        
        self.EnemyPlayer    = None
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
        
        self.ShowMyInfo()

    def PrintCards(self, Cards: list[Card], AddNum: int=0, UraShow: bool=True, MushiShow: bool=False) -> None:
        """
        通し番号付きでCardsの情報を表示する。

        Args:
            Cards (list[Card]): 表示するカードのリスト。
            AddNum (int, optional): 表示するカードの通し番号に加算する値。デフォルトは0。
            UraShow (bool, optional): 裏向きのカードを表示するかどうか。デフォルトはTrue。
            MushiShow (bool, optional): 攻撃可能なカードのみを表示するかどうか。デフォルトはFalse。

        """
        IsBlocker = False
        if MushiShow:
            for Card in Cards:
                if isinstance(Card, Mushi):
                    if (not Card.Ura) and Card.Blocker:
                        IsBlocker = True
                        break

        for i in range(len(Cards)):
            Card = Cards[i]
            if isinstance(Card, Mushi):
                if MushiShow and ((not Card.Blocker and IsBlocker) or (Card.Gitai)):
                    continue
            if Card.Ura:
                if UraShow:
                    print(str(i+AddNum) + ": ???")
            else:
                message = str(i+AddNum) + ": " + Card.Name + "\tC:" + str(Card.Cost)
                if MushiShow:
                    message += "\t"+str(Card.HP_result)+"\t"+Card.Color
                print(message)

    def ShowMyInfo(self) -> None:
        print(self.Name)
        print("場　　: ")
        self.PrintCards(self.__BattleZone, 20)
        print("手札　: ")
        self.PrintCards(self.__Hands)
        print("縄張り: " + str(len(self.__Nawabari)))
        print("山札　: " + str(len(self.__Deck)))
        print("コスト: " + str(self.Costs) + " / " + str(len(self.__Esaba)))
        print()

    def _ShowEnemyPlayerInfo(self, MushiShow: bool = False) -> None:
        # ShowEnemyPlayerInfo()及びShowEnemyAttackableMushiInfo()実装用の仮メソッド
        print(self.EnemyPlayer.Name)
        print("場　　: ")
        self.PrintCards(self.EnemyPlayer.__BattleZone, UraShow=False, MushiShow=MushiShow)
        print(f"手札　: {len(self.EnemyPlayer.__Hands)}")
        print(f"縄張り: {len(self.EnemyPlayer.__Nawabari)}")
        print(f"山札　: {len(self.EnemyPlayer.__Deck)}")
        print(f"コスト: {self.EnemyPlayer.Costs} / {len(self.EnemyPlayer.__Esaba)}")
        print()

    def ShowEnemyPlayerInfo(self) -> None:
        self._ShowEnemyPlayerInfo(MushiShow=False)

    def ShowEnemyAttackableMushiInfo(self) -> None:
        self._ShowEnemyPlayerInfo(MushiShow=True)

    def ShowChoosableMushiInfo(self) -> None:
        self.PrintCards(self.__BattleZone, UraShow=False)

    def ShowNawabariInfo(self) -> None:
        print(self.Name + "\n縄張り:")
        self.PrintCards(self.__Nawabari)

    def EnemyPlayerRefresh(self, EnemyPlayer: 'Player') -> None:
        self.EnemyPlayer = EnemyPlayer
    
    def BattleZoneRefresh(self) -> None:
        for MyMushi in self.__BattleZone:
            MyMushi.Refresh()
    
    def GetBZLen(self) -> int:
        return len(self.__BattleZone)
    
    def ShuffleDeck(self) -> None:
        random.shuffle(self.__Deck)
        # self.PrintCards(self.__Deck)

    def CntCost(self) -> int:
        self.Costs = len(self.__Esaba)
        return self.Costs

    def Draw(self) -> Card:
        drawed = self.__Deck.pop(0)
        self.__Hands.append(drawed)
        return drawed

    def PutCost(self, Num: int) -> None:
        put = self.__Hands.pop(Num)
        self.__Esaba.append(put)
        print("\n" + put.Name + " をエサ場にセットしました\n")

    def CostSelectAndPut(self) -> None:
        select_num = IntInputLoop("餌に置くカードを選んでください（置かないなら-1）: ", len(self.__Hands)-1, -1)
        if select_num != -1:
            self.PutCost(select_num)

    def PlayMushi(self, Mushi: Mushi) -> None:
        self.__BattleZone.append(Mushi)

    def PlayJutsu(self, Jutsu: 'Jutsu') -> None:
        if Jutsu.Choosable:
            self.ShowEnemyPlayerInfo()
            select_mushi = IntInputLoop("対象を選んでください（キャンセルする場合は-1）: ", self.EnemyPlayer.GetBZLen()-1, -1)
            if select_mushi == -1:
                return
            if Jutsu.Play(self.EnemyPlayer.__BattleZone[select_mushi]):
                self.EnemyPlayer.BrokeMushi(select_mushi, False)
        else:
            Jutsu.Play()
            
        if Jutsu.Charge:
            self.__Esaba.append(Jutsu)
        else:
            self.__Bochi.append(Jutsu)

    def PlayKyoka(self, Kyoka: 'Kyoka') -> None:
        self.ShowChoosableMushiInfo()
        select_mushi = IntInputLoop("対象を選んでください: ", self.GetBZLen()-1)
        self.__BattleZone[select_mushi].Kyokas.append(Kyoka)
        
        if Kyoka.Buffer:
            self.__BattleZone[select_mushi].DirectHPBuff(Kyoka.Bufflist[0])

    def Play(self, Num:int) -> None:
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
            if self.PlayJutsu(p_card) == 0:
                self.__Hands.append(p_card)
        elif issubclass(type(p_card), Kyoka):
            if self.GetBZLen() != 0:
                self.PlayKyoka(p_card)
            else:
                print("強化対象が存在しません\n")
                self.__Hands.append(p_card)
                return
        else:
            print("不明なカードです\n")
            return
        
        print("\n" + p_card.Name + " をプレイしました\n")

    def AttackMushi(self, Num:int) -> None:
        mushi = self.__BattleZone[Num]
        if mushi.Tap:
            print("\n攻撃済みです\n")
        else:
            self.AttackMushiChoice(mushi)

    def AttackMushiChoice(self, Mushi: Mushi) -> None:
        print("\n" + Mushi.Name)
        self.ShowMushiWaza(Mushi)
        select_attack = IntInputLoop("使用する攻撃を選んでください（攻撃しない場合は-1）: ", len(Mushi.AttackList)-1, -1)
        
        if select_attack == -1:
            return
        if len(self.EnemyPlayer.__BattleZone) > 0:
            self.ShowEnemyAttackableMushiInfo()
            select_mushi = IntInputLoop("対象を選んでください（キャンセルする場合は-1）: ", self.EnemyPlayer.GetBZLen()-1, -1)
            if select_mushi == -1:
                return
            self.AttackMushiExecute(Mushi, select_attack, self.EnemyPlayer.__BattleZone[select_mushi])
        else:
            self.AttackMushiExecute(Mushi, select_attack, self.EnemyPlayer)

    def ShowMushiWaza(self, Mushi: Mushi) -> None:
        print("攻撃: ")
        for Attack in range(len(Mushi.AttackList)):
            print(str(Attack) + ": " + Mushi.AttackList[Attack]['name'] + " " + str(Mushi.AttackList[Attack]['damage']) + " (+" + str(Mushi.Attack_result) + ")")

    def AttackMushiExecute(self, Mushi: Mushi, select_attack: int, Target: Union[Mushi, 'Player']):
        if Mushi.AttackList[select_attack]['method'](Target, Mushi.AttackList[select_attack]['damage'], Mushi.Color):
            if isinstance(Target, Mushi):
                self.EnemyPlayer.BrokeMushi(self.EnemyPlayer.__BattleZone.index(Target), True)

    def PlayerActionLoop(self) -> None:
        while not (self.GameSet or self.EnemyPlayer.GameSet):
            self.ShowEnemyPlayerInfo()
            self.ShowMyInfo()
            select_num = int(input("プレイするカードを選択してください（ターンエンドは-1）: "))
            print("\n====================================================================\n")
            if select_num != -1:
                if (select_num-20) < 0:
                    self.Play(select_num)
                elif (select_num-40) < 0:
                    self.AttackMushi(select_num-20)
            else:
                return

    def TurnStart(self, EnemyPlayer: 'Player') -> None:
        self.EnemyPlayerRefresh(EnemyPlayer)
        
        if self.GameSet or self.EnemyPlayer.GameSet:
            return
        
        self.BattleZoneRefresh()
        
        self.Draw()
        self.CntCost()
        
        self.ShowEnemyPlayerInfo()
        self.ShowMyInfo()
        
        self.CostSelectAndPut()
        self.CntCost()
        
        self.PlayerActionLoop()
        
        self.TurnEnd()

    def TurnEnd(self) -> None:
        pass

    def BrokeMushi(self, MushiNum: int, Direct: bool) -> None:
        self.__Bochi.append(self.__BattleZone.pop(MushiNum))
        if Direct:
            self.PlayerDamage(False)

    def IsTobidasuInBattleZone(self) -> bool:
        return any(mushi.Tobidasu for mushi in self.__BattleZone)

    def HasTobidasuCheck(self, draw_nawabari: Card) -> bool:
        if issubclass(type(draw_nawabari), Mushi):
            if draw_nawabari.Tobidasu:
                print(draw_nawabari.Name + "は＜とびだす＞を持っている！場に出しますか？\n\n0: 場に出さない\n1: 場に出す")
                play_tobidasu = IntInputLoop("入力: ", 1)
                return bool(play_tobidasu)
        return False

    def DrawNawabariChoice(self) -> Card:
        select_num = IntInputLoop("引く縄張りを選んでください: ", len(self.__Nawabari)-1)
        draw_nawabari = self.DrawNawabari(select_num)
        print(draw_nawabari.Name + "を引きました")
        return draw_nawabari

    def DrawNawabari(self, select_num: int) -> Card:
        draw_nawabari = self.__Nawabari.pop(select_num)
        draw_nawabari.Ura = False
        return draw_nawabari

    def PlayerDamage(self, Direct: bool) -> None:
        if Direct:
            print(self.Name + " への直接攻撃！！")
            
        if len(self.__Nawabari) > 0:
            print(self.Name + " の縄張りが1枚破壊された！\n")
            self.ShowNawabariInfo()
            
            draw_nawabari = self.DrawNawabariChoice()
            
            if self.IsTobidasuInBattleZone():
                self.__Hands.append(draw_nawabari)
            elif self.HasTobidasuCheck(draw_nawabari):
                self.PlayMushi(draw_nawabari)
                print(draw_nawabari.Name + "がとびだした！\n")
            else:
                self.__Hands.append(draw_nawabari)

        elif Direct:
            self.Lose()
            
        else:
            print(self.Name + "は縄張りがないので縄張りを引かなかった！")

    def Lose(self) -> None:
        print("\nゲームセット！！" + self.EnemyPlayer.Name + " の勝ち！")
        self.GameSet = True