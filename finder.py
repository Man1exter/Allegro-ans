import requests
from bs4 import BeautifulSoup
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *


class AllegroScraper(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Allegro Finder")
        self.setGeometry(100, 100, 800, 600)

        self.search_label = QLabel("Wyszukiwanie:")
        self.search_box = QLineEdit()
        self.search_button = QPushButton("Szukaj TOP10 aukcji z słowem kluczowym")
        self.search_result_label = QLabel("Wyniki wyszukiwania:")
        self.search_result_list = QListWidget()
        
        self.search_label.setStyleSheet('background-color:yellow; color: red; font-weight:bold; font-size: 20px;')
        self.search_label.setAlignment(Qt.AlignCenter)
        self.search_box.setStyleSheet('background-color:gray; color: black; font-weight:bold; font-size: 20px;')
        self.search_button.setStyleSheet('background-color:yellow; color: red; font-weight:bold; font-size: 20px;')
        self.search_result_label.setStyleSheet('background-color:yellow; color: red; font-weight:bold; font-size: 20px;')
        self.search_result_label.setAlignment(Qt.AlignCenter)
        self.search_result_list.setStyleSheet('background-color:gray; color: black; font-weight:bold; font-size: 20px;')

        layout = QVBoxLayout()
        layout.addWidget(self.search_label)
        layout.addWidget(self.search_box)
        layout.addWidget(self.search_button)
        layout.addWidget(self.search_result_label)
        layout.addWidget(self.search_result_list)
        self.setLayout(layout)

        self.search_button.clicked.connect(self.search)

    def search(self):
        query = self.search_box.text()
        url = f"https://allegro.pl/listing?string={query}&bmatch=baseline-product-cl-eyesa2-engag-dict43-ele-1-1-0318"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        listings = soup.find_all("div", class_="_9c44d_2I0-J")

        self.search_result_list.clear()
        for i, listing in enumerate(listings[:10]):
            title = listing.find("h2", class_="_9c44d_3pyzl _1h8um_1kwz7 _1fwol_1h8um").text
            price = listing.find("div", class_="_9c44d_1zemI _1fkm6_2GcLh").text
            url = listing.find("a", class_="_9c44d_2Kt69")["href"]
            item = f"{i+1}. {title} ({price})\n{url}"
            self.search_result_list.addItem(item)


if __name__ == "__main__":
    app = QApplication([])
    scraper = AllegroScraper()
    scraper.setStyleSheet('background-color:black;')
    scraper.show()
    app.exec()
