# coding: utf-8
import re
from operator import itemgetter

'''
攻撃：Attack(ATK)：
防御：Defense(DEF)
魔法攻撃：Magic Attack(MATK/MAT)
魔法防御：Magic Defense(MDEF/MDE)
敏捷性：Agility（AGI）
命中率：Dexterity（DEX）
回避率：Evasion（EVA）
クリティカル：Critical
'''

#キャラクターリスト
#["武器種","名前",攻撃力,武器スキル,チェイン数,バフ判定0なし:1あり:2中以下3:特殊,バフの値,デバフ判定,デバフの値,スキル数判定,スキル]
c_atk = [["片手剣","ステルク",2917+1731+780+50+650,4.5,7,3,1.45,0,1,1,1.2,1],
		 ["槍","アマリリス",3487+1731+1050+650,4.5,6,0,1,0,1,2,1.35,1.2],
		 ["槍","ミミ",3487+1731+1050+50+650,4.5,6,1,1.35,0,1,2,1.2,1.1],
		 ["片手剣","ネルケ",3431+1731+780+50+650,4.5,7,1,1.35,0,1,1,1.4,1],
		 ["メイス","メルル",3356+1731+705+650,4,7,3,1.35,0,1,0,1,1],
		 ["片手剣","ベルベイヌ",3333+1731+780+650,4.5,7,1,1.35,0,1,1,1.4,1],
		 ["片手剣","ロジー",3316+1731+780+650,4.5,7,0,1,0,1,1,1.4,1],
		 ["メイス","エスカ",3260+1731+705+50+650,4,7,1,1.45,0,1,1,1.2,1],
		 ["メイス","ソフィー",3500+1731+705+60+650,4,7,0,1,0,1,1,1.25,1],
		 ["メイス","ルルア",3273+1731+705+70+650,4,7,0,1,0,1,1,1.35,1],
		 ["片手剣","タンドリオン",4115+1731+780+50+650,4.5,7,1,1.4,0,1,0,1,1],
		 ["メイス","ベルガモット",2973+1731+705+650,4,7,1,1.4,0,1,1,1.15,1],
		 ["メイス","スール",3316+1731+705+120+650,4,7,0,1,0,1,1,1.2,1],
		 ["片手剣","鳳仙花梅",3144+1731+780+50+650,4.5,7,0,1,1,0.6,0,1,1],
		 ["メイス","マリー",3200+1731+705+50+650,4,7,1,1.4,0,1,0,1,1],
		 ["弓","キャットニップ",3029+1731+1050+650,4,6,0,1,0,1,1,1.25,1],
		 ["メイス","リディー",2229+1731+705+650,4,7,0,1,1,0.8,1,1.07,1],
		 ["片手剣","フォニク",3381+1731+780+650,4.5,7,0,1,0,1,0,1,1],
		 ["メイス","ヘーゼル",2173+1731+705+650,4,7,2,1.15,0,1,0,1,1],
		 ["メイス","ロロナ",2460+1731+705+650,4,7,0,1,0,1,0,1,1],
		 ["メイス","トトリ",2345+1731+705+650,4,7,0,1,0,1,0,1,1],
		 ["メイス","アーシャ",2345+1731+705+650,4,7,0,1,0,1,0,1,1],
		 ["片手剣","ラジアータ",2460+1731+780+650,4.5,7,0,1,0,1,1,1.25,1],
		 ["片手剣","リコリス",2572+1731+780+650,4.5,7,0,1,1,0.75,1,1.25,1],
		 ["片手剣","オーレル",3089+1731+780+650,4.5,7,0,1,0,1,1,1,1],
		]
#["武器種","名前",攻撃力,バフ判定,バフの値,デバフ判定,デバフの値,スキル数判定,スキル]
c_mat = [["杖","オーゼイユ",3210+1470+775+650,4,7,0,1,1,0.7,1,1.35,1],
		 ["杖","ウィルベル",3487+1470+775+50+650,4,7,0,1,0,1,2,1.25,1.1],
		 ["杖","マジョラム",3602+1470+775+50+650,4,7,1,1.4,0,1,1,1.2,1],
		 ["杖","鳳仙花春蘭",3316+1470+775+50+650,4,7,1,1.3,0,1,0,1,1],
		 ["杖","ライザ",3378+1470+775+50+650,4,7,1,1.3,0,1,0,1,1],
		 ["杖","大人ロロナ",3131+1470+775+650,4,7,0,1,0,1,0,1,1],
		 ["槍","アマリリス",1716+1731+1050+650,5,6,0,1,0,1,2,1.35,1.25]
		]

#print(c_atk)
#print(c_mat)

#ダメージ計算
#物理、魔法の判別
#new_atk = 攻撃力 * バフ
#new_deff = 防御力 * デバフ
#物理装備込み +1731
#魔法装備込み +1470
#basic_damage = (atk - deff) / 4
#final_damage = basic_damage * 4 * 3.908 * チェイン倍率 * スキル数X
#弓、槍の場合
#final_damage = basic_damage * 4 * 3.217 * チェイン倍率 * スキル数X

#ダメージランキングリスト
atk_rank = []
mat_rank = []
#汎用リスト
rank_list = []
#ダメージの格納
damage_float = []
#ソート後のリスト
s_mat_rank = []
s_atk_rank = []


#ダメージ計算クラス
class Damage():
	def __init__(self, weapon, name, atk, weapon_skill, chain_x, buff_judg, buff_val, debuff_judg, debuff_val, skill_judg, *skill_val):
		self.weapon = weapon
		self.name = name
		self.atk = atk
		self.weapon_skill = weapon_skill
		self.chain_x = chain_x
		self.buff_judg = buff_judg
		self.buff_val = buff_val
		self.debuff_judg = debuff_judg
		self.debuff_val = debuff_val
		self.skill_judg = skill_judg
		self.skill_val = skill_val
		
	def mat_final_damage(self):
		deff = 870 #敵の防御力
		#weapon_skill = 4 #武器スキル倍率
		shield_skill = 3 #盾スキル倍率
		final_damage_s = 0 #盾無し用
		skill_stren = 3.908 #スキル強化12^7
		chain = 0.2 #チェイン倍率
		drug = 1.3 #秘薬品質60
		
		#デバフ判定 1:あり 0:なし
		if self.debuff_judg > 0:
			deff *= self.debuff_val
		
		#バフ判定 1:あり 0:なし
		if self.buff_judg > 0:
			basic_damage = (self.atk * self.buff_val - deff) / 4
		else:
			#バフなし
			basic_damage = (self.atk - deff) / 4
			#秘薬バフ(品質60)
			basic_damage_d = (self.atk * drug - deff) / 4
			#秘薬バフ込みのダメージ
			final_damage = basic_damage_d * self.weapon_skill \
							* skill_stren * (1 + chain * self.chain_x) \
							* self.skill_val[0] * self.skill_val[1]			
			if self.chain_x > 6:
				#盾のダメージ
				final_damage_s = basic_damage_d * shield_skill \
								* skill_stren * (1 + chain * self.chain_x - 0.2) \
								* self.skill_val[0] * self.skill_val[1]
			rank_list = self.name + "(秘薬)【武器ダメージ : " + str((round(final_damage, 2))) + " 盾ダメージ : " + str((round(final_damage_s, 2))) + "】"
			mat_rank.append(rank_list)
			
		#通常のダメージ
		final_damage = basic_damage * self.weapon_skill \
					* skill_stren * (1 + chain * self.chain_x) \
					* self.skill_val[0] * self.skill_val[1]
		if self.chain_x > 6:
			#盾のダメージ
			final_damage_s = basic_damage * shield_skill \
								* skill_stren * (1 + chain * self.chain_x - 0.2) \
								* self.skill_val[0] * self.skill_val[1]
		rank_list = self.name + "【武器ダメージ : " + str((round(final_damage, 2))) + " 盾ダメージ : " + str((round(final_damage_s, 2))) + "】"
		mat_rank.append(rank_list)
		
	def atk_final_damage(self):
		deff = 870 #敵の防御力
		#weapon_skill = 4 #武器スキル倍率
		shield_skill = 3 #盾スキル倍率
		final_damage_s = 0 #盾無し用
		skill_stren = 3.908 #スキル強化12^7
		#skill_stren_b = 3.217 #スキル強化12^6
		chain = 0.2 #チェイン倍率
		#chain_b = 2 #チェイン倍率 6チェイン
		drug = 1.35 #秘薬品質60
		basic_damage0 = basic_damage1 = basic_damage_d = 0 #各バフに対応した変数
		
		#デバフ判定 1:あり 0:なし
		if self.debuff_judg > 0:
			deff *= self.debuff_val
			
		#バフ判定 1:あり 2:中以下 3:特殊 0:なし
		if self.buff_judg > 0:
			basic_damage1 = (self.atk * self.buff_val - deff) / 4
			
			final_damage = basic_damage1 * self.weapon_skill \
							* skill_stren * (1 + chain * self.chain_x) \
							* self.skill_val[0] * self.skill_val[1]
							
			if self.chain_x > 6:
				#盾のダメージ
				final_damage_s = basic_damage1 * shield_skill \
								* skill_stren * (1 + chain * self.chain_x - 0.2) \
								* self.skill_val[0] * self.skill_val[1]
								
			rank_list = self.name + "【武器ダメージ : " + str((round(final_damage, 2))) + " 盾ダメージ : " + str((round(final_damage_s, 2))) + "】"
			atk_rank.append(rank_list)
			
			#秘薬込み
			if self.buff_judg > 1:
				basic_damage_d = (self.atk * self.buff_val * drug - deff) / 4
				
				final_damage = basic_damage_d * self.weapon_skill \
								* skill_stren * (1 + chain * self.chain_x) \
								* self.skill_val[0] * self.skill_val[1]
				
				if self.chain_x > 6:
					#盾のダメージ
					final_damage_s = basic_damage_d * shield_skill \
									* skill_stren * (1 + chain * self.chain_x - 0.2) \
									* self.skill_val[0] * self.skill_val[1]
								
				rank_list = self.name + "(秘薬)【武器ダメージ : " + str((round(final_damage, 2))) + " 盾ダメージ : " + str((round(final_damage_s, 2))) + "】"
				atk_rank.append(rank_list)
				
		else:
			basic_damage0 = (self.atk - deff) / 4
			#秘薬込み
			basic_damage_d = (self.atk * drug - deff) / 4
			
			final_damage = basic_damage0 * self.weapon_skill \
							* skill_stren * (1 + chain * self.chain_x) \
							* self.skill_val[0] * self.skill_val[1]
			
			if self.chain_x > 6:
					#盾のダメージ
					final_damage_s = basic_damage0 * shield_skill \
									* skill_stren * (1 + chain * self.chain_x - 0.2) \
									* self.skill_val[0] * self.skill_val[1]
			
			rank_list = self.name + "【武器ダメージ : " + str((round(final_damage, 2))) + " 盾ダメージ : " + str((round(final_damage_s, 2))) + "】"
			atk_rank.append(rank_list)
				
			final_damage = basic_damage_d * self.weapon_skill \
							* skill_stren * (1 + chain * self.chain_x) \
							* self.skill_val[0] * self.skill_val[1]
							
			if self.chain_x > 6:
					#盾のダメージ
					final_damage_s = basic_damage_d * shield_skill \
									* skill_stren * (1 + chain * self.chain_x - 0.2) \
									* self.skill_val[0] * self.skill_val[1]
			rank_list = self.name + "(秘薬)【武器ダメージ : " + str((round(final_damage, 2))) + " 盾ダメージ : " + str((round(final_damage_s, 2))) + "】"						
			atk_rank.append(rank_list)
		

#正規表現
p = re.compile(r"\d+")

#魔法キャラリスト
for c_mat_i in range(7):
	#risult = Damage("杖","ウィルベル",2826+775+50,0,1,0,1,2,1.31,1.1)
	#print(vars(risult))
	'''
	risult = Damage(c_mat[c_mat_i][0],c_mat[c_mat_i][1],c_mat[c_mat_i][2],
					c_mat[c_mat_i][3],c_mat[c_mat_i][4],c_mat[c_mat_i][5],
					c_mat[c_mat_i][6],c_mat[c_mat_i][7],c_mat[c_mat_i][8],
					c_mat[c_mat_i][9],c_mat[c_mat_i][10],c_mat[c_mat_i][11]
					)
	'''
	#c_mat[i][0~11]をまとめて展開
	risult = Damage(*c_mat[c_mat_i])
	risult.mat_final_damage()

#魔法キャラのダメージをソートして出力
#print(sorted(mat_rank, key=lambda x: x[0], reverse=True))
s_mat_rank = sorted(mat_rank, key=lambda x: int(p.search(x).group()), reverse=True)
print(s_mat_rank)

print("\n#####################\n")


#物理キャラリスト
for c_atk_i in range(25):
	risult = Damage(*c_atk[c_atk_i])
	risult.atk_final_damage()
	
#物理キャラのダメージをソートして出力
#print(sorted(atk_rank, key=itemgetter(0), reverse=True))
s_atk_rank = sorted(atk_rank, key=lambda x: int(p.search(x).group()), reverse=True)
print(s_atk_rank)

