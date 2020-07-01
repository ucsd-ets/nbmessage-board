import unittest, os, subprocess, time, datetime, random, string

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from bs4 import BeautifulSoup

from . import get_driver

class BaseAcceptanceTester(unittest.TestCase):
    def setUp(self):
        self.proc = subprocess.Popen(['jupyter', 'notebook', '--allow-root', '--ip', '0.0.0.0', '--NotebookApp.token=""'])
        self.driver = get_driver()
        
        # FIXME make this better to wait for the server to start
        time.sleep(2)
        self.driver.get('http://127.0.0.1:8888')
        
        self.board1 = 'mboard'
        self.board2 = 'test'
        
        os.system('mkdir -p /var/lib/nbmessage-board/mboard')
        os.system('mkdir -p /var/lib/nbmessage-board/test')

    def tearDown(self):
        self.proc.terminate()
        os.system('rm -rf /var/lib/nbmessage-board/mboard /var/lib/nbmessage-board/test')
    
##### HELPER FUNCTIONS
    def create_message(self, board, author, body, m_id, close=True, add_notification=False, expiration_date='06/10/2020'):
        admin_tab = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.LINK_TEXT, 'nbmessage-board (Admin)')))
        admin_tab.click()
        
        # make sure we select a message board first
        select_board = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.ID, 'select-message-board')))

        for option in select_board.find_elements_by_tag_name('option'):
            if option.text == board:
                option.click()
                break

        messages = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.LINK_TEXT, 'Messages')))
        messages.click()

        # fill in the name
        name = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.NAME, 'author')))
        name.send_keys(author)

        # fill in the message ID
        message_id_el = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.NAME, 'message_id')))
        message_id_el.send_keys(m_id)

        # fill in the body        
        message_body_el = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.NAME, 'message_body')))
        message_body_el.send_keys(body)
        
        if add_notification:
            notification_check = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.NAME, 'set_notification')))
            notification_check.click()
            
            expiration = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.NAME, 'expiration_date')))
            expiration.send_keys(expiration_date)
            self.driver.save_screenshot('/opt/nbmessage-board/tests/acceptance/screenshots/date-selected.png')
            
            

        # submit, save, and close
        # (By.XPATH, '//*[@id="nbmessage-admin"]/button')
        submit_el = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#nbmessage-admin>button')))
        submit_el.click()

        time.sleep(1)

        # (By.XPATH, '//*[@id="save-message"]')
        save_el = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.ID, 'save-message')))
        save_el.click()

        time.sleep(1)
        
        if close:
            # (By.XPATH, "(//button[@id='close-modal'])[3]")
            close_el = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.ID, 'close-modal')))
            close_el.click()
            time.sleep(1)

    def get_soup(self):
        source = self.driver.page_source
        soup = BeautifulSoup(source, 'html.parser')
        return soup

class TestGeneralFeatures(BaseAcceptanceTester):
    def test_host(self):
        self.driver.get('http://127.0.0.1:8888')
        assert self.driver.title == 'Home Page - Select or create a notebook'
    
    def test_plugins_viewable(self):
        # tabs must exist
        admin_tab = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.ID, 'nbmessage-board-admin')))
        assert True

    def test_global_can_select_multiple(self):
        admin_tab = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.LINK_TEXT, 'nbmessage-board (Admin)')))
        admin_tab.click()

        select_board = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.ID, 'select-message-board')))

        found_test = False
        found_mboard = False
        for option in select_board.find_elements_by_tag_name('option'):
            if option.text == 'test':
                option.click()
                found_test = True
            elif option.text == 'mboard':
                found_mboard = True

        assert found_test
        assert found_mboard

class TestMessageCreationSystem(BaseAcceptanceTester):
    def test_create_message(self):
        body = """# What is Lorem Ipsum
        
        Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.
        """

        input_name = 'My Name'
        self.create_message('mboard', input_name, body, 'm1')
        
        # check announcements tab
        announcements = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.LINK_TEXT, 'Announcements')))
        announcements.click()
        
        # check that the mboard tab has the message
        mboard_tab = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.LINK_TEXT, 'mboard')))
        mboard_tab.click()
        mboard_tab.click()
        
        time.sleep(1)
        
        soup = self.get_soup()
        
        self.driver.save_screenshot('/opt/nbmessage-board/tests/acceptance/screenshots/admin-mboard.png')
        assert soup.find(id='nbmessage-messages') is not None
        assert soup.find(text='What is Lorem Ipsum') is not None
        assert soup.find(text=input_name) is not None
        
        # check that board 'test' doesn't have any messages
        test_tab = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.LINK_TEXT, 'test')))
        test_tab.click()
        test_tab.click()
        
        time.sleep(1)
        soup = self.get_soup()
        self.driver.save_screenshot('/opt/nbmessage-board/tests/acceptance/screenshots/admin-test.png')
        assert soup.find(text='No messages yet') is not None
        
    def test_add_multiple_messages(self):
        body1 = "# Hello\nThere"
        author1 = 'Name1'
        id_1 = 'm1'
        
        body2 = "# Hi\nThere"
        author2 = 'Name2'
        id_2 = 'm2'
        
        self.create_message(self.board1, author1, body1, id_1)
        self.driver.refresh()
        self.create_message(self.board1, author2, body2, id_2)
        
        # check announcements tab
        announcements = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.LINK_TEXT, 'Announcements')))
        announcements.click()
        
        # check that the mboard tab has the message
        mboard_tab = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.LINK_TEXT, 'mboard')))
        mboard_tab.click()
        mboard_tab.click()
        
        time.sleep(1)
        
        soup = self.get_soup()
        
        self.driver.save_screenshot('/opt/nbmessage-board/tests/acceptance/screenshots/admin-mboard-multi.png')
        
        assert soup.find(id='nbmessage-messages') is not None
        # message 1
        assert soup.find(text='Hello') is not None
        assert soup.find(text=author1) is not None
        
        # message 2
        assert soup.find(text='Hi') is not None
        assert soup.find(text=author2) is not None
        
        # check that board 'test' doesn't have any messages
        test_tab = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.LINK_TEXT, 'test')))
        test_tab.click()
        test_tab.click()
        
        time.sleep(1)
        soup = self.get_soup()
        assert soup.find(text='No messages yet') is not None
        
    def test_messages_isolated_between_message_boards(self):
        body1 = "# Hello\nThere"
        author1 = 'Name1'
        id_1 = 'm1'

        self.create_message(self.board1, author1, body1, id_1)
        self.driver.refresh()
        
        body2 = '# Hi\nThere'
        author2 = 'Name2'
        id_2 = 'm1'

        self.create_message(self.board2, author2, body2, id_2)
        
        announcements = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.LINK_TEXT, 'Announcements')))
        announcements.click()
        
        mboard_tab = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.LINK_TEXT, 'mboard')))
        mboard_tab.click()
        mboard_tab.click()
        
        soup = self.get_soup()
        
        self.driver.save_screenshot('/opt/nbmessage-board/tests/acceptance/screenshots/admin-multi.png')
        assert soup.find(id='nbmessage-messages') is not None
        # message 1
        assert soup.find(text='Hello') is not None
        assert soup.find(text=author1) is not None
        
        test_tab = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.LINK_TEXT, 'test')))
        test_tab.click()
        test_tab.click()
        
        soup = self.get_soup()
        
        self.driver.save_screenshot('/opt/nbmessage-board/tests/acceptance/screenshots/admin-multi2.png')
        assert soup.find(id='nbmessage-messages') is not None
        # message 2
        assert soup.find(text='Hi') is not None
        assert soup.find(text=author2) is not None
        
    def test_add_notification(self):
        body1 = "# Hello\nThere"
        author1 = 'Name1'
        id_1 = 'm1'

        
        expiration = datetime.datetime(2055, 1, 1) # this will be valid for awhile >:D
        expiration = expiration.strftime('%m/%d/%Y')

        self.create_message(self.board1, author1, body1, id_1, add_notification=True, expiration_date=expiration) # expiration date
        
    def test_add_multiple_notifications(self):
        letters = string.ascii_lowercase
        message_boards = ['test', 'mboard']
        messages_in_board = [0, 0]
        
        for i in range(10):
            # 2 paragraphs essentially
            body = ''.join(random.choice(letters) for i in range(300))
            body = body + '\n<br/>' + ''.join(random.choice(letters) for i in range(300))
            
            author = ''.join(random.choice(letters) for i in range(20))
            message_id = ''.join(random.choice(letters) for i in range(10))
            
            board = random.randint(0, 1)
            message_board = message_boards[board]
            
            self.create_message(message_board, author, body, message_id)
            messages_in_board[board] += 1
        
        announcements = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.LINK_TEXT, 'Announcements')))
        announcements.click()
        
        mboard_tab = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.LINK_TEXT, 'mboard')))
        mboard_tab.click()
        mboard_tab.click()
        
        soup = self.get_soup()
        mboard_messages = len(soup.select('.nbmessage-border'))
        assert mboard_messages == messages_in_board[1]
        self.driver.save_screenshot('/opt/nbmessage-board/tests/acceptance/screenshots/admin-mboard-multi.png')
        
        test_tab = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.LINK_TEXT, 'test')))
        test_tab.click()
        test_tab.click()
        
        soup = self.get_soup()
        test_messages = len(soup.select('.nbmessage-border'))
        assert test_messages == messages_in_board[0]
        
        self.driver.save_screenshot('/opt/nbmessage-board/tests/acceptance/screenshots/admin-test-multi.png')
    
##### NEGATIVE TEST CODE
    def test_add_message_with_same_id_fails(self):
        body1 = "# Hello\nThere"
        author1 = 'Name1'
        id_1 = 'm1'

        self.create_message(self.board1, author1, body1, id_1)
        self.driver.refresh()
        
        self.create_message(self.board1, author1, body1, id_1, close=False)
        
        soup = self.get_soup()
        self.driver.save_screenshot('/opt/nbmessage-board/tests/acceptance/screenshots/admin-mboard-same-id.png')

        assert soup.find(text='message_id = m1 already exist!')
        
