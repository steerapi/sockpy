import math
import random
import json

random_string_chars = 'abcdefghijklmnopqrstuvwxyz0123456789_'

def random_string(length, maxV=None):
  maxV = maxV or len(random_string_chars)
  ret = []
  for i in range(length):
    ret.append( random_string_chars[int(math.floor(random.random() * maxV))] )
  return ''.join(ret)

def closeFrame(code,reason):
  return 'c'+json.dumps([code, reason])

def quote(string):
  """
    Quote string, TODO: also taking care of unicode characters that browsers
    often break. Especially, take care of unicode surrogates:
    http://en.wikipedia.org/wiki/Mapping_of_Unicode_characters#Surrogates
  """
  quoted = json.dumps(string)
  return quoted

def random_number(maxV):
  return math.floor(random.random() * maxV)

def random_number_string(maxV):
  t = len(''+str(maxV - 1))
  p = '0'*(t+1)
  return (p + str(int(random_number(maxV))))[-t:]

def userSetCode(code):
  return code == 1000 or (code >= 3000 and code <= 4999)
  
  # 
  # // Assuming that url looks like: http://asdasd:111/asd
  # utils.getOrigin = function(url) {
  #     url += '/'
  #     parts = url.split('/').slice(0, 3)
  #     return parts.join('/')
  # }
  # 
  # utils.isSameOriginUrl = function(url_a, url_b) {
  #     // location.origin would do, but it's not always available.
  #     if (!url_b) url_b = _window.location.href
  # 
  #     return (url_a.split('/').slice(0,3).join('/')
  #                 ===
  #             url_b.split('/').slice(0,3).join('/'))
  # }
  # 
  # utils.getParentDomain = function(url) {
  #     // ipv4 ip address
  #     if (/^[0-9.]*$/.test(url)) return url
  #     // ipv6 ip address
  #     if (/^\[/.test(url)) return url
  #     // no dots
  #     if (!(/[.]/.test(url))) return url
  # 
  #     parts = url.split('.').slice(1)
  #     return parts.join('.')
  # }
  # 
  # utils.objectExtend = function(dst, src) {
  #     for(k in src) {
  #         if (src.hasOwnProperty(k)) {
  #             dst[k] = src[k]
  #         }
  #     }
  #     return dst
  # }
  # 
  # WPrefix = '_jp'
  # 
  # utils.polluteGlobalNamespace = function() {
  #     if (!(WPrefix in _window)) {
  #         _window[WPrefix] = {}
  #     }
  # }
  # 
  # 
  # utils.userSetCode = function (code) {
  #     return code === 1000 || (code >= 3000 && code <= 4999)
  # }
  # 
  # // See: http://www.erg.abdn.ac.uk/~gerrit/dccp/notes/ccid2/rto_estimator/
  # // and RFC 2988.
  # utils.countRTO = function (rtt) {
  #     rto
  #     if (rtt > 100) {
  #         rto = 3 * rtt // rto > 300msec
  #     } else {
  #         rto = rtt + 200 // 200msec < rto <= 300msec
  #     }
  #     return rto
  # }
  # 
  # utils.log = function() {
  #     if (_window.console && console.log && console.log.apply) {
  #         console.log.apply(console, arguments)
  #     }
  # }
  # 
  # utils.bind = function(fun, that) {
  #     if (fun.bind) {
  #         return fun.bind(that)
  #     } else {
  #         return function() {
  #             return fun.apply(that, arguments)
  #         }
  #     }
  # }
  # 
  # utils.flatUrl = function(url) {
  #     return url.indexOf('?') === -1 && url.indexOf('#') === -1
  # }
  # 
  # utils.amendUrl = function(url) {
  #     dl = _document.location
  #     if (!url) {
  #         throw new Error('Wrong url for SockJS')
  #     }
  #     if (!utils.flatUrl(url)) {
  #         throw new Error('Only basic urls are supported in SockJS')
  #     }
  # 
  #     //  '//abc' --> 'http://abc'
  #     if (url.indexOf('//') === 0) {
  #         url = dl.protocol + url
  #     }
  #     // '/abc' --> 'http://localhost:80/abc'
  #     if (url.indexOf('/') === 0) {
  #         url = dl.protocol + '//' + dl.host + url
  #     }
  #     // strip trailing slashes
  #     url = url.replace(/[/]+$/,'')
  #     return url
  # }
  # 
  # // IE doesn't support [].indexOf.
  # utils.arrIndexOf = function(arr, obj){
  #     for(i=0 i < arr.length i++){
  #         if(arr[i] === obj){
  #             return i
  #         }
  #     }
  #     return -1
  # }
  # 
  # utils.arrSkip = function(arr, obj) {
  #     idx = utils.arrIndexOf(arr, obj)
  #     if (idx === -1) {
  #         return arr.slice()
  #     } else {
  #         dst = arr.slice(0, idx)
  #         return dst.concat(arr.slice(idx+1))
  #     }
  # }
  # 
  # // Via: https://gist.github.com/1133122/2121c601c5549155483f50be3da5305e83b8c5df
  # utils.isArray = Array.isArray || function(value) {
  #     return {}.toString.call(value).indexOf('Array') >= 0
  # }
  # 
  # utils.delay = function(t, fun) {
  #     if(typeof t === 'function') {
  #         fun = t
  #         t = 0
  #     }
  #     return setTimeout(fun, t)
  # }
  # 
  # 
  # // Chars worth escaping, as defined by Douglas Crockford:
  # //   https://github.com/douglascrockford/JSON-js/blob/47a9882cddeb1e8529e07af9736218075372b8ac/json2.js#L196
  # json_escapable = /[\\\"\x00-\x1f\x7f-\x9f\u00ad\u0600-\u0604\u070f\u17b4\u17b5\u200c-\u200f\u2028-\u202f\u2060-\u206f\ufeff\ufff0-\uffff]/g,
  #     json_lookup = {
  # "\u0000":"\\u0000","\u0001":"\\u0001","\u0002":"\\u0002","\u0003":"\\u0003",
  # "\u0004":"\\u0004","\u0005":"\\u0005","\u0006":"\\u0006","\u0007":"\\u0007",
  # "\b":"\\b","\t":"\\t","\n":"\\n","\u000b":"\\u000b","\f":"\\f","\r":"\\r",
  # "\u000e":"\\u000e","\u000f":"\\u000f","\u0010":"\\u0010","\u0011":"\\u0011",
  # "\u0012":"\\u0012","\u0013":"\\u0013","\u0014":"\\u0014","\u0015":"\\u0015",
  # "\u0016":"\\u0016","\u0017":"\\u0017","\u0018":"\\u0018","\u0019":"\\u0019",
  # "\u001a":"\\u001a","\u001b":"\\u001b","\u001c":"\\u001c","\u001d":"\\u001d",
  # "\u001e":"\\u001e","\u001f":"\\u001f","\"":"\\\"","\\":"\\\\",
  # "\u007f":"\\u007f","\u0080":"\\u0080","\u0081":"\\u0081","\u0082":"\\u0082",
  # "\u0083":"\\u0083","\u0084":"\\u0084","\u0085":"\\u0085","\u0086":"\\u0086",
  # "\u0087":"\\u0087","\u0088":"\\u0088","\u0089":"\\u0089","\u008a":"\\u008a",
  # "\u008b":"\\u008b","\u008c":"\\u008c","\u008d":"\\u008d","\u008e":"\\u008e",
  # "\u008f":"\\u008f","\u0090":"\\u0090","\u0091":"\\u0091","\u0092":"\\u0092",
  # "\u0093":"\\u0093","\u0094":"\\u0094","\u0095":"\\u0095","\u0096":"\\u0096",
  # "\u0097":"\\u0097","\u0098":"\\u0098","\u0099":"\\u0099","\u009a":"\\u009a",
  # "\u009b":"\\u009b","\u009c":"\\u009c","\u009d":"\\u009d","\u009e":"\\u009e",
  # "\u009f":"\\u009f","\u00ad":"\\u00ad","\u0600":"\\u0600","\u0601":"\\u0601",
  # "\u0602":"\\u0602","\u0603":"\\u0603","\u0604":"\\u0604","\u070f":"\\u070f",
  # "\u17b4":"\\u17b4","\u17b5":"\\u17b5","\u200c":"\\u200c","\u200d":"\\u200d",
  # "\u200e":"\\u200e","\u200f":"\\u200f","\u2028":"\\u2028","\u2029":"\\u2029",
  # "\u202a":"\\u202a","\u202b":"\\u202b","\u202c":"\\u202c","\u202d":"\\u202d",
  # "\u202e":"\\u202e","\u202f":"\\u202f","\u2060":"\\u2060","\u2061":"\\u2061",
  # "\u2062":"\\u2062","\u2063":"\\u2063","\u2064":"\\u2064","\u2065":"\\u2065",
  # "\u2066":"\\u2066","\u2067":"\\u2067","\u2068":"\\u2068","\u2069":"\\u2069",
  # "\u206a":"\\u206a","\u206b":"\\u206b","\u206c":"\\u206c","\u206d":"\\u206d",
  # "\u206e":"\\u206e","\u206f":"\\u206f","\ufeff":"\\ufeff","\ufff0":"\\ufff0",
  # "\ufff1":"\\ufff1","\ufff2":"\\ufff2","\ufff3":"\\ufff3","\ufff4":"\\ufff4",
  # "\ufff5":"\\ufff5","\ufff6":"\\ufff6","\ufff7":"\\ufff7","\ufff8":"\\ufff8",
  # "\ufff9":"\\ufff9","\ufffa":"\\ufffa","\ufffb":"\\ufffb","\ufffc":"\\ufffc",
  # "\ufffd":"\\ufffd","\ufffe":"\\ufffe","\uffff":"\\uffff"}
  # 
  # // Some extra characters that Chrome gets wrong, and substitutes with
  # // something else on the wire.
  # extra_escapable = /[\x00-\x1f\ud800-\udfff\ufffe\uffff\u0300-\u0333\u033d-\u0346\u034a-\u034c\u0350-\u0352\u0357-\u0358\u035c-\u0362\u0374\u037e\u0387\u0591-\u05af\u05c4\u0610-\u0617\u0653-\u0654\u0657-\u065b\u065d-\u065e\u06df-\u06e2\u06eb-\u06ec\u0730\u0732-\u0733\u0735-\u0736\u073a\u073d\u073f-\u0741\u0743\u0745\u0747\u07eb-\u07f1\u0951\u0958-\u095f\u09dc-\u09dd\u09df\u0a33\u0a36\u0a59-\u0a5b\u0a5e\u0b5c-\u0b5d\u0e38-\u0e39\u0f43\u0f4d\u0f52\u0f57\u0f5c\u0f69\u0f72-\u0f76\u0f78\u0f80-\u0f83\u0f93\u0f9d\u0fa2\u0fa7\u0fac\u0fb9\u1939-\u193a\u1a17\u1b6b\u1cda-\u1cdb\u1dc0-\u1dcf\u1dfc\u1dfe\u1f71\u1f73\u1f75\u1f77\u1f79\u1f7b\u1f7d\u1fbb\u1fbe\u1fc9\u1fcb\u1fd3\u1fdb\u1fe3\u1feb\u1fee-\u1fef\u1ff9\u1ffb\u1ffd\u2000-\u2001\u20d0-\u20d1\u20d4-\u20d7\u20e7-\u20e9\u2126\u212a-\u212b\u2329-\u232a\u2adc\u302b-\u302c\uaab2-\uaab3\uf900-\ufa0d\ufa10\ufa12\ufa15-\ufa1e\ufa20\ufa22\ufa25-\ufa26\ufa2a-\ufa2d\ufa30-\ufa6d\ufa70-\ufad9\ufb1d\ufb1f\ufb2a-\ufb36\ufb38-\ufb3c\ufb3e\ufb40-\ufb41\ufb43-\ufb44\ufb46-\ufb4e\ufff0-\uffff]/g,
  #     extra_lookup
  # 
  # // JSON Quote string. Use native implementation when possible.
  # JSONQuote = (JSON && JSON.stringify) || function(string) {
  #     json_escapable.lastIndex = 0
  #     if (json_escapable.test(string)) {
  #         string = string.replace(json_escapable, function(a) {
  #             return json_lookup[a]
  #         })
  #     }
  #     return '"' + string + '"'
  # }
  # 
  # // This may be quite slow, so let's delay until user actually uses bad
  # // characters.
  # unroll_lookup = function(escapable) {
  #     i
  #     unrolled = {}
  #     c = []
  #     for(i=0 i<65536 i++) {
  #         c.push( String.fromCharCode(i) )
  #     }
  #     escapable.lastIndex = 0
  #     c.join('').replace(escapable, function (a) {
  #         unrolled[ a ] = '\\u' + ('0000' + a.charCodeAt(0).toString(16)).slice(-4)
  #         return ''
  #     })
  #     escapable.lastIndex = 0
  #     return unrolled
  # }
  # 
  # 
  # _all_protocols = ['websocket',
  #                       'xdr-streaming',
  #                       'xhr-streaming',
  #                       'iframe-eventsource',
  #                       'iframe-htmlfile',
  #                       'xdr-polling',
  #                       'xhr-polling',
  #                       'iframe-xhr-polling',
  #                       'jsonp-polling']
  # 
  # utils.probeProtocols = function() {
  #     probed = {}
  #     for(i=0 i<_all_protocols.length i++) {
  #         protocol = _all_protocols[i]
  #         // User can have a typo in protocol name.
  #         probed[protocol] = SockJS[protocol] &&
  #                            SockJS[protocol].enabled()
  #     }
  #     return probed
  # }
  # 
  # utils.detectProtocols = function(probed, protocols_whitelist, info) {
  #     pe = {},
  #         protocols = []
  #     if (!protocols_whitelist) protocols_whitelist = _all_protocols
  #     for(i=0 i<protocols_whitelist.length i++) {
  #         protocol = protocols_whitelist[i]
  #         pe[protocol] = probed[protocol]
  #     }
  #     maybe_push = function(protos) {
  #         proto = protos.shift()
  #         if (pe[proto]) {
  #             protocols.push(proto)
  #         } else {
  #             if (protos.length > 0) {
  #                 maybe_push(protos)
  #             }
  #         }
  #     }
  # 
  #     // 1. Websocket
  #     if (info.websocket !== false) {
  #         maybe_push(['websocket'])
  #     }
  # 
  #     // 2. Streaming
  #     if (pe['xhr-streaming'] && !info.null_origin) {
  #         protocols.push('xhr-streaming')
  #     } else {
  #         if (pe['xdr-streaming'] && !info.cookie_needed && !info.null_origin) {
  #             protocols.push('xdr-streaming')
  #         } else {
  #             maybe_push(['iframe-eventsource',
  #                         'iframe-htmlfile'])
  #         }
  #     }
  # 
  #     // 3. Polling
  #     if (pe['xhr-polling'] && !info.null_origin) {
  #         protocols.push('xhr-polling')
  #     } else {
  #         if (pe['xdr-polling'] && !info.cookie_needed && !info.null_origin) {
  #             protocols.push('xdr-polling')
  #         } else {
  #             maybe_push(['iframe-xhr-polling',
  #                         'jsonp-polling'])
  #         }
  #     }
  #     return protocols
  # }