from flask import Flask, request
import json
from urllib.parse import unquote

jobads = []
keywords = []

with open("../web_app/keywords", "r", encoding="utf-8") as fin:
    for line in fin:
        ## strip \n
        keywords.append(line[:-1])


with open("jobads.json", encoding='utf-8') as fin:
    for line in fin:
        jobads.append(json.loads(line, encoding='utf-8'))

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

@app.route("/api/")
def index():
    return ""

@app.route("/api/savetagged", methods=["POST"])
def savetagged():
    indata = request.form['tags']
    thaistring = bytes(unquote(indata), 'utf-8').decode('utf-8')
    splitstring = thaistring.split("|")
    with open("../web_app/keywords", "a", encoding="utf-8") as fout:
        for item in splitstring:
            fout.write(item+"\n")
            keywords.append(item) 
    return "OK"

@app.route("/api/getjobcount")
def getjobcount():
    from flask import jsonify
    count = {"count":str(len(jobads))}
    return jsonify(count)

@app.route("/api/gettagcount")
def gettagcount():
    from flask import jsonify
    count = {"count":str(len(keywords))}
    return jsonify(count)

@app.route("/api/gettaglist")
def gettaglist():
    from flask import jsonify
    taglist = [[i,keywords[i]] for i in range(len(keywords))]
    taglist = dict(taglist)
    return jsonify(taglist)

@app.route("/api/getjob")
def getjob():
    from flask import jsonify
    import random
    data = jobads[random.randint(0,len(jobads))]
    newstr = "" 
    mystr = data['desc']
    ## create TH vs EN chunks
    def isEN(char):
        return (ord(char) in range(32, 122+1))    
    def isTH(char):
        return (ord(char) in range(3585, 3675+1))

    def sameLang(char1, char2):
        return ( (isEN(char1) and isEN(char2)) or (isTH(char1) and isTH(char2)))

    chunks = []
    for i in range(len(mystr)):
        if(len(chunks) == 0):
            ## blank output = push down
            chunks.append(mystr[i])
        else:
            ## check if same language push down else new stack
            if(sameLang(mystr[i], chunks[-1][-1])):
                chunks[-1] = chunks[-1] + mystr[i]
            else:
                chunks.append(mystr[i])

    for chunk in chunks:
        if(isTH(chunk[0])):
            pivot = 0
            longest = 0
            nextpos = 0
            ## TH : do longest matching
            for i in range(len(chunk)):
                if(i == nextpos):
                    longest = ''
                    pivot = 0
                    for j in range(i, len(chunk)):
                        if(chunk[i:j+1] in keywords):
                            ## found keyword
                            longest = chunk[i:j+1]
                            pivot = j+1
                    if(longest == ''):        
                        newstr = newstr + chunk[i]
                        nextpos = i + 1 
                    else:
                        newstr = newstr + "<span style='background-color: yellow'>" + longest + "</span>"
                        nextpos = pivot
                else: pass
        else:
            ## EN : do whole match search
            for word in chunk.split(" "):
                if(word in keywords):
                    newstr = newstr + " " + "<span style='background-color: yellow'>" + word + "</span>"
                else:            
                    newstr = newstr + " " + word

    data['desc'] = newstr
    data['chunks'] = str(chunks)
    return jsonify(data)

@app.route("/api/tagjob", methods=['POST'])
def tagjob():
    #with open(outputfile, 'a', encoding='utf-8') as fout:
    type(request.json)	
    keywords.append("word"+len(keywords))
    
    ## write terms to a file 
   
    return "OK"

@app.route("/api/seetaggedjobs")
def seetaggedjobs():
    ## open tagged job file
        
    return "" 

if(__name__=="__main__"):
    print("running host")
    app.run(host='0.0.0.0')
                 
