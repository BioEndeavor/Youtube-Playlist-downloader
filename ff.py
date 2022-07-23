
from flask import Flask,render_template,request, send_from_directory,session,send_file
from pytube import YouTube
from pytube import Playlist
import logging
import PyPDF2
import gtts 
import pdfplumber
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'C:/Users/joash/OneDrive/Desktop/YOutube/static'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key =  os.urandom(24)
@app.route('/')
def index():
    return render_template('home.html')
@app.route('/Download')
@app.route('/result',methods = ['POST','GET'])
def r():
    s = list()
    U = ''  
    url = []
    if request.method == "POST":
      session['U'] = request.form['URL']   
      try: 
        U = request.form.get('URL')
        yt = Playlist(U)
        for a in yt.video_urls:
            s.append(YouTube(a).title)
            url.append(a)
      except:
         try : 
           yt = YouTube(U)
           s.append(yt.title)
         except:
            logging.exception("Failed Download")
            return "Video download failed!"
    return render_template('index.html',i = s,URL = U,f = url)

@app.route('/Down/')
def Downl():
    U = session.get('U',None)
    ytt = YouTube(U)
    p = ytt.streams.get_highest_resolution().download()
    #path = p.split("//")[-1]  
    return send_file(p,as_attachment=True)

@app.route('/Play')
def Playi():
    U = session.get('U',None)
    ytt = Playlist(U)
    for video in ytt.videos:
       p = video.streams.get_highest_resolution().download()
       #path = p.split("//")[-1]
       return send_file(p,as_attachment=True)


@app.route('/<int:ind>')
def d(ind):
    y = []
    U = session.get('U',None)
    for v in Playlist(U).video_urls:
        y.append(v)
    p = YouTube(y[ind]).streams.get_highest_resolution().download()
    return send_file(p,as_attachment=True)

@app.route('/pdf')
def p():
    return render_template('down.html')
@app.route('/pdta',methods = ['POST','GET'])
def pdf():
   if request.method == "POST":
     try:
      file = request.files['file']
      filename = file.filename
      pdfReader = PyPDF2.PdfFileReader(file)
      text = ""
      pages = pdfReader.numPages
      with pdfplumber.open(file) as pdf:
        #Loop through the number of pages
        for i in range(0, pages): 
          page = pdf.pages[i]
          text += page.extract_text()
      a = gtts.gTTS(text)
      ff = filename.split(".")[0]
      a.save('%s.mp3'%ff)
      filePath = '%s.mp3'%ff
      if os.path.isfile(filePath):
        return send_file(filePath,as_attachment=True)
     except:
        logging.exception("Failed Download")
        return "File Download Failed"
#  filepath = os.path.join(app.config['UPLOAD_FOLDER'], )

#    return send_from_directory(filepath,as_attachment=True,mimetype='audio/mp3')
#if file:
#            filename = secure_filename(file.filename)
#            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
if __name__ == '__main__':
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug=True,port = 3000)