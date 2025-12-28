"""
Yahoo Finance 주식 데이터 크롤러
테이블에서 주식 정보를 추출하여 엑셀 파일로 저장합니다.
"""
import re
import requests
from bs4 import BeautifulSoup
import pandas as pd
from typing import List, Dict
import time


class YahooFinanceCrawler:
    """Yahoo Finance 주식 데이터 크롤러 클래스"""
    
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        self.base_url = "https://finance.yahoo.com"
    
    def parse_html_table(self, html_content: str) -> List[Dict]:
        """
        HTML 테이블에서 주식 데이터를 추출합니다.
        
        Args:
            html_content: HTML 문자열
            
        Returns:
            주식 데이터 딕셔너리 리스트
        """
        soup = BeautifulSoup(html_content, 'html.parser')
        rows = soup.find_all('tr', {'data-testid': 'data-table-v2-row'})
        
        stocks = []
        for row in rows:
            try:
                stock_data = self._extract_row_data(row)
                if stock_data:
                    stocks.append(stock_data)
            except Exception as e:
                print(f"행 파싱 오류: {e}")
                continue
        
        return stocks
    
    def _extract_row_data(self, row) -> Dict:
        """개별 행에서 데이터를 추출합니다."""
        stock = {}
        
        # Symbol (티커)
        ticker_cell = row.find('td', {'data-testid-cell': 'ticker'})
        if ticker_cell:
            symbol_link = ticker_cell.find('a', {'data-testid': 'table-cell-ticker'})
            if symbol_link:
                symbol_span = symbol_link.find('span', class_='symbol')
                if symbol_span:
                    stock['Symbol'] = symbol_span.get_text(strip=True)
        
        # Name (회사명)
        name_cell = row.find('td', {'data-testid-cell': 'companyshortname.raw'})
        if name_cell:
            name_div = name_cell.find('div', class_='companyName')
            if name_div:
                stock['Name'] = name_div.get_text(strip=True)
        
        # Price (가격)
        price_cell = row.find('td', {'data-testid-cell': 'intradayprice'})
        if price_cell:
            price_streamer = price_cell.find('fin-streamer', {'data-field': 'regularMarketPrice'})
            if price_streamer:
                stock['Price'] = price_streamer.get('data-value', price_streamer.get_text(strip=True))
        
        # Change (변동액)
        change_cell = row.find('td', {'data-testid-cell': 'intradaypricechange'})
        if change_cell:
            change_streamer = change_cell.find('fin-streamer', {'data-field': 'regularMarketChange'})
            if change_streamer:
                stock['Change'] = change_streamer.get('data-value', change_streamer.get_text(strip=True))
        
        # Change % (변동률)
        percent_cell = row.find('td', {'data-testid-cell': 'percentchange'})
        if percent_cell:
            percent_streamer = percent_cell.find('fin-streamer', {'data-field': 'regularMarketChangePercent'})
            if percent_streamer:
                stock['Change %'] = percent_streamer.get('data-value', percent_streamer.get_text(strip=True))
        
        # Volume (거래량)
        volume_cell = row.find('td', {'data-testid-cell': 'dayvolume'})
        if volume_cell:
            volume_streamer = volume_cell.find('fin-streamer', {'data-field': 'regularMarketVolume'})
            if volume_streamer:
                stock['Volume'] = volume_streamer.get('data-value', volume_streamer.get_text(strip=True))
        
        # Avg Vol (3M) (3개월 평균 거래량)
        avgvol_cell = row.find('td', {'data-testid-cell': 'avgdailyvol3m'})
        if avgvol_cell:
            stock['Avg Vol (3M)'] = avgvol_cell.get_text(strip=True)
        
        # Market Cap (시가총액)
        marketcap_cell = row.find('td', {'data-testid-cell': 'intradaymarketcap'})
        if marketcap_cell:
            marketcap_streamer = marketcap_cell.find('fin-streamer', {'data-field': 'marketCap'})
            if marketcap_streamer:
                stock['Market Cap'] = marketcap_streamer.get('data-value', marketcap_streamer.get_text(strip=True))
        
        # P/E Ratio (TTM)
        pe_cell = row.find('td', {'data-testid-cell': 'peratio.lasttwelvemonths'})
        if pe_cell:
            pe_text = pe_cell.get_text(strip=True)
            stock['P/E Ratio (TTM)'] = pe_text if pe_text != '--' else None
        
        # 52 Wk Change %
        wk52_change_cell = row.find('td', {'data-testid-cell': 'fiftytwowkpercentchange'})
        if wk52_change_cell:
            wk52_streamer = wk52_change_cell.find('fin-streamer', {'data-field': 'fiftyTwoWeekChangePercent'})
            if wk52_streamer:
                stock['52 Wk Change %'] = wk52_streamer.get('data-value', wk52_streamer.get_text(strip=True))
        
        # 52 Wk Range
        wk52_range_cell = row.find('td', {'data-testid-cell': 'fiftyTwoWeekRange'})
        if wk52_range_cell:
            labels = wk52_range_cell.find('div', class_='labels')
            if labels:
                spans = labels.find_all('span')
                if len(spans) >= 2:
                    stock['52 Wk Range'] = f"{spans[0].get_text(strip=True)} - {spans[1].get_text(strip=True)}"
        
        return stock if stock else None
    
    def crawl_from_url(self, url: str, max_rows: int = 50) -> List[Dict]:
        """
        URL에서 주식 데이터를 크롤링합니다.
        
        Args:
            url: Yahoo Finance URL
            max_rows: 최대 추출할 행 수
            
        Returns:
            주식 데이터 딕셔너리 리스트
        """
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            stocks = self.parse_html_table(response.text)
            return stocks[:max_rows]
        except Exception as e:
            print(f"URL 크롤링 오류: {e}")
            return []
    
    def save_to_excel(self, stocks: List[Dict], filename: str = 'stock_data.xlsx'):
        """
        주식 데이터를 엑셀 파일로 저장합니다.
        
        Args:
            stocks: 주식 데이터 딕셔너리 리스트
            filename: 저장할 파일명
        """
        if not stocks:
            print("저장할 데이터가 없습니다.")
            return
        
        # 데이터 정리 및 포맷팅
        df_data = []
        for stock in stocks:
            row = {}
            row['Symbol'] = stock.get('Symbol', '')
            row['Name'] = stock.get('Name', '')
            row['Price'] = self._format_number(stock.get('Price', ''))
            row['Change'] = self._format_number(stock.get('Change', ''))
            row['Change %'] = self._format_percent(stock.get('Change %', ''))
            row['Volume'] = self._format_number(stock.get('Volume', ''))
            row['Avg Vol (3M)'] = stock.get('Avg Vol (3M)', '')
            row['Market Cap'] = self._format_market_cap(stock.get('Market Cap', ''))
            row['P/E Ratio (TTM)'] = stock.get('P/E Ratio (TTM)', '')
            row['52 Wk Change %'] = self._format_percent(stock.get('52 Wk Change %', ''))
            row['52 Wk Range'] = stock.get('52 Wk Range', '')
            df_data.append(row)
        
        df = pd.DataFrame(df_data)
        df.to_excel(filename, index=False, engine='openpyxl')
        print(f"데이터가 {filename}에 저장되었습니다. (총 {len(df_data)}개 행)")
    
    def _format_number(self, value):
        """숫자 포맷팅"""
        if not value or value == '':
            return ''
        try:
            # data-value 속성에서 가져온 경우
            if isinstance(value, str) and value.replace('.', '').replace('-', '').isdigit():
                num = float(value)
                return f"{num:,.2f}" if num != int(num) else f"{int(num):,}"
            return value
        except:
            return value
    
    def _format_percent(self, value):
        """퍼센트 포맷팅"""
        if not value or value == '':
            return ''
        try:
            num = float(value)
            sign = '+' if num >= 0 else ''
            return f"{sign}{num:.2f}%"
        except:
            return value
    
    def _format_market_cap(self, value):
        """시가총액 포맷팅"""
        if not value or value == '':
            return ''
        try:
            num = float(value)
            if num >= 1e12:
                return f"${num/1e12:.3f}T"
            elif num >= 1e9:
                return f"${num/1e9:.3f}B"
            elif num >= 1e6:
                return f"${num/1e6:.3f}M"
            else:
                return f"${num:,.0f}"
        except:
            return value


def main():
    """메인 함수"""
    crawler = YahooFinanceCrawler()
    
    # 사용자가 제공한 HTML을 파일에서 읽거나 직접 사용할 수 있습니다
    # 여기서는 URL을 사용하는 예시를 보여드립니다
    
    # 방법 1: HTML 파일에서 읽기
    try:
        with open('input.html', 'r', encoding='utf-8') as f:
            html_content = f.read()
        stocks = crawler.parse_html_table(html_content)
        print(f"HTML 파일에서 {len(stocks)}개의 주식 데이터를 추출했습니다.")
    except FileNotFoundError:
        print("input.html 파일을 찾을 수 없습니다.")
        print("Yahoo Finance URL을 사용하거나 HTML을 input.html 파일로 저장해주세요.")
        
        # 방법 2: URL에서 크롤링 (예시)
        # 예시 URL - 실제 사용 시 원하는 Yahoo Finance 페이지 URL을 사용하세요
        # url = "https://finance.yahoo.com/screener/predefined/day_gainers"
        # stocks = crawler.crawl_from_url(url, max_rows=50)
        stocks = []
    
    if stocks:
        # 50개로 제한
        stocks = stocks[:50]
        crawler.save_to_excel(stocks, 'stock_data.xlsx')
    else:
        print("추출된 데이터가 없습니다.")


if __name__ == "__main__":
    main()

