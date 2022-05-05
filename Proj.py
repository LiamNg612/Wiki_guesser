from flask import Flask, request, session, g, jsonify
import os.path
import sqlite3
import wikipedia

from pyhtml import script
from pyhtml import script,form,body,input_,html,head,div,h3,button,label,h1,ol,li,link,p,a,h2,ul,table,tr,th,span
#$ pip install wikipedia
app = Flask(__name__)
app.config['SECRET_KEY'] = "f12d12d123218238hgsafh"
DATABASE = os.path.join(os.path.dirname(os.path.abspath(__file__)),'proj.db')


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/leaderboard', methods=["POST"])
def leaderboard():
    if request.form.get('correct')=="T":
        conn = get_db()
        sql = "SELECT * FROM LEADERBOARD ORDER BY CORRECT DESC,TOTAL DESC"
        result = conn.execute(sql)
        result = result.fetchall()
        res = "<table id='leaderboard'><tr><th>User Name</th><th onclick='rankCorrect()'>Correct</th><th>Wrong</th><th onclick='rankByQuestion()'>Question</th></tr>"
        for r in result:
            res = res + "<tr><td>" + str(r[0]) + "</td><td>" + str(r[1]) + "</td><td>" + str(r[2]) + "</td><td>" + str(
                r[3]) + "</td></tr>"
        res = res + "</table>"
        return res
    elif request.form.get('question')=="T":
        conn = get_db()
        sql = "SELECT * FROM LEADERBOARD ORDER BY TOTAL DESC,CORRECT DESC"
        result = conn.execute(sql)
        result = result.fetchall()
        res = "<table id='leaderboard'><tr><th>User Name</th><th onclick='rankCorrect()'>Correct</th><th>Wrong</th><th onclick='rankByQuestion()'>Question</th></tr>"
        for r in result:
            res = res + "<tr><td>" + str(r[0]) + "</td><td>" + str(r[1]) + "</td><td>" + str(r[2]) + "</td><td>" + str(
                r[3]) + "</td></tr>"
        res = res + "</table>"
        return res


@app.route('/', methods=["GET"])
def main():
    conn = get_db()
    sql = "SELECT * FROM LEADERBOARD ORDER BY TOTAL DESC,CORRECT DESC"
    result = conn.execute(sql)
    result = result.fetchall()
    res="<table id='leaderboard'><tr><th>User Name</th><th onclick='rankCorrect()'>Correct</th><th>Wrong</th><th onclick='rankByQuestion()'>Question</th></tr>"
    for r in result:
        res = res+"<tr><td>"+str(r[0])+"</td><td>"+str(r[1])+"</td><td>"+str(r[2])+"</td><td>"+str(r[3])+"</td></tr>"
    res=res+"</table>"
    session['correct']=0
    session['wrong'] = 0
    session['number'] = 0
    if request.method == 'GET':
        response=html(
            head(
                script(src="static/jquery/jquery-3.6.0.js"),  # use jquery for js
                link(href="static/homepage.css",rel="stylesheet"),
                body(
                    h1("Welcome to my WikiGuesser"),
                    form(action="/game", method='POST')(
                    input_(type='text', name='UserName' , placeholder="UserName", required=""),
                    input_(type='text', name='insert', value="insert", style="display:none"),
                    input_(type='submit',value="Submit")
                ),h2("Leaderboard"),
                )
            )
        )
        scr=script(src="/static/action.js")
        return str(response)+res+str(scr)

@app.route('/game', methods=["GET", "POST"])
def wikiGuess():
    conn=get_db()
    cursor=conn.cursor()
    if request.method == 'POST':
        if request.form.get('insert')=="insert":
            username = request.form.get('UserName')
            session['username'] = username;
            sql="INSERT INTO LEADERBOARD VALUES(?,?,?,?);"
            cursor=conn.execute(sql , (username,session['correct'] ,session['wrong'] , session['number']))
            conn.commit()
        response=""
        title=""
        count=0;
        output=""
        while count<5:
            title = wikipedia.random()#using the wiki api get random topic
            try:
                sentence = wikipedia.WikipediaPage(title).summary # try catch the execption and will regenerate a proper topic
                pic = wikipedia.WikipediaPage(title).images
            except:
                title = wikipedia.random()
                sentence = wikipedia.WikipediaPage(title).summary #use wiki api to get the summary of the topic
                pic = wikipedia.WikipediaPage(title).images

            count = len(sentence.split(".")) #ensure the length of summary will larger than 5 so there can be more hints
        session['answer'] = title
        response = html(
            head(
                script(src="static/jquery/jquery-3.6.0.js"), #use jquery for js
                link(href="static/homepage.css", rel="stylesheet"),
            ),
            body(
                h1("Wikiguesser"),
                div(id="grid")(
                    div(id="result")(
                        h3("Correct"),
                        p(session['correct'] ),
                        h3("Wrong"),
                        p(session['wrong']),
                    ),
                    div(id="content")(
                        ul(id="para")(  # for showing the question
                        ),
                        button(id="start_btn", onclick="getHint()", style="margin-bottom:18px")(
                            # trying to use js to add hints button(click on it can get more hints)
                            "Start"
                        ),
                        div(id="sentence", style="display:none")(
                            sentence),  # this is for storing the variable to get by js
                        div(id="title", style="display:none")(
                            title),
                        div(id="pic", style="display:none")(
                            pic),

                        form(action='/game', method='POST', id="answeringForm")(  # user can input answer in this box
                            label(
                                "What is this article:"
                            ),
                            input_(type='text', name='answer'),
                            input_(type='submit'),
                        ),
                        div(id='response')(

                        ),
                        script(src="/static/action.js"),
                        script(src="/static/game.js")
                    ),


                ),
                a(href="/")(
                    "Home page"
                )
            )
        )
        session['response']=str(response)
        return str(response)


@app.route('/check', methods=["GET", "POST"])
def checkAns():
    username=session['username']
    conn = get_db()
    sql = "SELECT * FROM LEADERBOARD WHERE USERNAME=?"
    result = conn.execute(sql, (username,))
    result=result.fetchall()
    for r in result:
        data=r
    session['number']=data[3]+1
    number = session['number']
    if request.form.get('answer').lower()== session['answer'].lower():
        session['correct']=session['correct']+1
        correct = session['correct']
        sql = "UPDATE LEADERBOARD SET CORRECT=?,TOTAL=? WHERE USERNAME= ?;"
        cursor = conn.execute(sql, (correct,number,username))
        conn.commit()
        return "True"
    else:
        session['wrong'] = session['wrong']+1
        wrong = session['wrong']
        sql = "UPDATE LEADERBOARD SET WRONG=?,TOTAL=? WHERE USERNAME= ?;"
        cursor = conn.execute(sql, (wrong,number, username))
        conn.commit()
        return "wrong title: "+str(session['answer'].lower())+" user answer:"+str(request.form.get('answer').lower())


if __name__ ==   "__main__":
    app.run(debug=True)