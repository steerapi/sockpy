from ws4py.client.threadedclient import WebSocketClient
import utils

class WebSocketTransport(WebSocketClient):
  roundTrips = 2
  def __init__(self, ri, trans_url):
    url = trans_url + '/websocket'
    if url[0:5] == "https":
      url = 'wss' + url[5:]
    else:
      url = 'ws' + url[4:]
    self.ri = ri
    self.url = url
    WebSocketClient.__init__(self,url)
  def opened(self):
    pass
    # print "Connection opened..."
  def closed(self, code, reason=None):
    # print "[Connection closed]", code, (reason if reason else "")
    self.ri._didMessage(utils.closeFrame(1006, "WebSocket connection broken"))
  def received_message(self, m):
    # print "[Message received]", m    
    self.ri._didMessage(m)
  def doSend(self,m):
    # print "[Message sent]", m 
    self.send('[' + m + ']')
  def doCleanup(self):
    self.close()
    self.ri = None
  def enabled():
    return True
