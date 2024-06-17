#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import List
from abc import ABC,abstractmethod

WeakDic = {'Red':'Blue', 'Blue':'Green', 'Green':'Red'}

class Card(ABC):
    def __init__(self, Owner:'Player', Name:str, ID:str, Cost:int):
        self.Name   = Name
        self.ID     = ID
        self.Cost   = Cost
        self.Ura    = False
        self.Charge = False
        self.Owner  = Owner
    
    @abstractmethod
    def Play(self):
        pass

# 術カード実装

class Jutsu(Card):
    def __init__(self, Owner:'Player', Name:str, ID:str, Cost:int):
        super().__init__(Owner, Name, ID, Cost)
        self.Choosable = False
        
    def Play(self):
        pass

class IbukiOfMushi(Jutsu):
    def __init__(self, Owner:'Player'):
        super().__init__(Owner, "蟲の息吹", "MUSHI 127/130", 1)
        self.Charge = True

    def Play(self):
        self.Owner.MoveCard(self, self.Owner.__Hands, self.Owner.__Esaba)

class Bakunetsu(Jutsu):
    def __init__(self, Owner:'Player'):
        super().__init__(Owner, "塵芥虫の爆熱弾", "MUSHI 124/130", 1)

    def Play(self):
        self.Owner.Opp.PrintBattleZone(HideUra=True)

# 強化カード実装

class Kyoka(Card):
    def __init__(self, Owner:'Player', Name:str, ID:str, Cost:int):
        super().__init__(Owner, Name, ID, Cost)
        self.Buffer = False
        self.BuffList = []
    
    def Play(self):
        pass

class MinoKaku(Kyoka):
    def __init__(self, Owner:'Player'):
        super().__init__(Owner, "蓑虫の隠れ蓑", "MUSHI 106/130", 0)
        self.Buffer = True
        self.BuffList = [500,0]

    def Play(self):
        pass

# 蟲カード実装

class Mushi(Card):
    def __init__(self, Owner:'Player', Name:str, ID:str, Cost:int, HP:int, Color:str):
        super().__init__(Owner, Name, ID, Cost)
        self.HP         = HP
        self.Color      = Color
        self.Kyokas     = []
        self.AtkList    = []
        self.HPBuff     = 0
        self.AtkBuff    = 0
        self.Blocker    = False
        self.Gitai      = False
        self.Refresh()
        
    def Refresh(self):
        for kyoka in self.Kyokas:
            if kyoka.Buffer:
                self.HPBuff += kyoka.BuffList[0]
                self.AtkBuff += kyoka.BuffList[1]
        
        self.HP_result  = self.HP + self.HPBuff
        self.Atk_result = self.AtkBuff
        self.HPBuff     = 0
        self.AtkBuff    = 0
        self.Tap        = False
        self.Ura        = False
        self.Gitai      = False
           
    def DirectHPBuff(self, BuffNum:int):
        print(self.Name + " のHPが " + str(BuffNum) + " 増えた")
        self.HP_result += BuffNum
    
    def Damage(self, Damage_i:int, Color:str):
        dam_result = Damage_i*2 if WeakDic.get(self.Color) == Color else Damage_i
        self.HP_result -= dam_result
        print("\n" + self.Name + " に " + str(dam_result) + " のダメージ！！")
        if self.HP_result <= 0:
            print(self.Name + " は破壊された\n")
            self._Broke()
            return True
        else:
            print(self.Name + " の残り体力: " + str(self.HP_result) + "\n")
            return False
    
    def _Broke(self):
        pass
    
    def _SimpleAtk(self, Target, Damage_i:int, Color:str):
        self.Tap = True
        if issubclass(type(Target), Mushi):
            return Target.Damage(Damage_i+self.Atk_result, Color)
        else:
            Target.P_Damage(True)
            return False
    
    def _BuffAtk(self, Target, DamageAndBuff:List[int], Color:str):
        self.Tap = True
        if issubclass(type(Target), Mushi):
            r = Target.Damage(DamageAndBuff[0]+self.Atk_result, Color)
        else:
            Target.P_Damage(True)
            r = False
            
        self.HPBuff  += DamageAndBuff[1]
        self.AtkBuff += DamageAndBuff[2]
        
        return r
           
    def _EnUraAtk(self, Target, Damage_i:int, Color:str):
        self.Tap = True
        if issubclass(type(Target), Mushi):
            print("enura true")
            Target.Ura = True
        else:
            Target.P_Damage(True)
            
        return False
            
    def Play(self):
        self.Owner.MoveCard(self)
            
class SampleM(Mushi):
    def __init__(self, Owner:'Player'):
        super().__init__(Owner, "サンプルムシ", "0", 1, 100, 'Red')
        self.AtkList = [{'method':self._SimpleAtk, 'name':"シンプルに攻撃", 'damage':100}, 
                        {'method':self._BuffAtk, 'name':"シンプルに強化", 'damage':[0,0,100]}]
    
    def _SimpleAtk(self, Target, Damage_i:int, Color:str):
        return super()._SimpleAtk(Target, Damage_i, Color)
        
    def _BuffAtk(self, Target, DamageAndBuff:List[int], Color:str):
        return super()._BuffAtk(Target, DamageAndBuff, Color)
    
    def Play(self):
        super().Play()

class GinYanma(Mushi):
    def __init__(self, Owner:'Player'):
        super().__init__(Owner, "ギンヤンマ", "MUSHI 6/130", 5, 1100, 'Red')
        self.AtkList = [{'method':self._SimpleAtk, 'name':"とびかかる", 'damage':700}]
    
    def _SimpleAtk(self, Target, Damage_i:int, Color:str):
        return super()._SimpleAtk(Target, Damage_i, Color)
    
    def Play(self):
        super().Play()

class KooniYanma(Mushi):
    def __init__(self, Owner:'Player'):
        super().__init__(Owner, "コオニヤンマ", "MUSHI 11/130", 4, 800, 'Red')
        self.AtkList = [{'method':self._SimpleAtk, 'name':"とびかかる", 'damage':500}]
    
    def _SimpleAtk(self, Target, Damage_i:int, Color:str):
        return super()._SimpleAtk(Target, Damage_i, Color)
    
    def Play(self):
        super().Play()

class Akiakane(Mushi):
    def __init__(self, Owner:'Player'):
        super().__init__(Owner, "アキアカネ", "MUSHI 24/130", 2, 500, 'Red')
        self.AtkList = [{'method':self._SimpleAtk, 'name':"とびかかる", 'damage':200}]
    
    def _SimpleAtk(self, Target, Damage_i:int, Color:str):
        return super()._SimpleAtk(Target, Damage_i, Color)
    
    def Play(self):
        super().Play()

class NamiTentou(Mushi):
    def __init__(self, Owner:'Player'):
        super().__init__(Owner, "ナミテントウ", "MUSHI 30/130", 1, 300, 'Red')
        self.AtkList = [{'method':self._SimpleAtk, 'name':"かみつぶす", 'damage':100}]
    
    def _SimpleAtk(self, Target, Damage_i:int, Color:str):
        return super()._SimpleAtk(Target, Damage_i, Color)
    
    def Play(self):
        super().Play()

class KabutoMushi(Mushi):
    def __init__(self, Owner:'Player'):
        super().__init__(Owner, "カブトムシ", "MUSHI 40/130", 4, 800, 'Blue')
        self.AtkList = [{'method':self._SimpleAtk, 'name':"ツノ突進", 'damage':500},
                        {'method':self._EnUraAtk, 'name':"すくい投げ", 'damage':0}]
    
    def _SimpleAtk(self, Target, Damage_i:int, Color:str):
        return super()._SimpleAtk(Target, Damage_i, Color)
        
    def _EnUraAtk(self, Target, Damage_i:int, Color:str):
        return super()._EnUraAtk(Target, Damage_i, Color)
    
    def Play(self):
        super().Play()

class NamiAgeha(Mushi):
    def __init__(self, Owner:'Player'):
        super().__init__(Owner, "ナミアゲハ", "MUSHI 44/130", 4, 1100, 'Blue')
        self.AtkList = [{'method':self._SimpleAtk, 'name':"すいつくす", 'damage':300}]
        self.Blocker = True
        
    def Refresh(self):
        super().Refresh()
    
    def _SimpleAtk(self, Target, Damage_i:int, Color:str):
        return super()._SimpleAtk(Target, Damage_i, Color)
        
    def Play(self):
        super().Play()

class Kanaboon(Mushi):
    def __init__(self, Owner:'Player'):
        super().__init__(Owner, "カナブン", "MUSHI 63/130", 1, 300, 'Blue')
        self.AtkList = [{'method':self._SimpleAtk, 'name':"たいあたり", 'damage':100}]
    
    def _SimpleAtk(self, Target, Damage_i:int, Color:str):
        return super()._SimpleAtk(Target, Damage_i, Color)
    
    def Play(self):
        super().Play()

class Higurashi(Mushi):
    def __init__(self, Owner:'Player'):
        super().__init__(Owner, "ヒグラシ", "MUSHI 64/130", 2, 200, 'Blue')
        self.AtkList = [{'method':self._SimpleAtk, 'name':"しぼりとる", 'damage':200}]
    
    def _SimpleAtk(self, Target, Damage_i:int, Color:str):
        return super()._SimpleAtk(Target, Damage_i, Color)
    
    def Play(self):
        super().Play()

class TonosamaBatta(Mushi):
    def __init__(self, Owner:'Player'):
        super().__init__(Owner, "トノサマバッタ", "MUSHI 71/130", 5, 1200, 'Green')
        self.AtkList = [{'method':self._SimpleAtk, 'name':"くらいつく", 'damage':700}]
    
    def _SimpleAtk(self, Target, Damage_i:int, Color:str):
        return super()._SimpleAtk(Target, Damage_i, Color)
    
    def Play(self):
        super().Play()

class NijuyahoshiTentou(Mushi):
    def __init__(self, Owner:'Player'):
        super().__init__(Owner, "ニジュウヤホシテントウ", "MUSHI 91/130", 2, 300, 'Green')
        self.AtkList = [{'method':self._SimpleAtk, 'name':"かみつぶす", 'damage':300}]
    
    def _SimpleAtk(self, Target, Damage_i:int, Color:str):
        return super()._SimpleAtk(Target, Damage_i, Color)
    
    def Play(self):
        super().Play()

class WataAburaMushi(Mushi):
    def __init__(self, Owner:'Player'):
        super().__init__(Owner, "ワタアブラムシ", "MUSHI 91/130", 1, 300, 'Green')
        self.AtkList = [{'method':self._SimpleAtk, 'name':"とびかかる", 'damage':100}]
    
    def _SimpleAtk(self, Target, Damage_i:int, Color:str):
        return super()._SimpleAtk(Target, Damage_i, Color)
    
    def Play(self):
        super().Play()
