from urllib import request

def main():
    html = request.urlopen("http://www.oklx.com/cn/train/province/db56dd5d0177.html")
    print(html.read())

if __name__ == '__main__':
    main()