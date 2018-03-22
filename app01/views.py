from django.shortcuts import render,HttpResponse
from PIL import Image, ImageDraw, ImageFont, ImageFilter
# Create your views here.

def index(request):

    # return render(request, 'verify_code.html')
    return render(request, 'create_code_img.html')
def verify_code(request):
    #引入随机函数模块
    import random
    #定义变量，用于画面的背景色、宽、高
    bgcolor = (random.randrange(20, 100), random.randrange(
        20, 100), 255)
    width = 100
    height = 25
    #创建画面对象
    im = Image.new('RGB', (width, height), bgcolor)
    #创建画笔对象
    draw = ImageDraw.Draw(im)
    #调用画笔的point()函数绘制噪点
    for i in range(0, 100):
        xy = (random.randrange(0, width), random.randrange(0, height))
        fill = (random.randrange(0, 255), 255, random.randrange(0, 255))
        draw.point(xy, fill=fill)
    #定义验证码的备选值
    str1 = 'ABCD123EFGHIJK456LMNOPQRS789TUVWXYZ0'
    #随机选取4个值作为验证码
    rand_str = ''
    for i in range(0, 4):
        rand_str += str1[random.randrange(0, len(str1))]
    #构造字体对象，ubuntu的字体路径为“/usr/share/fonts/truetype/freefont”
    # font = ImageFont.truetype('FreeMono.ttf', 23)
    # font = ImageFont.load_default().font
    font = ImageFont.truetype('arial.ttf', 23)

    #构造字体颜色
    fontcolor = (255, random.randrange(0, 255), random.randrange(0, 255))
    #绘制4个字
    draw.text((5, 2), rand_str[0], font=font, fill=fontcolor)
    draw.text((25, 2), rand_str[1], font=font, fill=fontcolor)
    draw.text((50, 2), rand_str[2], font=font, fill=fontcolor)
    draw.text((75, 2), rand_str[3], font=font, fill=fontcolor)
    #释放画笔
    del draw
    #存入session，用于做进一步验证
    request.session['verifycode'] = rand_str
    """
    python2的为
    # 内存文件操作
    import cStringIO
    buf = cStringIO.StringIO()
    """
    # 内存文件操作-->此方法为python3的
    import io
    buf = io.BytesIO()
    #将图片保存在内存中，文件类型为png
    im.save(buf, 'png')
    #将内存中的图片数据返回给客户端，MIME类型为图片png
    return HttpResponse(buf.getvalue(), 'image/png')
    # return render(request,'verify_code.html')

def verifycodeValid(request):
    vc = request.POST['vc']
    if vc.upper() == request.session['verifycode']:
        return HttpResponse('ok')
    else:
        return HttpResponse('no')


# 将check_code包放在合适的位置，导入即可，我是放在utils下面
from app01 import check_code
from  io import  BytesIO

def create_code_img(request):


    f = BytesIO() #直接在内存开辟一点空间存放临时生成的图片

    img, code = check_code.create_validate_code() #调用check_code生成照片和验证码
    request.session['check_code'] = code #将验证码存在服务器的session中，用于校验
    img.save(f,'PNG') #生成的图片放置于开辟的内存中

    print(code)
    # post_check_code = request.POST.get('check_code')
    # session_check_code = request.session['check_code']
    # if post_check_code.lower() == session_check_code.lower():
    #     pass
    return HttpResponse(f.getvalue())  #将内存的数据读取出来，并以HttpResponse返回



