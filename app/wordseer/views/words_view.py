from flask.views import MethodView
from flask.json import jsonify, dumps
from flask import request
from sqlalchemy import func

from app import app, db
from app.wordseer import wordseer
from app.models import *

from app.helpers.application_view import register_rest_view

class WordsView(MethodView):

    def get(self, **kwargs):
        params = dict(kwargs, **request.args)
        keys = params.keys()

        if "project_id" in keys:
            project = Project.query.get(params["project_id"])
            part_of_speech = params["pos"][0]
            position = params["start"][0]
            limit = params["limit"][0]
            words_query = db.session.query(
                Word.lemma.label("lemma"),
                WordInSentence.surface.label("word"),
                func.count(Sentence.id).label("sentence_count")).\
                group_by(Word.lemma).\
                filter(Word.part_of_speech.like("%" + part_of_speech + "%")).\
                filter(Sentence.project_id == project.id).\
                filter(Word.id == WordInSentence.word_id).\
                filter(Sentence.id == WordInSentence.sentence_id)
            if "query_id" in keys:
                query = Query.query.get(params["query_id"])
                words_query.filter(SentenceInQuery.query_id == query.id)
                words_query.filter(SentenceInQuery.sentence_id == Sentence.id)

            #words = project.frequent_words(part_of_speech, limit)

            results = []

            for word in words_query:
                results.append({
                    "word": word.word,
                    "count": word.sentence_count,
                    "is_lemmatized": 1
                })

            return jsonify(results = results)

    def post(self):
        pass

    def delete(self, id):
        pass

    def put(self, id):
        pass

register_rest_view(
    WordsView,
    wordseer,
    'words_view',
    'word',
    parents=["project"],
)