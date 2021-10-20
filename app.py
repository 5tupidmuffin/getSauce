from getSauce import *
from user import user
from flask_sqlalchemy import SQLAlchemy
from models import *
from werkzeug.utils import secure_filename
import os
from api import *
from datetime import datetime
from models import results
from utils import getAnimeInfo, getVideoInfo, logit



UPLOAD_FOLDER = './UploadedImages'  # save uploaded files in this folder
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}  # supported File formats
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.register_blueprint(user)

def addResult(username, title, dateofsearch):
    """
    add results to the database

    username : username of user
    title : results title
    dateofsearch : time on which search was performed (datetime object)
    """
    newResult = results(username, title, dateofsearch)
    db.session.add(newResult)  # add new result
    db.session.commit()

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#  go to homepage
@app.route('/', methods= ['GET'])
def home():
    logit("Displaying Homepage")
    return render_template('./index.html')


@app.route('/results', methods= ['GET', 'POST'])
def resultspage():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
           
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')

            # if file is not uploaded the image link availability will be checked
            ImageLink = request.form['ImageLink']

            if ImageLink != '':
                logit("*** Image taken from Provided Link ***")

                results = asyncio.run(getUrlSauce(ImageLink))

                logit("******** Results Fetched From API ********")

                if len(results) == 0:  # if no results are found
                    logit("******* No Results Found *******")
                    return render_template('./results.html', results = None)

                if (results[0].type == 'video' or results[0].type == 'anime') and ('ActiveUser' in session):
                    currentTime = datetime.now()
                    addResult(session['ActiveUser'], results[0].title, currentTime)
                    logit("Search Saved in Database")
                    logit("Result Title: " + results[0].title)

                    if results[0].type == 'video':
                        extrainfo = getVideoInfo(results[0].url)
                        logit("Displaying Results Page")
                        return render_template('./results.html', results = results, extrainfo = extrainfo)
                    else:
                        extrainfo = getAnimeInfo(results[0].url)
                        logit("Displaying Results Page")
                        return render_template('./results.html', results = results, extrainfo = extrainfo)

                elif (results[0].type == 'video' or results[0].type == 'anime'):

                    if results[0].type == 'video':
                        extrainfo = getVideoInfo(results[0].url)
                        logit("Displaying Results Page")
                        return render_template('./results.html', results = results, extrainfo = extrainfo)
                    else:
                        extrainfo = getAnimeInfo(results[0].url)
                        logit("Displaying Results Page")
                        return render_template('./results.html', results = results, extrainfo = extrainfo)

                else:
                    logit("Displaying Results Page")
                    return render_template('./results.html', results = None)

            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            logit('***** Image Uploaded Successfully *****')

            logit("Filename is - " + file.filename)  # print the Filename
            pathToFile = './UploadedImages/' + file.filename

            results = asyncio.run(getImageSauce(pathToFile))

            logit("******** Results Fetched From API ********")


            if len(results) == 0:  # if no results are found
                logit("******* No Results Found *******")
                return render_template('./results.html', results = None)

            logit("results length : " + str(len(results)))
            if (results[0].type == 'video' or results[0].type == 'anime') and ('ActiveUser' in session):
                currentTime = datetime.now()
                addResult(session['ActiveUser'], results[0].title, currentTime)
                logit("Search Saved in Database")
                logit("Result Title: " + results[0].title)

                if results[0].type == 'video':
                    extrainfo = getVideoInfo(results[0].url)
                    logit("Displaying Results Page")
                    return render_template('./results.html', results = results, extrainfo = extrainfo)
                else:
                    extrainfo = getAnimeInfo(results[0].url)
                    logit("Displaying Results Page")
                    return render_template('./results.html', results = results, extrainfo = extrainfo)

            elif (results[0].type == 'video' or results[0].type == 'anime'):

                if results[0].type == 'video':
                    extrainfo = getVideoInfo(results[0].url)
                    logit("Displaying Results Page")
                    return render_template('./results.html', results = results, extrainfo = extrainfo)
                else:
                    extrainfo = getAnimeInfo(results[0].url)
                    logit("Displaying Results Page")
                    return render_template('./results.html', results = results, extrainfo = extrainfo)

            else:
                logit("displaying empty results")
                return render_template('./results.html', results = None)

    else:
        logit("redirected to Homepage")
        return redirect(url_for('home'))


#  go to about us page
@app.route('/about')
def aboutus():
    logit("Displaying About Page")
    return render_template('./about.html')

# generic error handler
@app.errorhandler(Exception)
def ErrorDisplay(e):
    print()
    logit("ERROR --> " + str(e))
    logit("Displaying Error Page")
    return render_template('./error.html', error = e)  # generic error handle

if __name__ == '__main__':
    db.create_all()
    logit("getSauce Successfully Started")
    app.run(debug = True, ssl_context='adhoc')  ## ssl_context so as to run app on https which will solve the anidb poster fetch problem

