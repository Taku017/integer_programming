from turtle import left
from types import new_class
from linear_relaxation import SimplexTable
import numpy as np
import time
import copy


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
    def __init__(self,bb_obj,bb_left,bb_right,bb_compare,maximum_integer_range,):
        self.bb_obj=bb_obj
        self.bb_left=bb_left
        self.bb_right=bb_right
        self.bb_compare=bb_compare
        self.tentative_sol=0#暫定解があるとき1にする
        self.z_ten=-1#暫定解の値を-1で初期化(最適解が0だった場合に備え0を避ける)
        self.x_ten= np.zeros(len(bb_obj))#暫定解の変数リストを0に初期化
        self.n=len(bb_obj)
        self.L=[]#考えるノードを入れておく
        self.items=[]#各分枝で整数に固定された変数を挿入していくリスト
        obj_constant_term=0#目的関数の定数項を保存する変数
        self.maximum_integer_range=maximum_integer_range#整数の取りうる最大
        #self.q=q#準最適解許容率
        #self.solution_pool=[]


        #分枝の階層、目的関数、制約条件を辞書として入れ初期化。階層0では元の制約条件のままで分枝して階層が増え変数が決まったらそのたびにobj,制約を書き換える
        self.L.append({'level': 0, 'obj': self.bb_obj, 'R': self.bb_right ,'L': self.bb_left ,'cmp': self.bb_compare,'obj_constant_term':obj_constant_term,'items':self.items})

    def knapsak_start_to_end(self):
        
        #print(self.L)
 

        
        while self.L!=0 :
            
            if len(self.L)==0:#Lに考えるべきノードでの問題が入っていなければ終了
                print("\nFinished.\n")
                print("The optomal solution :")
                print(self.x_ten,self.z_ten)
                return

            self.L = sorted(self.L, key=lambda x: x['R'][0])#各変数1を先に探索する場合   
            self.L = sorted(self.L, key=lambda x: x['level'], reverse=True)#Lを階層(level)でソートする(このコードは深さ優先探索としたいため)

            print("----------\n以下すべての部分問題のリスト(1番目が今から考える部分問題に選ばれる)\n")


            

            '''部分問題リストの表示'''
       
            #ここは視認性のために書いた。実行速度重視の場合はコメントアウトする
            for j in range(len(self.L)):
                print(j+1,end='.')
                if self.L[j]['level']!=self.n:
                    i=self.L[j]['level']
                    obj_display=str(self.L[j]['obj_constant_term'])+'+'
                    constraints_display=''
                    while i<len(self.bb_obj):
                        obj_display+=str(self.bb_obj[i]*-1)+'*(x'+str(i+1)+')'
                        constraints_display+=str(self.bb_left[0][i])+'*(x'+str(i+1)+')'
                        if i!=len(self.bb_obj)-1:
                            obj_display+='+'
                            constraints_display+='+'
                        if i==len(self.bb_obj)-1:
                            constraints_display+='≦'+str(self.L[j]['R'][0])
                        i+=1
                    
                    print("目的関数　　　　　:",end='')
                    print(obj_display)
                    print('　制約条件　　　　　:'+constraints_display+'\n　アイテム決定リスト:'+str(self.L[j]['items'])+"\n")
                if self.L[j]['level']==self.n:                
                    print("目的関数　　　　　:",end='')
                    print(self.L[j]['obj_constant_term'])
                    a=np.dot(self.bb_left[0],self.L[j]['items'])
                    print('　制約条件　　　　　:'+str(a)+'≦'+str(self.bb_right[0])+'\n　アイテム決定リスト:'+str(self.L[j]['items'])+"\n")                 
                
                

            print("----------\n")
            

            #print("\n")
            
            P=self.L[0]#今考える問題を取り出す
            del self.L[0]#取り出した問題は消す
            '''実行速度重視のときはここを出力させる'''
            #print(self.L) #LからPが消去されている確認

            #選ばれた部分問題を見たいとき
            #print("選ばれた部分問題")
            #print(P) 
            #print("目的関数:",end='')



            #print("----------\n")
            

            '''LP緩和'''
            if P['R'][0]>=0 and P['level']<self.n:#LP緩和が実行可能のとき(ここが負の時のみ実行不可能である。これはナップザック問題に限定したため) 
                simplex_table = SimplexTable( obj=P['obj'], e_left=P['L'], e_right=P['R'], e_compare=P['cmp'])
                relax_variable,relax_solution=simplex_table.start_end()
                #print(P['obj_constant_term'])
                print('上界計算結果:')
                print(relax_solution+P['obj_constant_term'],relax_variable) 
            if P['R'][0]<0 and P['level']<self.n:#LP緩和実行不可能のとき
                print("LP緩和実行不能。これ以下のノードを捨てる")
            
            

            '''最下層にたどり着いたとき'''#このとき整数条件満たす
            if P['level']==self.n:
                total_weight=0
                for i in range(len(self.bb_obj)):
                    total_weight+=self.bb_left[0][i]*P['items'][i]
                print("整数条件満たしているときの総重み:")
                print(total_weight)
                
                if total_weight>self.bb_right[0]:#重み制約を満たさない
                    print("Overweight")
                if total_weight<=self.bb_right[0]:
                    print("制約を満たす\nInteger　solution:",end="")
                    print(P['obj_constant_term'])

                '''解の更新'''
                if P['obj_constant_term']>self.z_ten and self.tentative_sol==1 and total_weight<=self.bb_right[0]:#すべての変数が整数(最下層)で暫定解より今の解が大きいとき
                    old_z_ten=self.z_ten
                    self.z_ten=P['obj_constant_term']
                    self.x_ten=P['items']
                    self.tentative_sol=1#1になっているときは整数条件を満たす暫定解がself.z_tenに入っていることを表す
                    print('暫定解が更新:'+str(old_z_ten)+'→'+str(self.z_ten))
                    print(self.x_ten,self.z_ten)

                if self.tentative_sol==0 and total_weight<=self.bb_right[0]:#暫定解の更新が今まで1度もなくすべての変数が整数(最下層)になり、制約を満たすとき
                    self.z_ten=P['obj_constant_term']
                    self.x_ten=P['items']
                    self.tentative_sol=1#暫定解が最低1度は更新されたことを示す
                    print('暫定解が登録:')
                    print(self.x_ten,self.z_ten)
       

            '''限定操作の表示'''
            if relax_solution+P['obj_constant_term']<=self.z_ten and P['level']<self.n:#このときは部分問題をLに入れずそれ以下のノードが考えられないため限定操作になる。
                print("上界値:"+str(relax_solution+P['obj_constant_term'])+'<='+str(self.z_ten)+"より、以下のノードを捨てる")


            '''分枝限定操作'''
            if relax_solution+P['obj_constant_term']>self.z_ten and P['level']<self.n and P['R'][0]>=0:#変数がすべて決まっている部分問題では分枝しない,かつLP実行不能のとき分枝しない
                obj0=P['obj'][0]#いまから0と1等に固定する変数の係数（目的関数の）
                left0=P['L'][0][0]#いまから0と1等に固定する変数の係数（制約条件の）
                lev=P['level']+1#階層を今の階層+1とする
                #print(obj0,left0)

                #print(P['R'],R_copy,new_right)
            
                #if文はdelするのに要素が0個のリストから削除する操作をしないため(なくてもいいかも)
                if len(P['obj']) > 0:
                    P['obj'] = np.delete(P['obj'], 0)
                if len(P['L']) > 0:#左辺は変数が0,1,2,...に対して同じでいいため下のfor文に入れなくていい
                    P['L'] = np.delete(P['L'],0,axis=1) #決まった変数の列を制約から消す（axis=1は列） 
                    P['L'] = np.delete(P['L'], 1, axis=0)  # axis=0で第1行を削除。制約が決まると制約が一つ意味をなさなくなるため消す
                if len(P['cmp']) > 0:
                    cmp_copy=copy.deepcopy(P['cmp'])
                    del cmp_copy[1]#一つ制約が不要になるため消去

            
                for i in range(maximum_integer_range+1):#0と1の二回。iが各分枝の固定する整数とも一致。この中にあるものは決まった変数によってそれぞれ別の値をとるもの(右辺、定数項、アイテム決定リスト等)
                    items_copy=copy.deepcopy(P['items'])#深いコピーで今考えている部分問題にて決まっている変数のリストをコピー
                    #print(items_copy,P['items'])
                    items_copy.append(i)
                    #print(items_copy,P['items'])
                    obj_con=P['obj_constant_term']+-1*i*obj0#変数が固定されたことで目的関数の係数で「定数項」になった分を保存！
                    new_right=copy.deepcopy(P['R'])
                    new_right=np.delete(new_right, 1)
                    new_right[0]=new_right[0]+left0*i*-1#左辺の係数が（変数が整数に決まったことにより）右辺に足される
                    #print(left0*i*-1)
                    #print(new_right)
                    self.L.append({'level': lev, 'obj': P['obj'], 'R': new_right,'L': P['L'] ,'cmp': cmp_copy,'obj_constant_term':obj_con,'items':items_copy})#二回分枝した分の部分問題をLに挿入
                    #copy.deepcopy(R_copy)は深いコピーという。import copyが前提。こうしないと二回目のループでR_copy[0]を書き換えたときに１回目のループのLの'R'が書き変わってしまう。
                    #pythonではリストをappendするとき参照渡しがされているため    
            
                #print(self.L)
                #print(self.L[0])
                #print("\n")
                #print(self.L[1])



        return




#例題1
obj=np.array([-16, -19, -23, -28])  #最大化を考えるので―1倍
value=np.array([2,3,4,5])
weight_limit=7
maximum_integer_range=1#整数条件の最大値
#q=0.8#準最適解許容率

'''
#これはコメントアウトしておく.
#例題1のシンプレックス法の入力のたのリストメモ
obj=np.array([-16, -19, -23, -28])
e_left=np.array([[2,3,4,5],#ここが重みの制約
                [1,0,0,0],
                [0,1,0,0],#ここの0と1で表された制約はLP緩和に使う
                [0,0,1,0],
                [0,0,0,1]])
e_right=np.array([7,1,1,1,1])#一つ目が重みの上限
e_compare=['Less','Less','Less','Less','Less']
#print(e_right,e_left)
'''





'''
#例題2
obj=np.array([-10, -14, -21])  #最大化を考えるので―1倍
value=np.array([2,3,6])
weight_limit=7
maximum_integer_range=2#整数条件の最大値
'''
'''これはコメントアウトしておくメモ
e_left=np.array([[2,3,6],#ここが重みの制約
                [1,0,0],
                [0,1,0],#ここの0と1で表された制約はLP緩和に使う
                [0,0,1]])
e_right=np.array([7,1,1,1])#一つ目が重みの上限
e_compare=['Less','Less','Less','Less']
maximum_integer_range=1
'''




'''
#例題3
obj=np.array([-3, -4, -1, -2])  #最大化を考えるので―1倍
value=np.array([2,3,1,3])
weight_limit=4
maximum_integer_range=1#整数条件の最大値
'''
'''
#ここはコメントアウトしておくメモ
#例題3
obj=np.array([-3, -4, -1, -2])  #最大化を考えるので―1倍
e_left=np.array([[2,3,1,3],#ここが重みの制約
                [1,0,0,0],
                [0,1,0,0],#ここの0と1で表された制約はLP緩和に使う
                [0,0,1,0],
                [0,0,0,1]])
e_right=np.array([4,1,1,1,1])#一つ目が重みの上限
e_compare=['Less','Less','Less','Less','Less']
maximum_integer_range=1
'''






#ここでシンプレックス法のプログラムに使う入力(制約リスト)を生成
e_right = np.array([weight_limit] + [maximum_integer_range] * len(obj))
# e_leftの作成
I = np.eye(len(value), dtype=int)  # 単位行列
e_left = np.vstack([value, I])  # 上に価値(value)を追加
e_compare=['Less'] * (len(obj) + 1)
print(e_left,e_right,e_compare)

start=time.time()
knapsack = Knapsack( bb_obj=obj, bb_left=e_left, bb_right=e_right,bb_compare=e_compare,maximum_integer_range=maximum_integer_range)
knapsack.knapsak_start_to_end()
finish=time.time()
print('Time:'+str(finish-start))
