"""
제공된 HTML 테이블에서 주식 데이터를 추출하여 엑셀 파일로 저장합니다.
"""
from crawler import YahooFinanceCrawler
import sys


def main():
    """HTML 문자열에서 직접 데이터 추출"""
    crawler = YahooFinanceCrawler()
    
    # 사용자가 제공한 HTML (일부만 표시됨)
    # 실제로는 전체 HTML이 필요합니다
    html_content = """
    <table class="yf-1uayyp1 bd">
    <!-- 여기에 전체 HTML 테이블 내용이 들어갑니다 -->
    </table>
    """
    
    # 또는 파일에서 읽기
    if len(sys.argv) > 1:
        html_file = sys.argv[1]
        try:
            with open(html_file, 'r', encoding='utf-8') as f:
                html_content = f.read()
        except FileNotFoundError:
            print(f"파일을 찾을 수 없습니다: {html_file}")
            return
    else:
        print("사용법: python parse_html.py <html_file>")
        print("또는 HTML 내용을 input.html 파일로 저장하세요.")
        return
    
    # HTML 파싱
    stocks = crawler.parse_html_table(html_content)
    
    if stocks:
        # 50개로 제한
        stocks = stocks[:50]
        print(f"총 {len(stocks)}개의 주식 데이터를 추출했습니다.")
        
        # 엑셀 파일로 저장
        crawler.save_to_excel(stocks, 'stock_data.xlsx')
        
        # 콘솔에 미리보기 출력
        print("\n=== 추출된 데이터 미리보기 ===")
        for i, stock in enumerate(stocks[:5], 1):
            print(f"\n{i}. {stock.get('Symbol', 'N/A')} - {stock.get('Name', 'N/A')}")
            print(f"   가격: {stock.get('Price', 'N/A')}, 변동률: {stock.get('Change %', 'N/A')}")
    else:
        print("추출된 데이터가 없습니다. HTML 형식을 확인해주세요.")


if __name__ == "__main__":
    main()

