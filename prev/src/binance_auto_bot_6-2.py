'''

하다가 잘 안되시면 계속 내용이 추가되고 있는 아래 FAQ를 꼭꼭 체크하시고

주식/코인 자동매매 FAQ
https://blog.naver.com/zacra/223203988739

그래도 안 된다면 구글링 해보시고
그래도 모르겠다면 클래스 댓글, 블로그 댓글, 단톡방( https://blog.naver.com/zacra/223111402375 )에 질문주세요! ^^

클래스 제작 완료 후 많은 시간이 흘렀고 그 사이 전략에 많은 발전이 있었습니다.
제가 직접 투자하고자 백테스팅으로 검증하여 더 안심하고 있는 자동매매 전략들을 블로그에 공개하고 있으니
완강 후 꼭 블로그&유튜브 심화 과정에 참여해 보세요! 기다릴께요!!

아래 빠른 자동매매 가이드 시간날 때 완독하시면 방향이 잡히실 거예요!
https://blog.naver.com/zacra/223086628069

  
'''
import ccxt
import time
import pandas as pd
import pprint


#챕터7까지 진행하시면서 봇은 점차 완성이 되어 갑니다!!!
#챕터6까지 완강 후 봇을 돌리셔도 되지만 이왕이면 7까지 완강하신 후 돌리시는 걸 추천드려요!


access = "A0X27AGgl8UYAC2cFMYzyrMlfxn1DsgrxoGjLVc2"          # 본인 값으로 변경
secret = "JkaADmlhsKOAcOlSsYw1WJ7DIpSnM9gGzP7dLRBx"          # 본인 값으로 변경

# binance 객체 생성
binance = ccxt.binance(config={
    'apiKey': access, 
    'secret': secret,
    'enableRateLimit': True,
    'options': {
        'defaultType': 'future'
    }
})

#포지션 잡을 코인을 설정합니다.
Target_Coin_Ticker = "BTC/USDT"
Target_Coin_Symbol = "BTCUSDT"

#해당 코인의 정보를 가져옵니다
btc = binance.fetch_ticker(Target_Coin_Ticker)
#현재 종가 즉 현재가를 읽어옵니다.
btc_price = btc['close']

print(btc['close'])


#시장가 taker 0.04, 지정가 maker 0.02

# create_market_sell_order -> create_order 주문으로 변경하는걸 권장드립니다. 아래 처럼요!
# create_market_buy_order -> create_order 주문으로 변경하는걸 권장드립니다. 아래 처럼요!
# create_limit_sell_order -> create_order 주문으로 변경하는걸 권장드립니다. 아래 처럼요!
# create_limit_sell_order -> create_order 주문으로 변경하는걸 권장드립니다. 아래 처럼요!
# 기존 방식도 동작하지만 코드에서 음영처리 되고 리턴되는 값이 없는 식으로 코드가 변경되어서 create_order 주문으로 사용하세요!!!



#시장가 숏 포지션 잡기 
#print(binance.create_market_sell_order(Target_Coin_Ticker, 0.002))
#print(binance.create_order(Target_Coin_Ticker, 'market', 'sell', 0.002, None))

#시장가 롱 포지션 잡기 
#print(binance.create_market_buy_order(Target_Coin_Ticker, 0.001))
#print(binance.create_order(Target_Coin_Ticker, 'market', 'buy', 0.002, None))


time.sleep(0.1)

#잔고 데이타 가져오기 
balance = binance.fetch_balance(params={"type": "future"})
#pprint.pprint(balance)

print(balance['USDT'])

amt = 0 #수량 정보 0이면 매수전(포지션 잡기 전), 양수면 롱 포지션 상태, 음수면 숏 포지션 상태
entryPrice = 0 #평균 매입 단가. 따라서 물을 타면 변경 된다.
leverage = 1   #레버리지, 앱이나 웹에서 설정된 값을 가져온다.
unrealizedProfit = 0 #미 실현 손익..그냥 참고용 

#실제로 잔고 데이타의 포지션 정보 부분에서 해당 코인에 해당되는 정보를 넣어준다.
for posi in balance['info']['positions']:
    if posi['symbol'] == Target_Coin_Symbol:
        leverage = float(posi['leverage'])
        entryPrice = float(posi['entryPrice'])
        unrealizedProfit = float(posi['unrealizedProfit'])
        amt = float(posi['positionAmt'])

print("amt:",amt)
print("entryPrice:",entryPrice)
print("leverage:",leverage)
print("unrealizedProfit:",unrealizedProfit)

#음수를 제거한 절대값 수량 ex -0.1 -> 0.1 로 바꿔준다.
abs_amt = abs(amt)

#0.1%증가한 금액을 의미합니다
entryPrice = entryPrice * 1.001


#지정가 숏 포지션 잡기 
#print(binance.create_limit_sell_order(Target_Coin_Ticker, abs_amt, entryPrice))
#print(binance.create_order(Target_Coin_Ticker, 'limit', 'sell', abs_amt, entryPrice))

#지정가 롱 포지션 잡기 
#print(binance.create_limit_buy_order(Target_Coin_Ticker, abs_amt, btc_price))
#print(binance.create_order(Target_Coin_Ticker, 'limit', 'buy', abs_amt, entryPrice))






