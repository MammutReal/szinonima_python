import sys
import json

from PySide6.QtWidgets import QApplication, QMainWindow, QTextBrowser, QDockWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QCheckBox, QWidget
from PySide6.QtGui import Qt
from PySide6.QtCore import QRegularExpression, QRegularExpressionMatch, QUrl, QDir
from PySide6.QtWebEngineWidgets import QWebEngineView

TOBBSZOROS_SZOFAJOK = ["I.", "II.", "III.", "IV.", "V.", "VI.", "VII.", "VIII.", "IX.", "X"]

class Szinonimak:
    def __init__(self):
        with open('data.json', encoding="utf8") as json_file:
            self.szinonimak = json.load(json_file)

        self._words = []
        with open("words.txt", encoding="utf8") as word_file:
            data = word_file.read()
            self._words = data.split("\n")

        self._pattern = ""
        self._cimszo=True
        self._szinonimak=True
        self._szolasok=False
        self._antonimak=False
        self._exact_match=True
        self._rhyme = False  
        self._anagramma = False

    def _getszocikkfej(self, szinonima):
        html = "<strong>"
        re = QRegularExpression(self._pattern)

        if self._pattern != "":
            if self._anagramma:
                w = szinonima["szocikkfej"]["cimszo"].lower()
                w = "".join(sorted(w))
                if w == self._pattern:
                    html += '<span class="highlighted">' + szinonima["szocikkfej"]["cimszo"] + '</span>'
                else:
                    html += szinonima["szocikkfej"]["cimszo"]
            else:
                if re.match(szinonima["szocikkfej"]["cimszo"]).hasMatch():
                    html += '<span class="highlighted">' + szinonima["szocikkfej"]["cimszo"] + '</span>'
                else:
                    html += szinonima["szocikkfej"]["cimszo"]

        alakvaltozatok = []
        if "alakvaltozatok" in szinonima["szocikkfej"].keys():
            for alakvaltozat in szinonima["szocikkfej"]["alakvaltozatok"]:
                if self._pattern != "":
                    if self._anagramma:
                        w = alakvaltozat.lower()
                        w = "".join(sorted(w))
                        if w == self._pattern:
                            alakvaltozatok.append('<span class="highlighted">' + alakvaltozat + '</span>')
                        else:
                            alakvaltozatok.append(alakvaltozat)
                    else:
                        if re.match(alakvaltozat).hasMatch():
                            alakvaltozatok.append('<span class="highlighted">' + alakvaltozat + '</span>')
                        else:
                            alakvaltozatok.append(alakvaltozat)
            alakvaltozatok = ", ".join(alakvaltozatok)
            html += ", " + alakvaltozatok

        if "homonima" in szinonima["szocikkfej"].keys():
            html += "<sup>" + str(szinonima["szocikkfej"]["homonima"]) + "</sup>"
        if "tobbszoros_szofaj" in szinonima["szocikkfej"].keys():
            html += " " + TOBBSZOROS_SZOFAJOK[szinonima["szocikkfej"]["tobbszoros_szofaj"]-1]

        html += "</strong>"
        html += " (" + szinonima["szocikkfej"]["szofaj"] + ")"
        return html

    def _getszinonima(self, szinonima):
        parts = []
        if "ertelmi_kiegeszites_elotte" in szinonima.keys():
            parts.append("[" + szinonima["ertelmi_kiegeszites_elotte"] + "]")
        if "vonzat_elotte" in szinonima.keys():
            parts.append("&lt;" + szinonima["vonzat_elotte"] + "&gt;")
        re = QRegularExpression(self._pattern)
        
        szinonima_added = False
        if self._szinonimak:
            if self._pattern != "":
                if self._anagramma:
                    w = szinonima["szinonima"].lower()
                    w = "".join(sorted(w))
                    if w == self._pattern:
                        parts.append('<span class="highlighted">' + szinonima["szinonima"] + '</span>')
                        szinonima_added = True
                else:
                    if re.match(szinonima["szinonima"]).hasMatch():
                        parts.append('<span class="highlighted">' + szinonima["szinonima"] + '</span>')
                        szinonima_added = True
        if not szinonima_added:
            parts.append(szinonima["szinonima"])

        if "ertelmi_kiegeszites_mogotte" in szinonima.keys():
            parts.append("[" + szinonima["ertelmi_kiegeszites_mogotte"] + "]")
        if "vonzat_mogotte" in szinonima.keys():
            parts.append("&lt;" + szinonima["vonzat_mogotte"] + "&gt;")
        if "minosites" in szinonima.keys():
            parts.append("(<em>" + ", ".join(szinonima["minosites"]) + "</em>)")
        return " ".join(parts)

    def _getantonima(self, antonima):
        parts = []
        if "ertelmi_kiegeszites_elotte" in antonima.keys():
            parts.append("[" + antonima["ertelmi_kiegeszites_elotte"] + "]")
        if "vonzat_elotte" in antonima.keys():
            parts.append("&lt;" + antonima["vonzat_elotte"] + "&gt;")
        re = QRegularExpression(self._pattern)
        
        antonima_added = False
        if self._antonimak:
            if self._pattern != "":
                if self._anagramma:
                    w = antonima["antonima"].lower()
                    w = "".join(sorted(w))
                    if w == self._pattern:
                        parts.append('<span class="highlighted antonima">' + antonima["antonima"] + '</span>')
                        antonima_added = True
                else:
                    if re.match(antonima["antonima"]).hasMatch():
                        parts.append('<span class="highlighted antonima">' + antonima["antonima"] + '</span>')
                        antonima_added = True
        if not antonima_added:
            parts.append('<span class="antonima">' + antonima["antonima"] + '</span>')

        if "ertelmi_kiegeszites_mogotte" in antonima.keys():
            parts.append("[" + antonima["ertelmi_kiegeszites_mogotte"] + "]")
        if "vonzat_mogotte" in antonima.keys():
            parts.append("&lt;" + antonima["vonzat_mogotte"] + "&gt;")
        if "minosites" in antonima.keys():
            parts.append("(<em>" + ", ".join(antonima["minosites"]) + "</em>)")
        return " ".join(parts)

    def _getszolas(self, szolas):
        parts = []
        if "ertelmi_kiegeszites_elotte" in szolas.keys():
            parts.append("[" + szolas["ertelmi_kiegeszites_elotte"] + "]")
        if "vonzat_elotte" in szolas.keys():
            parts.append("&lt;" + szolas["vonzat_elotte"] + "&gt;")

        if self._szolasok:
            if self.szolas_re.match(szolas["szolas"]).hasMatch():
                parts.append('<span class="highlighted">' + szolas["szolas"] + '</span>')
            else:
                parts.append(szolas["szolas"])

        if "ertelmi_kiegeszites_mogotte" in szolas.keys():
            parts.append("[" + szolas["ertelmi_kiegeszites_mogotte"] + "]")
        if "vonzat_mogotte" in szolas.keys():
            parts.append("&lt;" + szolas["vonzat_mogotte"] + "&gt;")
        if "minosites" in szolas.keys():
            parts.append("(<em>" + ", ".join(szolas["minosites"]) + "</em>)")
        return " ".join(parts)

    def _getszinonimabokor(self, szinonimabokor):
        html = ""
        elo = []
        if "ertelmi_kiegeszites" in szinonimabokor.keys():
            elo.append("[" + szinonimabokor["ertelmi_kiegeszites"] + "]")
        if "vonzat" in szinonimabokor.keys():
            elo.append("&lt;" + szinonimabokor["vonzat"] + "&gt;")
        if "minosites" in szinonimabokor.keys():
            elo.append("(<em>" + ", ".join(szinonimabokor["minosites"]) + "</em>)")

        jelentesek = []
        for aljelentes in szinonimabokor["szinonimak"]:
            szinonimak = []
            for szinonima in aljelentes:
                szinonimak.append(self._getszinonima(szinonima))
            jelentesek.append(", ".join(szinonimak))

        szolasok = []
        if "szolasok" in szinonimabokor.keys():
            # html += " <strong>Sz:</strong> "
            for szolas in szinonimabokor["szolasok"]:
                szolasok.append(self._getszolas(szolas))

        antonimajelentesek = []
        if "antonimak" in szinonimabokor.keys():
            for aljelentes in szinonimabokor["antonimak"]:
                antonimak = []
                for antonima in aljelentes:
                    antonimak.append(self._getantonima(antonima))
                antonimajelentesek.append(", ".join(antonimak))

        if len(elo) > 0:
            html += " ".join(elo) + ": "
        html += "◊ "
        html += " | ".join(jelentesek)
        if len(szolasok) > 0:
            html += " <strong>Sz:</strong> "
            html += "; ".join(szolasok)
        if len(antonimajelentesek) > 0:
            html += " ♦ "
            html += " | ".join(antonimajelentesek)
        return html

    def _getszocikk(self, szinonima):
        html = '<div class="szocikk"><p class="firstline">'
        html += self._getszocikkfej(szinonima)
        html += " "
        html += self._getszinonimabokor(szinonima["szinonimabokrok"][0])
        html += "</p>"
        for i in range(1, len(szinonima["szinonimabokrok"])):
            html += '<p class="szinonimabokor">'
            szinonimabokor = szinonima["szinonimabokrok"][i]
            html += self._getszinonimabokor(szinonimabokor)
            html += "</p>"
        html += '</div>'
        return html

    def find(self, text):
        html = '<!DOCTYPE html><html lang="hu"></html><head><link rel="stylesheet" type="text/css" href="styles.css"></head></body>'
        szavak = []
        cimszavak = []
        szinonimak = []
        antonimak = []
        szolasok = []
        self._pattern = text

        self.szolas_pattern = ""
        self.szolas_re = QRegularExpression("")
        if self._szolasok:
            self.szolas_pattern = text
            self.szolas_re = QRegularExpression(self.szolas_pattern)

        if self._anagramma:
            self._pattern = text.lower()
            self._pattern = "".join(sorted(self._pattern))
        else:
            if self._rhyme:
                self._pattern = self._pattern.replace("?", "[bcdfghjklmnpqrstvwxyz]")
                self._pattern = self._pattern.replace("*", "[bcdfghjklmnpqrstvwxyz]*")
            else:
                letter = "["
                letter += "\\"
                letter += "wóőöúüűáéí"
                letter += "\\"
                letter += "-"
                letter += ","
                letter += "]"
                self._pattern = self._pattern.replace("?", letter).replace("*", letter + "*")
                self._pattern = self._pattern
            if self._exact_match:
                self._pattern = "^" + self._pattern + "$"
            re = QRegularExpression(self._pattern)

        for word in self._words:
            if self._anagramma:
                w = word.lower()
                w = sorted(w)
                if w == self._pattern:
                    szavak.append(word)
            else:
                match = re.match(word)
                if match.hasMatch():
                    szavak.append(word)

        for szinonima in self.szinonimak:
            if self._cimszo:
                if self._anagramma:
                    w = szinonima["szocikkfej"]["cimszo"].lower()
                    w = "".join(sorted(w))
                    if w == self._pattern:
                        cimszavak.append(szinonima)
                        szavak.append(szinonima["szocikkfej"]["cimszo"])
                    if "alakvaltozatok" in szinonima["szocikkfej"].keys():
                        for alakvaltozat in szinonima["szocikkfej"]["alakvaltozatok"]:
                            w = alakvaltozat.lower()
                            w = "".join(sorted(w))
                            if w == self._pattern:
                                szavak.append(alakvaltozat)
                                if szinonima not in cimszavak:
                                    cimszavak.append(szinonima)

                else:
                    match = re.match(szinonima["szocikkfej"]["cimszo"])
                    if match.hasMatch():
                        cimszavak.append(szinonima)
                        szavak.append(szinonima["szocikkfej"]["cimszo"])
                    if "alakvaltozatok" in szinonima["szocikkfej"].keys():
                        for alakvaltozat in szinonima["szocikkfej"]["alakvaltozatok"]:
                            match = re.match(alakvaltozat)
                            if match.hasMatch():
                                szavak.append(alakvaltozat)
                                if szinonima not in cimszavak:
                                    cimszavak.append(szinonima)
            for szinonimabokor in szinonima["szinonimabokrok"]:
                if self._szinonimak:
                    for aljelentes in szinonimabokor["szinonimak"]:
                        for item in aljelentes:
                            if self._anagramma:
                                w = item["szinonima"].lower()
                                w = "".join(sorted(w))
                                if w == self._pattern:
                                    szavak.append(item["szinonima"])
                                    if szinonima not in cimszavak and szinonima not in szinonimak:
                                        szinonimak.append(szinonima)
                            else:
                                match = re.match(item["szinonima"])
                                if match.hasMatch():
                                    szavak.append(item["szinonima"])
                                    if szinonima not in cimszavak and szinonima not in szinonimak:
                                        szinonimak.append(szinonima)
                if self._szolasok:
                    for szolas in szinonimabokor.get("szolasok", []):
                        match = self.szolas_re.match(szolas["szolas"])
                        if match.hasMatch():
                            if szinonima not in szolasok:
                                szolasok.append(szinonima)
                if self._antonimak:
                    for aljelentes in szinonimabokor.get("antonimak", []):
                        for item in aljelentes:
                            if self._anagramma:
                                w = item["antonima"].lower()
                                w = "".join(sorted(w))
                                if w == self._pattern:
                                    szavak.append(item["antonima"])
                                    if szinonima not in antonimak:
                                        antonimak.append(szinonima)
                            else:
                                match = re.match(item["antonima"])
                                if match.hasMatch():
                                    szavak.append(item["antonima"])
                                    if szinonima not in antonimak:
                                        antonimak.append(szinonima)

        if len(szavak) > 0:
            html += '<div class="section">'
            szavak = list(set(szavak))
            szavak.sort()
            html += '<p>' + ", ".join(szavak) + '</p>'
            html += '</div>'
        if len(cimszavak) > 0:
            html += '<div class="section">'
            for cimszo in cimszavak:
                html += self._getszocikk(cimszo)
            html += "</div>"
        if len(szinonimak) > 0:
            html += '<div class="section">'
            for szinonima in szinonimak:
                html += self._getszocikk(szinonima)
            html += '</div>'
        if len(szolasok) > 0:
            html += '<div class="section">'
            for szolas in szolasok:
                html += self._getszocikk(szolas)
            html += '</div>'
        if len(antonimak) > 0:
            html += '<div class="section">'
            for antonima in antonimak:
                html += self._getszocikk(antonima)
            html += '</div>'

        if len(cimszavak) == 0 and len(szinonimak) == 0 and len(szolasok) == 0 and len(antonimak) == 0:
            html += '<p class="notfound">Nincs találat</p>'

        html += "</body>"
        return html

    def get_all(self):
        html = '<!DOCTYPE html><html lang="hu"></html><head><link rel="stylesheet" type="text/css" href="styles.css"></head></body>'
        for szocikk in self.szinonimak:
            html += self._getszocikk(szocikk)
        html += "</body>"
        return html


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.szinonimak = Szinonimak()

        self.browser = QWebEngineView() #QTextBrowser()

        self.isFirst = True 
        self.browser.loadFinished.connect(self.onLoadFinished)

        # with open("styles.css") as file:
        #     self.browser.setStyleSheet(file.read())
        self.setCentralWidget(self.browser)
        # html = self.szinonimak.find("^a[bcdfghjklmnpqrstvwxyz]*a[bcdfghjklmnpqrstvwxyz]*ó$")
        # with open("temp.html", "w", encoding="utf8") as file:
        #     file.write(html)
        # self.browser.setHtml(html)
        dir = QDir()
        self.path = dir.absoluteFilePath("temp.html")
        self.browser.load(QUrl.fromLocalFile(self.path))

        self.dock = QDockWidget()
        self.dock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.dock)

        container = QWidget()
        self.dock.setWidget(container)
        layout = QVBoxLayout()

        search_layout = QHBoxLayout()
        self.search = QLineEdit(container)
        self.search.returnPressed.connect(self.onSearch)
        self.search.setToolTip("Minta alapján is lehet keresni, a * több, a ? egy karaktert helyettesít.\nEntert ütve is elindul a keresés.")
        self.search_button = QPushButton("Keresd!", container)
        self.search_button.setDefault(True)
        self.search_button.clicked.connect(self.onSearch)

        search_layout.addWidget(self.search)
        search_layout.addWidget(self.search_button)
        layout.addLayout(search_layout)

        layout.addSpacing(20)

        self.in_cimszo = QCheckBox("Címszóban", container)
        self.in_cimszo.setChecked(self.szinonimak._cimszo)
        self.in_cimszo.checkStateChanged.connect(self.onCimszo)
        self.in_szinonimak = QCheckBox("Szinonímák között", container)
        self.in_szinonimak.setChecked(self.szinonimak._szinonimak)
        self.in_szinonimak.checkStateChanged.connect(self.onSzinonimak)
        self.in_szolasok = QCheckBox("Szólások között", container)
        self.in_szolasok.setChecked(self.szinonimak._szolasok)
        self.in_szolasok.checkStateChanged.connect(self.onSzolasok)
        self.in_antonimak = QCheckBox("Antonimák között", container)
        self.in_antonimak.setChecked(self.szinonimak._antonimak)
        self.in_antonimak.checkStateChanged.connect(self.onAntonimak)
        layout.addWidget(self.in_cimszo)
        layout.addWidget(self.in_szinonimak)
        layout.addWidget(self.in_szolasok)
        layout.addWidget(self.in_antonimak)

        layout.addSpacing(20)

        self.exact_match = QCheckBox("Pontos egyezés", container)
        self.exact_match.setChecked(self.szinonimak._exact_match)
        self.exact_match.checkStateChanged.connect(self.onExactMatch)
        self.rhyme = QCheckBox("Rímkeresés", container)
        self.rhyme.setChecked(self.szinonimak._rhyme)
        self.rhyme.checkStateChanged.connect(self.onRhyme)
        self.rhyme.setToolTip("A megadott minta alapján keres, de csakis a mintában szereplő magánhangzókkal, minden más magánhangzót kiszűrve.")
        self.anagramma = QCheckBox("Anagramma", container)
        self.anagramma.setChecked(self.szinonimak._anagramma)
        self.anagramma.checkStateChanged.connect(self.onAnagramma)
        layout.addWidget(self.exact_match)
        layout.addWidget(self.rhyme)
        layout.addWidget(self.anagramma)

        # self.all_button = QPushButton("Komplett szinonimaszótár", container)
        # self.all_button.clicked.connect(self.onAll)
        # layout.addWidget(self.all_button)

        layout.addStretch(100)
        container.setLayout(layout)

    def onSearch(self):
        pattern = self.search.text()
        html = self.szinonimak.find(pattern)
        with open("temp.html", "w", encoding="utf8") as file:
            file.write(html)
        self.browser.reload()
        
    def onAll(self):
        html = self.szinonimak.get_all()        
        with open("temp.html", "w", encoding="utf8") as file:
            file.write(html)
        self.browser.reload()

    def onRhyme(self, state):
        self.szinonimak._rhyme = (state == Qt.CheckState.Checked)

    def onExactMatch(self, state):
        self.szinonimak._exact_match = (state == Qt.CheckState.Checked)

    def onCimszo(self, state):
        self.szinonimak._cimszo = (state == Qt.CheckState.Checked)

    def onSzinonimak(self, state):
        self.szinonimak._szinonimak = (state == Qt.CheckState.Checked)

    def onSzolasok(self, state):
        self.szinonimak._szolasok = (state == Qt.CheckState.Checked)
    
    def onAntonimak(self, state):
        self.szinonimak._antonimak = (state == Qt.CheckState.Checked)

    def onAnagramma(self, state):
        self.szinonimak._anagramma = (state == Qt.CheckState.Checked)

    def onLoadFinished(self):
        if self.isFirst:
            self.browser.reload()
        self.isFirst = False        

if __name__ == "__main__":
    app = QApplication()
    widget = MainWindow()
    widget.showMaximized()
    sys.exit(app.exec())
