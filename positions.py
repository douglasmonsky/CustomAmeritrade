class Positions:

    def __init__(self, position_data):
        self.position_data = position_data['securitiesAccount']
        self.start_total = self.position_data["initialBalances"]["liquidationValue"]
        self.current_total = self.position_data["currentBalances"]["liquidationValue"]
        self.stock_positions = self.position_data['positions']



        for position in self.stock_positions:
            short_quant = int(position['shortQuantity'])
            long_quant = int(position['longQuantity'])
            if short_quant:
                position_type = 'short'
                quant = short_quant
            else:
                position_type = 'long'
                quant = long_quant
            avg_price = round(float(position['averagePrice']), 2)
            day_change = round(float(position['currentDayProfitLoss']), 2)
            symbol = position['instrument']['symbol']
            text = f'{position_type.upper()} {quant} shares of {symbol} for an average price of {avg_price}. This is a net change of {day_change}.'
            text_lines.append(text)
            if self.finviz_session and include_news == True:
                news_container = self.finviz_session.get_news(symbol)
                if news_container:
                    text_lines.append(f'Recent {symbol} news articles:')
                    for news in news_container:
                        news_text = f'{news[0]}, {news[1].strip()}: <a href="{news[3]}">{news[2]}</a>'
                        text_lines.append(news_text)
            text_lines.append('')







class Position:

    def __init__(self):