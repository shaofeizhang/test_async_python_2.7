import tornado.ioloop
import tornado.web
from tornado import httpclient
import tornado.gen
import requests
import json
from tornado import gen
import tornado.ioloop
from tornado import testing


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Desfault get handler")

class GetHandler(tornado.web.RequestHandler):
    def get(self):
        url = "https://api.github.com/events"
        r = requests.get(url)
        self.write(r.content)

class PostHandler(tornado.web.RequestHandler):
    def post(self):
        r = requests.post('https://httpbin.org/post')
        self.write(r.content)
        
class WebPage(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")

class GenAsyncHandler(tornado.web.RequestHandler):
    @gen.coroutine
    def get(self):
        http_client = httpclient.AsyncHTTPClient()
        response1 = yield http_client.fetch("http://google.com")
        print(response1.request_time)
        response2 = yield http_client.fetch("http://www.qq.com")
        print(response2.request_time)
        
class ListAsyncHandler(tornado.web.RequestHandler):
    @gen.coroutine
    def get(self):
        http_client = httpclient.AsyncHTTPClient()
        lineList = [line.rstrip('\n') for line in open("url_list.txt")]

        for i in lineList: 
         try:
             response1 = yield http_client.fetch(i)
             print(response1.request_time)
         except:
             print("An exception occurred with"+i)
        print("done")
        
class ListAsyncHandler1(tornado.web.RequestHandler):
    @gen.coroutine
    def get(self):
        http_client = httpclient.AsyncHTTPClient()
        response1, response2, response3 = yield [http_client.fetch("http://google.com"),
                                  http_client.fetch("http://www.qq.com"),http_client.fetch("http://www.amazon.com")]
        
        print(response1.request_time)
        print(response2.request_time)
        print(response3.request_time)
        
# This test uses coroutine style.
class MyTestCase(testing.AsyncTestCase):
    @tornado.testing.gen_test
    def test_http_fetch(self):
        client = AsyncHTTPClient()
        response = yield client.fetch("http://www.tornadoweb.org")
        # Test contents of response
        self.assertIn("FriendFeed", response.body)

# This test uses argument passing between self.stop and self.wait.
class MyTestCase2(testing.AsyncTestCase):
    def test_http_fetch(self):
        client = AsyncHTTPClient()
        client.fetch("http://www.tornadoweb.org/", self.stop)
        response = self.wait()
        # Test contents of response
        self.assertIn("FriendFeed", response.body)
         

def make_app():
    return tornado.web.Application([
        (r"/", GenAsyncHandler),
        (r"/list",ListAsyncHandler),
        (r"/list1",ListAsyncHandler1),
        (r"/post", PostHandler),
        (r"/index", WebPage)
    ])

if __name__ == "__main__":
    
    app = make_app()
    app.listen(8888)
    print("PORT 8888 is listening")
    tornado.ioloop.IOLoop.current().start()
    

