import http.client

def request(input, lang):
    conn = http.client.HTTPSConnection('inputtools.google.com')
    conn.request('GET', '/request?text=' + input + '&itc=' + lang + '&num=1&cp=0&cs=1&ie=utf-8&oe=utf-8&app=test')
    res = conn.getresponse()
    return res

def transliteration(input, lang):
    output = ''
    if ' ' in input:
        input = input.split(' ')
        for i in input:
            res = request(input = i, lang = lang)
            res = res.read()
            if i==0:
                output = str(res, encoding = 'utf-8')[14+4+len(i):-31]
            else:
                output = output + ' ' + str(res, encoding = 'utf-8')[14+4+len(i):-31]
    else:
        res = request(input = input, lang = lang)
        res = res.read()
        output = str(res, encoding = 'utf-8')[14+4+len(input):-31]
    return output