#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import List
from abc import ABC,abstractmethod

WeakDic = {'Red':'Blue', 'Blue':'Green', 'Green':'Red'}

class Card(ABC):
    def __init__(self, Name:str, ID:str, Cost:int):
        self.Name   = Name
        self.ID     = ID
        self.Cost   = Cost
        self.Ura    = False
    
    @abstractmethod
    def Play(self):
        pass
        
class Jutsu(Card):
    def __init__(self, Name:str, ID:str, Cost:int):
        super().__init__(Name, ID, Cost)
        
    def Play(self):
        pass

class Kyoka(Card):
    def __init__(self, Name:str, ID:str, Cost:int):
        super().__init__(Name, ID, Cost)
    
    def Play(self):
        pass

class Mushi(Card):
    def __init__(self, Name:str, ID:str, Cost:int, HP:int, Color:str):
        super().__init__(Name, ID, Cost)
        self.HP         = HP
        self.Color      = Color
        self.Tap        = False
        self.Kyokas     = []
        self.AtkList    = []
        self.HPBuff     = 0
        self.AtkBuff    = 0
        self.HP_result  = 0
        self.Atk_result = 0
        
    def Refresh(self):
        self.HP_result  = self.HP + self.HPBuff
        self.Atk_result = self.AtkBuff
        self.HPBuff     = 0
        self.AtkBuff    = 0
        self.Tap        = False
        self.Ura        = False
           
    def Damage(self, Damage_i:int, Color:str):
        dam_result = Damage_i*2 if WeakDic.get(self.Color) == Color else Damage_i
        self.HP_result -= dam_result
        print("\n" + self.Name + " に " + str(dam_result) + " のダメージ")
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
            r = Target.Damage(Damage_i+self.Atk_result, Color)
        else:
            Target.P_Damage(True)
            r = False
            
        self.HPBuff  += DamageAndBuff[1]
        self.AtkBuff += DamageAndBuff[2]
        
        return r
           
    def _EnUraAtk(self, Target, Damage_i:int, Color:str):
        self.Tap = True
        if issubclass(type(Target), Mushi):
            Target.Ura = True
        else:
            Target.P_Damage(True)
            
        return False
            
    def Play(self):
        pass
            
class SampleM(Mushi):
    def __init__(self):
        super().__init__("サンプルムシ", "0", 1, 100, 'Red')
        self.AtkList = [{'method':self._SimpleAtk, 'name':"シンプルに攻撃", 'damage':100}, 
                        {'method':self._BuffAtk, 'name':"シンプルに強化", 'damage':[0,0,100]}]
    
    def _SimpleAtk(self, Target, Damage_i:int, Color:str):
        return super()._SimpleAtk(Target, Damage_i, Color)
        
    def _BuffAtk(self, Target, DamageAndBuff:List[int], Color:str):
        return super()._BuffAtk(Target, DamageAndBuff, Color)
    
    def Play(self):
        pass
        
class Ginyanma(Mushi):
    def __init__(self):
        super().__init__("ギンヤンマ", "0", 5, 1100, 'Red')
        self.AtkList = [{'method':self._SimpleAtk, 'name':"とびかかる", 'damage':700}]
    
    def _SimpleAtk(self, Target, Damage_i:int, Color:str):
        return super()._SimpleAtk(Target, Damage_i, Color)
    
    def Play(self):
        pass

class Kabutomushi(Mushi):
    def __init__(self):
        super().__init__("カブトムシ", "0", 4, 800, 'Blue')
        self.AtkList = [{'method':self._SimpleAtk, 'name':"ツノ突進", 'damage':500},
                        {'method':self._EnUraAtk, 'name':"すくい投げ", 'damage':0}]
    
    def _SimpleAtk(self, Target, Damage_i:int, Color:str):
        return super()._SimpleAtk(Target, Damage_i, Color)
        
    def _EnUraAtk(self, Target, Damage_i:int, Color:str):
        return super()._EnUraAtk(Target, Damage_i, Color)
    
    def Play(self):
        pass