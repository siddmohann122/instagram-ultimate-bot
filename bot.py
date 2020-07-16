from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
#import all the selenium packages






class Bot:
	def __init__(self, username, pw):#logs in your account
		self.username = username#username
		self.password=pw#password
		self.driver = webdriver.Chrome(ChromeDriverManager().install())#driver
		"""Lines above just set up everything we need"""

		self.driver.get('https://www.instagram.com/')#go to instagram.com
		sleep(2)#wait 1 second
		self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/article/div[2]/div[1]/div/form/div[2]/div/label/input').send_keys(username)#eneter username
		self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/article/div[2]/div[1]/div/form/div[3]/div/label/input').send_keys(pw)#eneter username
		self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/article/div[2]/div[1]/div/form/div[4]').click()#hits enter
		sleep(5)#wait 3 seconds

		try:
			self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div/div/div/button').click()
			sleep(2)
		except:
			pass

		try:
			self.driver.find_element_by_xpath('/html/body/div[4]/div/div/div/div[3]/button[2]').click()
		except:
			pass
		"""Lines above login"""

	def get_followers_and_following(self,f,acc='me'):#gets a list of the people who follow you and who you follow
		if acc=='me':
			self.go_to_others_profile(self.username)
		else:
			go_to_others_profile(acc)
		if f=='followers':
			WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/section/main/div/header/section/ul/li[2]'))).click()
			sleep(2)
		else:
			WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="react-root"]/section/main/div/header/section/ul/li[3]/a'))).click()
			sleep(2)
		"""Goes to the the followers or following button"""


		scroll_box=WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[4]/div/div/div[2]')))#defines the box of the followers
		last_ht = 0
		ht=1
		while last_ht != ht:
			last_ht = ht
			sleep(3)
			ht = self.driver.execute_script("""
				arguments[0].scrollTo(0, arguments[0].scrollHeight);
				return arguments[0].scrollHeight;
				""", scroll_box)

		"""Lines above scroll through the box"""
		links = scroll_box.find_elements_by_tag_name('a')
		names = [name.text for name in links if name.text != '']#adds the names of the people to this list by extracting the name from the links

		self.driver.find_element_by_xpath("/html/body/div[4]/div/div/div[1]/div/div[2]/button").click()# close button
		self.driver.back()#go back
		self.driver.back()#go back
		self.driver.back()#go back
		return names#makes this function hold the value of the names

	def get_unfollowers(self,send_message=False):#gets the people that dont follow you back
		followers=self.get_followers_and_following('followers')#stores your followers
		following=self.get_followers_and_following('yedey')#stores people you follow
		print(len(followers))
		print(len(following))
		trouble=[]
		for p in following:
			if p not in followers:
				trouble.append(p)
		if send_message:#requests to send a message
			for person in trouble:
				self.send_message(person,'You dont folow me back...nah jk im bored so i descided to make a bot that would send this to all the people that dont follow me back have a nice day')
		print(trouble)
		return trouble

	def send_message(self,follower,message,unsend=True):
		WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/section/nav/div[2]/div/div/div[3]/div/div[2]/a'))).click()#click on dm button on homepage
		WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/section/div/div[2]/div/div/div[1]/div[1]/div/div[3]/button'))).click()#click compose message
		sleep(2)
		self.driver.find_element_by_xpath('/html/body/div[4]/div/div/div[2]/div[1]/div/div[2]/input').send_keys(follower)
		sleep(2)
		WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[4]/div/div/div[2]/div[2]/div[1]/div/div[3]/button'))).send_keys(message)
		WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[4]/div/div/div[1]/div/div[2]/div/button'))).click()
		sleep(2)
		WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="react-root"]/section/div/div[2]/div/div/div[2]/div[2]/div/div[2]/div/div/div[2]/textarea'))).send_keys(message)#type message
		WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/section/div/div[2]/div/div/div[2]/div[2]/div/div[2]/div/div/div[3]/button'))).click()
		WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/section/div/div[1]/div/div[1]/a/div/div/img'))).click()#click send
	def unfollow_someone(self,person):
		self.go_to_others_profile(person)
		try:	
			WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/section/main/div/header/section/div[1]/div[1]/span/span[1]/button'))).click()
		except:
			WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/section/main/div/header/section/div[1]/div[2]/span/span[1]/button'))).click()
			WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[4]/div/div/div/div[3]/button[1]'))).click()
	def go_to_others_profile(self,person):
		x=WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="react-root"]/section/nav/div[2]/div/div/div[2]/input')))
		x.send_keys(person)
		WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="react-root"]/section/nav/div[2]/div/div/div[2]/div[3]/div[2]/div/a[1]'))).click()


