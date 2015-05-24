from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import get_template
from django.template import Context
from django.utils import timezone
from django.http import HttpResponse, HttpResponseNotFound,\
    HttpResponseServerError, HttpResponseBadRequest, HttpResponseRedirect
from models import Activity, UserPage, UserCSS, Selected, Comment
from forms import ActForm, RegistryForm, UserPageForm, CommentForm
from urllib2 import urlopen, URLError
from bs4 import BeautifulSoup
from xmlparser import parse 
import datetime


MAXACTS = 10


def getPrice(act):
    if act['free']:
        return 0
    else:
        return int(act['price'])


def updateDB(acts):
    for act in acts:
        try:
            title = act['title']
            type = act['type']
            price = getPrice(act) 
            date = act['date']
            time = act['time']
            long = act['long'] == '1'
            url = act['url']
        except KeyError:
            print "Activity", title, "is not complete"
            continue
        try:
            newAct = Activity.objects.get(title=title, date=date, time=time)
            newAct.type = type
            newAct.price = price
            newAct.long = long
            newAct.url = url
        except Activity.DoesNotExist:
            newAct = Activity(title=title, type=type, price=price, date=date,
                        time=time, long=long, url=url)
        newAct.save()


def getXML():
    try:
        html = urlopen('http://goo.gl/809BPF').read()
    except URLError:
        return None
    soup = BeautifulSoup(html)
    xmlLink = 'http://datos.madrid.es'
    xmlLink += soup.find("span", {"class": "xml"}).parent.a.get("href")
    try:
        xml = urlopen(xmlLink).read()
    except URLError:
        return None
    return xml


def updateActs(request):
    if request.method != 'GET':
        return HttpResponseBadRequest("Wrong method")
    if not request.user.is_authenticated():
        resp = addToTemplate(request, 'Necesitas estar registrado.')
        return HttpResponse(resp)
    xml = getXML()
    if xml == None:
        return HttpResponseServerError("enlace del xml no disponible")
    acts = parse(xml)
    updateDB(acts)
    return HttpResponseRedirect('/todas')


def getText(soup):
    html = soup.find('div', {'class': 'parrafo'})
    if html == None:
        return ""
    text = ""
    for p in html.children:
        text += unicode(p)
    return text


def getImage(soup):
    url = soup.find('div', {'class': 'ftl'})
    if url is None:
        return ""
    parts = unicode(url.img).split('/', 1)
    img = parts[0] + 'http://datos.madrid.es/' + parts[1]
    return img


def getMoreInfo(url):
    try:
        html = urlopen(url).read()
    except URLError:
        print "Wrong url:", url
        return ""
    soup = BeautifulSoup(html)
    url = soup.find('a', {'class': 'punteado'})
    if url != None:
        url = 'http://www.madrid.es' + url.get('href')
        info = getMoreInfo(url)
        return info
    else:
        info = '<br/>' + getText(soup)
        info += "<br/><br/>" + getImage(soup)
        return info
        

def actToXml(address, act):
    xml = '<item>\n<title>' + act.title + '</title>\n'
    xml += '<description>Mas informacion en el enlace</description>\n'
    xml += '<link>http://' + address + '/actividad/' + str(act.id) + '</link>\n'
    xml += '</item>\n\n'
    return xml


def pageToXml(address, page):
    title = getUserPageTitle(page)
    if title.startswith('P&aacutegina de'):
        title = title[0] + 'a' +title[8:]
    xml = '<item>\n<title>' + title + '</title>\n'
    xml += '<description>' + page.description + '</description>\n'
    xml += '<link>http://' + address + '/' + page.nick + '</link>\n</item>\n\n'
    return xml


def setLikes(user, act):
    whoLikes = act.whoLikes.all()
    if user in whoLikes:
        html = '<p>Te gusta esta actividad</p><form action="/dontlike/'
        html += str(act.id) + '"method="POST"><input type="submit" value='
        html += '"Ya no me gusta"></form>'
    else:
        html = '<br/><form action="/like/' + str(act.id) + '"method="POST">'
        html += '<input type="submit" value="Me gusta!"></form>'
    return html


def setToChannel(username, act, owner):
    html = '<br/><form action="/actividad/' + str(act.id)
    if username != owner:
        html += '/add" method="POST">'
        html +=  '<input type="submit" value="Al canal"></form>'
    else:
        html += '/delete" method="POST">'
        html +=  '<input type="submit" value="Eliminar actividad"></form>'
        html += '<br/>'    
    return html


def setComments(request, coms, act):
    html = '<h4>Comentarios:</h4>'
    for com in coms:
        time =  str(timezone.localtime(com.date))[:16]
        html += 'De ' + com.nick + ':<br/>' + time + '<br/>'
        html += '<div class="comment"><p>' + com.text + '</p></div><br/>'
    if request.user.is_authenticated():
        form = CommentForm()
        template = get_template('commentform.html')
        c = Context({'form': form, 'id': str(act.id)})
        html += template.render(c)
    else:
        html += '<p>Neceitas estar registrado para poder dejar comentarios</p>'
    return html
    


def actToHtml(act, request, owner=''):
    html = '<li>Tipo de evento: ' + act.type + '</li>'
    html += '<li>Precio: '
    if act.price == 0:
        html += "evento gratuito"
    else:
        html += str(act.price)
    html += '</li><li>Fecha: ' + str(act.date) + '</li>'
    html += '<li>Hora: ' + str(act.time) + '</li>'
    if act.long:
        html += '<li>Es un evento de larga duraci&oacuten</li>'
    html += '<li>M&aacutes informaci&oacuten <a href="' + act.url + '">'
    html += 'aqu&iacute</a></li><li>Tiene ' + str(act.likes) + ' me gusta</li>'
    if request.user.is_authenticated():
        html += setLikes(request.user, act)
        html += setToChannel(request.user.username, act, owner)   
    return html


def actsToHtml(acts, request, owner = ''):
    html = ''
    for act in acts:
        html += '<h3><a href="/actividad/' + str(act.id) + '">'
        html += act.title + '</a></h3><lu>'
        html += actToHtml(act, request, owner) + '</lu><br/>'
    if html == '':
        html = 'No hay actividades disponibles'
    return html


def selectedToHtml(selected, request, owner):
    html = ''
    for sel in selected:
        html += '<h3><a href="/actividad/' + str(sel.act.id) + '">'
        html += sel.act.title + '</a></h3><lu><li>Elegida en '
        html += str(sel.date) + '</lu><br/>'
        html += actToHtml(sel.act, request, owner)

    if html == '':
        html = 'No hay actividades disponibles'
    return html


def formToHtml(tempName, formType):
    if formType == 'ActForm':
        form = ActForm()
    elif formType == 'RegistryForm':
        form = RegistryForm()
    elif formType == 'UserCreationForm':
        form = UserCreationForm()
    elif formType == 'UserPageForm':
        form = UserPageForm()
    else:
        print "WRONG FORM TYPE"
        return ''
    template = get_template(tempName)
    c = Context({'form': form})
    return template.render(c)


def pageToHtml(page, inMain, request):
    html = '<lu><li>Propietario: ' + page.nick + '</li>'
    html += '<li>Descripci&oacuten: ' + page.description + '</li>'
    html += '<li>Canal rss ' + '<a href="/' + page.nick + '/rss">Aqu&iacute'
    html += '</a></li>'
    if not inMain:
        html += selectedToHtml(page.selected.all(), request, page.nick)
    html += '</lu>'
    return html


def pagesToHtml(pages, request):
    html = ''
    for page in pages:
        html += '<h3><a href="/' + page.nick + '">' + getUserPageTitle(page)
        html += '</a></h3>' + pageToHtml(page, True, request) + '<br/>'
    if html == '':
        html = 'No hay paginas de usuarios disponibles'
    return html


def getUserPageTitle(page):
    if page.title == '':
        return 'P&aacutegina de ' + page.nick
    else:
        return page.title


def filtActs(form):
    data = form.cleaned_data
    acts = Activity.objects.all()
    if data['title'] != "":
        acts = acts.filter(title__icontains = data['title'])
    if data['price'] != None:
        acts = acts.filter(price = data['price'])
    if data['date'] != None:
        acts = acts.filter(date = data['date'])
    return acts
   

def getUserInfo(request):
    try:
        page = UserPage.objects.get(nick=request.user.username)
        html = 'Actividades disponibles para el canal:<br/><lu>'
        selected = page.selected.all()
        for sel in selected:
            html += '<li>' + sel.act.title + '</li>'
        html += '</lu><br/>Puedes tener '
        html += str(10 - page.nActs) + ' actividades m&aacutes'
        html += '<br/>Canal actualizado por &uacuteltima vez: '
        html += str(timezone.localtime(page.updated))[:16] + '<br/>'
        html += '<br/><form action="/update" method="POST">'
        html +=  '<input type="submit"value="Actualizar actividades"></form>'
        html += '<br/>'
    except UserPage.DoesNotExist:
        html = 'USUARIO SIN PAGINA PEROSNAL<br/>'
    return html


def checkActReq(request, id):
    if request.method != 'POST':
        return (HttpResponseBadRequest("Wrong method"), None, None)
    if not request.user.is_authenticated():
        return (HttpResponse('Necesitas estar registrado'), None, None)
    try:
        page = UserPage.objects.get(nick = request.user.username)
    except UserPage.DoesNotExist:
        return (HttpResponse('USUARIO SIN PAGINA PERSONAL'), None, None)
    try:
        act = Activity.objects.get(id = id)
    except Activity.DoesNotExist:
        return (HttpResponseNotFound('actividad no encontrada'), None, None)
    return (None, page, act)


def newUserPage(name):
    defaultCSS = UserCSS()
    defaultCSS.save()
    newPage = UserPage(nick = name, css = defaultCSS) 
    newPage.save()
    return newPage


def editPage(name, data):
    try:
        page = UserPage.objects.get(nick = name)
    except UserPage.DoesNotExist:
       page = newUserPage(name)
    css = page.css
    if data['title'] != '':
        page.title = data['title']
    if data['desc'] != '':
        page.description = data['desc']
    if data['bgCont'] != '':
        css.bgCont = data['bgCont']
    if data['bgBanner'] != '':
        css.bgBanner = data['bgBanner']
    if data['bgCopyRigth'] != '':
        css.bgCopyRigth = data['bgCopyRigth']
    if data['bgLogBox'] != '':
        css.bgLogBox = data['bgLogBox']
    if data['bgMenu'] != '':
        css.bgMenu = data['bgMenu']
    if data['wordColorCont'] != '':
        css.wordColorCont = data['wordColorCont']
    if data['wordColorBanner'] != '':
        css.wordColorBanner = data['wordColorBanner']
    if data['wordColorCopyRigth'] != '':
        css.wordColorCopyRigth = data['wordColorCopyRigth']
    if data['wordColorLogBox'] != '':
        css.wordColorLogBox = data['wordColorLogBox']
    if data['wordColorMenu'] != '':
        css.wordColorMenu = data['wordColorMenu']
    if data['wordSizeCont'] != None:
        css.wordSizeCont = data['wordSizeCont']
    if data['wordSizeBanner'] != None:
        css.wordSizeBanner = data['wordSizeBanner']
    if data['wordSizeCopyRigth'] != None:
        css.wordSizeCopyRigth = data['wordSizeCopyRigth']
    if data['wordSizeLogBox'] != None:
        css.wordSizeLogBox = data['wordSizeLogBox']
    if data['wordSizeMenu'] != None:
        css.wordSizeMenu = data['wordSizeMenu']
    css.save()
    page.save()
     

def isLogged(user):
    if user.is_authenticated():
        logged = 'Bienvenido ' + user.username + '. <a href="/logout">'
        logged += 'Cerrar sesi&oacuten.</a>'
    else:
        form = formToHtml('loginform.html', 'RegistryForm')
        logged = form
    return logged


def addToTemplate(request, content, inMain = False):
    template = get_template('index.html')
    logged = isLogged(request.user)
    c = Context({'content': content, 'logged': logged, 'inMain': inMain,
                'user': request.user.username})
    return template.render(c)


def serveCSS(request):
    if request.method != 'GET':
        return HttpResponseBadRequest("Wrong method")
    if request.user.is_authenticated():
        try:
            page = UserPage.objects.get(nick = request.user.username)
            css = page.css
        except UserPage.DoesNotExist:
            css = UserCSS()
    else:
        css = UserCSS()
    cssTemplate = get_template('style.css')
    c = Context({'bgCont': css.bgCont, 'bgBanner': css.bgBanner, 
      'bgCopyRigth': css.bgCopyRigth, 'bgLogBox': css.bgLogBox,
      'bgMenu': css.bgMenu, 'wcCont': css.wordColorCont,
      'wcBanner': css.wordColorBanner, 'wcCopyRigth': css.wordColorCopyRigth,
      'wcLogBox': css.wordColorLogBox, 'wcMenu': css.wordColorMenu,
      'wsCont': css.wordSizeCont, 'wsBanner': css.wordSizeBanner,
      'wsCopyRigth': css.wordSizeCopyRigth, 'wsLogBox': css.wordSizeLogBox,
      'wsMenu': css.wordSizeMenu})
    return HttpResponse(cssTemplate.render(c), content_type="text/css")

def getUpcomingActs():
    today_date = datetime.datetime.today()
    last_date = datetime.date(today_date.year+4,1,1)
    last_time = datetime.time(23, 59, 59)
    acts = Activity.objects.filter(date__range=(today_date, last_date))
    acts = acts.filter(time__range=(today_date, last_time))[:10]
    return acts


def mainPage(request):
    if request.method != 'GET':
        return HttpResponseBadRequest("Wrong method")
    acts = getUpcomingActs()
    html = '<h2>Actividades:</h2>' + actsToHtml(acts, request)
    pages = UserPage.objects.all()
    html += '<h2>Paginas de usuarios:</h2>' + pagesToHtml(pages, request)
    resp = addToTemplate(request, html, True)
    return HttpResponse(resp)


def getActivity(request, id):
    if request.method != 'GET':
        return HttpResponseBadRequest("Wrong method")
    try:
        act = Activity.objects.get(id = id)
        html = '<h3>' + act.title + '</h3>'
        html += actToHtml(act, request)
        html += getMoreInfo(act.url) + '</br>'
    except Activity.DoesNotExist:
        return HttpResponseNotFound("Actividad no encontrada")
    coms = act.comments.all()
    html += setComments(request, coms, act)
    resp = addToTemplate(request, html)
    return HttpResponse(resp)


@csrf_exempt
def getAll(request):
    if request.method == 'POST':
        form = ActForm(request.POST)
        if form.is_valid():
            acts = filtActs(form)
        else:
            resp = 'Datos incorrectos. Formato de la fecha: aaaa-mm-dd'
            resp = addToTemplate(request, resp)
            return HttpResponseBadRequest(resp)
    elif request.method == 'GET':
        acts = Activity.objects.all()
    else:
        return HttpResponseBadRequest("Wrong method")
    form = formToHtml('actform.html', 'ActForm')
    html = "Buscar actividades por:<br/><br/>" + form + "<br/>"
    loged = request.user.is_authenticated()
    if loged:
        html += getUserInfo(request)
    html += actsToHtml(acts, request)
    resp = addToTemplate(request, html)
    return HttpResponse(resp)


def getUserPage(request, nick):
    if request.method != 'GET':
        return HttpResponseBadRequest("Wrong method")
    try:
        page = UserPage.objects.get(nick = nick)
    except UserPage.DoesNotExist:
        return HttpResponseNotFound('Pagina no encontrada')
    html = '<h1>' + getUserPageTitle(page) + '</h1>'
    html += pageToHtml(page, False, request)
    if request.user.is_authenticated():
        html += formToHtml('userpageform.html', 'UserPageForm')
    resp = addToTemplate(request, html)
    return HttpResponse(resp)


@csrf_exempt
def signin(request):
    if request.method == 'GET':
        form = formToHtml('registryform.html', 'UserCreationForm')
        resp = addToTemplate(request, form)
        return HttpResponse(resp)
    elif request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            new_user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, new_user)
            return HttpResponseRedirect('/edituserpage')
        else:
            resp = 'Los datos introducidos no son correctos'
            resp = addToTemplate(request, resp)
            return HttpResponse(resp)
    else:
        return HttpResponseBadRequest("Wrong method")


@csrf_exempt
def editUserPage(request):
    if not request.user.is_authenticated():
        response = 'Necesitas estar registrado para modificar tu pagina'
        return HttpResponse(response)
    if request.method == 'GET':
        html = "Modifica tu pagina personal:<br/>"
        html += formToHtml('userpageform.html', 'UserPageForm')
        resp = addToTemplate(request, html)
        try:
            page = UserPage.objects.get(nick = request.user.username)
        except UserPage.DoesNotExist:
            page = newUserPage(request.user.username)
        return HttpResponse(resp)
    elif request.method == 'POST':
        form = UserPageForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            name = request.user.username
            editPage(name, data)
            return HttpResponseRedirect('/' + name)
        else:
            return HttpResponse('Los datos que has introducido no sn validos')
    else:
        return HttpResponseBadRequest("Wrong method")


@csrf_exempt
def addActivity(request, id):
    (resp, page, act) = checkActReq(request, id)
    if resp != None:
        return resp
    if page.nActs >= MAXACTS:
        resp = 'Has alcanzado el limite de actividades que puedes tener'
        resp = addToHtml(request, resp)
        return HttpResponse(resp)
    selected = Selected(act = act, date = datetime.datetime.now())
    selected.save()
    page.selected.add(selected)
    page.nActs = len(page.selected.all())
    page.save()
    return HttpResponseRedirect('/actividad/' + str(act.id))


@csrf_exempt
def delActivity(request, id):
    (resp, page, act) = checkActReq(request, id)
    if resp != None:
        return resp
    if page.nActs <= 0:
        return HttpResponse('No tienes actividades que borrar')
    selected = Selected.objects.get(act = act)
    page.selected.remove(selected)
    page.nActs = len(page.selected.all())
    page.save()
    return HttpResponseRedirect('/' + request.user.username)


def sendHelp(request):
    if request.method != 'GET':
        return HttpResponseBadRequest("Wrong method")
    fd = open('templates/help.txt', 'r')
    helpText = fd.read()
    fd.close()
    resp = addToTemplate(request, helpText)
    return HttpResponse(resp)


def getRSS(request, nick):
    if request.method != 'GET':
        return HttpResponseBadRequest("Wrong method")
    try:
        page = UserPage.objects.get(nick = nick)
    except UserPage.DoesNotExist:
        return HttpResponseNotFound('Canal rss de ' + nick + ' no encontrado')
    selected = page.selected.all()
    title = getUserPageTitle(page)
    if title.startswith('P&aacutegina de'):
        title = title[0] + 'a' +title[8:]
    rss = '<?xml version="1.0" encoding="UTF-8"?>\n'
    rss += '<rss version="2.0">\n<channel>\n\n'
    rss += '<title>' + title + '</title>\n'
    rss += '<description>' + page.description + '</description>\n\n'
    for sel in selected:
        rss += actToXml(request.get_host(), sel.act)
    rss += '</channel>\n</rss>'
    return HttpResponse(rss, content_type='text/html')


def getMainRSS(request):
    if request.method != 'GET':
        return HttpResponseBadRequest("Wrong method")
    acts = getUpcomingActs()
    rss = '<?xml version="1.0"?>\n''<rss version="2.0">\n<channel>\n\n'
    rss += '<title>Disfruta Madrid!</title>\n<description>Disfruta de las '
    rss += ' actividades que tendran lugar durante los proximos 100 dias en '
    rss += 'la comunidad de Madrid y de las paginas de los usuarios'
    rss += '</description>\n\n'
    for act in acts[:10]:
        rss += actToXml(request.get_host(), act)
    pages = UserPage.objects.all()
    for page in pages:
        rss += pageToXml(request.get_host(), page)
    rss += '</channel>\n</rss>'
    return HttpResponse(rss, content_type='text/html')


@csrf_exempt
def loggingIn(request):
    if request.method != 'POST':
        return HttpResponseBadRequest("Wrong method")
    name = request.POST['nick']
    password = request.POST['password']
    user = authenticate(username=name, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            return HttpResponseRedirect('/')
        else:
            resp = 'La cuenta esta deshabilitada.'
    else:
        resp = 'Nombre de usuario y la clave no coinciden'
    resp = addToTemplate(request, resp)
    return HttpResponse(resp)


def loggingOut(request):
    if request.method != 'GET':
        return HttpResponseBadRequest("Wrong method")
    logout(request)
    resp = addToTemplate(request, 'Has cerrado la sesion')
    return HttpResponse(resp)


@csrf_exempt
def addComment(request, id):
    if request.method != 'POST':
        return HttpResponseBadRequest("Wrong method")
    if not request.user.is_authenticated():
        resp = addToTemplate(request, 'Necesitas estar registrado')
        return HttpResponse(resp)
    try:
        act = Activity.objects.get(id = id)
        form = CommentForm(request.POST)
        form.nick = request.user.username
        if form.is_valid():
            text = form.cleaned_data['text']
            comment = Comment(nick = request.user.username, text = text)
            comment.save()
            act.comments.add(comment)
        return HttpResponseRedirect('/actividad/' + str(id))
    except Activity.DoesNotExist:
        resp = addToTemplate(request, 'La actividad no existe')
        return HttpResponse(resp)


@csrf_exempt
def addLikes(request, id):
    if request.method != 'POST':
        return HttpResponseBadRequest("Wrong method")
    if not request.user.is_authenticated():
        resp = addToTemplate(request, 'Necesitas estar registrado')
        return HttpResponse(resp)
    try:
        act = Activity.objects.get(id = id)
    except Activity.DoesNotExist:
        resp = addToTemplate(request, 'Actividad no encontrada')
        return HttpResponseNotFound(resp)
    act.likes += 1
    act.whoLikes.add(request.user)
    act.save()
    return HttpResponseRedirect('/actividad/' + str(id))


@csrf_exempt
def subLikes(request, id):
    if request.method != 'POST':
        return HttpResponseBadRequest("Wrong method")
    if not request.user.is_authenticated():
        resp = addToTemplate(request, 'Necesitas estar registrado')
        return HttpResponse(resp)
    try:
        act = Activity.objects.get(id = id)
    except Activity.DoesNotExist:
        resp = addToTemplate(request, 'Actividad no encontrada')
        return HttpResponseNotFound(resp)
    if request.user in act.whoLikes.all():
        act.likes -= 1
        act.whoLikes.remove(request.user)
        act.save()
    return HttpResponseRedirect('/actividad/' + str(id))
