from wsgiref import simple_server
import json
from utils import *
import falcon
from CssConection import *


app = falcon.API()
res = Resource(app)
app.add_route('/', Main())
app.add_route('/train', TrainPage())
app.add_route("/jquery", JQUERY())
app.add_route("/test", Img())
app.add_route('/images',res)
app.add_route("/train/res", Train())
# app.add_route(res.image_path, GetImg(res.image_path))
connect_css(app)

if __name__ == "__main__":
    host = "127.0.0.1"
    port = 8000
    http = simple_server.make_server(host, port, app)
    print("Serving on %s:%s" % (host, port))
    http.serve_forever()
