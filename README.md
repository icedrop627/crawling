# Yahoo Finance 주식 데이터 크롤러

Yahoo Finance의 주식 테이블 데이터를 자동으로 크롤링하여 엑셀 파일로 저장하는 도구입니다.

## 설치 방법

```bash
pip install -r requirements.txt
```

## 사용 방법

### 간단한 사용 (권장)

**Python 파일 하나만 실행하면 자동으로 데이터를 가져옵니다!**

```bash
python stock_crawler.py
```

기본적으로 Yahoo Finance의 상승주(day gainers) 페이지에서 최대 50개의 데이터를 가져옵니다.

### 다른 페이지 크롤링

URL을 인자로 전달하여 다른 페이지도 크롤링할 수 있습니다:

```bash
# 상승주
python stock_crawler.py https://finance.yahoo.com/screener/predefined/day_gainers

# 하락주
python stock_crawler.py https://finance.yahoo.com/screener/predefined/day_losers

# 거래량 상위
python stock_crawler.py https://finance.yahoo.com/screener/predefined/most_actives
```

### 작동 원리

1. 먼저 간단한 HTTP 요청(requests)으로 시도합니다 (빠름)
2. 실패하면 브라우저 자동화(Selenium)를 사용합니다 (느리지만 JavaScript 페이지도 처리 가능)

## 출력 형식

엑셀 파일에는 다음 컬럼들이 포함됩니다:

- Symbol (티커)
- Name (회사명)
- Price (가격)
- Change (변동액)
- Change % (변동률)
- Volume (거래량)
- Avg Vol (3M) (3개월 평균 거래량)
- Market Cap (시가총액)
- P/E Ratio (TTM) (주가수익비율)
- 52 Wk Change % (52주 변동률)
- 52 Wk Range (52주 범위)

## 주의사항

- Yahoo Finance는 웹 스크래핑을 제한할 수 있습니다. 적절한 User-Agent를 사용하고 있습니다.
- 너무 많은 요청을 보내지 않도록 주의하세요.
- 데이터는 참고용으로만 사용하세요.
- Selenium을 사용하는 경우 Chrome 브라우저가 필요합니다 (자동으로 ChromeDriver를 다운로드합니다).
- 첫 실행 시 ChromeDriver 다운로드로 인해 시간이 걸릴 수 있습니다.

