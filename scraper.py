import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
import json
import cherrypy
import cherrypy_cors
cherrypy_cors.install()

class Root(object):
	@cherrypy.expose
	@cherrypy.tools.json_in()
	@cherrypy.tools.json_out()
	def index(self, email, password, **kwargs):
		b = webdriver.PhantomJS(executable_path='/usr/local/bin/phantomjs')
		b.get('https://www.netflix.com/Login?locale=en-US')
		b.find_element_by_id('email').send_keys(email)
		b.find_element_by_id('password').send_keys(password)
		b.implicitly_wait(3) # 3 seconds
		b.find_element_by_id('login-form-contBtn').click()
		b.implicitly_wait(6) # 6 seconds
		if not b.current_url == 'http://www.netflix.com/browse':
			return {"fail":"true"}
		b.get('https://www.netflix.com/WiViewingActivity')
		assert b.current_url == 'https://www.netflix.com/WiViewingActivity'
		n = datetime.date.today()
		ds = str(n.month) + "/" + str(n.day) + "/" + str(n.year)[2:]
		s = BeautifulSoup(b.page_source, "lxml")
		if b:
			b.close()
		a=[]
		b={}
		for r in s.find_all('li', class_='retableRow'):
			t = r.find('span', class_='seriestitle', text=True)
			d = r.find('div', class_='col date nowrap', text=True)
			if t:
				a.append(t.text)
				b["lastDate"] = d.text
				if t.text not in b:
					b[t.text] = 1;
				else:
					b[t.text] = b[t.text] + 1
		print b
		return b
def CORS():
    cherrypy.response.headers["Access-Control-Allow-Origin"] = "*"

if __name__ == '__main__':
	config = {
	    '/': {
	        'cors.expose.on': True,
	    }
	}
	'''
	cherrypy.tools.CORS = cherrypy.Tool('before_handler', CORS)
	cherrypy.quickstart(Root(), '/', conf)'''
	cherrypy.config.update({'server.socket_host': '10.12.40.67',
                        'server.socket_port': 4321,
                       })
	cherrypy.quickstart(Root(), '/', config)

'''def run():

'''
