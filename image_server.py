from pathlib import Path
import pprint
import io
from wsgiref.simple_server import make_server
from PIL import Image as Image
from PIL import ImageDraw, ImageFont
from datetime import datetime as dt

def application(environ, start_response, debug=False, w=200, h=100):
    '''
    How to tes POST case
        1. using cmd
            curl -w \n http://localhost:port --data query=test_body -X POST
        2. using powershell
            use curl.exe s curl
    '''
    start_response('200 OK', [('Content-Type', 'image/jpeg')])
    if debug:
        print('------------------------')
        pprint.pprint(environ)
        print('------------------------')
        
    method = environ.get('REQUEST_METHOD')
    #print(method)

    # path_info = environ.get('PATH_INFO')
    # print('[INFO] path_info:{}'.format(path_info))

    # query = environ.get('QUERY_STRING')
    # print('[INFO] query:{}'.format(query))

    content_length = environ.get('CONTENT_LENGTH')
    # if content_length is None:
    #     print('[INFO] Content-Length:{}'.format('None'))
    # else:
    #     print('[INFO] Content-Length:{}'.format(content_length))

    body = get_request_body(environ, method)
    if not body is None:
        print('[INFO] body: {}'.format(body))

    data = get_data(w, h)

    return [data]

def get_request_body(environ, method):
    # get content length to read a file object
    content_length = environ.get('CONTENT_LENGTH', 0)
    if method == 'POST':
        body = environ.get('wsgi.input').read(int(content_length))
    elif method == 'GET':
        body = None
    return body

def pil2hex(img):
    output = io.BytesIO()
    img.save(output, format='JPEG')
    hex_data = output.getvalue()
    return hex_data

def get_data(w, h, fp_img=None):
    size = (w, h)
    if not fp_img is None and Path(fp_img).exists():
        img = load_img(fp_img)
        img = img.resize(size)
    else:
        text = make_text()
        img = make_image(w, h, text)
    return pil2hex(img)

def load_img(fp_img):
    img = Image.open(fp_img)
    return img

def make_image(w, h, text, color_bg=None, color_font=None, font_size=64):
    if color_bg is None:
        color_gb = (128,128,128)
    if color_font is None:
        color_font = (255, 0, 0)
    img = Image.new('RGB', (w, h), color=color_bg)
    draw = ImageDraw.Draw(img)
    font = get_font(font_size)
    position = tuple([0, max(h//2, 0)])
    draw.text(position, text, fill=color_font, font=font)
    return img

def get_font(font_size):
    p_font = Path(get_fp_font())
    assert p_font.exists()
    font = ImageFont.truetype(str(p_font), font_size)

def get_fp_font():
    return r'C:\WINDOWS\Fonts\MSGOTHIC.ttc'

def make_text():
    t_datetime = dt.now()
    t_str = t_datetime.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
    return t_str

if __name__ == '__main__':
    port = 8000
    with make_server('', port, application) as httpd:
        print(f'[INFO] serving port {port}')
        httpd.serve_forever()
