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
    def __init__(self,bb_obj,bb_left,bb_right,bb_compare,maximum_integer_range,q):
        self.bb_obj=bb_obj
        self.bb_left=bb_left
        self.bb_right=bb_right
        self.bb_compare=bb_compare
        self.tentative_sol=0#暫定解があるとき1にする
        self.z_ten=-1#暫定解の値を-1で初期化(最適解が0だった場合に備え0を避ける)
        print('初期暫定解:-1とする')
        self.x_ten= np.zeros(len(bb_obj))#暫定解の変数リストを0に初期化
        self.n=len(bb_obj)
        self.L=[]#考えるノードを入れておく
        self.items=[]#各分枝で整数に固定された変数を挿入していくリスト
        obj_constant_term=0#目的関数の定数項を保存する変数
        self.maximum_integer_range=maximum_integer_range#整数の取りうる最大
        self.simplex_count=0#シンプレックス法の回数
        self.q=q#準最適解許容率
        self.process_pool=[]#準最適解を考えるときにノードを入れておく
        self.solution_pool=[]#準最適解を入れる

 
        '''LP緩和'''
        if self.bb_right[0]>=0 :#LP緩和 
            simplex_table = SimplexTable( obj=obj, e_left=bb_left, e_right=bb_right, e_compare=bb_compare)
            relax_variable,relax_solution=simplex_table.start_end()
            self.simplex_count+=1
            #print(P['obj_constant_term'])
            #print('上界計算結果:')
            #print(relax_solution+L['obj_constant_term'],relax_variable) 

        #分枝の階層、目的関数、制約条件を辞書として入れ初期化。階層0では元の制約条件のままで分枝して階層が増え変数が決まったらそのたびにobj,制約を書き換える.
        self.L.append({'level': 0, 'obj': self.bb_obj, 'R': self.bb_right ,'L': self.bb_left ,'cmp': self.bb_compare,'obj_constant_term':obj_constant_term,'items':self.items,'upper_world':relax_solution})        
      
    def finding_suboptimal_solution(self):
        print('\n====================\n準最適解探索開始\n保存したノード:')
        for l in range(len(self.process_pool)):
            print('level:'+str(self.process_pool[l]['level'])+'  上界値:'+str(self.process_pool[l]['upper_world']))
        while True:
            
            '''終了処理'''
            if len(self.process_pool)==0:#Lに考えるべきノードでの問題が入っていなければ終了
                print("\nFinished.\n")
                print("The suboptomal solution :")
                for m in range(len(self.solution_pool)):
                    print(self.solution_pool[m]['solution'],self.solution_pool[m]['x'])
                print('Simplex count:'+str(self.simplex_count)) 
                return

            '''ここは実行時間重視ならばコメントアウトする。'''
            '''深さ優先探索にしてわかりやすくしているだけ。最適解の更新はないため探索順による効率の改善には影響しないと思う。したがってソートしている分だけ実行が遅くなる'''
            self.process_pool = sorted(self.process_pool, key=lambda x: x['R'][0])#各変数1を先に探索する場合
            self.process_pool = sorted(self.process_pool, key=lambda x: x['level'], reverse=True)#process_poolを階層(level)でソートする(このコードは深さ優先探索としたいため)         

            P=self.process_pool[0]#今考える問題を取り出す
            del self.process_pool[0]
            print('----------\n今考える部分問題のアイテム決定リスト:')
            #print('\n')
            print(P['items'])
            '''最下層にたどり着いたとき'''#このとき整数条件満たす
            if P['level']==self.n:
                if P['upper_world']<0:#重み制約を満たさない(負の上界はありえない。下の上界計算で重み制限を満たさないときP['upper_world']=-1とするようにした)
                    print("Overweight")
                if P['upper_world']>=0:#制約を満たす
                    print("制約を満たす許容解:",end="")
                    print(P['obj_constant_term'])
                   

                '''解の更新'''
                if P['obj_constant_term']>=self.z_ten*(1-self.q/100) and P['upper_world']>=0:#すべての変数が整数(最下層)で暫定解*qより今の解が大きいとき
                    self.solution_pool.append({'x':P['items'],'solution':P['obj_constant_term']})
                    print("得られた許容解:"+str(P['upper_world'])+'>=暫定解*(1-q/100):'+str(self.z_ten*(1-self.q/100))+'より、解プールに追加:'+str(P['obj_constant_term']))#level==4でかつ実行可能のとき(許容解のとき)、P['upper_world']==P['obj_constant_term']である
                if P['obj_constant_term']<self.z_ten*(1-self.q/100) and P['upper_world']>=0:
                    print("得られた許容解:"+str(P['upper_world'])+'<暫定解*(1-q/100):'+str(self.z_ten*(1-self.q/100))+"より、解プールに追加せず")
            
                    
            '''限定操作の表示'''
            if P['upper_world']<=self.z_ten*(1-self.q/100) and P['level']<self.n:#上界が最適解*q以下のときはそれ以下のノードを考えない
                print("上界値:"+str(P['upper_world'])+'<=暫定解*(1-q/100):'+str(self.z_ten*(1-self.q/100))+"より、以下のノードを捨てる")

            '''分枝限定操作(ほぼknapsak_start_to_endのコピペ)'''
            if P['upper_world']>self.z_ten*(1-self.q/100) and P['level']<self.n and P['R'][0]>=0:#変数がすべて決まっている部分問題では分枝しない,かつLP実行不能のとき分枝しない
                print("上界値:"+str(P['upper_world'])+'>暫定解*(1-q/100):'+str(self.z_ten*(1-self.q/100))+"より、ノードを分枝する")
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

                    #分枝したときに即LP緩和を実行する
                    '''LP緩和'''
                    if new_right[0]>=0 and lev<self.n:#LP緩和が実行可能のとき(ここが負の時のみ実行不可能である。これはナップザック問題に限定したため) 
                        simplex_table = SimplexTable( obj=P['obj'], e_left=P['L'], e_right=new_right, e_compare=cmp_copy)
                        relax_variable,relax_solution=simplex_table.start_end()
                        #print(relax_variable,relax_solution)
                        self.simplex_count+=1
                        #print(P['obj_constant_term'])
                        print('部分問題'+str(i+1)+'.上界計算結果:')
                        print(relax_solution+obj_con,relax_variable) 
                        upper_world=relax_solution+obj_con
                    if new_right[0]<0 and lev<self.n:#LP緩和実行不可能のとき
                        print('部分問題'+str(i+1)+".LP緩和実行不能。これ以下のノードを捨てる")
                        upper_world=-1
                    if lev==self.n:#すべての変数が整数に決まったとき
                        if np.dot(self.bb_left[0],items_copy)<=self.bb_right[0]:
                            upper_world=obj_con
                        if np.dot(self.bb_left[0],items_copy)>self.bb_right[0]:#重み制約を満たさないとき
                            upper_world=-1

                    self.process_pool.append({'level': lev, 'obj': P['obj'], 'R': new_right,'L': P['L'] ,'cmp': cmp_copy,'obj_constant_term':obj_con,'items':items_copy,'upper_world':upper_world})#二回分枝した分の部分問題をLに挿入




    def knapsak_start_to_end(self):
        
        #print(self.L)
         
        while True:
            
            '''終了処理'''
            if len(self.L)==0:#Lに考えるべきノードでの問題が入っていなければ終了
                print("\nFinished.\n")
                print("The optomal solution :")
                print(self.x_ten,self.z_ten)
                print('Simplex count:'+str(self.simplex_count))
                if self.q!=0:#準最適解を求めたいとき
                    self.finding_suboptimal_solution()                    
                return

            #self.L = sorted(self.L, key=lambda x: x['R'][0])#各変数1を先に探索する場合
            self.L = sorted(self.L, key=lambda x: x['upper_world'],reverse=True)#上界でソートする場合
            #self.L = sorted(self.L, key=lambda x: x['level'], reverse=True)#Lを階層(level)でソートする(このコードは深さ優先探索としたいため)

            print("====================\n以下すべての部分問題のリスト(1番目が今から考える部分問題に選ばれる)\n")


            

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
                    print('　制約条件　　　　　:'+constraints_display+'\n　アイテム決定リスト:'+str(self.L[j]['items']))
                if self.L[j]['level']==self.n:                
                    print("目的関数　　　　　:",end='')
                    print(self.L[j]['obj_constant_term'])
                    a=np.dot(self.bb_left[0],self.L[j]['items'])
                    print('　制約条件　　　　　:'+str(a)+'≦'+str(self.bb_right[0])+'\n　アイテム決定リスト:'+str(self.L[j]['items']))  
                if self.L[j]['upper_world']>=0:
                    print("　上界値　　　　　　:"+str(self.L[j]['upper_world'])+"\n")
                if self.L[j]['upper_world']<0:
                    print("　上界値　　　　　　:実行不能(-1とする)\n")
                
                

            print("----------\n")
            

            #print("\n")
            
            P=self.L[0]#今考える問題を取り出す
            del self.L[0]#取り出した問題は消す
            '''実行速度重視で過程を見たいときはここを出力させる'''
            #print(self.L) #LからPが消去されている確認

            #選ばれた部分問題を見たいとき
            #print("選ばれた部分問題")
            #print(P) 
            #print("目的関数:",end='')



            #print("----------\n")
            
            
            '''ここはコメントアウトしておく。
            #LP緩和を計算する場所を分枝したときに変えたため。
            if P['R'][0]>=0 and P['level']<self.n:#LP緩和が実行可能のとき(ここが負の時のみ実行不可能である。これはナップザック問題に限定したため) 
                simplex_table = SimplexTable( obj=P['obj'], e_left=P['L'], e_right=P['R'], e_compare=P['cmp'])
                relax_variable,relax_solution=simplex_table.start_end()
                self.simplex_count+=1
                #print(P['obj_constant_term'])
                print('上界計算結果:')
                print(relax_solution+P['obj_constant_term'],relax_variable) 
            if P['R'][0]<0 and P['level']<self.n:#LP緩和実行不可能のとき
                print("LP緩和実行不能。これ以下のノードを捨てる")
            '''
            
            

            '''最下層にたどり着いたとき'''#このとき整数条件満たす
            if P['level']==self.n:
                if P['upper_world']<0:#重み制約を満たさない(負の上界はありえない。下の上界計算で重み制限を満たさないときP['upper_world']=-1とするようにした)
                    print("Overweight")
                if P['upper_world']>=0:#制約を満たす
                    print("制約を満たす\nInteger　solution:",end="")
                    print(P['obj_constant_term'])
                    if self.q!=0 and self.z_ten*(1-self.q/100)<P['upper_world']:#準最適解を求めたいとき、かつ暫定解*(1-q/100)より大きいとき
                        self.process_pool.append(P)

                '''解の更新'''
                if P['obj_constant_term']<=self.z_ten and self.tentative_sol==1 and P['upper_world']>=0:#解の更新をしない場合の表示
                    print("得られた許容解:"+str(P['upper_world'])+'<=暫定解:'+str(self.z_ten)+"より、暫定解の更新せず")
                if P['obj_constant_term']>self.z_ten and self.tentative_sol==1 and P['upper_world']>=0:#すべての変数が整数(最下層)で暫定解より今の解が大きいとき
                    old_z_ten=self.z_ten
                    print("得られた許容解:"+str(P['upper_world'])+'>暫定解:'+str(self.z_ten)+"より、暫定解が更新:"+str(old_z_ten)+'→'+str(P['obj_constant_term']))
                    self.z_ten=P['obj_constant_term']
                    self.x_ten=P['items']
                    self.tentative_sol=1#1になっているときは整数条件を満たす暫定解がself.z_tenに入っていることを表す
                    print(self.x_ten,self.z_ten)


                if self.tentative_sol==0 and P['upper_world']>=0:#暫定解の更新が今まで1度もなくすべての変数が整数(最下層)になり、制約を満たすとき
                    self.z_ten=P['obj_constant_term']
                    self.x_ten=P['items']
                    self.tentative_sol=1#暫定解が最低1度は更新されたことを示す
                    print('暫定解が初めて登録:')
                    print(self.x_ten,self.z_ten)
       


            '''限定操作の表示'''
            if P['upper_world']<=self.z_ten and P['level']<self.n:#このときは部分問題をLに入れずそれ以下のノードが考えられないため限定操作になる。
                print("上界値:"+str(P['upper_world'])+'<=暫定解:'+str(self.z_ten)+"より、以下のノードを捨てる")
                if P['upper_world']>=0 and self.q!=0 and self.z_ten*(1-self.q/100)<P['upper_world']:#LP緩和実行可能かつ準最適解を求めたいとき、かつ保存すべき時
                    self.process_pool.append(P)


            '''分枝限定操作'''
            if P['upper_world']>self.z_ten and P['level']<self.n and P['R'][0]>=0:#変数がすべて決まっている部分問題では分枝しない,かつLP実行不能のとき分枝しない
                print("上界値:"+str(P['upper_world'])+'>暫定解:'+str(self.z_ten)+"より、ノードを分枝する")
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

                    #分枝したときに即LP緩和を実行する
                    '''LP緩和'''
                    if new_right[0]>=0 and lev<self.n:#LP緩和が実行可能のとき(ここが負の時のみ実行不可能である。これはナップザック問題に限定したため) 
                        simplex_table = SimplexTable( obj=P['obj'], e_left=P['L'], e_right=new_right, e_compare=cmp_copy)
                        #print(P['obj'],P['L'],new_right,cmp_copy)
                        relax_variable,relax_solution=simplex_table.start_end()
                        self.simplex_count+=1
                        #print(P['obj_constant_term'])
                        #print(lev,len(self.bb_obj)-lev)
                        #LP緩和解の整数判定を行う。
                        #result='false'
                        result=self.determine_integer(lev,relax_variable)#整数判定
                        print('部分問題'+str(i+1)+'.上界計算結果:')
                        print(relax_solution+obj_con,relax_variable) 
                        print('整数条件判定:'+str(result))      
                        
                        #整数条件を満たすか判定(満たしていれば暫定解と比較してそれ以下のノードを捨てる)
                        
                        if result==True:
                            item_ten=copy.deepcopy(items_copy)
                            item_ten.extend([round(relax_variable[i]) for i in range(len(self.bb_obj)-lev)])
                            
                            if self.tentative_sol==1 and self.z_ten>=relax_solution+obj_con:#更新しない場合の表示
                                print('アイテム決定リスト:'+str(item_ten))
                                print("得られた許容解:"+str(relax_solution+obj_con)+'<=暫定解:'+str(self.z_ten)+'より、暫定解を更新せず')
                            if self.tentative_sol==1 and self.z_ten<relax_solution+obj_con:
                                self.x_ten=item_ten
                                old_z_ten=self.z_ten
                                print('アイテム決定リスト:'+str(item_ten))
                                self.z_ten=relax_solution+obj_con
                                print("得られた許容解:"+str(self.z_ten)+'>暫定解:'+str(old_z_ten)+'より、暫定解が更新:'+str(old_z_ten)+'→'+str(self.z_ten)+str(self.x_ten))
                              


                            if self.tentative_sol==0:
                                self.x_ten=item_ten
                                self.z_ten=relax_solution+obj_con
                                print('初めて暫定解が登録:'+str(self.z_ten)+str(self.x_ten))
                                self.tentative_sol=1
                            print('整数条件を満たすためこれより下のノードを捨てる')
                            if self.q!=0 and self.z_ten*(1-self.q/100)<relax_solution+obj_con:#準最適解を考えるとき、階層を変数の数とする。
                                self.process_pool.append({'level': lev,'obj': P['obj'], 'R': new_right,'L': P['L'] ,'cmp': cmp_copy,'obj_constant_term':obj_con,'items':items_copy,'upper_world':relax_solution+obj_con})
                            continue#部分問題をLに入れない(限定操作)
                                
                        upper_world=relax_solution+obj_con
                    if new_right[0]<0 and lev<self.n:#LP緩和実行不可能のとき
                        print('部分問題'+str(i+1)+".LP緩和実行不能。これ以下のノードを捨てる")
                        upper_world=-1
                    if lev==self.n:#すべての変数が整数に決まったとき
                        if np.dot(self.bb_left[0],items_copy)<=self.bb_right[0]:
                            upper_world=obj_con
                        if np.dot(self.bb_left[0],items_copy)>self.bb_right[0]:#重み制約を満たさないとき
                            upper_world=-1

                    print(items_copy)
                    self.L.append({'level': lev, 'obj': P['obj'], 'R': new_right,'L': P['L'] ,'cmp': cmp_copy,'obj_constant_term':obj_con,'items':items_copy,'upper_world':upper_world})#二回分枝した分の部分問題をLに挿入
                    #copy.deepcopy(R_copy)は深いコピーという。import copyが前提。こうしないと二回目のループでR_copy[0]を書き換えたときに１回目のループのLの'R'が書き変わってしまう。
                    #pythonではリストをappendするとき参照渡しがされているため    

                #print(self.L)
                #print(self.L[0])
                #print("\n")
                #print(self.L[1])

    def determine_integer(self, level,relax_variable):
        #整数かどうかを考える変数の数
        end_index = len(self.bb_obj) - level
        tolerance = 1e-6#この値と比較する
        # すべての要素をチェックし、1つでもFalseがあればすぐに終了
        for j in range(end_index):
            value = relax_variable[j]
            # 四捨五入した値との差が許容範囲内かチェック
            if abs(value - round(value)) >= tolerance:
                return False
        return True




             
#例題1
obj=np.array([-16, -19, -23, -28])  #最大化を考えるので―1倍
value=np.array([2,3,4,5])
weight_limit=7
maximum_integer_range=1#整数条件の最大値
q=20#解プール機能


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
q=100#解プール機能
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
q=0
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
#print(e_left,e_right,e_compare)

start=time.time()
knapsack = Knapsack( bb_obj=obj, bb_left=e_left, bb_right=e_right,bb_compare=e_compare,maximum_integer_range=maximum_integer_range,q=q)
knapsack.knapsak_start_to_end()
finish=time.time()
print('Time:'+str(finish-start))
