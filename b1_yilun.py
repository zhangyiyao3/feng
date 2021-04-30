def same_d(a1,a2,b1,b2,a_sign):
    #a1 low a2 high b1 low b2 high
    if a_sign == 1:
        return (a1 > b1 and a2 > b2)
    else:
        return (a1 < b1 and a2 < b2)
    
def new_extreme(a1,a2,b1,b2,a_sign):
    #whether b has new extreme than a,true return true
    if a_sign == 1:
        return b2 >= a2
    else:
        return a1 >= b1
    
def exist_opposite(cur_i,d,pos):
    #print("exist_opposite")
    #print('e0'+str(cur_i+pos))
        #print('e1'+str(df1.iloc[cur_i+pos,0]))
    return df1['od'].iloc[cur_i+pos]==-d and same_d(df1.iloc[cur_i,0],df1.iloc[cur_i,1],\
     df1.iloc[cur_i+pos,0],df1.iloc[cur_i+pos,1],d)

def exist_new_extreme(cur_i,d,start,end):
    j = start
    while j <= end:
        if new_extreme(df1.iloc[cur_i,0],df1.iloc[cur_i,1],df1.iloc[cur_i + j,0],df1.iloc[cur_i + j,1],d):
            return cur_i + j,True
        j = j + 1
    return cur_i,False

def judge(prev_i,cur_i,d):#d the direction of fenxing to be confirmed, prev_i the previous confirmed
    #d == df1['od][cur_i] should hold when finished and prev_i = cur_i is set
    global od_list 
    
    
    
    #print('start ' + str(cur_i))
    if cur_i + 4 >= len(df1)-1:
        #print('finished')
        
        #stop()
        return 0
        
    if cur_i - prev_i < 4 or df1['od'].iloc[cur_i] != d:
        cur_i = cur_i + 1
        #print(cur_i)
        judge(prev_i,cur_i,d)
    else:# at least 4 bars later and direction correct
        # now df1['od'].iloc[cur_i] ==d and cur_i - prev_i >= 4 
        
        new_i,label1 = exist_new_extreme(cur_i,d,2,3)
        if label1 == True:
            cur_i = new_i
            #print("f1")
            judge(prev_i,cur_i,d)
        else:
            k = 4
            if cur_i  + k + 1>= len(df1)-1:
                #print ("finishe2!")
                return 0
            
            while not exist_opposite(cur_i,d,k):
            #while True:    
                #kth >=4 later bar does not match opposite fenxing
                new_i,label2 = exist_new_extreme(cur_i,d,k,k)
                if label2 == True:
                    cur_i = new_i
                    judge(prev_i,cur_i,d)
                    return 0
                    #print('f2')
                else:
                    k = k + 1
                    if cur_i  + k >= len(df1)-1:
                        #print ("finishe4!")
                        return 0
                
            #confirmed by existent opposite fenxing
            prev_i = cur_i
            cur_i = cur_i + k
            od_list = od_list + [prev_i]
            #print('added' + str(prev_i))
            #print('input ' + str(cur_i))
            #print('-d ' + str(d))
            judge(prev_i,cur_i,-d)
    #print('post call judge' + str(cur_i))
#end judge


def select(listidx,days_before=5,T='1m',buy='buy1'):
    #NDAY=5
    extra=days_before
    b=get_price(sec.index[0],fields=['low','high'],\
                        frequency=T,count=3,end_date=datetime.date.today()-\
                   datetime.timedelta(extra))#end day must be current date + 1
    print('example data,the last 3 bars')
    print(b)
    stock_list=[]
    count=0
    for i_out in listidx:
        count+=1
        if count%50==9:
            print('{} stocks processed'.format(count+1))
         
        
        b=get_price(i_out,fields=['low','high','close'],\
                    frequency=T,skip_paused=True,count=750,end_date=datetime.date.today()-\
               datetime.timedelta(extra))#end day must be current date + 1
        #print(sec.index[i_out])
        cl=b.iloc[-1]['close']
        b['datetime']=b.index
        df=b
        while ( True ):
            temp_len = len(df)
            i=0
            while i<=len(df)-4:
                if (df.iloc[i+2,0]>=df.iloc[i+1,0] and df.iloc[i+2,1]<=df.iloc[i+1,1]) or\
                (df.iloc[i+2,0]<=df.iloc[i+1,0] and df.iloc[i+2,1]>=df.iloc[i+1,1]):
                    if df.iloc[i+1,0]>df.iloc[i,0]:
                        df.iloc[i+2,0] = max(df.iloc[i+1:i+3,0])
                        df.iloc[i+2,1] = max(df.iloc[i+1:i+3,1])
                        df.drop(df.index[i+1],inplace=True)

                        continue
                    else:
                        df.iloc[i+2,0] = min(df.iloc[i+1:i+3,0])
                        df.iloc[i+2,1] = min(df.iloc[i+1:i+3,1])
                        df.drop(df.index[i+1],inplace=True)

                        continue
                i = i + 1
           # print(len(df))    
            if len(df)==temp_len:
                break

        df= df.reset_index(drop=True)  
        #get difenxing and dingfenxing
        ul=[0]
        for i in range(len(df)-2):
            if df.iloc[i+2,0] < df.iloc[i+1,0] and df.iloc[i,0] < df.iloc[i+1,0]:
                ul = ul + [1]
                continue
            if df.iloc[i+2,0] > df.iloc[i+1,0] and df.iloc[i,0] > df.iloc[i+1,0]:
                ul = ul + [-1]# difenxing -1 dingfenxing +1
                continue
            else:
                ul = ul + [0]
        ul = ul + [0]
        global df1
        df1 = pd.concat((df[['low','high']],pd.DataFrame(ul),df['datetime']),axis=1)

        i = 0

        while df1.iloc[i,2] == 0 and i < len(df1)-2:
            i = i + 1
        df1=df1[i:]  

        i = 0
        while ( sum(abs(df1.iloc[i+1:i+4,2]))>0 or df1.iloc[i,2]==0) and i < len(df1)-2:
            i = i + 1
        df1=df1[i:]
        df1.rename(columns= {0:'od'},inplace=True)
        #df1.columns=Index(['low', 'high', 'od', 'datetime'], dtype='object')
        if len(df1)<=60:
            #print('error!need more k bars')
            continue
        #remove those within 3 bars
        df1=df1.reset_index(drop=True)
        global od_list#od_list are the index of df1 whose corresponding point are fenxing extreme vertex

        od_list=[0]
        judge(0,0,1) 
        #od_list are the index of df1 whose corresponding point are fenxing extreme vertex
        #print(df1.head())
        #print(od_list)
        #generate seg
        start = 0
        plist=[df1.iloc[od_list[i],i%2] for i in range(len(od_list))]
        tlist=[df1.iloc[od_list[i],3] for i in range(len(od_list))]
        purebi=[]
        for i in range(1,len(od_list)):
            if i%2==1:
                a=df1.iloc[od_list[i],i%2]>max(df1.iloc[od_list[i-1]:od_list[i],i%2])
                purebi.append(a)
            else:
                a=df1.iloc[od_list[i],i%2]<min(df1.iloc[od_list[i-1]:od_list[i],i%2])
                purebi.append(a)
        if len(plist)<13:
            #print('too short{}'.format(len(plist)))
            continue
        if plist[-1]<plist[-2] and plist[-1]<min(plist[-3],plist[-5],plist[-7]) \
        and plist[-2]>=plist[-5]\
        and ( ( max(plist[-4],plist[-2])<min(plist[-7],plist[-9]) and plist[-6]>=plist[-9]\
              and plist[-1]/plist[-2]>plist[-5]/plist[-6] and all(purebi[-9:]) ) \
  or (max(plist[-4],plist[-2])<min(plist[-7],plist[-9],plist[-11]) \
      and plist[-8]>=plist[-11]  and plist[-1]/plist[-2]>plist[-5]/plist[-6] and all(purebi[-11:]) )\
  or (max(plist[-4],plist[-2],plist[-6])<min(plist[-9],plist[-11]) and \
      plist[-8]>=plist[-11] and plist[-1]/plist[-2]>plist[-7]/plist[-8]  and all(purebi[-11:]) )\
  or (max(plist[-4],plist[-2],plist[-6])<min(plist[-9],plist[-11]) and \
      plist[-8]>=plist[-11] and plist[-1]/plist[-2]>plist[-7]/plist[-8]  and all(purebi[-11:]) )\
  or (max(plist[-4],plist[-2],plist[-6],plist[-8])<min(plist[-9],plist[-13])\
      and plist[-10]>=plist[-13] and plist[-1]/plist[-2]>plist[-9]/plist[-10]  and all(purebi[-11:]))):
            p=pd.DataFrame()
            p['last8bi']=tlist[-8:]
            p['price']=plist[-8:]
            print('{}selected \n {}'.format(i_out,p))
            stock_list.append(i_out)
     
    print('{}:{}'.format(T,stock_list))
    
print('done')

import pandas as pd
import numpy as np

sec=get_all_securities()#all stocks code sec.index
 
    
listidx=[]
for i in range(sec.shape[0]):
    if not (sec.iloc[i]['end_date']!=datetime.date(2200, 1, 1)\
            or sec.iloc[i]['display_name'][0]=='*' or sec.iloc[i]['display_name'][0]=='S'\
    or '退' in sec.iloc[i]['display_name'] or sec.index[i][:3]=='688'\
            or sec.iloc[i]['start_date']>datetime.date.today()-datetime.timedelta(270) ):
         
        listidx+=[sec.index[i]]
print('{} candidate stocks'.format(len(listidx)))

print('-------1d--------')
select(listidx,T='1d',days_before=0)
print('-------60m--------')
select(listidx,T='60m',days_before=0)
print('-------30m--------')
select(listidx,T='30m',days_before=0)