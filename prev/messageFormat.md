#업비트 Json파일 구성 예

# dist -> 무조건 "upbit" 로 입력 
# ticker -> "KRW-BTC" ,"KRW-ETH" 등의 원화마켓 티커를 입력
# type -> "limit" 지정가매매, "market" 시장가매매, "cancel" 지정가주문 취소로 정의
# side -> "buy"는 매수, "sell"은 매도
# price_money -> 지정가 매매"limit"의 경우엔 !!!매매할 가격!!!, 시장가"market" 매매할 경우 !!!매수금액!!!
# amt -> 지정가 매매에 사용할 수량
# etc_num -> 추가 필요한 정보 있으면 넣을 넘버형 데이타 (현재 사용 안함 필요하면 쓰세용!) 
# etc_str -> 추가 필요한 정보 있으면 넣을 스트링형 데이타 (현재 사용 안함 필요하면 쓰세용!) 




#바이낸스 Json파일 구성 예

# dist -> 무조건 "binance" 로 입력 
# ticker -> "BTC/USDT" ,"ETH/USDT" 등의 선물마켓 티커를 입력 
# type -> "limit" 지정가매매, "market" 시장가매매, "cancel" 지정가주문 취소, 'stop' 스탑로스로 정의
# side -> "long"는 롱포지션, "short"은 숏포지션
# price_money -> 지정가 매매"limit"의 경우엔 진입 가격 혹은 청산 가격!
# amt -> 포지션 잡을 수량
# etc_num -> 스탑 로스의 경우 스탑로스 비중 (ex 0.2면 마이너스 20%에 스탑로스 )
# etc_str -> 추가 필요한 정보 있으면 넣을 스트링형 데이타 (현재 사용 안함 필요하면 쓰세용!) 


#바이비트 Json파일 구성 예

# dist -> 무조건 "bybit" 로 입력 
# ticker -> "BTC/USDT" ,"ETH/USDT" 등의 선물마켓 티커를 입력 
# type -> "limit" 지정가매매, "market" 시장가매매, "cancel" 지정가주문 취소, 'stop' 스탑로스로 정의
# side -> "long"는 롱포지션, "short"은 숏포지션
# price_money -> 지정가 매매"limit"의 경우엔 진입 가격 혹은 청산 가격!
# amt -> 포지션 잡을 수량
# etc_num -> 스탑 로스의 경우 스탑로스 비중 (ex 0.2면 마이너스 20%에 스탑로스 )
# etc_str -> 'open'의 경우 포지션 오픈, 'close'의 경우 포지선 종료 이걸 구분 안하면 양방향 포지션 매매가 됨(롱과 숏이 공존)