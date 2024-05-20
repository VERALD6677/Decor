import os
from decorators import logger_func, logger
from old_project_function import get_article_date, get_article_header, get_actual_link, make_soup, check_article_body, _get_response

KEYWORDS = ['дизайн', 'фото', 'web', 'python', 'Wasteland', 'ViRush', 'нейросеть', 'робот']

def test_1():
    path = 'main.log'
    if os.path.exists(path):
        os.remove(path)

    @logger
    def hello_world():
        return 'Hello World'

    @logger
    def summator(a, b=0):
        return a + b

    @logger
    def div(a, b):
        return a / b

    assert 'Hello World' == hello_world(), "Функция возвращает 'Hello World'"
    result = summator(a=2, b=2)
    assert isinstance(result, int), 'Должно вернуться целое число'
    assert result == 4, '2 + 2 = 4'
    result = div(a=6, b=2)
    assert result == 3, '6 / 2 = 3'

    assert os.path.exists(path), 'файл main.log должен существовать'

    summator(a=4.3, b=2.2)
    summator(a=0, b=0)

    with open(path) as log_file:
        log_file_content = log_file.read()

    assert 'summator' in log_file_content, 'должно записаться имя функции'
    for item in (4.3, 2.2, 6.5):
        assert str(item) in log_file_content, f'{item} должен быть записан в файл'

def test_2():
    paths = ('log_1.log', 'log_2.log', 'log_3.log')

    for path in paths:
        if os.path.exists(path):
            os.remove(path)

        @logger_func(path)
        def hello_world():
            return 'Hello World'

        @logger_func(path)
        def summator(a, b=0):
            return a + b

        @logger_func(path)
        def div(a, b):
            return a / b

        assert 'Hello World' == hello_world(), "Функция возвращает 'Hello World'"
        result = summator(2, 2)
        assert isinstance(result, int), 'Должно вернуться целое число'
        assert result == 4, '2 + 2 = 4'
        result = div(6, 2)
        assert result == 3, '6 / 2 = 3'
        summator(4.3, b=2.2)

    for path in paths:
        assert os.path.exists(path), f'файл {path} должен существовать'

        with open(path) as log_file:
            log_file_content = log_file.read()

        assert 'summator' in log_file_content, 'должно записаться имя функции'

        for item in (4.3, 2.2, 6.5):
            assert str(item) in log_file_content, f'{item} должен быть записан в файл'

def test_old_project():
    @logger
    def get_all_articles(soup):
        return soup.find_all('article')

    @logger
    def get_articles_containing_keywords(keywords, articles):
        result_articles = []
        for article in articles:
            full_article_soup = make_soup(get_actual_link(article))
            article_words = check_article_body(full_article_soup)
            if any(keyword in article_words for keyword in keywords):
                result_articles.append(article)
        return result_articles

    url = 'https://habr.com/ru/all/'
    soup = make_soup(url)
    all_articles = get_all_articles(soup)
    filtered_articles = get_articles_containing_keywords(KEYWORDS, all_articles)
    for article in filtered_articles:
        print(get_article_date(article))
        print(get_article_header(article))
        print(get_actual_link(article))

if __name__ == '__main__':
    test_1()
    test_2()
    test_old_project()
