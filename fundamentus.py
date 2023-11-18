import re
import urllib.request
import urllib.parse
import http.cookiejar
import certifi
import ssl

from lxml.html import fragment_fromstring
from collections import OrderedDict
from decimal import Decimal


def get_data(*args, **kwargs):
    """
    Busca e recupera os dados das ações do site fundamentus.com.br com base nos parâmetros fornecidos.

    :return: Um dicionário ordenado com os dados das ações, onde as chaves são os tickers das ações e os
             valores são dicionários contendo os indicadores financeiros e suas respectivas informações.
    """

    url = 'http://www.fundamentus.com.br/resultado.php'
    cookie_jar = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(
        urllib.request.HTTPSHandler(context=ssl.create_default_context(cafile=certifi.where())),
        urllib.request.HTTPCookieProcessor(cookie_jar)
    )
    opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows; U; Windows NT 6.1; rv:2.2) Gecko/20110201'),
                         ('Accept', 'text/html, text/plain, text/css, text/sgml, */*;q=0.01')]

    data = {'pl_min': '',
            'pl_max': '',
            'pvp_min': '',
            'pvp_max': '',
            'psr_min': '',
            'psr_max': '',
            'divy_min': '',
            'divy_max': '',
            'pativos_min': '',
            'pativos_max': '',
            'pcapgiro_min': '',
            'pcapgiro_max': '',
            'pebit_min': '',
            'pebit_max': '',
            'fgrah_min': '',
            'fgrah_max': '',
            'firma_ebit_min': '',
            'firma_ebit_max': '',
            'margemebit_min': '',
            'margemebit_max': '',
            'margemliq_min': '',
            'margemliq_max': '',
            'liqcorr_min': '',
            'liqcorr_max': '',
            'roic_min': '',
            'roic_max': '',
            'roe_min': '',
            'roe_max': '',
            'liq_min': '',
            'liq_max': '',
            'patrim_min': '',
            'patrim_max': '',
            'divbruta_min': '',
            'divbruta_max': '',
            'tx_cresc_rec_min': '',
            'tx_cresc_rec_max': '',
            'setor': '',
            'negociada': 'ON',
            'ordem': '1',
            'x': '28',
            'y': '16'
            }

    with opener.open(url, urllib.parse.urlencode(data).encode('UTF-8')) as link:
        content = link.read().decode('ISO-8859-1')

    pattern = re.compile('<table id="resultado".*</table>', re.DOTALL)
    content = re.findall(pattern, content)[0]
    page = fragment_fromstring(content)
    result = parse_data(page)

    return result


def parse_data(page):
    """
    Analisa o conteúdo HTML da página de resultados e extrai os dados das ações em um dicionário ordenado.

    :param page: Objeto lxml.html contendo o conteúdo da tabela de resultados extraída da página.
    :return: Um dicionário ordenado com os dados das ações, onde as chaves são os tickers das ações e os
             valores são dicionários contendo os indicadores financeiros e suas respectivas informações.
    """

    result = OrderedDict()

    for rows in page.xpath('tbody')[0].findall("tr"):
        result.update({rows.getchildren()[0][0].getchildren()[0].text: {
            'Cotacao': to_decimal(rows.getchildren()[1].text),
            'P/L': to_decimal(rows.getchildren()[2].text),
            'P/VP': to_decimal(rows.getchildren()[3].text),
            'PSR': to_decimal(rows.getchildren()[4].text),
            'DY': to_decimal(rows.getchildren()[5].text),
            'P/Ativo': to_decimal(rows.getchildren()[6].text),
            'P/Cap.Giro': to_decimal(rows.getchildren()[7].text),
            'P/EBIT': to_decimal(rows.getchildren()[8].text),
            'P/ACL': to_decimal(rows.getchildren()[9].text),
            'EV/EBIT': to_decimal(rows.getchildren()[10].text),
            'EV/EBITDA': to_decimal(rows.getchildren()[11].text),
            'Mrg.Ebit': to_decimal(rows.getchildren()[12].text),
            'Mrg.Liq.': to_decimal(rows.getchildren()[13].text),
            'Liq.Corr.': to_decimal(rows.getchildren()[14].text),
            'ROIC': to_decimal(rows.getchildren()[15].text),
            'ROE': to_decimal(rows.getchildren()[16].text),
            'Liq.2meses': to_decimal(rows.getchildren()[17].text),
            'Pat.Liq': to_decimal(rows.getchildren()[18].text),
            'Div.Brut/Pat.': to_decimal(rows.getchildren()[19].text),
            'Cresc.5anos': to_decimal(rows.getchildren()[20].text)
        }})

    return result


def to_decimal(input_str):
    """
    Converte uma string em um número Decimal.

    A função considera os seguintes casos:
    - Troca vírgulas por pontos.
    - Remove pontos usados como separadores de milhar.
    - Converte porcentagens em valores decimais.

    Args:
        input_str (str): A string a ser convertida em um número Decimal.

    Returns:
        Decimal: O número Decimal correspondente à string fornecida.
    """

    input_str = input_str.replace('.', '').replace(',', '.')
    is_percentage = input_str.endswith('%')

    if is_percentage:
        input_str = input_str[:-1]
        return Decimal(input_str) / 100
    else:
        return Decimal(input_str)


def filter_stocks(stocks, filters):
    """
    Filtra as ações com base nos critérios fornecidos.

    :param stocks: Dicionário de ações e seus indicadores.
    :param filters: Dicionário contendo os filtros a serem aplicados.
    :return: Dicionário de ações filtradas.
    """

    filtered_stocks = {}

    for ticker, indicators in stocks.items():
        meets_criteria = True
        for key, value in filters.items():
            if key not in indicators or indicators[key] < value[0] or indicators[key] > value[1]:
                meets_criteria = False
                break
        if meets_criteria:
            filtered_stocks[ticker] = indicators

    return filtered_stocks


def analyze_stocks(stocks):
    """
    Analisa as ações com base em critérios de análise fundamentalista.

    :param stocks: Dicionário de ações e seus indicadores.
    :return: Dicionário de ações selecionadas após análise.
    """

    # Defina os critérios de seleção aqui.
    filters = {
        'P/L': (0, 20),
        'P/VP': (0, 2),
        'DY': (0.02, 1),
        'ROE': (0.15, 1),
        'ROIC': (0.12, 1),
        'P/EBIT': (0, 10),
        'EV/EBIT': (0, 10),
        'Mrg.Ebit': (0.10, 1),
        'Mrg.Liq.': (0.05, 1),
        'Liq.Corr.': (1.5, 3),
    }

    return filter_stocks(stocks, filters)


if __name__ == '__main__':
    from waiting_bar import WaitingBar

    progress_bar = WaitingBar('[*] Downloading...')
    result = analyze_stocks(get_data())
    progress_bar.stop()
