# '''

# 하다가 잘 안되시면 계속 내용이 추가되고 있는 아래 FAQ를 꼭꼭 체크하시고

# 주식/코인 자동매매 FAQ
# https://blog.naver.com/zacra/223203988739

# 그래도 안 된다면 구글링 해보시고
# 그래도 모르겠다면 클래스 댓글, 블로그 댓글, 단톡방( https://blog.naver.com/zacra/223111402375 )에 질문주세요! ^^

# 클래스 제작 완료 후 많은 시간이 흘렀고 그 사이 전략에 많은 발전이 있었습니다.
# 제가 직접 투자하고자 백테스팅으로 검증하여 더 안심하고 있는 자동매매 전략들을 블로그에 공개하고 있으니
# 완강 후 꼭 블로그&유튜브 심화 과정에 참여해 보세요! 기다릴께요!!

# 아래 빠른 자동매매 가이드 시간날 때 완독하시면 방향이 잡히실 거예요!
# https://blog.naver.com/zacra/223086628069

  
# '''
# import ccxt
# import time
# import pandas as pd
# import pprint
       
# import myBinance
# import keys.ende_key as ende_key  #암복호화키
# import keys.my_key as my_key    #업비트 시크릿 액세스키

# import json



# #암복호화 클래스 객체를 미리 생성한 키를 받아 생성한다.
# simpleEnDecrypt = myBinance.SimpleEnDecrypt(ende_key.ende_key)


# #암호화된 액세스키와 시크릿키를 읽어 복호화 한다.
# Binance_AccessKey = simpleEnDecrypt.decrypt(my_key.binance_access)
# Binance_ScretKey = simpleEnDecrypt.decrypt(my_key.binance_secret)


# # binance 객체 생성
# binanceX = ccxt.binance(config={
#     'apiKey': Binance_AccessKey, 
#     'secret': Binance_ScretKey,
#     'enableRateLimit': True,
#     'options': {
#         'defaultType': 'future'
#     }
# })


# #선물 마켓에서 거래중인 모든 코인을 가져옵니다.
# Tickers = binanceX.fetch_tickers()


# #나의 코인
# LovelyCoinList = ['BTC/USDT']

# #모든 선물 거래가능한 코인을 가져온다.
# for ticker in Tickers:

#     try: 

   
#         #하지만 여기서는 USDT 테더로 살수 있는 모든 선물 거래 코인들을 대상으로 돌려봅니다.
#         if "/USDT" in ticker:
#             Target_Coin_Ticker = ticker

#             #러블리 코인이 아니라면 스킵! 러블리 코인만 대상으로 한다!!
#             if myBinance.CheckCoinInList(LovelyCoinList,ticker) == False:
#                 continue

            
#             time.sleep(0.5)

#             Target_Coin_Symbol = ticker.replace("/", "").replace(":USDT", "")

                        
#             leverage = 10 #레버리지 10
#             test_amt = 0.001 #테스트할 수량!


            

#             #################################################################################################################
#             #영상엔 없지만 레버리지를 3으로 셋팅합니다! 
#             try:
#                 print(binanceX.fapiPrivate_post_leverage({'symbol': Target_Coin_Symbol, 'leverage': leverage}))
#             except Exception as e:
#                 try:
#                     print(binanceX.fapiprivate_post_leverage({'symbol': Target_Coin_Symbol, 'leverage': leverage}))
#                 except Exception as e:
#                     print("error:", e)
#             #앱이나 웹에서 레버리지를 바뀌면 바뀌니깐 주의하세요!!
#             #################################################################################################################


#             #잔고 데이타 가져오기 
#             balance = binanceX.fetch_balance(params={"type": "future"})
#             time.sleep(0.1)

#             amt_s = 0 
#             amt_b = 0
#             entryPrice_s = 0 #평균 매입 단가. 따라서 물을 타면 변경 된다.
#             entryPrice_b = 0 #평균 매입 단가. 따라서 물을 타면 변경 된다.


#             isolated = True #격리모드인지 


#             target_rate = 0.01 #목표 수익율


#             print("------")
#             #숏잔고
#             for posi in balance['info']['positions']:
#                 if posi['symbol'] == Target_Coin_Symbol and posi['positionSide'] == 'SHORT':
#                     print(posi)
#                     amt_s = float(posi['positionAmt'])
#                     entryPrice_s= float(posi['entryPrice'])
#                     leverage = float(posi['leverage'])
#                     isolated = posi['isolated']
#                     break


#             #롱잔고
#             for posi in balance['info']['positions']:
#                 if posi['symbol'] == Target_Coin_Symbol and posi['positionSide'] == 'LONG':
#                     print(posi)
#                     amt_b = float(posi['positionAmt'])
#                     entryPrice_b = float(posi['entryPrice'])
#                     leverage = float(posi['leverage'])
#                     isolated = posi['isolated']
#                     break



#             #################################################################################################################
#             #영상엔 없지만 격리모드가 아니라면 격리모드로 처음 포지션 잡기 전에 셋팅해 줍니다,.
#             if isolated == False:
#                 try:
#                     print(binanceX.fapiPrivate_post_margintype({'symbol': Target_Coin_Symbol, 'marginType': 'ISOLATED'}))
#                 except Exception as e:
#                     try:
#                         print(binanceX.fapiprivate_post_margintype({'symbol': Target_Coin_Symbol, 'marginType': 'ISOLATED'}))
#                     except Exception as e:
#                         print("error:", e)
#             #################################################################################################################    


            
#             #해당 코인 가격을 가져온다.
#             coin_price = myBinance.GetCoinNowPrice(binanceX, Target_Coin_Ticker)


#             #롱 포지션이 없을 경우
#             if abs(amt_b) == 0:

            
#                 #롱 시장가 주문!
#                 params = {
#                     'positionSide': 'LONG'
#                 }
#                 #data = binanceX.create_market_buy_order(Target_Coin_Ticker, test_amt, params)
#                 data = binanceX.create_order(Target_Coin_Ticker, 'market', 'buy', test_amt, None, params)
#                 print(data)


#                 #예로 1% 상승한 가격에 지정가 주문으로 롱 포지션 종료하려면..
#                 target_price = data['price'] * (1.0 + target_rate)
                            

#                 #롱 포지션 지정가 종료 주문!!     
#                 params = {
#                     'positionSide': 'LONG'
#                 }
#                 #binanceX.create_limit_sell_order(Target_Coin_Ticker, data['amount'], target_price, params)
#                 binanceX.create_order(Target_Coin_Ticker, 'limit', 'sell', test_amt, target_price, params)

#                 stop_price = data['price'] * (1.0 - target_rate)

                
#                 #스탑로스!
#                 myBinance.SetStopLossLongPrice(binanceX,Target_Coin_Ticker,stop_price)


#             else:
#                 #롱 포지션이 있는 경우
#                 if abs(amt_b) > 0:
#                     #롱 수익율을 구한다!
#                     revenue_rate_b = (coin_price - entryPrice_b) / entryPrice_b * 100.0

#                     print("revenue_rate_b : ", revenue_rate_b)




#             #숏 포지션이 없을 경우
#             if abs(amt_s) == 0:


#                 #숏 시장가 주문!
#                 params = {
#                     'positionSide': 'SHORT'
#                 }
#                 #data = binanceX.create_market_sell_order(Target_Coin_Ticker, test_amt,params)
#                 data = binanceX.create_order(Target_Coin_Ticker, 'market', 'sell', test_amt, None, params)



#                 #예로 1% 상승한 가격에 지정가 주문으로 숏 포지션 종료하려면..
#                 target_price = data['price'] * (1.0 - target_rate)
                            

#                 #롱 포지션 지정가 종료 주문!!                 
#                 params = {
#                     'positionSide': 'SHORT'
#                 }
#                 #binanceX.create_limit_buy_order(Target_Coin_Ticker, data['amount'], target_price ,params)
#                 binanceX.create_order(Target_Coin_Ticker, 'limit', 'buy', test_amt, target_price, params)


#                 stop_price = data['price'] * (1.0 + target_rate)
                

#                 #스탑로스!
#                 myBinance.SetStopLossShortPrice(binanceX,Target_Coin_Ticker,stop_price)


#             else:
#                 #숏 포지션이 있는 경우
#                 if abs(amt_s) > 0:

#                     #숏 수익율을 구한다!
#                     revenue_rate_s = (entryPrice_s - coin_price) / entryPrice_s * 100.0

#                     print("revenue_rate_s : ", revenue_rate_s)



#     except Exception as e:
#         print("error:", e)








