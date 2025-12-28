"""
Yahoo Finance 주식 데이터 자동 크롤러
Python 파일 하나만 실행하면 자동으로 데이터를 가져와 엑셀 파일로 저장합니다.
"""
from crawler import YahooFinanceCrawler
import time
import sys


def crawl_with_selenium(url: str, max_rows: int = 50):
    """
    Selenium을 사용하여 Yahoo Finance 페이지에서 데이터를 크롤링합니다.
    JavaScript로 동적 로딩되는 페이지에 필요합니다.
    """
    try:
        from selenium import webdriver
        from selenium.webdriver.chrome.service import Service
        from selenium.webdriver.chrome.options import Options
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        from webdriver_manager.chrome import ChromeDriverManager
    except ImportError:
        print("❌ Selenium이 설치되지 않았습니다.")
        print("다음 명령어로 설치하세요: pip install selenium webdriver-manager")
        return []
    
    print("🌐 브라우저를 시작하는 중...")
    
    # Chrome 옵션 설정
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # 브라우저 창을 띄우지 않음
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
    
    driver = None
    try:
        # ChromeDriver 자동 설치 및 설정
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        print(f"📡 페이지 로딩 중: {url}")
        driver.get(url)
        
        # 테이블이 로드될 때까지 대기 (최대 30초)
        print("⏳ 데이터 로딩 대기 중...")
        wait = WebDriverWait(driver, 30)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'tr[data-testid="data-table-v2-row"]')))
        
        # 추가 대기 (JavaScript 렌더링 완료를 위해)
        time.sleep(3)
        
        # HTML 가져오기
        html_content = driver.page_source
        
        # 크롤러로 파싱
        crawler = YahooFinanceCrawler()
        stocks = crawler.parse_html_table(html_content)
        
        return stocks[:max_rows] if stocks else []
        
    except Exception as e:
        print(f"❌ Selenium 크롤링 오류: {e}")
        return []
    finally:
        if driver:
            driver.quit()
            print("🔒 브라우저를 종료했습니다.")


def crawl_with_requests(url: str, max_rows: int = 50):
    """
    requests를 사용하여 Yahoo Finance 페이지에서 데이터를 크롤링합니다.
    간단하지만 JavaScript로 동적 로딩되는 경우 작동하지 않을 수 있습니다.
    """
    print(f"📡 페이지 요청 중: {url}")
    crawler = YahooFinanceCrawler()
    stocks = crawler.crawl_from_url(url, max_rows)
    return stocks


def main():
    """메인 실행 함수"""
    print("=" * 70)
    print("Yahoo Finance 주식 데이터 자동 크롤러")
    print("=" * 70)
    
    # Yahoo Finance URL 설정
    # 사용자가 원하는 페이지 URL로 변경 가능
    # 예시: 상승주, 하락주, 거래량 상위 등
    default_url = "https://finance.yahoo.com/screener/predefined/day_gainers"
    
    # 명령줄 인자로 URL 받기
    if len(sys.argv) > 1:
        url = sys.argv[1]
    else:
        url = default_url
    
    max_rows = 50
    
    print(f"\n📊 크롤링 대상: {url}")
    print(f"📈 최대 추출 개수: {max_rows}개\n")
    
    # 방법 1: requests로 시도 (빠르지만 JavaScript 페이지는 실패할 수 있음)
    print("방법 1: 간단한 HTTP 요청 시도 중...")
    stocks = crawl_with_requests(url, max_rows)
    
    # 방법 2: 실패하면 Selenium 사용 (느리지만 JavaScript 페이지도 처리 가능)
    if not stocks:
        print("\n방법 1 실패. 방법 2: 브라우저 자동화 시도 중...")
        print("(이 방법은 Chrome 브라우저가 필요하며 시간이 더 걸릴 수 있습니다)")
        stocks = crawl_with_selenium(url, max_rows)
    
    if not stocks:
        print("\n❌ 데이터를 추출할 수 없습니다.")
        print("\n가능한 원인:")
        print("1. 인터넷 연결 문제")
        print("2. Yahoo Finance 페이지 구조 변경")
        print("3. JavaScript 동적 로딩 페이지 (Selenium 필요)")
        print("\n해결 방법:")
        print("- Selenium이 설치되어 있는지 확인: pip install selenium webdriver-manager")
        print("- Chrome 브라우저가 설치되어 있는지 확인")
        return
    
    # 결과 출력
    print(f"\n✅ 총 {len(stocks)}개의 주식 데이터를 추출했습니다.")
    
    # 엑셀 파일로 저장
    crawler = YahooFinanceCrawler()
    output_file = 'stock_data.xlsx'
    crawler.save_to_excel(stocks, output_file)
    
    # 미리보기 출력
    print("\n" + "=" * 70)
    print("데이터 미리보기 (처음 5개)")
    print("=" * 70)
    for i, stock in enumerate(stocks[:5], 1):
        print(f"\n{i}. {stock.get('Symbol', 'N/A')} - {stock.get('Name', 'N/A')}")
        print(f"   가격: ${stock.get('Price', 'N/A')}")
        print(f"   변동: {stock.get('Change', 'N/A')} ({stock.get('Change %', 'N/A')})")
        print(f"   거래량: {stock.get('Volume', 'N/A')}")
        print(f"   시가총액: {stock.get('Market Cap', 'N/A')}")
    
    if len(stocks) > 5:
        print(f"\n... 외 {len(stocks) - 5}개 더")
    
    print("\n" + "=" * 70)
    print(f"✅ 완료! '{output_file}' 파일을 확인하세요.")
    print("=" * 70)


if __name__ == "__main__":
    main()

