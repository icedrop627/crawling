"""
사용자가 제공한 HTML 테이블에서 주식 데이터를 추출합니다.
"""
from crawler import YahooFinanceCrawler


# 사용자가 제공한 HTML (일부)
PROVIDED_HTML = """<table class="yf-1uayyp1 bd"><thead class="yf-1uayyp1"><tr class="yf-1uayyp1"><th data-testid-header="ticker" class="[&amp;_.symbol]:tw-text-md yf-1uayyp1 so lpin shad"><div class="colCont yf-1uayyp1"> Symbol</div></th><th data-testid-header="companyshortname.raw" class="leftAlignHeader companyName yf-1uayyp1 so"><div class="colCont yf-1uayyp1"> Name</div></th><th data-testid-header="sparkline" class=" yf-1uayyp1"><div class="colCont yf-1uayyp1"> <span data-svelte-h="svelte-1uypmr0">&nbsp;</span></div></th><th data-testid-header="intradayprice" class="yf-1uayyp1 so"><div class="colCont yf-1uayyp1"> <div class="container yf-1d5e06g"><span>Price</span> </div></div></th><th data-testid-header="intradaypricechange" class="yf-1uayyp1 so"><div class="colCont yf-1uayyp1"> Change</div></th><th data-testid-header="percentchange" class="yf-1uayyp1 so sorted"><div class="colCont yf-1uayyp1"><div aria-hidden="true" class="icon fin-icon inherit-icn sz-medium yf-sv6wwp"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M16.59 8.59 12 13.17 7.41 8.59 6 10l6 6 6-6z"></path></svg></div> Change %</div></th><th data-testid-header="dayvolume" class="yf-1uayyp1 so"><div class="colCont yf-1uayyp1"> Volume</div></th><th data-testid-header="avgdailyvol3m" class="yf-1uayyp1 so"><div class="colCont yf-1uayyp1"> Avg Vol (3M)</div></th><th data-testid-header="intradaymarketcap" class="yf-1uayyp1 so"><div class="colCont yf-1uayyp1"> Market Cap</div></th><th data-testid-header="peratio.lasttwelvemonths" class="yf-1uayyp1 so"><div class="colCont yf-1uayyp1"> <div class="yf-10yevti"><span>P/E Ratio </span><span>(TTM) </span></div></div></th><th data-testid-header="fiftytwowkpercentchange" class="yf-1uayyp1 so"><div class="colCont yf-1uayyp1"> <div class="yf-10yevti"><span>52 Wk </span><span>Change % </span></div></div></th><th data-testid-header="fiftyTwoWeekRange" class=" yf-1uayyp1"><div class="colCont yf-1uayyp1"> 52 Wk Range</div></th> </tr></thead> <tbody>"""


def main():
    """제공된 HTML에서 데이터 추출"""
    crawler = YahooFinanceCrawler()
    
    # 사용자가 제공한 HTML을 파일로 저장하거나 직접 사용
    print("HTML 테이블에서 주식 데이터를 추출합니다...")
    
    # 파일에서 읽기 시도
    try:
        with open('input.html', 'r', encoding='utf-8') as f:
            html_content = f.read()
        print("input.html 파일에서 읽었습니다.")
    except FileNotFoundError:
        print("input.html 파일을 찾을 수 없습니다.")
        print("전체 HTML 테이블을 input.html 파일로 저장하거나,")
        print("브라우저에서 페이지 소스 보기(Ctrl+U)로 전체 HTML을 복사하여 저장하세요.")
        return
    
    # HTML 파싱
    stocks = crawler.parse_html_table(html_content)
    
    if stocks:
        # 50개로 제한
        stocks = stocks[:50]
        print(f"\n총 {len(stocks)}개의 주식 데이터를 추출했습니다.")
        
        # 엑셀 파일로 저장
        output_file = 'stock_data.xlsx'
        crawler.save_to_excel(stocks, output_file)
        
        # 미리보기 출력
        print("\n=== 추출된 데이터 미리보기 (처음 5개) ===")
        for i, stock in enumerate(stocks[:5], 1):
            print(f"\n{i}. {stock.get('Symbol', 'N/A')} - {stock.get('Name', 'N/A')}")
            print(f"   가격: ${stock.get('Price', 'N/A')}")
            print(f"   변동: {stock.get('Change', 'N/A')} ({stock.get('Change %', 'N/A')})")
            print(f"   거래량: {stock.get('Volume', 'N/A')}")
            print(f"   시가총액: {stock.get('Market Cap', 'N/A')}")
    else:
        print("\n추출된 데이터가 없습니다.")
        print("HTML 형식을 확인해주세요. <table> 태그와 <tbody> 내부의 <tr> 태그가 필요합니다.")


if __name__ == "__main__":
    main()

