import utils

class REventTarget:
  def __init__(self):
    self._listeners = {}
  def addEventListener(self,eventType,listener):
    if eventType not in self._listeners:
      self._listeners[eventType] = []
    arr = self._listeners[eventType]
    if listener not in arr:
      arr.append(listener)
  def removeEventListener(self,eventType,listener):
    if eventType not in self._listeners:
      return
    arr = self._listeners[eventType]
    if listener in arr:
      if len(arr)>1:
        self._listeners[eventType] = arr[:idx].append(arr[idx+1:])
      else:
        del self._listeners[eventType]
  def dispatchEvent(self,type,message=None):
    if type in self._listeners:
      for v in self._listeners[type]:
        v(message)
