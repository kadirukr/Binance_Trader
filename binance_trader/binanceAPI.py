from binance.client import Client

#LIMIT VARIABLE TAEGLICH ANPASSEN -- Datum zuletzt geaendert: 11.07.2019 nach 3 Uhr

LIMIT_VAR = 10


def get_close_prices(api_key, api_secret, number_of_candle, currency):
    client = Client(api_key, api_secret)

    candles = client.get_klines(symbol=currency, interval=Client.KLINE_INTERVAL_1DAY, limit=LIMIT_VAR)
    #openCourse = candles[number_of_candle][1]
    closeCourse = candles[number_of_candle][4]
        
    return closeCourse


def calculate_multiplicator(period):
    multiplicator = 2.0/(period+1)

    return multiplicator

def calculate_ema_of_ema(closePrice, prevEMA, period, prev_ema_of_ema):
    #outOfPeriodEMA float Wert - Wert der Periode -1 um den ersten die Berechnung zum laufen zu bekommen
    #outOfPeriodDEMA float Wert 
    ema_of_ema = calculate_ema(closePrice, prevEMA) * calculate_multiplicator(period) + prev_ema_of_ema * (1 - calculate_multiplicator(period))

    return ema_of_ema

def calculate_ema_of_ema_of_ema(closePrice, prevEMA, period, prev_ema_of_ema, prev_ema_of_ema_of_ema):
    ema_of_ema_of_ema = calculate_ema_of_ema(closePrice, prevEMA, period, prev_ema_of_ema) * calculate_multiplicator(period) + prev_ema_of_ema_of_ema * (1 - calculate_multiplicator(period))

    return ema_of_ema_of_ema

def calculate_ema(closePrice, prevEMA): 
    #periode int Wert (wir arbeiten mit 9 Tagen)
    #closePrice float Wert
    #prevEMA float Wert
    multiplicator = calculate_multiplicator(9)
    ema = (closePrice * multiplicator) + (prevEMA * (1 - multiplicator))
    
    return ema

#-------------------------------------------------------------------------------------#
#dema und tema werden aus der main Methode aufgerufen restliche Berechnungen erfolgen 
#aus den beiden Funktionen heraus

def calculate_dema(closePrice, prevEMA, period, prev_ema_of_ema):
    ema_mal_zwei = 2 * calculate_ema(closePrice, prevEMA) 
    ema_of_ema = (calculate_ema(closePrice, prevEMA) * 0.2) + (prev_ema_of_ema * 0.8)
    dema = ema_mal_zwei - ema_of_ema

    return dema

def calculate_tema(closePrice, prevEMA, period, prev_ema_of_ema, prev_ema_of_ema_of_ema):
    ema_mal_drei = 3 * calculate_ema(closePrice, prevEMA)
    ema_of_ema_mal_drei = 3 * calculate_ema_of_ema(closePrice, prevEMA, period, prev_ema_of_ema)
    ema_of_ema_of_ema_summand = calculate_ema_of_ema_of_ema(closePrice, prevEMA, period, prev_ema_of_ema, prev_ema_of_ema_of_ema) 
    tema = (ema_mal_drei - ema_of_ema_mal_drei) + ema_of_ema_of_ema_summand

    return tema

#-------------------------------------------------------------------------------------#

def DEMA_TEMA_execution():
    api_key = 'WGEwMFkKEA0Txro85TdJKfaHMc5e66edL1qn1IxXiqlEjglInZSbmVe2cQ3pmnkT'
    api_secret = 'lFkT6l2R7vWplMjUFHxTxde8pWH25PjhuHGvrf5jX9CSR9nFMN28YtDQ5eH42Hwf'

    #currencies
    currencyArray =    ['BTCUSDT',          
                        'ETHUSDT',
                        'EOSUSDT',
                        'LTCUSDT', 
                        'XRPUSDT',
                        'TRXUSDT',
                        'ADAUSDT', 
                        'NEOUSDT',
                        'XLMUSDT',
                        'IOTAUSDT',
                        'DASHUSDT',]

    #ema(ema) fuer die erste Rechnung - Start der Berechnungen
    period = 9
    
    # Array Rangfolge [prevOutOfPeriodEMA, prevOutOfPeriodDEMA, prevEMA, prevOutOfPeriodTEMA]
    #prevOutOfPeriodEMA==prevEMA
    currency_dic = {'BTCUSDT':[11165.6092, 11575.0932, 11165.6092, 11257.0106],
                    'ETHUSDT':[302.5474, 307.7957, 302.5474, 301.5732],
                    'EOSUSDT':[6.3786, 6.0774, 6.3786, 5.8973],
                    'LTCUSDT':[127.6245, 124.6796, 127.6245, 122.1022],
                    'XRPUSDT':[0.4261, 0.4158, 0.4261, 0.4039],
                    'TRXUSDT':[0.0341, 0.0336, 0.0341, 0.0327], 
                    'ADAUSDT':[0.0885, 0.0862 ,0.0885, 0.0838], 
                    'NEOUSDT':[17.2503, 17.9747, 17.2503, 17.5568],
                    'XLMUSDT':[0.1142, 0.1082 , 0.1142, 0.1054],
                    'IOTAUSDT':[0.4186, 0.4072, 0.4186, 0.4003],
                    'DASHUSDT':[164.2174, 162.5564, 164.2174, 158.4988],
                    }
    

    for currency in currencyArray:

        prevOutOfPeriodEMA = currency_dic[currency][0]
        prevOutOfPeriodDEMA = currency_dic[currency][1]
        prevEMA = currency_dic[currency][2]
        prevOutOfPeriodTEMA = currency_dic[currency][3]

        prev_ema_of_ema = 2 * prevOutOfPeriodEMA - prevOutOfPeriodDEMA
        prev_ema_of_ema_of_ema = prevOutOfPeriodTEMA - (3 * prevOutOfPeriodEMA - 3 * prev_ema_of_ema)

        array_DEMA = []
        array_TEMA = []
    
        print('*********' + currency + '*********')
        LIMIT = 0


        while LIMIT<LIMIT_VAR:
        
            closePrice = float(get_close_prices(api_key, api_secret, LIMIT, currency))
            
            #calculate_dema(closePrice, prevEMA, period, outOfPeriodEMA, outOfPeriodDEMA)
            dema = str(calculate_dema(closePrice, prevEMA, period, prev_ema_of_ema))
            array_DEMA.append(dema)
            if len(array_DEMA) > 2:
                array_DEMA.remove(array_DEMA[0])
    
            #calculate_tema(closePrice, prevEMA, period, prev_ema_of_ema, prev_ema_of_ema_of_ema)
            tema = str(calculate_tema(closePrice, prevEMA, period, prev_ema_of_ema, prev_ema_of_ema_of_ema))
            array_TEMA.append(tema)
            if len(array_TEMA) > 2:
                array_TEMA.remove(array_TEMA[0])
            
            if len(array_DEMA) > 1 and array_DEMA[0] > array_TEMA[0] and array_DEMA[1] < array_TEMA[1]:
                print('{} KAUFEN!'.format(currency))
                print('DEMA {}: {}'.format(currency, array_DEMA))
                print('TEMA {}: {}'.format(currency, array_TEMA))
                print('Kerze {}'.format(LIMIT))

                print('prozentuale Differenz DEMA und TEMA')
                print(float(array_TEMA[1])/float(array_DEMA[1]))

    
            #prev_ema_of_ema_of_ema ueberschreiben
            prev_ema_of_ema_of_ema = calculate_ema_of_ema_of_ema(closePrice, prevEMA, period, prev_ema_of_ema, prev_ema_of_ema_of_ema)

            #calculate_ema_of_ema(closePrice, prevEMA, period, prev_ema_of_ema) 
            #emaofema und prevEMA immer wieder ueberschreiben
            prev_ema_of_ema = calculate_ema_of_ema(closePrice, prevEMA, period, prev_ema_of_ema)
            prevEMA = calculate_ema(closePrice, prevEMA)
            '''
            print('closePrice: {}'.format(closePrice))
            print('DEMA: {}'.format(array_DEMA))
            print('TEMA: {}'.format(array_TEMA))
            '''

            LIMIT += 1
        
        #print('DEMA: {}'.format(array_DEMA))
        #print('TEMA: {}'.format(array_TEMA))
        print('prozentuale Differenz DEMA und TEMA')
        print(float(array_TEMA[1])/float(array_DEMA[1]))
    

