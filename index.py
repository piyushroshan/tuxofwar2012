import os
import datetime
import string
import userdb
import questiondb
import simplejson as json
from google.appengine.ext.webapp import template
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

class index(webapp.RequestHandler):
	def get(self):
		self.response.headers['Content-Type'] = 'text/html'
		path = os.path.join(os.path.dirname(__file__), 'templates/index.html')
		self.response.out.write(template.render(path,""))

class contestStart(webapp.RequestHandler):
	def get(self,var):
		user = users.get_current_user()
		if not user:
			self.redirect(users.create_login_url(self.request.uri))
		else:
			if not userdb.userPlayExist():
				userdb.userPlayStart(var)
				self.redirect('/?auth=1')
			else:
				if userdb.boolRemainingTime()==True:
					self.redirect('/?auth=1')
				else:
					self.response.headers['Content-Type'] = 'text/html'
					self.response.out.write('You have finished the contest. You cannot participate again <a href="/"">Back to Tux of War</a>')


class contestStop(webapp.RequestHandler):
	def get(self):
		self.response.out.write(userdb.userPlayStop())
		self.redirect('/?end=1')
		

class contestQuestion(webapp.RequestHandler):
	def get(self,var):
		self.response.headers['Content-Type'] = 'application/json'
		r = questiondb.getQuestion(int(userdb.userPermutation(int(var))),int(var))
		self.response.out.write(r)

class contestAnswer(webapp.RequestHandler):
	def get(self):
		self.response.out.write(userdb.userAnswerSubmit(
								int(userdb.userPermutation(int(self.request.get('question')))),
								self.request.get('answer')))

class contestActiveuser(webapp.RequestHandler):
	def get(self):
		self.response.headers['Content-Type'] = 'application/json'
		user = users.get_current_user()
		if user:
			self.response.out.write("{ \"name\" : \""+user.nickname()+"\" }")
		else:
			self.response.out.write("{ \"name\" : \"NULL\" }")
			
class remainingTime(webapp.RequestHandler):
	def get(self):
		user = users.get_current_user()
		if user:
			time = userdb.userRemainingTime()
			self.response.out.write("{ \"time\" :\""+ str(time)+"\" }")
		else:
			self.response.out.write("{ \"time\" :\""+str(0)+"\" }")




class adminQuestionsAdd(webapp.RequestHandler):
	def get(self):
		if users.get_current_user():
			if users.is_current_user_admin():
				self.response.headers['Content-Type'] = 'text/html'
				path = os.path.join(os.path.dirname(__file__), 'templates/question.html')
				self.response.out.write(template.render(path,""))
			else:
				print "Not allowed!"
		else:
			self.redirect(users.create_login_url(self.request.uri))
	

class adminQuestionsSubmit(webapp.RequestHandler):
	def post(self):
		if users.get_current_user():
			if users.is_current_user_admin():
				q = questiondb.questionm(questionNumber=string.atoi(self.request.get('qno')),
										question=self.request.get('ques'),
										qimage=self.request.get('qimg'),
										opt1=self.request.get('opt1'),
										opt2=self.request.get('opt2'),
										opt3=self.request.get('opt3'),
										opt4=self.request.get('opt4'),
										ans=self.request.get('ans'))
				q.put()
				self.redirect('/admin/questions/list/')
			else:
				print "Not allowed!"
		else:
			self.redirect(users.create_login_url(self.request.uri))

class adminQuestionsList(webapp.RequestHandler):
	def get(self):
		if users.get_current_user():
			if users.is_current_user_admin():
				self.response.headers['Content-Type'] = 'text/html'
				query = questiondb.questionm.all()
				result = query.fetch(100)
				template_values = { 'questions' : result }
				path = os.path.join(os.path.dirname(__file__), 'templates/questionlist.html')
				self.response.out.write(template.render(path, template_values))
			else:
				print "Not allowed!"
		else:
			self.redirect(users.create_login_url(self.request.uri))

class adminQuestionsAnswered(webapp.RequestHandler):
	def get(self):
		if users.get_current_user():
			if users.is_current_user_admin():
				self.response.headers['Content-Type'] = 'text/html'
				self.response.out.write("Answered Questions<br />")
				query = userdb.userAnswer.all().order('elapsedTime')
				result = query.fetch(100)
				for ans in result:
					self.response.out.write(ans.user.nickname()+str(ans.question)+
											ans.answer+str(ans.elapsedTime)+"<br />")
			else:
				print "Not allowed!"
		else:
			self.redirect(users.create_login_url(self.request.uri))

class adminContestUsers(webapp.RequestHandler):
	def get(self):
		if users.get_current_user():
			if users.is_current_user_admin():
				self.response.headers['Content-Type'] = 'text/html'
				query = userdb.userPlay.all().order('startTime')
				result = query.fetch(100)
				for ans in result:
					self.response.out.write(ans.user.nickname()+ans.tathvaID+"<br />")
					self.response.out.write(ans.questionSet)
					self.response.out.write("<br />")
			else:
					print "Not allowed!"
		else:
			self.redirect(users.create_login_url(self.request.uri))

application = webapp.WSGIApplication(
									[('/', index),
									('/contest/start/(.*)|/',contestStart),
									('/contest/stop/',contestStop),
									('/contest/question/(\d*)|/', contestQuestion),
									('/contest/answer/', contestAnswer),
									('/contest/time/', remainingTime),
									('/contest/activeuser/', contestActiveuser),
									('/admin/questions/add/contest', adminQuestionsAdd),
									('/admin/questions/submit/', adminQuestionsSubmit),
									('/admin/questions/list/',adminQuestionsList),
									('/admin/questions/answered/',adminQuestionsAnswered),
									('/admin/contest/users/',adminContestUsers)],
									debug=True)

def main():
	run_wsgi_app(application)

if __name__ == "__main__":
	main()
