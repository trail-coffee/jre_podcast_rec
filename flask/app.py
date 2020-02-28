from flask import Flask, Response, render_template, request
import json
import wtforms
from wtforms import StringField, Form, SelectField
from html import unescape
from recommender import recommender
import run_model as rm
import pickle

app = Flask(__name__)

episodes = rm.my_recommender.get_ep_names()
topics = rm.my_recommender.get_topics()

tpc_list = []
for i,v in enumerate(topics):
    tpc_list.append((topics[i],topics[i]))

class SearchForm(Form):
    autocomp = StringField('Pick Episode', id='city_autocomplete')
    toplist = SelectField('Pick Topic', choices = tpc_list, id='topic_list')


@app.route('/_autocomplete', methods=['GET'])
def autocomplete():
    return Response(json.dumps(episodes), mimetype='application/json')


@app.route('/', methods=['GET', 'POST'])
def index():
    form = SearchForm(request.form)
    return render_template("index.html", form=form)

@app.route('/ep_rec/', methods=['GET', 'POST'])
def ep_rec():
    form = SearchForm(request.form)
    ep_name = unescape(form.autocomp.data)
    ep_recs = rm.my_recommender.recommend_ep(ep_name)
    return Response(json.dumps(ep_recs), mimetype='application/json')

@app.route('/tpc_rec/', methods=['GET', 'POST'])
def topic_rec():
    form = SearchForm(request.form)
    topic_name = unescape(form.toplist.data)
    print(form.toplist.data)
    ep_recs = rm.my_recommender.recommend_topic(topic_name)
    return Response(json.dumps(ep_recs), mimetype='application/json')

if __name__ == '__main__':
    app.run(debug=True)
