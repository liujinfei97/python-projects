#所有可以被访问的URL列表


from views import *

urls = [
    ('/time',show_time),
    ('/hello',say_hi),
    ('/bye',say_bye)
]