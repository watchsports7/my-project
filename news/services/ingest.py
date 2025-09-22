from . import rsport, ria, tass

def fetch_all_news():
    print("=== Загружаем все новости ===")
    total = 0
    total += rsport.fetch_rsport_news()
    total += ria.fetch_ria_news()
    total += tass.fetch_tass_news()
    print(f"Всего добавлено {total} новостей")
    return total
