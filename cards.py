#!/usr/bin/env python
# -*- coding: utf-8 -*-

from abc import ABC,abstractmethod

WeakDic = {'Red':'Blue', 'Blue':'Green', 'Green':'Red'}

class Card(ABC):
    def __init__(self, Name:str, ID:str, Cost:int):
        self.Name   = Name
        self.ID     = ID
        self.Cost   = Cost
        self.Ura    = False
        self.Charge = False
    
    @abstractmethod
    def Play(self):
        pass

class Jutsu(Card):
    def __init__(self, Name:str, ID:str, Cost:int):
        super().__init__(Name, ID, Cost)
        self.Choosable = False
        
    def Play(self):
        pass

class Kyoka(Card):
    def __init__(self, Name:str, ID:str, Cost:int):
        super().__init__(Name, ID, Cost)
        self.Buffer = False
        self.BuffList = []
    
    def Play(self):
        pass

class Mushi(Card):
    def __init__(self, Name:str, ID:str, Cost:int, HP:int, Color:str):
        super().__init__(Name, ID, Cost)
        self.HP         = HP
        self.Color      = Color
        self.Kyokas     = []
        self.AttackList    = []
        self.HPBuff     = 0
        self.AttackBuff    = 0
        self.Blocker    = False
        self.Gitai      = False
        self.Tobidasu   = False
        self.Refresh()
        
    def Refresh(self):
        for kyoka in self.Kyokas:
            if kyoka.Buffer:
                self.HPBuff += kyoka.BuffList[0]
                self.AttackBuff += kyoka.BuffList[1]
        
        self.HP_result  = self.HP + self.HPBuff
        self.Attack_result = self.AttackBuff
        self.HPBuff     = 0
        self.AttackBuff    = 0
        self.Tap        = False
        self.Ura        = False
        self.Gitai      = False
        
    def DirectHPBuff(self, BuffNum:int):
        print(self.Name + " のHPが " + str(BuffNum) + " 増えた")
        self.HP_result += BuffNum
    
    def Damage(self, Damage_i:int, Color:str):
        if Damage_i < 0:
            dam_result = 0
        else:
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
    
    def SimpleAttack(self, Target, Damage_i:int, Color:str):
        self.Tap = True
        if issubclass(type(Target), Mushi):
            return Target.Damage(Damage_i+self.Attack_result, Color)
        else:
            Target.PlayerDamage(True)
            return False
    
    def BuffAttack(self, Target, DamageAndBuff:list[int], Color:str):
        self.Tap = True
        if issubclass(type(Target), Mushi):
            r = Target.Damage(DamageAndBuff[0]+self.Attack_result, Color)
        else:
            Target.PlayerDamage(True)
            r = False
            
        self.HPBuff  += DamageAndBuff[1]
        self.AttackBuff += DamageAndBuff[2]
        
        return r
    
    def DebuffAttack(self, Target, DamageAndBuff:list[int], Color:str):
        self.Tap = True
        if issubclass(type(Target), Mushi):
            r = Target.Damage(DamageAndBuff[0] + self.Attack_result, Color)
            Target.HPBuff  -= DamageAndBuff[1]
            Target.AttackBuff -= DamageAndBuff[2]
        else:
            Target.PlayerDamage(True)
            r = False
        
        return r
        
    def EnemyUraAttack(self, Target, Damage_i:int, Color:str):
        self.Tap = True
        if issubclass(type(Target), Mushi):
            Target.Ura = True
        else:
            Target.PlayerDamage(True)
            
        return False
            
    def Play(self):
        pass

# 術カード実装
class IbukiOfMushi(Jutsu):
    def __init__(self):
        super().__init__("蟲の息吹", "MUSHI 127/130", 1)
        self.Charge = True

    def Play(self):
        pass

class Bakunetsu(Jutsu):
    def __init__(self):
        super().__init__("塵芥虫の爆熱弾", "", 1)
        self.Choosable = True
        
    def Play(self, Mushi: Mushi):
        return Mushi.Damage(600, None)

# 強化カード実装
class MinoKaku(Kyoka):
    def __init__(self):
        super().__init__("蓑虫の隠れ蓑", "MUSHI 106/130", 0)
        self.Buffer = True
        self.BuffList = [500,0]

    def Play(self):
        pass

# 蟲カード実装
class SampleM(Mushi):
    def __init__(self):
        super().__init__("サンプルムシ", "0", 1, 100, 'Red')
        self.AttackList = [{'method':self.SimpleAttack, 'name':"シンプルに攻撃", 'damage':100}, 
                        {'method':self.BuffAttack, 'name':"シンプルに強化", 'damage':[0,0,100]}]
    
    def SimpleAttack(self, Target, Damage_i:int, Color:str):
        return super().SimpleAttack(Target, Damage_i, Color)
        
    def BuffAttack(self, Target, DamageAndBuff:list[int], Color:str):
        return super().BuffAttack(Target, DamageAndBuff, Color)
    
    def Play(self):
        pass

class GinYanma(Mushi):
    def __init__(self):
        super().__init__("ギンヤンマ", "MUSHI 6/130", 5, 1100, 'Red')
        self.AttackList = [{'method':self.SimpleAttack, 'name':"とびかかる", 'damage':700}]
    
    def SimpleAttack(self, Target, Damage_i:int, Color:str):
        return super().SimpleAttack(Target, Damage_i, Color)
    
    def Play(self):
        pass

class KooniYanma(Mushi):
    def __init__(self):
        super().__init__("コオニヤンマ", "MUSHI 11/130", 4, 800, 'Red')
        self.AttackList = [{'method':self.SimpleAttack, 'name':"とびかかる", 'damage':500}]
    
    def SimpleAttack(self, Target, Damage_i:int, Color:str):
        return super().SimpleAttack(Target, Damage_i, Color)
    
    def Play(self):
        pass

class Akiakane(Mushi):
    def __init__(self):
        super().__init__("アキアカネ", "MUSHI 24/130", 2, 500, 'Red')
        self.AttackList = [{'method':self.SimpleAttack, 'name':"とびかかる", 'damage':200}]
    
    def SimpleAttack(self, Target, Damage_i:int, Color:str):
        return super().SimpleAttack(Target, Damage_i, Color)
    
    def Play(self):
        pass

class NamiTentou(Mushi):
    def __init__(self):
        super().__init__("ナミテントウ", "MUSHI 30/130", 1, 300, 'Red')
        self.AttackList = [{'method':self.SimpleAttack, 'name':"かみつぶす", 'damage':100}]
    
    def SimpleAttack(self, Target, Damage_i:int, Color:str):
        return super().SimpleAttack(Target, Damage_i, Color)
    
    def Play(self):
        pass

class KabutoMushi(Mushi):
    def __init__(self):
        super().__init__("カブトムシ", "MUSHI 40/130", 4, 800, 'Blue')
        self.AttackList = [{'method':self.SimpleAttack, 'name':"ツノ突進", 'damage':500},
                        {'method':self.EnemyUraAttack, 'name':"すくい投げ", 'damage':0}]
    
    def SimpleAttack(self, Target, Damage_i:int, Color:str):
        return super().SimpleAttack(Target, Damage_i, Color)
        
    def EnemyUraAttack(self, Target, Damage_i:int, Color:str):
        return super().EnemyUraAttack(Target, Damage_i, Color)
    
    def Play(self):
        pass

class NamiAgeha(Mushi):
    def __init__(self):
        super().__init__("ナミアゲハ", "MUSHI 44/130", 4, 1100, 'Blue')
        self.AttackList = [{'method':self.SimpleAttack, 'name':"すいつくす", 'damage':300}]
        self.Blocker = True
        
    def Refresh(self):
        super().Refresh()
    
    def SimpleAttack(self, Target, Damage_i:int, Color:str):
        return super().SimpleAttack(Target, Damage_i, Color)
        
    def Play(self):
        pass

class MinZemi(Mushi):
    def __init__(self):
        super().__init__("ミンミンゼミ", "MUSHI 47/130", 3, 500, 'Blue')
        self.AttackList = [{'method':self.SimpleAttack, 'name':"しぼりとる", 'damage':200}]
        self.Tobidasu = True
        
    def Refresh(self):
        super().Refresh()
    
    def SimpleAttack(self, Target, Damage_i:int, Color:str):
        return super().SimpleAttack(Target, Damage_i, Color)
        
    def Play(self):
        pass

class Kanaboon(Mushi):
    def __init__(self):
        super().__init__("カナブン", "MUSHI 63/130", 1, 300, 'Blue')
        self.AttackList = [{'method':self.SimpleAttack, 'name':"たいあたり", 'damage':100}]
    
    def SimpleAttack(self, Target, Damage_i:int, Color:str):
        return super().SimpleAttack(Target, Damage_i, Color)
    
    def Play(self):
        pass

class Higurashi(Mushi):
    def __init__(self):
        super().__init__("ヒグラシ", "MUSHI 64/130", 2, 200, 'Blue')
        self.AttackList = [{'method':self.SimpleAttack, 'name':"しぼりとる", 'damage':200}]
    
    def SimpleAttack(self, Target, Damage_i:int, Color:str):
        return super().SimpleAttack(Target, Damage_i, Color)
    
    def Play(self):
        pass

class TonosamaBatta(Mushi):
    def __init__(self):
        super().__init__("トノサマバッタ", "MUSHI 71/130", 5, 1200, 'Green')
        self.AttackList = [{'method':self.SimpleAttack, 'name':"くらいつく", 'damage':700}]
    
    def SimpleAttack(self, Target, Damage_i:int, Color:str):
        return super().SimpleAttack(Target, Damage_i, Color)
    
    def Play(self):
        pass

class NamiYou(Mushi):
    def __init__(self):
        super().__init__("ナミアゲハ（幼虫）", "MUSHI 79/130", 3, 700, 'Green')
        self.AttackList = [{'method':self.SimpleAttack, 'name':"かじる", 'damage':200},
                        {'method':self.DebuffAttack, 'name':"くさいツノ", 'damage':[0,0,400]}]
        
    def Refresh(self):
        super().Refresh()
    
    def SimpleAttack(self, Target, Damage_i:int, Color:str):
        return super().SimpleAttack(Target, Damage_i, Color)

    def DebuffAttack(self, Target, DamageAndBuff:list[int], Color:str):
        return super().DebuffAttack(Target, DamageAndBuff, Color)
        
    def Play(self):
        pass

class NanaModo(Mushi):
    def __init__(self):
        super().__init__("ナナフシモドキ", "MUSHI 80/130", 3, 400, 'Green')
        self.AttackList = [{'method':self.SimpleAttack, 'name':"かぶりつく", 'damage':400}]
        self.Gitai = True
        
    def Refresh(self):
        super().Refresh()
    
    def SimpleAttack(self, Target, Damage_i:int, Color:str):
        return super().SimpleAttack(Target, Damage_i, Color)
        
    def Play(self):
        pass

class NijuyahoshiTentou(Mushi):
    def __init__(self):
        super().__init__("ニジュウヤホシテントウ", "MUSHI 91/130", 2, 300, 'Green')
        self.AttackList = [{'method':self.SimpleAttack, 'name':"かみつぶす", 'damage':300}]
    
    def SimpleAttack(self, Target, Damage_i:int, Color:str):
        return super().SimpleAttack(Target, Damage_i, Color)
    
    def Play(self):
        pass

class WataAburaMushi(Mushi):
    def __init__(self):
        super().__init__("ワタアブラムシ", "MUSHI 95/130", 1, 300, 'Green')
        self.AttackList = [{'method':self.SimpleAttack, 'name':"とびかかる", 'damage':100}]
    
    def SimpleAttack(self, Target, Damage_i:int, Color:str):
        return super().SimpleAttack(Target, Damage_i, Color)
    
    def Play(self):
        pass
