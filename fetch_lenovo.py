from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import sys
import codecs
import time
from pyvirtualdisplay import Display

url = "http://outlet.lenovo.com/outlet_us/laptops/#/?page-index=1&page-size=100&facet-1=3&sort-criteria=2"
display = Display(visible=0, size=(800, 600))
display.start()

driver = webdriver.Firefox()
#driver.manage().window().setPosition(new Point(-2000, 0));
#driver.get("http://outlet.lenovo.com/outlet_us/laptops/#/?page-index=1&facet-2=1&page-size=100&facet-1=2&facet-3=14")
#driver.get("http://outlet.lenovo.com/outlet_us/laptops/#/?page-index=1&page-size=100&facet-3=14&facet-8=9&sort-criteria=2&facet-1=1&facet-1=3")
driver.get(url)
#assert "Python" in driver.title
#elem = driver.find_elemen:t_by_name("q")
#elem.send_keys("pycon")
#elem.send_keys(Keys.RETURN)
#assert "No results found." not in driver.page_source
#driver.implicitly_wait(30)
driver.set_window_size(1000,1000)
i = 0
for i in range(0,18):
#  i += 1
  time.sleep(4)
  driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

f = codecs.open("a.html", "w", "utf-8")
f.write(driver.page_source)
f.close()
driver.close()
