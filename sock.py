import utils
import wstrans
import json
import uuid

from events import REventTarget

class SockPy(REventTarget):
  CONNECTING = 0
  OPEN = 1
  CLOSING = 2
  CLOSED = 3
  def __init__(self, url,devel=False,debug=False,info=None,rtt=None):
    self._base_url = url
    self._server = utils.random_number_string(1000)
    self.protocol = "websocket"
    self.readyState = SockPy.CONNECTING
    self._connid = utils.random_string(8)
    self._trans_url = self._base_url + '/' + self._server + '/' + self._connid
    self._transport = None
    REventTarget.__init__(self)
    
  def connect(self):
    self._transport = wstrans.WebSocketTransport(self,self._trans_url)
    self._transport.connect()

  def _dispatchOpen(self):
    if self.readyState == SockPy.CONNECTING:
      self.readyState = SockPy.OPEN
      self.dispatchEvent("open")
    else:
      self._didClose(1006, "Server lost session")
  def _dispatchMessage(self,data):
    if self.readyState != SockPy.OPEN:
      return
    self.dispatchEvent("message", data)
  def _dispatchHeartbeat(self):
    if self.readyState != SockPy.OPEN:
      return
    self.dispatchEvent("heartbeat")
  def _didClose(self, code, reason):
    if self.readyState != SockPy.CONNECTING and self.readyState != SockPy.OPEN and self.readyState != SockPy.CLOSING:
      raise Exception("INVALID_STATE_ERR")
    if self._transport:
      self._transport.doCleanup()
      self._transport = None
    close_data = {"code":code,"reason":reason,"wasClean":utils.userSetCode(code)}
    self.readyState = SockPy.CLOSED
    self.dispatchEvent("close",close_data)
    
  def _didMessage(self, data):
    type = str(data)[0:1]
    if type=='o':
      self._dispatchOpen()
    elif type=='a':
      payload = json.loads(str(data)[1:] or '[]')
      for p in payload:
        self._dispatchMessage(p)
    elif type=='m':
      payload = json.loads(data[1:] or 'null')
      self._dispatchMessage(payload)      
    elif type=='c':
      payload = json.loads(data[1:] or '[null,null]')
      self._didClose(payload[0],payload[1])
    elif type=='h':
      self._dispatchHeartbeat()
    
  def close(self):
    if code and not utilsl.userSetCode(code):
      raise Exception("INVALID_ACCESS_ERR")
    if self.readyState != SockPy.CONNECTING and self.readyState != SockPy.OPEN:
      return False
    self.readyState = SockPy.CLOSING
    self._didClose(code or 1000, reason or "Normal closure")
    return True

  def send(self, data):
    if self.readyState == SockPy.CONNECTING:
      raise Exception("INVALID_ACCESS_ERR")
    if self.readyState == SockPy.OPEN:
      self._transport.doSend(utils.quote('' + data))
    return True

if __name__ == "__main__":

  uid = str(uuid.uuid4())
  data = json.dumps({"type":"send","address":"vertx.basicauthmanager.login","body":{"username":"dev","password":"dev"},"replyAddress":uid})        
  def onopen(_data):
    sock.send(data)
  def onmessage(data):
    print data

  sock = SockPy("http://localhost:8080/eventbus")
  sock.addEventListener("open", onopen)
  sock.addEventListener("message", onmessage)
  sock.connect()
