import falcon

class TrainCSS():
    def on_get(self,req,res):
        res.content_type = "text/css"
        res.status = falcon.HTTP_200
        res.stream = open("templates/css/train.css", "rb")

class MainCSS():
    def on_get(self,req,res):
        res.content_type = "text/css"
        res.status = falcon.HTTP_200
        res.stream = open("templates/css/main.css", "rb")

class MenuCSS():
    def on_get(self,req,res):
        res.content_type = "text/css"
        res.status = falcon.HTTP_200
        res.stream = open("templates/css/menu.css", "rb")

class IndexCSS():
    def on_get(self,req,res):
        res.content_type = "text/css"
        res.status = falcon.HTTP_200
        res.stream = open("templates/css/index.css", "rb")

def connect_css(app):
    app.add_route('/css/train.css', TrainCSS())
    app.add_route('/css/main.css', MainCSS())
    app.add_route('/css/menu.css', MenuCSS())
    app.add_route('/css/index.css', IndexCSS())