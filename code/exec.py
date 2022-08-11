import time

from main import scrap

site_url = 'https://books.toscrape.com/'
dir_path = './results/test'

print('start scrapping ...')

def test():
    start = time.time()
    result = scrap(site_url, dir_path, dl_img = True)
    end = time.time()
    execution_time = format(end - start)
    return (result, execution_time)

test_result = test()
print(test_result)