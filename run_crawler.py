"""
Yahoo Finance 주식 데이터 크롤러 실행 스크립트
사용자가 제공한 HTML 테이블에서 최대 50개의 주식 데이터를 추출하여 엑셀 파일로 저장합니다.
"""
from crawler import YahooFinanceCrawler
import os


def main():
    """메인 실행 함수"""
    crawler = YahooFinanceCrawler()
    
    print("=" * 60)
    print("Yahoo Finance 주식 데이터 크롤러")
    print("=" * 60)
    
    # HTML 파일 확인
    html_file = 'input.html'
    
    if not os.path.exists(html_file):
        print(f"\n❌ {html_file} 파일을 찾을 수 없습니다.")
        print("\n사용 방법:")
        print("1. Yahoo Finance 페이지를 브라우저에서 엽니다")
        print("2. F12를 눌러 개발자 도구를 엽니다")
        print("3. Elements 탭에서 <table> 태그를 찾습니다")
        print("4. <table> 태그를 우클릭 > Copy > Copy outerHTML")
        print("5. 복사한 내용을 input.html 파일로 저장합니다")
        print("\n또는 페이지 소스 보기(Ctrl+U)로 전체 HTML을 복사하여 저장하세요.")
        return
    
    # HTML 파일 읽기
    try:
        with open(html_file, 'r', encoding='utf-8') as f:
            html_content = f.read()
        print(f"\n✓ {html_file} 파일을 읽었습니다.")
    except Exception as e:
        print(f"\n❌ 파일 읽기 오류: {e}")
        return
    
    # HTML 파싱
    print("\n데이터 추출 중...")
    stocks = crawler.parse_html_table(html_content)
    
    if not stocks:
        print("\n❌ 추출된 데이터가 없습니다.")
        print("HTML 형식을 확인해주세요. <table> 태그와 <tbody> 내부의 <tr> 태그가 필요합니다.")
        return
    
    # 50개로 제한
    original_count = len(stocks)
    stocks = stocks[:50]
    
    print(f"✓ 총 {len(stocks)}개의 주식 데이터를 추출했습니다.")
    if original_count > 50:
        print(f"  (원본 데이터: {original_count}개, 50개로 제한)")
    
    # 엑셀 파일로 저장
    output_file = 'stock_data.xlsx'
    try:
        crawler.save_to_excel(stocks, output_file)
        print(f"\n✓ 데이터가 '{output_file}' 파일로 저장되었습니다.")
    except Exception as e:
        print(f"\n❌ 엑셀 파일 저장 오류: {e}")
        return
    
    # 미리보기 출력
    print("\n" + "=" * 60)
    print("데이터 미리보기 (처음 5개)")
    print("=" * 60)
    for i, stock in enumerate(stocks[:5], 1):
        print(f"\n{i}. {stock.get('Symbol', 'N/A')} - {stock.get('Name', 'N/A')}")
        print(f"   가격: ${stock.get('Price', 'N/A')}")
        print(f"   변동: {stock.get('Change', 'N/A')} ({stock.get('Change %', 'N/A')})")
        print(f"   거래량: {stock.get('Volume', 'N/A')}")
        print(f"   시가총액: {stock.get('Market Cap', 'N/A')}")
    
    if len(stocks) > 5:
        print(f"\n... 외 {len(stocks) - 5}개 더")
    
    print("\n" + "=" * 60)
    print("완료!")
    print("=" * 60)


if __name__ == "__main__":
    main()

