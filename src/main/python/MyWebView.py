from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWebEngineWidgets import  QWebEngineSettings, QWebEngineScript
from PyQt5.QtCore import QFile
from QSSLoader import QSSLoader
import time


class MyWebView(QWebEngineView):

    def __init__(self, parent=None):
        super(MyWebView, self).__init__(parent)
        style_sheet = QSSLoader.read_qss_file("./scrollbarstyle.css")
        styleJS = ("(function() {"
                 "css = document.createElement('style');"
                 "css.type = 'text/css';"
                 "css.id = 'scrollbarStyle';"
                 "document.head.append(css);"
                 "css.innerText =`"+style_sheet+"`;})()\n")
        script = QWebEngineScript()
        script.setWorldId(QWebEngineScript.MainWorld)
        script.setSourceCode(styleJS);

        self.page().scripts().insert(script);
        self.page().runJavaScript(styleJS, QWebEngineScript.ApplicationWorld)
        self.settings().setAttribute(QWebEngineSettings.JavascriptEnabled, True)
        self.settings().setAttribute(QWebEngineSettings.LocalContentCanAccessRemoteUrls,
                                            True)
        self.settings().setAttribute(QWebEngineSettings.ErrorPageEnabled, True)
        self.settings().setAttribute(QWebEngineSettings.PluginsEnabled, True)

    # 重写createwindow()
    # def createWindow(self, QWebEnginePage_WebWindowType):
    #     new_webview = MyWebView()
    #     # style_sheet = QSSLoader.read_qss_file(":/scrollbarstyle.css")
    #     # new_webview.setStyle(style_sheet)
    #     new_webview.settings().setAttribute(QWebEngineSettings.JavascriptEnabled, True)
    #     new_webview.settings().setAttribute(QWebEngineSettings.LocalContentCanAccessRemoteUrls,
    #                                          True)
    #     new_webview.settings().setAttribute(QWebEngineSettings.ErrorPageEnabled, True)
    #     new_webview.settings().setAttribute(QWebEngineSettings.PluginsEnabled, True)
    #     styleJS = ("(function() {"
    #                "css = document.createElement('link');"
    #                "css.type = 'text/css';"
    #                "css.id = 'scrollbarStyle';"
    #                "document.body.append(css);"
    #                "css.href ='http://localhost/scrollbarstyle.css';})()\n")
    #     script = QWebEngineScript()
    #     script.setWorldId(QWebEngineScript.MainWorld)
    #     script.setSourceCode(styleJS);
    #
    #     new_webview.page().scripts().insert(script);
    #     new_webview.page().runJavaScript(styleJS, QWebEngineScript.ApplicationWorld)
    #     self.mainwindow.create_tab(new_webview)
    #     return new_webview