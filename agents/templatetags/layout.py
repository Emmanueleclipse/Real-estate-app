from django import template
from django.utils.html import format_html
from django.conf import settings
from scripts.extramedia import javascript, cssmedia

register = template.Library()

# grab source files from extramedia.py if in DEBUG mode

@register.simple_tag(takes_context=True)
def javascripts(context, name):
	if settings.SERVER_ENVIRONMENT == 'LIVE':
		return format_html('<script type="text/javascript" src="https://agencystatic.bienfacile.com/{}"></script>', name)
	elif settings.SERVER_ENVIRONMENT == 'STAGING':
		return format_html('<script type="text/javascript" src="/static/publish/{}"></script>', name)
	else:
		paths = ''
		for path in javascript['/static/'+name]:
			paths += '<script type="text/javascript" src="'+path['file']+'"></script>'
		return format_html(paths)

@register.simple_tag(takes_context=True)
def css(context, name):
	if settings.SERVER_ENVIRONMENT == 'LIVE':
		return format_html('<link href="https://agencystatic.bienfacile.com/{}" rel="stylesheet">', name)
	elif settings.SERVER_ENVIRONMENT == 'STAGING':
		return format_html('<link href="/static/publish/{}" rel="stylesheet"/>', name)
	else:
		paths = ''
		for path in cssmedia['/static/'+name]:
			paths += '<link href="'+path+'" rel="stylesheet"/>'
		return format_html(paths)

# Lay our panels

@register.simple_tag(takes_context=True)
def sectionstart(context, percentage):
	if context.request.user_agent.is_mobile:
		return format_html('<div class="swiper-slide">')
	return format_html('<div class="col-md-{}">', int(round(percentage*12)))

@register.simple_tag
def sectionend():
	return format_html('</div>')

@register.simple_tag(takes_context=True)
def sectionnext(context, percentage):
	return sectionend()+sectionstart(context,percentage)

@register.simple_tag(takes_context=True)
def sectionrow(context):
	if context.request.user_agent.is_mobile:
		return format_html('<div class="swiper-container" style="padding-left: 8px"><div class="swiper-wrapper">')
	return format_html('<div class="row" style="padding-left: 8px">')

@register.simple_tag(takes_context=True)
def sectionrowend(context):
	if context.request.user_agent.is_mobile:
		return format_html('</div></div>')
	return format_html('</div>')

def staticimagepath():
	if settings.SERVER_ENVIRONMENT == 'LIVE':
		return 'https://agencystatic.bienfacile.com/'
	elif settings.SERVER_ENVIRONMENT == 'STAGING':
		return '/static/publish/images/'
	else:
		return '/static/bienfacile/images/'

@register.simple_tag
def staticimageurl():
	return staticimagepath()

@register.simple_tag
def panel(name):
    return format_html('<div id="{}"><img src="{}throbber.gif" alt="Loading..."/></div>', name, staticimagepath())

@register.simple_tag
def paneltitle(name):
    return format_html('<h4>{}</h4>', name)

@register.simple_tag
def searchbar(name):
    return format_html('<div class="panel panel-default"><form><div class="panel-body"><div class="form-group"><div class="input-group"><input id="{}" type="text" class="form-control input-sm" placeholder="search here..."><span class="input-group-btn"><button class="btn btn-default btn-sm" type="button"><i class="fa fa-search"></i></button></span></div></div></div></form></div>', name)

#@register.simple_tag
#def searchbar(name):
#    return format_html('<nav class="navbar"><div class="container"><form class="navbar-form"><div class="form-group" style="display:inline;"><div class="fill"><input class="form-control" type="text" id="{}"><span class="btn btn-default"><i class="fa fa-search"></i></span></div></div></form></div></nav>', name)

