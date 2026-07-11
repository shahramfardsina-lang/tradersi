from PySide6.QtCore import Qt, QTimer
from concurrent.futures import ThreadPoolExecutor, as_completed
from PySide6.QtGui import QColor
from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QListWidget,
    QTableWidget,
    QTableWidgetItem,
    QFrame,
    QLineEdit,
    QHeaderView,
)

from gui.styles import DARK_STYLE
from core.market_data import MarketData
from core.candles import get_candles
from core.indicators import calculate_rsi


class InfoCard(QFrame):

    def __init__(self, title, value, color):
        super().__init__()

        self.setObjectName("card")

        layout = QVBoxLayout(self)

        self.title = QLabel(title)
        self.title.setAlignment(Qt.AlignCenter)

        self.value = QLabel(value)
        self.value.setAlignment(Qt.AlignCenter)

        self.value.setStyleSheet(f"""
            color:{color};
            font-size:22px;
            font-weight:bold;
        """)

        layout.addWidget(self.title)
        layout.addWidget(self.value)

    def setValue(self, text):
        self.value.setText(text)


class MainWindow(QMainWindow):

    def __init__(self):

        super().__init__()

        self.setWindowTitle("Crypto AI Analyzer PRO")

        self.resize(1600,900)

        self.setStyleSheet(DARK_STYLE)

        central = QWidget()

        self.setCentralWidget(central)

        root = QHBoxLayout(central)

        ##################################################
        # LEFT MENU
        ##################################################

        self.menu = QListWidget()

        self.menu.addItems([

            "🏠 Dashboard",

            "📈 Market Scanner",

            "⭐ Watchlist",

            "📊 Charts",

            "💼 Portfolio",

            "🤖 AI Advisor",

            "📄 Reports",

            "⚙ Settings",

        ])

        self.menu.setMaximumWidth(220)

        root.addWidget(self.menu)

        ##################################################
        # RIGHT
        ##################################################

        right = QVBoxLayout()

        root.addLayout(right)

        ##################################################
        # TITLE
        ##################################################

        title = QLabel("Crypto AI Analyzer PRO")

        title.setStyleSheet("""

            font-size:30px;

            font-weight:bold;

        """)

        right.addWidget(title)

        ##################################################
        # TOP CARDS
        ##################################################

        cards = QHBoxLayout()

        self.marketCard = InfoCard(
            "Market Status",
            "...",
            "#22c55e"
        )

        self.fearCard = InfoCard(
            "Fear & Greed",
            "...",
            "#f59e0b"
        )

        self.domCard = InfoCard(
            "BTC Dominance",
            "...",
            "#3b82f6"
        )

        self.aiCard = InfoCard(
            "AI Score",
            "...",
            "#ef4444"
        )

        self.coinCard = InfoCard(
            "Coins",
            "0",
            "#14b8a6"
        )

        cards.addWidget(self.marketCard)
        cards.addWidget(self.fearCard)
        cards.addWidget(self.domCard)
        cards.addWidget(self.aiCard)
        cards.addWidget(self.coinCard)

        right.addLayout(cards)
        ##################################################
        # SEARCH
        ##################################################
        self.search = QLineEdit()
        self.search.textChanged.connect(
            self.filter_table
        )
        self.search.setPlaceholderText(
            "Search coin..."
        )

        right.addWidget(self.search)
        ##################################################
        # TABLE
        ##################################################

        self.table = QTableWidget()
        self.table.setStyleSheet("""
        QTableWidget {
            background-color: #111111;
            alternate-background-color: #222222;
            color: white;
            gridline-color: #333333;
        }
        """)

        self.table.verticalHeader().setStyleSheet("""
        QHeaderView::section {
            background-color: #2b2b2b;
            color: white;
            border: 1px solid #3c3c3c;
        }
        """)
        self.table.setColumnCount(8)

        self.table.setHorizontalHeaderLabels([
            "Coin",

            "Price",

            "24h %",

            "Volume",

            "RSI",

            "Trend",

            "AI",

            "Signal",

        ])
        


        self.table.horizontalHeader().setStyleSheet("""
        QHeaderView::section {
            background-color: #1f2937;
            color: #ef4444;
            font-weight: bold;
        }
         """)

        self.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )

        self.table.setAlternatingRowColors(True)

        right.addWidget(self.table)

        ##################################################
        # BOTTOM
        ##################################################

        bottom = QHBoxLayout()

        self.status = QLabel("🟢 Ready")

        self.scanBtn = QPushButton(
            "🚀 Scan Market"
        )

        bottom.addWidget(self.status)

        bottom.addStretch()

        bottom.addWidget(self.scanBtn)

        right.addLayout(bottom)

        ##################################################
        # TIMER
        ##################################################

        self.timer = QTimer()

        self.timer.timeout.connect(
            self.update_dashboard
        )

        self.timer.start(30000)

        self.coins_data = []
        self.rsi_cache = {}
        self.rsi_batch_index = 0
        self.rsi_batch_size = 10
        self.initial_rsi_completed = False
        self.executor = ThreadPoolExecutor(max_workers=5)

        self.rsi_timer = QTimer()
        self.rsi_timer.timeout.connect(self.process_rsi_batch)
        self.rsi_timer.start(3000)

        self.update_dashboard()

        self.scanBtn.clicked.connect(
            self.scan_market
        )
        ##################################################
    # UPDATE DASHBOARD
    ##################################################


    def update_dashboard(self):

        try:

            coins = MarketData.get_top_coins(100)

            if coins:
                self.coins_data = coins

            # RSI فقط برای 20 ارز اول؛ بقیه بعداً با مقدار تقریبی
            rsi_limit = 20

            if not coins:

                if self.coins_data:
                    self.status.setText("🟡 Cached Data")
                    self.marketCard.setValue("Cached")
                    return

                self.status.setText("🔴 Offline")
                self.marketCard.setValue("Offline")
                self.coinCard.setValue("0")
                return

            self.status.setText("🟢 Connected - Loading RSI batches")

            self.coinCard.setValue(str(len(coins)))
            self.marketCard.setValue("Live")

            self.table.setRowCount(len(coins))

            for row, coin in enumerate(coins):

                self.table.setItem(row, 0, QTableWidgetItem(coin["symbol"]))
                self.table.setItem(row, 1, QTableWidgetItem(f"${coin['price']:,.4f}"))
                self.table.setItem(row, 2, QTableWidgetItem(f"{coin['change']:+.2f}%"))
                self.table.setItem(row, 3, QTableWidgetItem(f"{coin['volume']:,.0f}"))
                estimated_rsi = max(
                    0,
                    min(
                        100,
                        int(50 + coin['change'] * 4)
                    )
                )

                if coin["symbol"] in self.rsi_cache:

                    rsi_item = QTableWidgetItem(
                      str(self.rsi_cache[coin["symbol"]])
                    )

                else:

                    rsi_item = QTableWidgetItem(
                        f"{estimated_rsi} ⚠"
                    )

                self.table.setItem(row, 4, rsi_item)
                trend = "Bull" if coin["change"] > 0 else "Bear"

                trend_item = QTableWidgetItem(trend)
                trend_item.setForeground(
                    QColor("#22c55e") if trend == "Bull" else QColor("#ef4444")
                )
                self.table.setItem(row, 5, trend_item)

                ai_score = max(0, min(100, int(50 + coin["change"] * 5)))
                ai_item = QTableWidgetItem(str(ai_score))

                if ai_score >= 70:
                    ai_item.setForeground(QColor("#22c55e"))
                elif ai_score <= 40:
                    ai_item.setForeground(QColor("#ef4444"))

                self.table.setItem(row, 6, ai_item)

                if ai_score >= 70:
                    signal = "BUY"
                elif ai_score <= 40:
                    signal = "SELL"
                else:
                    signal = "HOLD"

                signal_item = QTableWidgetItem(signal)

                if signal == "BUY":
                    signal_item.setForeground(QColor("#22c55e"))
                elif signal == "SELL":
                    signal_item.setForeground(QColor("#ef4444"))
                else:
                    signal_item.setForeground(QColor("#f59e0b"))

                self.table.setItem(row, 7, signal_item)

        except Exception as e:

            self.status.setText("🔴 Error")
            print(e)

    ##################################################
    # SCAN
    ##################################################
    def filter_table(self):

        text = self.search.text().lower()

        for row in range(self.table.rowCount()):

            item = self.table.item(row, 0)

            if item is None:
                continue

            symbol = item.text().lower()

            visible = text in symbol

            self.table.setRowHidden(
            row,
            not visible
            )

    def process_rsi_batch(self):

        if not self.coins_data:
            return

        if not self.initial_rsi_completed:
            missing=[(i,c) for i,c in enumerate(self.coins_data) if c["symbol"] not in self.rsi_cache]
            if not missing:
                self.initial_rsi_completed=True
                self.rsi_batch_index=0
                self.status.setText("✅ All RSI Loaded")
                return
            batch=missing[:self.rsi_batch_size]
            futures={self.executor.submit(get_candles,c["name"].lower()):(r,c) for r,c in batch}
            for fut in as_completed(futures):
                row,coin=futures[fut]
                try:
                    prices,error=fut.result()
                    if prices:
                        rsi=calculate_rsi(prices)
                        self.rsi_cache[coin["symbol"]]=rsi
                        self.table.setItem(row,4,QTableWidgetItem(str(rsi)))
                except Exception as e:
                    print(e)
            self.status.setText(f"RSI Loaded {len(self.rsi_cache)}/{len(self.coins_data)}")
            return

        start=self.rsi_batch_index*self.rsi_batch_size
        end=min(start+self.rsi_batch_size,len(self.coins_data))
        batch=[(i,self.coins_data[i]) for i in range(start,end)]
        futures={self.executor.submit(get_candles,c["name"].lower()):(r,c) for r,c in batch}
        for fut in as_completed(futures):
            row,coin=futures[fut]
            try:
                prices,error=fut.result()
                if prices:
                    rsi=calculate_rsi(prices)
                    self.rsi_cache[coin["symbol"]]=rsi
                    self.table.setItem(row,4,QTableWidgetItem(str(rsi)))
            except: pass
        self.rsi_batch_index=(self.rsi_batch_index+1)%max(1,(len(self.coins_data)+self.rsi_batch_size-1)//self.rsi_batch_size)

    def scan_market(self):

        self.status.setText(
            "🚀 Scanning market..."
        )

        self.update_dashboard()

        self.status.setText(
            "✅ Scan completed"
        )