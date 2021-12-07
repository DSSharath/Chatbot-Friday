import uuid
import pyodbc
import textwrap
from flask import Flask, render_template, request
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.trainers import ListTrainer



app = Flask(__name__)
app.secret_key="abc"

sess_id=uuid.uuid4() #Generate random UUID

bot = ChatBot("Friday")
trainer = ChatterBotCorpusTrainer(bot)
trainer.train('chatterbot.corpus.english')

@app.route("/")
def home():    
    return render_template("home.html") 



@app.route("/get")
def get_bot_response():    
    userText = request.args.get('msg')    
    res= str(bot.get_response(userText)) 

    server='tcp:myserver' #Enter server name here
    database='mydb' #Enter database name here
    username='myusername' #Enter username here
    password='mypassword' #Enter password here

    db_connection=pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+password)
    cursor=db_connection.cursor() #Create cursor object
    data_log=textwrap.dedent("""
        INSERT INTO MESSAGE_LOG(sess_id,mess_sent,mess_sent_time,mess_rec,mess_rec_time) 
        VALUES (sess_id,userText,CURRENT_TIMESTAMP,res,CURRENT_TIMESTAMP)""")
    cursor.execute(data_log)

    return res

if __name__ == "__main__":    
    app.run()
