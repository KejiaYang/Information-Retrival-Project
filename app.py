from flask import Flask, flash, redirect, render_template, request, session, abort, jsonify
from random import randint
from dataset import return_all
from algo import retrieval
 
app = Flask(__name__)

class Q():
  qr = "NO QUERY"

qr_global = Q()

#@app.route("/hello/<string:name>")
@app.route("/hello",methods=['GET', 'POST'])
def hello():
    if request.method == 'POST':
      print ("ifffffff")
      qr_global.qr = request.get_json(force=True)
      
    resume = return_all(48105, 1, True)
    return render_template(
        'idx.html',**locals())


@app.route("/hello/return.html",methods=['GET', 'POST'])
def rt():
    # quotes = [ "'If people do not believe that mathematics is simple, it is only because they do not realize how complicated life is.' -- John Louis von Neumann ",
    #            "'Computer science is no more about computers than astronomy is about telescopes' --  Edsger Dijkstra ",
    #            "'To understand recursion you must first understand recursion..' -- Unknown",
    #            "'You look at things that are and ask, why? I dream of things that never were and ask, why not?' -- Unknown",
    #            "'Mathematics is the key and door to the sciences.' -- Galileo Galilei",
    #            "'Not everyone will understand your journey. Thats fine. Its not their journey to make sense of. Its yours.' -- Unknown"  ]
    # randomNumber = randint(0,len(quotes)-1) 
    # quote = quotes[randomNumber]
    # resume = return_all(48105, 1, True)
    resumes_dict, bm25, method2 = retrieval(qr_global.qr)
    print(len(resumes_dict))
    print(qr_global.qr)
    return render_template(
        'return.html',**locals())

@app.route("/hello/about.html",methods=['GET', 'POST'])
def about():
    return render_template(
        'about.html',**locals())

@app.route("/hello/methodology.html",methods=['GET', 'POST'])
def methodology():
    return render_template(
        'methodology.html',**locals())

@app.route("/hello/dataset.html",methods=['GET', 'POST'])
def dataset():
    return render_template(
        'dataset.html',**locals())

@app.route("/hello/bm25.html",methods=['GET', 'POST'])
def bm25():
    return render_template(
        'bm25.html',**locals())

@app.route("/hello/bm25ctf.html",methods=['GET', 'POST'])
def bm25ctf():
    return render_template(
        'bm25ctf.html',**locals())

@app.route("/hello/teammember.html",methods=['GET', 'POST'])
def teammember():
    return render_template(
        'teammember.html',**locals())

@app.route("/hello/reference.html",methods=['GET', 'POST'])
def reference():
    return render_template(
        'reference.html',**locals())

@app.route("/hello/performance.html",methods=['GET', 'POST'])
def performance():
    return render_template(
        'performance.html',**locals())
 
if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000, debug=True)