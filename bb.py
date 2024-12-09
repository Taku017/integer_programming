from turtle import left
from types import new_class
from linear_relaxation import SimplexTable
import numpy as np
import time


'''
#例題
obj=np.array([-3, -4, -5, -6])  #最大化を考えるので―1倍
e_left=np.array([[2,3,4,5],
                [1,0,0,0],
                [0,1,0,0],
                [0,0,1,0],
                [0,0,0,1]])
e_right=np.array([6,1,1,1,1])
e_compare=['Less','Less','Less','Less','Less']
'''


'''
#巡回する問題
obj=np.array([-16, -19, -23, -28])  #最大化を考えるので―1倍
e_left=np.array([[2,3,4,5],#ここが重みの制約
                [1,0,0,0],
                [0,1,0,0],
                [0,0,1,0],
                [0,0,0,1]])
e_right=np.array([7,1,1,1,1])#一つ目の要素が重みの上限
e_compare=['Less','Less','Less','Less','Less']
'''



'''
obj=np.array([-21])  #最大化を考えるので―1倍
e_left=np.array([[6]])
e_right=np.array([4])#一つ目の要素が重みの上限
e_compare=['Less']



v_cnt=len(obj) #変数の数は目的関数の変数とする
a_cnt=0 #人為変数の数の初期化
s_cnt=0 #スラック変数の数の初期化

#それぞれ変数の数を決める
for cmp in e_compare:
    if cmp=="Greater":
        a_cnt+=1
        s_cnt+=1
    if cmp=="Equal":
        a_cnt+=1
    if cmp=="Less":
        s_cnt+=1


start=time.time()
simplex_table = SimplexTable( obj=obj, e_left=e_left, e_right=e_right, e_compare=e_compare)
relax_variable,relax_solution=simplex_table.start_end()

finish=time.time()


print(relax_variable,relax_solution)


jikan=finish-start
print("\nTime:"+str(jikan))
'''



'''ここからナップザック問題'''
class Knapsack:
    def __init__(self,bb_obj,bb_left,bb_right,bb_compare):
        self.bb_obj=bb_obj
        self.bb_left=bb_left
        self.bb_right=bb_right
        self.bb_compare=bb_compare
        self.tentative_sol=0#暫定解があるとき1にする
        self.z_ten=-1#暫定解の値を-1で初期化(最適解が0だった場合に備え0を避ける)
        self.x_ten= np.zeros(len(bb_obj))#暫定解の変数リストを0に初期化
        self.n=len(bb_obj)
        self.L=[]#考えるノードを入れておく

        obj_constant_term=0#目的関数の定数項を保存する変数

        #分枝の階層、目的関数、制約条件を辞書として入れ初期化。階層0では元の制約条件のままで分枝して階層が増え変数が決まったらそのたびにobj,制約を書き換える
        self.L.append({'level': 0, 'obj': self.bb_obj, 'R': self.bb_right ,'L': self.bb_left ,'cmp': self.bb_compare,'obj_constant_term':obj_constant_term})

    def knapsak_start_to_end(self):
        
        print(self.L)
 
        if len(self.L)==0:#Lに考えるべきノードでの問題が入っていなければ終了
            print("end.")
            return
        

        self.L = sorted(self.L, key=lambda x: x['level'], reverse=True)#Lを階層(level)でソートする(このコードは深さ優先探索としたいため)

        P=self.L[0]#今考える問題を取り出す
        print(P)
        del self.L[0]#取り出した問題は消す
        print(self.L)
        
        '''LP緩和'''
        if P['R'][0]>=0:#LP緩和が実行可能のとき
            simplex_table = SimplexTable( obj=P['obj'], e_left=P['L'], e_right=P['R'], e_compare=P['cmp'])
            relax_variable,relax_solution=simplex_table.start_end()
#        print(relax_variable,relax_solution)
            


        '''分枝限定操作'''
        if relax_solution+P['obj_constant_term']>self.tentative_sol:#elseのときは部分問題をLに入れずそれ以下のノードが考えられないため限定操作になる。
            obj0=P['obj'][0]#いまから0と1に固定する変数の係数（目的関数の）
            left0=P['L'][0][0]#いまから0と1に固定する変数の係数（制約条件の）
            lev=P['level']+1#階層を今の階層+1とする
            print(obj0,left0)
            new_right=np.delete(P['R'], 1)
            R_copy=new_right
            print(P['R'],R_copy,new_right)
            
            if len(P['obj']) > 0:
                P['obj'] = np.delete(P['obj'], 0)
            if len(P['L']) > 0:
                P['L'] = np.delete(P['L'],0,axis=1) #決まった変数の列を制約から消す（axis=1は列） 
                P['L'] = np.delete(P['L'], 1, axis=0)  # axis=0で第1行を削除。制約が決まると制約が一つ意味をなさなくなるため消す
            if len(P['cmp']) > 0:
                del P['cmp'][1]#一つ制約が不要になるため消去

            
            for i in range(2):#0と1の二回    
                print(i)
                obj_con=P['obj_constant_term']+-1*i*obj0#変数が固定されたことで定数項になった分を保存
                R_copy[0]=new_right[0]+left0*i*-1#左辺の係数が（変数が整数に決まったことにより）右辺に足される
                print(left0*i*-1)
                print(R_copy)
                self.L.append({'level': lev, 'obj': P['obj'], 'R': R_copy,'L': P['L'] ,'cmp': P['cmp'],'obj_constant_term':obj_con})#二回分枝した分の部分問題をLに挿入
                
            
            print(self.L[0])
            print("\n")
            print(self.L[1])


        return






obj=np.array([-16, -19, -23, -28])  #最大化を考えるので―1倍
e_left=np.array([[2,3,4,5],#ここが重みの制約
                [1,0,0,0],
                [0,1,0,0],#ここの0と1で表された制約はLP緩和に使う
                [0,0,1,0],
                [0,0,0,1]])
e_right=np.array([7,1,1,1,1])#一つ目が重みの上限
e_compare=['Less','Less','Less','Less','Less']


start=time.time()
knapsack = Knapsack( bb_obj=obj, bb_left=e_left, bb_right=e_right,bb_compare=e_compare)
knapsack.knapsak_start_to_end()
