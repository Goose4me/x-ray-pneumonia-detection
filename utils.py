import json
from keras.models import load_model
from keras.preprocessing import image
import numpy as np
import os
import uuid
import mimetypes
import falcon
from TrainModel import *

class Train():
    accurancy = 0
    def on_get(self, req, resp):
        if self.accurancy == 0:
            self.accurancy = train(0)
        resp.status = falcon.HTTP_200
        resp.body = json.dumps({'accurancy':self.accurancy})


    def on_post(self, req, resp):
        epochs = req.bounded_stream.read(req.content_length)
        print(req.bounded_stream.read(req.content_length))
        self.accurancy = train(int(epochs))
        resp.status = falcon.HTTP_200
        resp.body = json.dumps({'accurancy':self.accurancy})
        


class Resource(object):
    image_path = "/img"
    prediction = -1
    def __init__(self, app):
        self.app = app
    def on_get(self, req, resp):
        if self.image_path != "/img":
            self.prediction = make_prediction(self.image_path)
        else:
            self.prediction = "No photo"
        resp.status = falcon.HTTP_200
        resp.body = json.dumps({"prediction":str(self.prediction), "path":self.image_path})


    def on_post(self, req, resp):
        ext = mimetypes.guess_extension(req.content_type)
        name = '{uuid}{ext}'.format(uuid=uuid.uuid4(), ext=ext)
        self.image_path = os.path.join("img", name)

        chunk = req.bounded_stream.read(req.content_length)
        with open(self.image_path, 'wb') as f:
            f.write(chunk)
        print(req.bounded_stream.read())
        resp.status = falcon.HTTP_200
        resp.location = '/images/' + name
        self.app.add_route("/"+self.image_path.replace("\\","/"), GetImg(self.image_path))
        resp.body = json.dumps({"prediction":str(self.prediction), "path":self.image_path.replace("\\","/")})



class Img():
    def on_get(self, req, res):
        res.content_type = "text/html"
        res.status = falcon.HTTP_200
        res.stream = open("templates/index.html", "rb")

    def on_post(self, req, res):
        res.stream = req.stream


class JQUERY():
    def on_get(self, req, res):
        res.content_type = "text/html"
        res.status = falcon.HTTP_200
        res.stream = open("resources/jquery-3.2.1.min.js", "rb")

class Main():
    def on_get(self,req,res):
        res.content_type = "text/html"
        res.status = falcon.HTTP_200
        res.stream = open("templates/main.html", "rb")


class TrainPage():
    def on_get(self, req, res):
        res.content_type = "text/html"
        res.status = falcon.HTTP_200
        res.stream = open("templates/train.html", "rb")

class GetImg():
    def __init__(self, path):
        self.path = path
    def on_get(self, req, res):
        res.status = falcon.HTTP_200
        res.stream = open(self.path, "rb")