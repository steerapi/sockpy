from sock import SockPy
from events import REventTarget
import uuid
import json

class EventBus(REventTarget):
  CONNECTING = 0
  OPEN = 1
  CLOSING = 2
  CLOSED = 3

  TypeString = type("")
  TypeDict = type({})
  TypeFunction = type(lambda x:x)
  
  def onopen(self, message):
    self.state = EventBus.OPEN
    self.dispatchEvent("open")
    
  def onclose(self, message):
    self.state = EventBus.CLOSED
    self.dispatchEvent("close")

  def onmessage(self,message):
    data = json.loads(message)
    body = data["body"]
    replyAddress = None
    if "replyAddress" in data:
      replyAddress = data["replyAddress"]
    address = data["address"]
    replyHandler = None
    if replyAddress:
      def _replyHandler(reply,replyHandler):
        self.send(replyAddress,reply,replyHandler)
      replyHandler = _replyHandler
    handlers = None
    
    if address in self.handlerMap:
      handlers = self.handlerMap[address]
    if handlers:
      handlers_copy = handlers[:]
      for handler_copy in handlers_copy:
        handler_copy(body, replyHandler)
    else:
      handler = None
      print "reply",self.replyHandlers, address
      if address in self.replyHandlers:
        handler = self.replyHandlers[address]
      if handler:
        del self.replyHandlers[address]
        handler(body,replyHandler)

  def __init__(self,url,devel=False,debug=False,info=None,rtt=None):
    self.sockConn = SockPy(url,devel=devel,debug=debug,info=info,rtt=rtt)
    self.handlerMap = {}
    self.replyHandlers = {}
    self.state = EventBus.CONNECTING
    self.sockConn.addEventListener("open", self.onopen)
    self.sockConn.addEventListener("close", self.onclose)
    self.sockConn.addEventListener("message", self.onmessage)
    REventTarget.__init__(self)
    
  def checkOpen(self):
    if self.state != EventBus.OPEN:
      raise Exception("INVALID_STATE_ERR")    

  def checkSpecified(self,paramName, paramType, param=None, optional=False):
    if not optional and not param:
      raise Exception("Parameter " + paramName + " must be specified")
    if param and type(param) != paramType:
      raise Exception("Parameter " + paramName + " must be of type " + paramType)    

  def connect(self):
    self.sockConn.connect()
  def close(self):
    self.checkOpen()
    self.state = EventBus.CLOSING
    self.sockJSConn.close()
  def readyState(self):
    return self.state
    
  def send(self,address,message,replyHandler):
    self.sendOrPub("send", address, message, replyHandler)
    
  def publish(self,address,message,replyHandler):
    self.sendOrPub("publish", address, message, replyHandler)
  
  def registerHandler(self,address,handler):
    print "registerHandler"
    self.checkSpecified("address", 'string', address)
    self.checkSpecified("handler", 'function', handler)
    self.checkOpen()
    handlers = None
    if address in self.handlerMap:
      handlers = self.handlerMap[address]
    if not handlers:
      handlers = [handler]
      self.handlerMap[address] = handlers
      msg = { "type":"register", "address": address }
      self.sockJSConn.send(json.dumps(msg))
    else:
      handlers.append(handler)

  def unregisterHandler(self,address,handler):
    self.checkSpecified("address", EventBus.TypeString, address)
    self.checkSpecified("handler", EventBus.TypeFunction, handler)
    self.checkOpen()
    handlers = None
    if address in self.handlerMap:
      handlers = self.handlerMap[address]
    if handlers:
      if handler in handlers:
        handlers.remove(handler)
      if len(handlers)==0:
        msg = { "type":"unregister", "address": address }
        self.sockJSConn.send(json.dumps(msg))
        del handlerMap[address]

  def sendOrPub(self, sendOrPub, address, message, replyHandler=None):
    self.checkSpecified("address", EventBus.TypeString, address, False)
    self.checkSpecified("message", EventBus.TypeDict, message, False)
    self.checkSpecified("replyHandler", EventBus.TypeFunction, replyHandler, True)
    self.checkOpen()
    envelope = { "type" : sendOrPub,
                 "address" : address,
                 "body" : message }
    if replyHandler:
      replyAddress = str(uuid.uuid4())
      envelope["replyAddress"] = replyAddress
      self.replyHandlers[replyAddress] = replyHandler
    jsonStr = json.dumps(envelope)
    self.sockConn.send(jsonStr)

if __name__ == "__main__":
  import time
  eb = EventBus("http://localhost:8080/eventbus")
  def onopen(message):
    print "onopen"
    def replyHandler(reply, replier=None):
      eb.send("vertx.basicauthmanager.login", {"username":"dev","password":"dev"}, replyHandler)
      print "onreply"
      print reply
    eb.send("vertx.basicauthmanager.login", {"username":"dev","password":"dev"}, replyHandler)
  eb.addEventListener("open", onopen)
  eb.connect()

  while True:
    time.sleep(1)


    