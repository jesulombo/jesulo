import sys
from bs4 import BeautifulSoup
from torpy.http.requests import TorRequests


def scraper():
    grab = None
    lista = ""
    print('scraper : INFO : stay in tune...', flush=True)
    with open('site.txt', 'r') as f:
        line = f.read()
        link = line.strip()

    while grab is None:
        try:
            with TorRequests() as tor_requests:
                with tor_requests.get_session() as sess:
                    grab = sess.get(link)
                    print(grab)
        except:
            # El error de la librería torpy no tiene importancia y no afecta a futuros runs
            print("scraper : ERROR : line 20 torpy error")
            #sys.exit(1) envía correo de aviso
            #sys.exit(0) NO envía correo
            sys.exit(0)

    soup = BeautifulSoup(grab.text, 'html.parser')
    for enlace in soup.find_all('a'):
        acelink = enlace.get('href')
        canal = enlace.text
        if not str(acelink).startswith("acestream://") or canal == "aquÃ­":
            pass
        else:
            link = str(acelink).replace("acestream://", "")
            lista += str((canal + "\n" + link + "\n"))

            contenido = ((lista.replace(u'\xa0', u' ')).strip())

    if contenido != "":
        print("scraper : OK : channels retrieved")
    else:
        print("scraper : ERROR : channels could not be retrieved")
        sys.exit(0)

    return contenido

#scraper()
