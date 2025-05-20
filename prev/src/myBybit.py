import ccxt
import time
import pandas as pd
import pprint
import numpy


from cryptography.fernet import Fernet


'''

아래 구글 드라이브 링크에 권한 요청을 해주세요!
이후 업데이트 사항은 여기서 실시간으로 편하게 다운로드 하시면 됩니다. (클래스 구독이 끝나더라도..)
https://drive.google.com/drive/folders/1cTRATmFwHuKDz-hEa-DP4lBblzdxK0YM?usp=sharing



하다가 잘 안되시면 계속 내용이 추가되고 있는 아래 FAQ를 꼭꼭 체크하시고

주식/코인 자동매매 FAQ
https://blog.naver.com/zacra/223203988739

그래도 안 된다면 구글링 해보시고
그래도 모르겠다면 클래스 댓글, 블로그 댓글, 단톡방( https://blog.naver.com/zacra/223111402375 )에 질문주세요! ^^

클래스 제작 후 전략의 많은 발전이 있었습니다.
백테스팅으로 검증해보고 실제로 제가 현재 돌리는 최신 전략을 완강 후 제 블로그에서 체크해 보셔요!
https://blog.naver.com/zacra

기다릴게요 ^^!

'''

#암호화 복호화 클래스
class SimpleEnDecrypt:
    def __init__(self, key=None):
        if key is None: # 키가 없다면
            key = Fernet.generate_key() # 키를 생성한다
        self.key = key
        self.f   = Fernet(self.key)
    
    def encrypt(self, data, is_out_string=True):
        if isinstance(data, bytes):
            ou = self.f.encrypt(data) # 바이트형태이면 바로 암호화
        else:
            ou = self.f.encrypt(data.encode('utf-8')) # 인코딩 후 암호화
        if is_out_string is True:
            return ou.decode('utf-8') # 출력이 문자열이면 디코딩 후 반환
        else:
            return ou
        
    def decrypt(self, data, is_out_string=True):
        if isinstance(data, bytes):
            ou = self.f.decrypt(data) # 바이트형태이면 바로 복호화
        else:
            ou = self.f.decrypt(data.encode('utf-8')) # 인코딩 후 복호화
        if is_out_string is True:
            return ou.decode('utf-8') # 출력이 문자열이면 디코딩 후 반환
        else:
            return ou


#RSI지표 수치를 구해준다. 첫번째: 분봉/일봉 정보, 두번째: 기간, 세번째: 기준 날짜
def GetRSI(ohlcv,period,st):
    delta = ohlcv["close"].diff()
    up, down = delta.copy(), delta.copy()
    up[up < 0] = 0
    down[down > 0] = 0
    _gain = up.ewm(com=(period - 1), min_periods=period).mean()
    _loss = down.abs().ewm(com=(period - 1), min_periods=period).mean()
    RS = _gain / _loss
    return float(pd.Series(100 - (100 / (1 + RS)), name="RSI").iloc[st])

#이동평균선 수치를 구해준다 첫번째: 분봉/일봉 정보, 두번째: 기간, 세번째: 기준 날짜
def GetMA(ohlcv,period,st):
    close = ohlcv["close"]
    ma = close.rolling(period).mean()
    return float(ma.iloc[st])

#볼린저 밴드를 구해준다 첫번째: 분봉/일봉 정보, 두번째: 기간, 세번째: 기준 날짜
#차트와 다소 오차가 있을 수 있습니다.
def GetBB(ohlcv,period,st):
    dic_bb = dict()

    ohlcv = ohlcv[::-1]
    ohlcv = ohlcv.shift(st + 1)
    close = ohlcv["close"].iloc[::-1]

    unit = 2.0
    bb_center=numpy.mean(close[len(close)-period:len(close)])
    band1=unit*numpy.std(close[len(close)-period:len(close)])

    dic_bb['ma'] = float(bb_center)
    dic_bb['upper'] = float(bb_center + band1)
    dic_bb['lower'] = float(bb_center - band1)

    return dic_bb




#일목 균형표의 각 데이타를 리턴한다 첫번째: 분봉/일봉 정보, 두번째: 기준 날짜
def GetIC(ohlcv,st):

    high_prices = ohlcv['high']
    close_prices = ohlcv['close']
    low_prices = ohlcv['low']


    nine_period_high =  ohlcv['high'].shift(-2-st).rolling(window=9).max()
    nine_period_low = ohlcv['low'].shift(-2-st).rolling(window=9).min()
    ohlcv['conversion'] = (nine_period_high + nine_period_low) /2
    
    period26_high = high_prices.shift(-2-st).rolling(window=26).max()
    period26_low = low_prices.shift(-2-st).rolling(window=26).min()
    ohlcv['base'] = (period26_high + period26_low) / 2
    
    ohlcv['sunhang_span_a'] = ((ohlcv['conversion'] + ohlcv['base']) / 2).shift(26)
    
    
    period52_high = high_prices.shift(-2-st).rolling(window=52).max()
    period52_low = low_prices.shift(-2-st).rolling(window=52).min()
    ohlcv['sunhang_span_b'] = ((period52_high + period52_low) / 2).shift(26)
    
    
    ohlcv['huhang_span'] = close_prices.shift(-26)


    nine_period_high_real =  ohlcv['high'].rolling(window=9).max()
    nine_period_low_real = ohlcv['low'].rolling(window=9).min()
    ohlcv['conversion'] = (nine_period_high_real + nine_period_low_real) /2
    
    period26_high_real = high_prices.rolling(window=26).max()
    period26_low_real = low_prices.rolling(window=26).min()
    ohlcv['base'] = (period26_high_real + period26_low_real) / 2
    


    
    dic_ic = dict()

    dic_ic['conversion'] = ohlcv['conversion'].iloc[st]
    dic_ic['base'] = ohlcv['base'].iloc[st]
    dic_ic['huhang_span'] = ohlcv['huhang_span'].iloc[-27]
    dic_ic['sunhang_span_a'] = ohlcv['sunhang_span_a'].iloc[-1]
    dic_ic['sunhang_span_b'] = ohlcv['sunhang_span_b'].iloc[-1]


  

    return dic_ic




#MACD의 12,26,9 각 데이타를 리턴한다 첫번째: 분봉/일봉 정보, 두번째: 기준 날짜
def GetMACD(ohlcv,st):
    macd_short, macd_long, macd_signal=12,26,9

    ohlcv["MACD_short"]=ohlcv["close"].ewm(span=macd_short).mean()
    ohlcv["MACD_long"]=ohlcv["close"].ewm(span=macd_long).mean()
    ohlcv["MACD"]=ohlcv["MACD_short"] - ohlcv["MACD_long"]
    ohlcv["MACD_signal"]=ohlcv["MACD"].ewm(span=macd_signal).mean() 

    dic_macd = dict()
    
    dic_macd['macd'] = ohlcv["MACD"].iloc[st]
    dic_macd['macd_siginal'] = ohlcv["MACD_signal"].iloc[st]
    dic_macd['ocl'] = dic_macd['macd'] - dic_macd['macd_siginal']

    return dic_macd




#분봉/일봉 캔들 정보를 가져온다 첫번째: 바이비트 객체, 두번째: 코인 티커, 세번째: 기간 (1d,4h,1h,15m,10m,1m ...)
def GetOhlcv(bybit, Ticker, period):
    #바이비트는 리미트를 반드시 걸어줘야 된다.
    btc_ohlcv = bybit.fetch_ohlcv(Ticker, period,since=None, limit=200)
    df = pd.DataFrame(btc_ohlcv, columns=['datetime', 'open', 'high', 'low', 'close', 'volume'])
    df['datetime'] = pd.to_datetime(df['datetime'], unit='ms')
    df.set_index('datetime', inplace=True)
    return df


#스탑로스를 걸어놓는다. 해당 가격에 해당되면 바로 손절한다. 첫번째: 바이낸스 객체, 두번째: 코인 티커, 세번째: 손절 수익율 (1.0:마이너스100% 청산, 0.9:마이너스 90%, 0.5: 마이너스 50%)
#네번째 웹훅 알림에서 사용할때는 마지막 파라미터를 False로 넘겨서 사용한다. 트레이딩뷰 웹훅 강의 참조..
def SetStopLoss(bybit, Ticker, cut_rate, Rest = True):
    if Rest == True:
        time.sleep(0.1)



    orders = bybit.fetch_orders(Ticker,None,None,{'orderType': 'conditional'})

    for order in orders:
        if order['status'].strip() == "open" :
            print(bybit.cancel_order(order['id'],Ticker,{'orderType': 'conditional','stop_order_id' : order['id']}))



    #잔고 데이타를 가지고 온다.
    balance = bybit.fetch_positions(None, {'type':'Future'})
    if Rest == True:
        time.sleep(0.1)
                            
    amt = 0
    entryPrice = 0
    leverage = 0

    #평균 매입단가와 수량을 가지고 온다.
    #숏포지션을 잡았는지 여부 
    Already_Short = False

    #실제로 잔고 데이타의 포지션 정보 부분에서 해당 코인에 해당되는 정보를 넣어준다.
    for posi in balance:
        if posi['info']['symbol'] == Ticker.replace("/", "").replace(":USDT","") and posi['info']['side'] == "Sell":
            amt = float(posi['info']['size']) * -1

            #사이즈가 0미만이라면 포지션을 잡은거다 숏 포지션 잡았다!
            if amt < 0:
                Already_Short = True

            entryPrice = float(posi['info']['entry_price'])
            leverage = float(posi['info']['leverage'])
            break

    #숏포지션을 안잡았다면 롱 포지션을 뒤져주자!
    if Already_Short == False:
        for posi in balance:
            if posi['info']['symbol'] == Ticker.replace("/", "").replace(":USDT","") and posi['info']['side'] == "Buy":

                amt = float(posi['info']['size'])

                entryPrice = float(posi['info']['entry_price'])
                leverage = float(posi['info']['leverage'])
                break
        


    danger_rate = ((100.0 / leverage) * cut_rate) * 1.0

    #롱일 경우의 손절 가격을 정한다.
    stopPrice = entryPrice * (1.0 - danger_rate*0.01)

    #숏일 경우의 손절 가격을 정한다.
    if amt < 0:
        stopPrice = entryPrice * (1.0 + danger_rate*0.01)


    stopPrice = float(bybit.price_to_precision(Ticker, stopPrice))

    side_str = "sell"

    if amt < 0:
        side_str = "buy"

    side = 1

    if amt < 0:
        side = 2



    print("####Try Stop Loss ######################" , Ticker)


    print(bybit.create_order(Ticker, 'market', side_str, abs(amt), stopPrice, {'position_idx':side,'reduce_only': True,'close_on_trigger':True,'stopLossPrice':stopPrice}))



    print("####STOPLOSS SETTING DONE ######################" )





#스탑로스를 걸어놓는다. 해당 가격에 해당되면 바로 손절한다. 첫번째: 바이낸스 객체, 두번째: 코인 티커, 세번째: 손절 가격
#네번째 웹훅 알림에서 사용할때는 마지막 파라미터를 False로 넘겨서 사용한다. 트레이딩뷰 웹훅 강의 참조..
def SetStopLossPrice(bybit, Ticker, stopPrice, Rest = True):
    if Rest == True:
        time.sleep(0.1)


    #잔고 데이타를 가지고 온다.
    balance = bybit.fetch_positions(None, {'type':'Future'})
    if Rest == True:
        time.sleep(0.1)
                                       
    amt = 0


    #평균 매입단가와 수량을 가지고 온다.
    #숏포지션을 잡았는지 여부 
    Already_Short = False

    #실제로 잔고 데이타의 포지션 정보 부분에서 해당 코인에 해당되는 정보를 넣어준다.
    for posi in balance:
        if posi['info']['symbol'] == Ticker.replace("/", "").replace(":USDT","") and posi['info']['side'] == "Sell":
            amt = float(posi['info']['size']) * -1

            #사이즈가 0미만이라면 포지션을 잡은거다 숏 포지션 잡았다!
            if amt < 0:
                Already_Short = True


            break

    #숏포지션을 안잡았다면 롱 포지션을 뒤져주자!
    if Already_Short == False:
        for posi in balance:
            if posi['info']['symbol'] == Ticker.replace("/", "").replace(":USDT","") and posi['info']['side'] == "Buy":

                amt = float(posi['info']['size'])


                break
        

    side_str = "sell"

    if amt < 0:
        side_str = "buy"

    side = 1

    if amt < 0:
        side = 2




    stopPrice = float(bybit.price_to_precision(Ticker, stopPrice))


            
    print("####Try Stop Loss ######################", Ticker)


    print(bybit.create_order(Ticker, 'market', side_str, abs(amt), stopPrice, {'position_idx':side,'reduce_only': True,'close_on_trigger':True,'stopLossPrice':stopPrice}))



    print("####STOPLOSS SETTING DONE ######################" )







#양방향 모드를 위한 스탑로스 롱
def SetStopLossLongPrice(bybit, Ticker, stopPrice, Rest = True):


    #잔고 데이타를 가지고 온다.
    balance = bybit.fetch_positions(None, {'type':'Future'})
    if Rest == True:
        time.sleep(0.1)
                                       
    amt = 0


    for posi in balance:
        if posi['info']['symbol'] == Ticker.replace("/", "").replace(":USDT","") and posi['info']['side'] == "Buy":
            print("\n>>>>>>>>>>>>>>>>>>>>>>")
            pprint.pprint(posi)
            print(">>>>>>>>>>>>>>>>>>>>>>")

            amt = float(posi['info']['size'])


            break
    


    stopPrice = float(bybit.price_to_precision(Ticker, stopPrice))


        
    print("####Try Stop Loss ######################",Ticker)

    print(bybit.create_order(Ticker, 'market', 'sell', amt, stopPrice, {'position_idx':1,'reduce_only': True,'close_on_trigger':True,'stopLossPrice':stopPrice}))

    print("####STOPLOSS SETTING DONE ######################" )





#양방향 모드를 위한 스탑로스 숏
def SetStopLossShortPrice(bybit, Ticker, stopPrice, Rest = True):


    #잔고 데이타를 가지고 온다.
    balance = bybit.fetch_positions(None, {'type':'Future'})
    if Rest == True:
        time.sleep(0.1)
                                       
    amt = 0


    #실제로 잔고 데이타의 포지션 정보 부분에서 해당 코인에 해당되는 정보를 넣어준다.
    for posi in balance:
        if posi['info']['symbol'] == Ticker.replace("/", "").replace(":USDT","") and posi['info']['side'] == "Sell":
            print("\n>>>>>>>>>>>>>>>>>>>>>>")
            pprint.pprint(posi)
            print(">>>>>>>>>>>>>>>>>>>>>>")
            amt = float(posi['info']['size']) 

            break



    stopPrice = float(bybit.price_to_precision(Ticker, stopPrice))

 
    print("####Try Stop Loss ######################",Ticker)


    print(bybit.create_order(Ticker, 'market', 'buy', amt, stopPrice, {'position_idx':2,'reduce_only': True,'close_on_trigger':True,'stopLossPrice':stopPrice}))


    print("####STOPLOSS SETTING DONE ######################" )




#구매할 수량을 구한다.  첫번째: 돈(USDT), 두번째:코인 가격, 세번째: 비율 1.0이면 100%, 0.5면 50%
def GetAmount(usd, coin_price, rate):

    target = usd * rate 

    amout = target/coin_price

    #print("amout", amout)
    return amout

#거래할 코인의 현재가를 가져온다. 첫번째: 바이비트 객체, 두번째: 코인 티커
def GetCoinNowPrice(bybit,Ticker):
    coin_info = bybit.fetch_ticker(Ticker)
    coin_price = coin_info['last'] # coin_info['close'] == coin_info['last'] 

    return coin_price


        
#거래대금 폭발 여부 첫번째: 캔들 정보, 두번째: 이전 5개의 평균 거래량보다 몇 배 이상 큰지
#이전 캔들이 그 이전 캔들 5개의 평균 거래금액보다 몇 배이상 크면 거래량 폭발로 인지하고 True를 리턴해줍니다
#현재 캔들[-1]은 막 시작했으므로 이전 캔들[-2]을 보는게 맞다!
def IsVolumePung(ohlcv,st):

    Result = False
    try:
        avg_volume = (float(ohlcv['volume'].iloc[-3]) + float(ohlcv['volume'].iloc[-4]) + float(ohlcv['volume'].iloc[-5]) + float(ohlcv['volume'].iloc[-6]) + float(ohlcv['volume'].iloc[-7])) / 5.0
        if avg_volume * st < float(ohlcv['volume'].iloc[-2]):
            Result = True
    except Exception as e:
        print("IsVolumePung ---:", e)

    
    return Result



#내가 포지션 잡은 (가지고 있는) 코인 개수를 리턴하는 함수
def GetHasCoinCnt(bybit):

    #잔고 데이타 가져오기 
    balances = bybit.fetch_positions(None, {'type':'Future'})
    
    time.sleep(0.1)

    #선물 마켓에서 거래중인 코인을 가져옵니다.
    Tickers = bybit.load_markets().keys()
    print("-------------------")
    #선물 마켓에서 거래중인 코인을 가져옵니다.
        
    CoinCnt = 0
        #모든 선물 거래가능한 코인을 가져온다.
    for ticker in Tickers:

        if "/USDT:USDT" in ticker:
            Target_Coin_Symbol = ticker.replace("/", "").replace(":USDT","")

            amt = 0

            #숏포지션을 잡았는지 여부 
            Already_Short = False

            #실제로 잔고 데이타의 포지션 정보 부분에서 해당 코인에 해당되는 정보를 넣어준다.
            for posi in balances:
                if posi['info']['symbol'] == Target_Coin_Symbol and posi['info']['side'] == "Sell":
                    amt = float(posi['info']['size']) * -1

                    #사이즈가 0미만이라면 포지션을 잡은거다 숏 포지션 잡았다!
                    if amt < 0:
                        Already_Short = True


                    break

            #숏포지션을 안잡았다면 롱 포지션을 뒤져주자!
            if Already_Short == False:
                for posi in balances:
                    if posi['info']['symbol'] == Target_Coin_Symbol and posi['info']['side'] == "Buy":

                        amt = float(posi['info']['size'])
                
                        break


            if amt != 0:
                CoinCnt += 1


    return CoinCnt


#바이비트 선물 거래에서 거래량이 많은 코인 순위 (테더 선물 마켓)
def GetTopCoinList(bybit, top):
    print("--------------GetTopCoinList Start-------------------")

    #선물 마켓에서 거래중인 코인을 가져옵니다.
    Tickers = bybit.load_markets()
    
    dic_coin_money = dict()
    #모든 선물 거래가능한 코인을 가져온다.
    for ticker in Tickers:

        try: 

            if "/USDT:USDT" in ticker:
                time.sleep(0.1)
                data = bybit.fetch_ticker(ticker)
                print(ticker,"----- \n",data['baseVolume'] * data['close'])

                dic_coin_money[ticker] = data['baseVolume'] * data['close']

        except Exception as e:
            print("---:", e)


    dic_sorted_coin_money = sorted(dic_coin_money.items(), key = lambda x : x[1], reverse= True)


    coin_list = list()
    cnt = 0
    for coin_data in dic_sorted_coin_money:
        print("####-------------", coin_data[0], coin_data[1])
        cnt += 1
        if cnt <= top:
            coin_list.append(coin_data[0])
        else:
            break

    print("--------------GetTopCoinList End-------------------")

    return coin_list


#해당되는 리스트안에 해당 코인이 있는지 여부를 리턴하는 함수
def CheckCoinInList(CoinList,Ticker):
    InCoinOk = False
    for coinTicker in CoinList:
        if coinTicker == Ticker:
            InCoinOk = True
            break

    return InCoinOk
    
#최소 포지션 수량을 리턴합니다! 비트코인 0.001 이더리움 0.01 등..
def GetMinimumAmount(bybit,ticker):
    min_amount = 0.01
    Tickers = bybit.fetch_markets()
    for coin_info in Tickers:
        if coin_info['id'] == ticker.replace("/", "").replace(":USDT",""): #BTCUSDT로 넘어와야 되는데 실수로 BTC/USDT 티커를 넘길경우를 대비해 / 를 없애주는 로직!
            min_amount = coin_info['limits']['amount']['min']
            break
    return min_amount

#해당 티커의 모든 주문(스탑로스 리미트 주문 포함)을 취소한다!
def CancelAllOrder(bybit,ticker):
    bybit.cancel_all_orders(ticker)

    orders = bybit.fetch_orders(ticker,None,None,{'orderType': 'conditional'})

    for order in orders:
        if order['status'].strip() == "open" :
            print(bybit.cancel_order(order['id'],ticker,{'orderType': 'conditional','stop_order_id' : order['id']}))


#숏 주문에 대한 트레일링 스탑 기능입니다!
#현재 주문 시점을 기준으로 트레일링 스탑을 겁니다. 바이낸스와는 다르게 가격으로 스탑로스를 거는 것은 바이비트에서 지원하지 않습니다.
# https://blog.naver.com/zhanggo2/222670005498

def add_trailing_to_sell_order(bybit, ticker, ratio=0.2):
    # Trailing stop can only be placed when traders are holding an existing open position.
    # error returned if there isn't existing sell order

    # Need an adjustment for retracement since the price and allowed retracement float digit
    # numbers are different depending on the tickers

    '''
    price = bybit.fetch_ticker(ticker)['last']
    float_count = str(price)[::-1].find('.')

    retracement = round(float(float(price)*ratio/100), float_count)

    if retracement == 0:
        # Put minimum number to prevent failure with Stoploss err
        retracement = round(pow(0.1, float_count),float_count)

    print("{} Sell retracement {}".format(ticker, retracement))

    # bybit USDT perpetual doesn't support activationPrice -> only activates at current price
    params = {
        'symbol': ticker.replace("/", "").replace(":USDT",""),
        'side' : 'Sell',
        'trailing_stop': retracement, # cannot be less than 0, 0 means cancel TS
    }
                 
    return bybit.private_post_v5_position_trading_stop(params)
    '''
    
    return "Not Working"


#롱 주문에 대한 트레일링 스탑 기능입니다!
#현재 주문 시점을 기준으로 트레일링 스탑을 겁니다. 바이낸스와는 다르게 가격으로 스탑로스를 거는 것은 바이비트에서 지원하지 않습니다.
# https://blog.naver.com/zhanggo2/222670005498

def add_trailing_to_buy_order(bybit, ticker, ratio=0.2):
    # Trailing stop can only be placed when traders are holding an existing open position.
    # error returned if there isn't existing buy order

    # Need an adjustment for retracement since the price and allowed retracement float digit
    # numbers are different depending on the tickers
    '''
    price = bybit.fetch_ticker(ticker)['last']
    float_count = str(price)[::-1].find('.')

    retracement = round(float(float(price)*ratio/100), float_count)

    if retracement == 0:
        # Put minimum number to prevent failure with Stoploss err
        retracement = round(pow(0.1, float_count),float_count)

    print("{} Buy retracement {}".format(ticker, retracement))

    # bybit USDT perpetual doesn't support activationPrice -> only activates at current price
    params = {
        'symbol': ticker.replace("/", "").replace(":USDT",""),
        'side' : 'Buy',
        'trailing_stop': retracement, # cannot be less than 0, 0 means cancel TS
    }

    return bybit.private_post_v5_position_trading_stop(params)
    '''

    return "Not Working"



#현재 평가금액을 구한다!
def GetTotalRealMoney(balance):



    try:
        return float(balance['info']['result']['USDT']['equity'])
    except Exception as e:
        result = 0
        for data in balance['info']['result']['list']:
            for data2 in data['coin']:
                if data2['coin'] == 'USDT':
                    result = float(data2['equity'])
                    break
                
        return result
    

#코인의 평가 금액을 구한다!
#세번째 파라미터 posiSide에는  "Buy"나 "Sell" 을 넣습니다.
def GetCoinRealMoney(balance2,ticker,posiSide):

    Money = 0
    for posi in balance2:
        if posi['info']['symbol'] == ticker.replace("/", "").replace(":USDT","") and posi['info']['side'] == posiSide:
            #pprint.pprint(posi)
            
            try:
                Money = float(posi['info']['position_margin']) + float(posi['info']['occ_closing_fee']) + float(posi['info']['unrealised_pnl'])

            except Exception as e:
                Money = float(posi['initialMargin']) + float(posi['info']['unrealisedPnl'])

            break


    return Money

