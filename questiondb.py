# Model Defining Questions Database
import string
from google.appengine.ext import db
class questionm(db.Model):
	questionNumber = db.IntegerProperty(required=True)
	question = db.StringProperty(required=True, multiline=True)
	qimage = db.StringProperty()
	opt1 = db.StringProperty(required=True, multiline=True)
	opt2 = db.StringProperty(required=True, multiline=True)
	opt3 = db.StringProperty(required=True, multiline=True)
	opt4 = db.StringProperty(required=True, multiline=True)
	ans = db.StringProperty(required=True)


def getQuestion(num,var):
	query = questionm.all()

	q = query.filter('questionNumber =',num).get()
	if q:
		return ("{"+
				"\"num\" : " + "\""+ str(var) +"\""+","+
				"\"question\" : "+"\""+q.question.replace('\r\n','<br />')+"\""+","+
				"\"image\" : "+"\""+q.qimage+"\""+","+ 
				"\"options\" : " + "["+
									"\""+q.opt1.replace('\r\n','<br />')+"\""+","+
									"\""+q.opt2.replace('\r\n','<br />')+"\""+","+
									"\""+q.opt3.replace('\r\n','<br />')+"\""+","+
									"\""+q.opt4.replace('\r\n','<br />')+"\""+
									"]"+
				"}")
	else:
		return ("{"+
			"\"num\" : " + "\""+"\""+","+
			"\"question\" : "+"\""+"Sorry question not found. We'll fix it Soon"+"\""+","+
			"\"image\" : "+"\""+"\""+","+ 
			"\"options\" : " + "["+
								"\""+""+"\""+","+
								"\""+""+"\""+","+
								"\""+""+"\""+","+
								"\""+""+"\""+
								"]"+
			"}")
