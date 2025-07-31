from selenium import webdriver 
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time, random, pickle, os

def wait_for_comment_post(driver, timeout=10):
    WebDriverWait(driver, timeout).until(
        lambda d: d.find_element(By.CSS_SELECTOR, 'textarea[aria-label="댓글 달기..."]').get_attribute("value") == ""
    )

def insta_comment_bot():
    username = "hamode41735"
    password = "japan12%"
    target_url = "https://www.instagram.com/p/C2het1cPqkz/?img_index=1"
    comment_list =  ['이새끼 애미는 왜 이런 클럽직원이나 하는 못배운 좆밥을 쳐낳은거지? 몸 팔다가 실수로 피임실패했나?','이새끼 애미 씨발년은 어쩌다가 이런걸 쳐 낳았을까.. 애미도 무식하고 천박한 씨발년이겠지?','너 애가 왜 이렇게 좆같이 생겼어? 니네 부모 사진 좀 올려봐 닮았나 보게', '어떻게 이런 열등한 새끼가 이 세상에 나올 수가 있지. 애미애비가 실수로 쳐낳은 성욕 부산물 새끼']
  
    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument('--disable-gpu')
    options.add_argument('--start-maximized')

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.implicitly_wait(10)

    # 📁 쿠키가 존재하면 쿠키로 로그인
    cookie_file = "instagram_cookies.pkl"
    driver.get("https://www.instagram.com/")
    time.sleep(5)

    if os.path.exists(cookie_file):
        try:
            with open(cookie_file, "rb") as f:
                cookies = pickle.load(f)
            for cookie in cookies:
                if 'sameSite' in cookie and cookie['sameSite'] == 'None':
                    cookie['sameSite'] = 'Strict'
                driver.add_cookie(cookie)
            driver.refresh()
            print("✅ 쿠키로 로그인 완료")
            time.sleep(5)
        except Exception as e:
            print("❌ 쿠키 로딩 실패:", e)
    else:
        # 🔐 수동 로그인 후 쿠키 저장
        driver.get("https://www.instagram.com/accounts/login/")
        time.sleep(5)
        try:
            user_input = driver.find_element(By.NAME, "username")
            pass_input = driver.find_element(By.NAME, "password")
            user_input.send_keys(username)
            pass_input.send_keys(password)
            pass_input.send_keys(Keys.ENTER)
            print("✅ 로그인 시도 중...")
            time.sleep(10)
            pickle.dump(driver.get_cookies(), open(cookie_file, "wb"))
            print("✅ 쿠키 저장 완료")
        except Exception as e:
            print("❌ 로그인 실패:", e)
            return

    # 🚀 타겟 게시물로 이동
    driver.get(target_url)
    time.sleep(5)

    # 💬 댓글 작성 루프
    comment_index = 0

    try:
     posted_count = 0 
     while True:
        comment = comment_list[comment_index]
        print(f"📝 댓글 입력 중: {comment}")

        # JS로 댓글 입력
        js_code = '''
        const textarea = document.querySelector('textarea[aria-label="댓글 달기..."]');
        if (textarea) {
            textarea.focus();
            textarea.value = '';
            const chars = arguments[0].split('');
            for (let char of chars) {
                textarea.value += char;
                const inputEvent = new InputEvent('input', {
                    bubbles: true,
                    cancelable: true,
                    inputType: 'insertText',
                    data: char
                });
                textarea.dispatchEvent(inputEvent);
            }
            textarea.value += arguments[1];
            const inputEvent = new InputEvent('input', {
                bubbles: true,
                cancelable: true,
                inputType: 'insertText',
                data: arguments[1]
            });
            textarea.dispatchEvent(inputEvent);
        }
        '''
        driver.execute_script(js_code, comment, '\u200B')
        print("⏳ 수동으로 '게시' 버튼을 눌러주세요...")

        try:
            wait_for_comment_post(driver, timeout=30)
            posted_count += 1
            print(f"✅ 댓글 게시 확인됨 ({posted_count}번째 댓글)")
            time.sleep(2)
        except Exception:
            print("❌ 댓글 게시 감지 실패. 다시 시도하거나 수동 확인 필요")
         

        # 다음 댓글로 순환
        comment_index = (comment_index + 1) % len(comment_list)  # 리스트 끝나면 처음으로
        time.sleep(random.randint(5, 8))

    except KeyboardInterrupt:
        print("\n🛑 사용자에 의해 종료되었습니다.")

    print("🎉 봇 작업 종료")
insta_comment_bot()
