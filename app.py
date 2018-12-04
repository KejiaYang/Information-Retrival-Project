from flask import Flask, flash, redirect, render_template, request, session, abort, jsonify
from random import randint
 
app = Flask(__name__)

#@app.route("/hello/<string:name>")
@app.route("/hello",methods=['GET', 'POST'])
def hello():
    quotes = [ "'If people do not believe that mathematics is simple, it is only because they do not realize how complicated life is.' -- John Louis von Neumann ",
               "'Computer science is no more about computers than astronomy is about telescopes' --  Edsger Dijkstra ",
               "'To understand recursion you must first understand recursion..' -- Unknown",
               "'You look at things that are and ask, why? I dream of things that never were and ask, why not?' -- Unknown",
               "'Mathematics is the key and door to the sciences.' -- Galileo Galilei",
               "'Not everyone will understand your journey. Thats fine. Its not their journey to make sense of. Its yours.' -- Unknown"  ]
    randomNumber = randint(0,len(quotes)-1) 
    quote = quotes[randomNumber]
    qr = "NO QUERY"
    if request.method == 'POST':
      print ("ifffffff")
      qr = request.get_json(force=True)
      print(qr)

    return render_template(
        'idx.html',**locals())


 
if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000)