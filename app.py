from flask import Flask, render_template, url_for, request, redirect
import os

from crawler import TwitterClient, TweetCleaner



app = Flask(__name__)
client = TwitterClient()
cleaner = TweetCleaner()
clean = False



@app.route('/', methods=['GET','POST'])
def index():
    if request.method == 'POST':
        search_content = request.form["input"]
        
        ## Do processing on text and pass to text object below
        text = client.get_tweets_for_keyword(search_content)
        if clean:
            text = cleaner.process_tweets(text)
        # print(text)

        return render_template('d3.html', text=text)
    else:
        return render_template('index.html')



@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r


@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)

def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                 endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)



if __name__ == '__main__':
    
    
    app.run(debug=True, use_reloader=False)
