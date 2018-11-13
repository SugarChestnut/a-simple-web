from flask import Flask, render_template, request, escape,session
from flask import copy_current_request_context
from letter_search import letter

from DBcm import UseDatabase, ConnectionError, CredentialsError, SQLError
#
from threading import Thread
#导入线程模块
from checker import check_logged_in

app = Flask(__name__)
#创建一个Flask的对象实例，赋值给app

app.config['dbconfig'] = {'host': '127.0.0.1',
						'user': 'ch07',
						'password': 'ch07pw',
						'database': 'search_logDB',}
						

@app.route('/login')
def do_login() -> str:
	session['logged_in'] = True
	return 'You are logged in.'


@app.route('/logout')
def do_logout() -> str:
	try:
		session.pop('logged_in')
		return 'You are noe logged out'
	
	except KeyError as err:
		print ('You are not login.')
	
	return 'You are not login.'
"""
@app.route('/')
#route：函数修饰符，'/'是URL
def hello() -> str:
	return "rentaotao"
"""
	
@app.route("/search", methods = ["POST"])
def do_search() -> "html":
#定义一个普通函数，html是返回类型
	
	@copy_current_request_context
	def log_request(req: "flask_request", res: str) -> None:
				
		"""			
		conn = mysql.connector.connect(**dbconfig)
		cursor = conn.cursor()
		"""
	
		try:
			with UseDatabase(app.config['dbconfig']) as cursor:
				_SQL = """insert into log(phrase, letters, ip, results)
						values(%s, %s, %s, %s)"""
				cursor.execute(_SQL, (req.form['phrase'],
								req.form['letters'],
								req.remote_addr,
								res,))
								
		except ConnectionError as err:
			print('Is your detabase switched on? Error:', str(err))
			
		except CredentialsError as err:
			print('User-id/password issues. Error:', str(err))
		
		"""				
		conn.commit()
		cursor.close()
		conn.close()
		"""
	
	phrase = request.form["phrase"]
	letters = request.form["letters"]
	title = "Here are your results:"
	results = str(letter(phrase, letters))
	
	try:
		#定义异常处理
		log_request(request, results)
		
	except Exception as err:
		print('****Loggong failed with this error', str(err))
	
	#render_template函数，就是先引入web模块，然后传递参数，对模块进行渲染
	return render_template("results.html",
				the_phrase = phrase,
				the_letters = letters,
				the_title = title,
				the_results = results,)

							
@app.route("/")
@app.route("/entry")
def entry_page() -> "html":
	return render_template("entry.html", the_title = "Welcome to search_letter on the web!")


@app.route("/viewlog")
@check_logged_in
#check方法必须包含在这个URL里面，不然无法起作用
def view_log() -> "html":
	dbconfig = {'host': '127.0.0.1',
				'user': 'ch07',
				'password': 'ch07pw',
				'database': 'search_logDB',}
	
	try:	
		with UseDatabase(dbconfig) as cursor:
			_SQL = """select * from log"""
			cursor.execute(_SQL)
			res = cursor.fetchall()
		
			"""
			contents = []
			with open("D:/ch06/todo.log") as log:
				for line in log:
					contents.append([])
					for item in line.split('|'):
						contents[-1].append(escape(item))
			"""
		titles = ("id", "ts", "phrase", "letters", "ip", "results")
		return render_template("viewlog.html",
								the_title = "View Log",
								the_row_titles = titles,
								the_data = res,)
								
	except ConnectionError as err:
		print('Is your detabase switched on? Error:', str(err))
		
	except CredentialsError as err:
		print('User-id/password issues. Error:', str(err))
	
	except SQLError as err:
		print('Is your query correct? Error:', str(err))
	
	except Exception:
		print('Something went wrong:', str(err))
	
	return 'Error'
		

app.secret_key = 'rentaotao'		
if __name__ == "__main__":
	#让web应用开始运行
	app.run(debug = True)
