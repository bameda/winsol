#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# WinSOL (https://forja.rediris.es/projects/cd-crisol)
# Copyright (C) 2006-2007 by David Barragán Merino <bamedai@di.uc3m.es>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.

import web				# Webpy lib
import os				# Os and sys lib
import sys
import shutil
sys.path.append("/usr/share/winsol/web")
os.chdir("/usr/share/winsol/web")
sys.path.append("/usr/share/winsol")	# WinSOL lib
import winsollib
from pyDes import triple_des

##############################################
## WinSOL Web Services Configuration values ##
##############################################

# Main

## The WinSOL directory path.
MASTER_DIR = "/usr/share/winsol"
## The System configuration directory path.
SYSTEM_CONFIG_DIR = "/etc/winsol"
## The System temp directory path.
SYSTEM_TEMP_DIR = "/var/lib/winsol"
## The http url to the WinSOL interface.
HOST = "http://localhost"

# System's DTD files

## The category DTD file path
CATEGORIES_DTD = MASTER_DIR + "/categories.dtd"
## Teh application DTD file path.
APPS_DTD = MASTER_DIR + "/apps.dtd"
## The Includes DTD file path.
INCLUDES_DTD = MASTER_DIR + "/includes.dtd"

# System's XML files

## The System categories XML file path
MASTER_CATEGORIES_XML = SYSTEM_CONFIG_DIR + "/categories.xml"
## The system applications XML file path.
MASTER_APPS_XML = SYSTEM_CONFIG_DIR + "/apps.xml"

# User's XML files name

## The User category XML file name.
USER_CATEGORIES_XML_FILE = "/categories.xml"
## The User applications XML file name.
USER_APPS_XML_FILE = "/apps.xml"
## The User included XML file name.
USER_INCLUDES_XML_FILE = "/includes.xml"

# System directories

## System html template directory path.
TEMPLATES_DIR = MASTER_DIR + "/baseconfig/templates"
## System mail template directory path.
MAIL_TEMPLATES_DIR = MASTER_DIR + "/web/templates/mails"
## System Users directory path.
USERS_DIR = SYSTEM_TEMP_DIR + "/users"
## System Software directory path.
SOFTWARE_DIR = SYSTEM_TEMP_DIR + "/software"
## System Icons directory path
ICONS_DIR =  SYSTEM_TEMP_DIR + "/icons"
## System Manuals directory path.
MANUALS_DIR = SYSTEM_TEMP_DIR + "/manuals"

# DDBB

## SGDDBB type.
DB_GS = 'mysql'
## SGDDBB user name.
DB_USER = "user_winsol"
## SGDDBB password.
DB_PASSWORD = "pass_winsol"
## SGDDBB DDBB name.
DB_NAME = "winsol"
## SGDDBB users table name.
DB_TABLE_USER = "_users"
## SGDDBB stadistic applications table name.
DB_TABLE_APPS_STADISTIC = "_stadistic_app"

# SMTP Server

## SMTP server.
SMTP_SERVER = "localhost"
## SMTP port.
SMTP_PORT = "25"
## Use Login to send mail value. (1=yes or 0=no).
USE_LOGIN = 0
## SMTP user name. (if USE_LOGIN=1).
SMTP_USER = "user_winsol"
## SMTP user pasword. (if USE_LOGIN=1).
SMTP_PASSWORD = "pass"
## From addres.
MAIL_FROM_ADDRS = "WinSOL <user_winsol@localhost>"
## ISO subject.
MAIL_COMPOSITION_SUBJECT = "[WinSOL] Get your WinSOL composition"
## Password Subject.
MAIL_PASSWORD_SUBJECT = "[WinSOL] Get your user password here"
## Mail template name.
MAIL_TEMPLATE = "default"

# Miscelanea

## Default Category icon file name
CATEGORY_ICON="default_category.png"
## Default Category icon file url
CATEGORY_ICON_URL="/static/images/categories/default_category.png"
## Default Application icon file name
APPLICATION_ICON="default_app.png"
## Default Application icon file url
APPLICATION_ICON_URL="/static/images/apps/default_app.png"
## Key to encrypt the user password.
PASSWD_CRYPTO_KEY="MySecretTripleDesKeyData"

# Check the System configuration
if not os.path.exists(SYSTEM_CONFIG_DIR):
	print "EE - The configuratión file dont exist in '" + SYSTEM_CONFIG_DIR + "'."
	print "     Please reinstall or solves the problem."
else:
	execfile(SYSTEM_CONFIG_DIR+"/web_config")
	if len(PASSWD_CRYPTO_KEY) < 16:
		PASSWD_CRYPTO_KEY = PASSWD_CRYPTO_KEY + PASSWD_CRYPTO_KEY[:16 - len(PASSWD_CRYPTO_KEY)]
	elif len(PASSWD_CRYPTO_KEY) < 24:
		PASSWD_CRYPTO_KEY = PASSWD_CRYPTO_KEY + PASSWD_CRYPTO_KEY[:24 - len(PASSWD_CRYPTO_KEY)]
	else:
		PASSWD_CRYPTO_KEY = PASSWD_CRYPTO_KEY[:24]


# Check the Temp Directory
if not os.path.exists(SYSTEM_TEMP_DIR):
	os.mkdir(SYSTEM_TEMP_DIR)
	os.mkdir(SOFTWARE_DIR)
	os.mkdir(ICONS_DIR)
	os.mkdir(MANUALS_DIR)
	os.mkdir(USERS_DIR)
else:
	if not os.path.exists(SOFTWARE_DIR): 
		os.mkdir(SOFTWARE_DIR)
	if not os.path.exists(ICONS_DIR): 
		os.mkdir(ICONS_DIR)
	if not os.path.exists(MANUALS_DIR): 
		os.mkdir(MANUALS_DIR)
	if not os.path.exists(USERS_DIR): 
		os.mkdir(USERS_DIR)

## The DTDs path file List.
dtd_files = [ CATEGORIES_DTD, APPS_DTD, INCLUDES_DTD]

## Generate a dictionary with all user paths with \em user_home, \em app_xml_file, \em category_xml_file, \em includes_xml_file, \em image_dir, \em software_dir, \em manuals_dir, \em html_dir and \em icon_dir.
#
# @param username - The User nick.
# @return A dictionary with all user paths information.
def get_all_user_path(username):
        return {'user_home':USERS_DIR + "/" + username,
                'apps_xml_file':USERS_DIR + "/" + username + USER_APPS_XML_FILE,
                'categories_xml_file':USERS_DIR + "/" + username + USER_CATEGORIES_XML_FILE,
                'includes_xml_file':USERS_DIR + "/" + username + USER_INCLUDES_XML_FILE,
                'image_dir':USERS_DIR + "/" + username + "/image",
                'software_dir':USERS_DIR + "/" + username + "/image/software",
                'manuals_dir':USERS_DIR + "/" + username + "/image/manuals",
                'html_dir':USERS_DIR + "/" + username + "/image/html",
                'icons_dir':USERS_DIR + "/" + username + "/image/html/icons"}

## Remove all in any user directory.
#
# @param username - The User nick.
def mrproper_image(username):
	dir = get_all_user_path(username)
	if os.path.exists(dir['image_dir']):
		os.system( "rm -rf '"+ dir['image_dir'] + "'")	
	os.mkdir(dir['image_dir'])
	os.mkdir(dir['software_dir'])
	os.mkdir(dir['manuals_dir'])
	os.mkdir(dir['html_dir'])
	os.mkdir(dir['icons_dir'])

## Make the user home.
#
# @param username - The User nick.
def make_user_home(username):
        dir=get_all_user_path(username)
        if not os.path.exists(dir['user_home']):
                os.mkdir(dir['user_home'])
        if not os.path.exists(dir['image_dir']):
                os.mkdir(dir['image_dir'])
        if not os.path.exists(dir['software_dir']):
                os.mkdir(dir['software_dir'])
        if not os.path.exists(dir['manuals_dir']):
                os.mkdir(dir['manuals_dir'])
        if not os.path.exists(dir['html_dir']):
                os.mkdir(dir['html_dir'])
        if not os.path.exists(dir['icons_dir']):
                os.mkdir(dir['icons_dir'])
        if not os.path.exists(dir['categories_xml_file']):
                shutil.copy(MASTER_DIR+"/baseconfig/categories.xml",dir['categories_xml_file'])
        if not os.path.exists(dir['apps_xml_file']):
                shutil.copy(MASTER_DIR+"/baseconfig/apps.xml",dir['apps_xml_file'])
        if not os.path.exists(dir['includes_xml_file']):
                shutil.copy(MASTER_DIR+"/baseconfig/includes.xml",dir['includes_xml_file'])

## Send a specific mail.
#
# @param subject - \em Subject email addres.
# @param user_info - The user information dictionary: name, surname and mail.
# @param text_file - The text file name template.
# @param html_file - The html file name template.
#
# @see create_html_mail()
def send_mail(subject, user_info, text_file, html_file):
	import smtplib
	from Cheetah.Template import Template

	# Generate the plain text and html text.
	mail_dic = {'user':user_info}
	fromaddr = MAIL_FROM_ADDRS
	toaddrs = user_info['name']+" "+user_info['surname']+" <"+user_info['mail']+">"
	text = Template( file=MAIL_TEMPLATES_DIR+"/"+MAIL_TEMPLATE+"/"+text_file, searchList=[mail_dic])	
	html = Template( file=MAIL_TEMPLATES_DIR+"/"+MAIL_TEMPLATE+"/"+html_file, searchList=[mail_dic])
 	
	# Conect to the smtp server and send the e-mail.
    	server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
	if USE_LOGIN:
		server.login(SMTP_USER, SMTP_PASSWORD)
    	
	server.sendmail(fromaddr, toaddrs, create_html_mail(fromaddr, toaddrs, subject, "" + str(text), "" + str(html)))
    	server.quit()

## Create a mime-message that will render HTML in popular MUAs, text in better ones.
#
# @param from_addr - \em From email addres.
# @param to_addrs - \em To email addres.
# @param subject - \em Subject email addres.
# @param text - The email information in text format. 
# @param html - The email indormation in html format.
# @return the email.
def create_html_mail(from_addr="", to_addrs= "", subject="", text="", html="" ):
	import MimeWriter
	import mimetools
	import cStringIO
	
	out = cStringIO.StringIO()  
	writer = MimeWriter.MimeWriter(out)
	
	# set up some basic headers, we put subject here
	writer.addheader("From", from_addr)
	writer.addheader("To", to_addrs)
	writer.addheader("Subject", subject)
	writer.addheader("MIME-Version", "1.0")
	writer.startmultipartbody("alternative")
	writer.flushheaders()
	
	# The plain text section
	if text != "":
		txtin = cStringIO.StringIO(text)
		subpart = writer.nextpart()
		subpart.addheader("Content-Transfer-Encoding", "quoted-printable")
		pout = subpart.startbody("text/plain", [("charset", 'utf8')])
		mimetools.encode(txtin, pout, 'quoted-printable')
		txtin.close()

	# The html section
	if html != "":
		htmlin = cStringIO.StringIO(html)
		# Start the html subpart of the message
		subpart = writer.nextpart()
		subpart.addheader("Content-Transfer-Encoding", "quoted-printable")
		# Returns us a file-ish object we can write to
		pout = subpart.startbody("text/html", [("charset", 'utf8')])
		mimetools.encode(htmlin, pout, 'quoted-printable')
		htmlin.close()

	# Clpse and finish
	writer.lastpart()
	msg = out.getvalue()
	out.close()
	return msg

## Get the type of any file.
#
# @param file - A path to any file.
# @return The file type.
def get_file_type(file):
    	t = mimetypes.guess_type(file)
    	if t and t[0]:
        	return t[0]
    	return 'application/octet-stream'

## Meke the applications stadistic from a WinSOL image.
#
# @param image - A WinSOL Image
def make_applications_stadistic(image):
	for app in image.get_all_apps():
		if app.is_included():
			for cat_label in app.get_categories():
				categ = image.get_category_by_label(cat_label) 
				if categ != None and categ.is_included():
					# Add 1 to app download_number in DDBB
					# If it doesn't it we inset a new tupple in DDBB.i
					application = list(web.select(DB_TABLE_APPS_STADISTIC, where=web.sqlwhere({'name':app.get_name()})))
					if len(application) == 0:
						# Insert the new application.
						web.insert(DB_TABLE_APPS_STADISTIC, name=app.get_name(), download_number=1)
					else:
						# Update the application.
						number = application[0].download_number + 1
						web.update(DB_TABLE_APPS_STADISTIC, where=web.sqlwhere(web.storify({'name': app.get_name()})), download_number=number)
					break

###################
## Web Interface ##
###################


## The url List
#
#	\li url ::= [tuple*]
#       \li tuple ::= html_page, class_name 
#	\li html_page ::= str
#	\li class_name ::= str
#
# @see Web.py Project (hhtp://www.webpy.org) 
urls = ( '/', 'login',
         '/login.html', 'login',
	 '/help.html', 'help',
         '/logout.html', 'logout',
         '/add_user.html', 'add_user',
	 '/get_password.html', 'get_password',
         '/account.html', 'account',
         '/index.html' , 'index', 
         '/list_all.html', 'list_all',
	 '/list_all_select_all/(.*)','list_all_select_all',
	 '/list_all_unselect_all/(.*)','list_all_unselect_all',
	 '/list_all_select_category/(.*)/(.*)','list_all_select_category',
	 '/list_all_unselect_category/(.*)/(.*)','list_all_unselect_category',
	 '/list_all_select_application/(.*)/(.*)','list_all_select_application',
	 '/list_all_unselect_application/(.*)/(.*)','list_all_unselect_application',
	 '/list_all_select_all_by_category/(.*)/(.*)','list_all_select_all_by_category',
	 '/list_all_unselect_all_by_category/(.*)/(.*)','list_all_unselect_all_by_category',
         '/color.css' , 'style_color',
         '/layout.css', 'style_layout',
         '/category/(.*)', 'category',
         '/add_cat.html', 'add_category',
         '/del_cat/(.*)', 'del_category',
         '/modify_cat/(.*)', 'modify_category',
         '/select_cat/(.*)', 'select_category',
	 '/category_select_application/(.*)/(.*)', 'category_select_application',
	 '/category_unselect_application/(.*)/(.*)', 'category_unselect_application',
      	 '/select_all_apps_by_cat/(.*)', 'select_all_apps_by_category',
         '/unselect_all_apps_by_cat/(.*)', 'unselect_all_apps_by_category',
         '/unselect_cat/(.*)', 'unselect_category',
         '/app/(.*)', 'app',
         '/add_app.html', 'add_application',
         '/del_app/(.*)', 'del_application',
         '/modify_app/(.*)', 'modify_application',
         '/select_app/(.*)', 'select_application',
         '/unselect_app/(.*)', 'unselect_application',
         '/add_app_man_online/(.*)', 'add_application_man_online',
         '/add_app_man_offline/(.*)', 'add_application_man_offline',
         '/make_composition.html', 'make_composition',
	 '/precompile_composition.html', 'precompile_composition',
	 '/static/(.*)', 'view_static_files'
        )

## Class for \em Login process.
#
# @author David Barragán Merino <bameda [AT] di.uc3m [DOT] com>
# @author CRISOL-UC3M <htp://crisol.uc3m.es>
class login:     
	
	## Get method. Show the \em Login page
	#
	# @param errors - List of error messages.
	# @param messages - List of \em 'Ok' messages.  
	def GET(self, errors = [], messages = []):
                user ={'nick':"", 'password':""}
                web.render ('login.html')

	## Post method. Make the \em Login process and show the main page.
	#
	def POST(self):
                login = web.input()
		
		tdes = triple_des(PASSWD_CRYPTO_KEY)
		login.password = tdes.encrypt(login.password, "*")

                users = web.select(DB_TABLE_USER, where=web.sqlwhere(login))
                if len(users) == 1:
                        # Login OK
			web.setcookie('nick', login.nick)
			make_user_home(login.nick)
			user_path = get_all_user_path(login.nick)
                        image =  winsollib.Image([MASTER_CATEGORIES_XML, MASTER_APPS_XML, user_path['categories_xml_file'], user_path['apps_xml_file'], user_path['includes_xml_file']], dtd_files)
                        #menu_categories = image.get_all_categories_dict()
			errors = []
			messages = ["Ha entrado como el usuario \"" + login.nick + "\""]
			web.seeother('index.html')
                elif len(users) > 1:
                        # DB CORRUPT
                        print "La base de Datos está corrupta. Contacte con el administrador."
                else:
                     user = login
                     messages = []
                     errors = ["Nick o password incorrecto.", "Intentelo de nuevo, registrese o obtenga su password si no la recuerda."]
                     web.render ('login.html')

## Class for \em Logout process.
#
# @author David Barragán Merino <bameda [AT] di.uc3m [DOT] com>
# @author CRISOL-UC3M <htp://crisol.uc3m.es>
class logout:
	
	## Get method. Make the \em Logiut process and delete the cookie from the client.
	#
        def GET(self):
                web.setcookie('username', '','Fri, 23-Mar-1984 00:00:00 GMT' )
		web.seeother ('login.html')

## Class for See the User Manuals and FAQs.
#
# @author David Barragán Merino <bameda [AT] di.uc3m [DOT] com>
# @author CRISOL-UC3M <htp://crisol.uc3m.es>
class help:

	## Get method. Show the help page.
        #
	def GET(self):
		cookie = web.cookies()
		user_path = get_all_user_path(cookie.nick)
		image =  winsollib.Image([MASTER_CATEGORIES_XML, MASTER_APPS_XML, user_path['categories_xml_file'], user_path['apps_xml_file'], user_path['includes_xml_file']], dtd_files)
		menu_categories = image.get_all_categories_dict()
		size = float(image.calculate_size()) / 1000
		web.render ('help.html')

## Class for \em Get \em password process. 
#
# @author David Barragán Merino <bameda [AT] di.uc3m [DOT] com>
# @author CRISOL-UC3M <htp://crisol.uc3m.es>
class get_password:
	
	## Get method. Show the \em Get \em your \em password form.
	#
	# @param errors - List of errors messages.
	def GET(self, errors = [], messages = []):
		user = {'nick':""}
		web.render('get_password.html')
	
	## Post method. Send a mail to the user with his password.
	#
	def POST(self):
		user = web.input()
		errors = []
		users =  list(web.select(DB_TABLE_USER, where=web.sqlwhere(user)))
	        if len(users) == 1:

			tdes = triple_des(PASSWD_CRYPTO_KEY)
			passwd = tdes.decrypt(users[0].password, "*")

			# Send the mail
			user_info = {"nick":user.nick,
				"name":users[0].name,
				"surname":users[0].surname,
				"password":passwd,
				"mail":users[0].mail}
			try:
				send_mail(MAIL_PASSWORD_SUBJECT, user_info, "password_text_mail.txt", "password_html_mail.txt")
			except Exception:
				errors.append("No se ha podido enviar el E-mail con su información personal.")
				errors.append("Pongase en contacto con el administrador de WinSOL para solucionar el problema.")
				web.render('get_password.html')
			else:
				messages = ["Se le ha enviado al  usuario \""+ user.nick + "\" un e-mail con su información personal en el que se incluye su Contraseña.."]
				web.render('get_password.html')
		elif len(users) > 1:
                	# DB CORRUPT
                        print "La base de Datos está corrupta. Contacte con el administrador"
	        else:
        		errors.append("Nick incorrecto. Puede que el usuario no esté registrado")
			errors.append("Intentelo de nuevo, registrese o obtenga su password si no la recuerda.")
                	web.render ('get_password.html')

## Class for View/Modify the User Account.
#
# @author David Barragán Merino <bameda [AT] di.uc3m [DOT] com>
# @author CRISOL-UC3M <htp://crisol.uc3m.es>
class account:

        ## Get method. Show the \em User \em Information form.
        #
        # @param errors - List of errors messages.
        # @param messages - List of \em 'Ok' messages.
        def GET(self, errors = [], messages = []):
                cookie = web.cookies()
                user_path = get_all_user_path(cookie.nick)
                image =  winsollib.Image([MASTER_CATEGORIES_XML, MASTER_APPS_XML, user_path['categories_xml_file'], user_path['apps_xml_file'], user_path['includes_xml_file']], dtd_files)
                menu_categories = image.get_all_categories_dict()
		size = float(image.calculate_size()) / 1000

                user_info =  list(web.select(DB_TABLE_USER, where=web.sqlwhere(web.storify({'nick': cookie.nick}))))
                user ={'nick': cookie.nick,
                       'password': user_info[0].password,
                       'password2': user_info[0].password,
                       'mail': user_info[0].mail,
                       'mail2': user_info[0].mail,
                       'name': user_info[0].name,
                       'surname': user_info[0].surname}
                web.render ('account.html')
        
        ## Post method. Modify the User Account..
        #
        def POST(self):
                user = web.input()
                cookie = web.cookies()
                user_path = get_all_user_path(cookie.nick)
                image =  winsollib.Image([MASTER_CATEGORIES_XML, MASTER_APPS_XML, user_path['categories_xml_file'], user_path['apps_xml_file'],
 user_path['includes_xml_file']], dtd_files)
                menu_categories = image.get_all_categories_dict()
		size = float(image.calculate_size()) / 1000
                errors = []
                messages = []
                
		if user.nick == "" or user.password == "" or user.mail == "" or user.nick == None or user.password == None or user.mail == None: 
                        errors.append("Debe completar todos los campos marcados en negrita. Son obligatorios.")
                        web.render ('account.html')
                else:
			# Check user_info
	                name = {'nick':user.nick}
	                if len(web.select(DB_TABLE_USER, where=web.sqlwhere(name)) ) > 0:
	                        # OK
				err = 0
	                        if user.password != user.password2:
	                                errors.append("Las passwords no coinciden o son nulas.")
					err += 1
	                        if user.mail != user.mail2:
	                                errors.append("Los e-mails no coinciden o son nulas")
					err += 1
	                        if err == 0:
				
					tdes = triple_des(PASSWD_CRYPTO_KEY)
					passwd = tdes.encrypt(user.password, "*")

        	                        web.update(DB_TABLE_USER, where=web.sqlwhere(web.storify({'nick': cookie.nick})), password=passwd, mail=user.mail, name = user.name, surname = user.surname)
                	                messages = ["Se han modificado los datos con éxito."]
					web.render('account.html')
				else:
                	        	web.render('account.html')

               	 	elif len(web.select(DB_TABLE_USER, where=web.sqlwhere(name)) ) == 0:
               		        # User don't exist
                	        # Never make this code.
	               	        errors.append("El usuario \"" + user.nick + "\" no existe.")
	                        web.render ('acount.html')
	                else:
        	               # DB CORRUPT
       		               print "La base de Datos está corrompida. Compruebe que \"nick\" es PRIMARY KEY."
 
## Class for \em Add \em user process.
#
# @author David Barragán Merino <bameda [AT] di.uc3m [DOT] com>
# @author CRISOL-UC3M <htp://crisol.uc3m.es>
class add_user:

	## Get method. Show the \em Add \em User form.
	#
	# @param errors - List off error messages.
        def GET(self, errors = [], messages = []):
               	user ={'nick':"", 
                       'password':"",
                       'password2':"",
                       'mail':"",
                       'mail2':"",
		       'name':"",
		       'surname':""}
               	web.render ('add_user.html')

	## Post method. Add an user to the DDBB.
	#
        def POST(self):
                user = web.input()
                errors = []
		messages = []
                if user.nick == "" or user.password == "" or user.mail == "" or user.nick == None or user.password == None or user.mail == None:
                        errors.append("Debe completar todos los campos marcados en negrita. Son obligatorios.")
                        
			web.render ('add_user.html') 
		else:
			# Check user_info
                	name = {'nick':user.nick}
                	if len(web.select(DB_TABLE_USER, where=web.sqlwhere(name)) ) == 0:
                	        # OK
				err = 0
                	        if user.password != user.password2:
                	                errors.append("Las passwords no coinciden o son nulas.")
					err += 1
                	        if user.mail != user.mail2:
                	                errors.append("Los e-mails no coinciden o son nulas")
					err += 1
                	        if err == 0:

                        	        tdes = triple_des(PASSWD_CRYPTO_KEY)
					passwd = tdes.encrypt(user.password, "*")

	                                web.insert(DB_TABLE_USER, nick=user.nick, password=passwd, mail=user.mail, name = user.name, surname = user.surname)
        	                        messages.append("El usuario \""+ user.nick + "\" ha sido creado con éxito.")
					web.render ('add_user.html')
				else:
					web.render ('add_user.html')

	                elif len(web.select(DB_TABLE_USER, where=web.sqlwhere(name)) ) == 1:
        	                # User exist
	                        errors.append("El usuario \"" + user.nick + "\" ya existe.")
                	        web.render ('add_user.html')
               	 	else:
                        	# DB CORRUPT
                        	print "La base de Datos está corrompida. Compruebe que \"nick\" es PRIMARY KEY."

## Class for \em Main \em Page.
#
# @author David Barragán Merino <bameda [AT] di.uc3m [DOT] com>
# @author CRISOL-UC3M <htp://crisol.uc3m.es>
class index:

	## Get method. Show the main page.
        #
        # @param errors - List of error messages.
        # @param messages - List of \em 'Ok' messages.
	def GET(self, errors = [], messages = []):
                cookie = web.cookies() 
                user_path = get_all_user_path(cookie.nick)
                image =  winsollib.Image([MASTER_CATEGORIES_XML, MASTER_APPS_XML, user_path['categories_xml_file'], user_path['apps_xml_file'], user_path['includes_xml_file']], dtd_files)
                menu_categories = image.get_all_categories_dict()
		size = float(image.calculate_size()) / 1000
		web.render ('index.html')

## Clast for \em View \em List process. 
#
# @author David Barragán Merino <bameda [AT] di.uc3m [DOT] com>
# @author CRISOL-UC3M <htp://crisol.uc3m.es>
class list_all:

	## Get method. Show the first/main list.
	#
	#@param list_mode - The list mode type (0 < list_mode < 3)
	def GET(self, list_mode = "1"):
                cookie = web.cookies()
                user_path = get_all_user_path(cookie.nick)
                image =  winsollib.Image([MASTER_CATEGORIES_XML, MASTER_APPS_XML, user_path['categories_xml_file'], user_path['apps_xml_file'], user_path['includes_xml_file']], dtd_files)
                menu_categories = image.get_all_categories_dict()
		size = float(image.calculate_size()) / 1000
		web.render ('list_all.html')

	## Post method. Show the list that it has selected.
	#
        def POST(self):
                cookie = web.cookies()
                user_path = get_all_user_path(cookie.nick)
                image =  winsollib.Image([MASTER_CATEGORIES_XML, MASTER_APPS_XML, user_path['categories_xml_file'], user_path['apps_xml_file'], user_path['includes_xml_file']], dtd_files)
                dat = web.input()
                menu_categories = image.get_all_categories_dict()
		size = float(image.calculate_size()) / 1000
                list_mode = dat.mode
                web.render ('list_all.html')

## Class for \em Select \em All in \em list_all.html page. (\b +)
#
# @author David Barragán Merino <bameda [AT] di.uc3m [DOT] com>
# @author CRISOL-UC3M <htp://crisol.uc3m.es>
class list_all_select_all:

        ## Get method. Select all Categories and Applications.
        #
        # @param list_mode - The list mode type (0 < list_mode < 3)
        def GET(self, list_mode):
                cookie = web.cookies()
                user_path = get_all_user_path(cookie.nick)
                image =  winsollib.Image([MASTER_CATEGORIES_XML, MASTER_APPS_XML, user_path['categories_xml_file'], user_path['apps_xml_file'], user_path['includes_xml_file']], dtd_files)
                error = image.select_all_apps()
		error = image.select_all_categories()
                image.save_includes_to_xml_file()
                menu_categories = image.get_all_categories_dict()
                size = float(image.calculate_size()) / 1000
                web.render ('list_all.html')

        ## Post method. Show the list that it has selected.
        #
        # @param list_mode - The list mode type (0 < list_mode < 3) (don't use it).
        def POST(self, list_mode):
                cookie = web.cookies()
                user_path = get_all_user_path(cookie.nick)
                image =  winsollib.Image([MASTER_CATEGORIES_XML, MASTER_APPS_XML, user_path['categories_xml_file'], user_path['apps_xml_file'], user_path['includes_xml_file']], dtd_files)
                dat = web.input()
                menu_categories = image.get_all_categories_dict()
                size = float(image.calculate_size()) / 1000
                list_mode = dat.mode
                web.render ('list_all.html')

## Class for \em Unselect \em All in \em list_all.html page. (\b +)
#
# @author David Barragán Merino <bameda [AT] di.uc3m [DOT] com>
# @author CRISOL-UC3M <htp://crisol.uc3m.es>
class list_all_unselect_all:

        ## Get method. Unselect all Categories and Applications.
        #
        # @param list_mode - The list mode type (0 < list_mode < 3)
        def GET(self, list_mode):
                cookie = web.cookies()
                user_path = get_all_user_path(cookie.nick)
                image =  winsollib.Image([MASTER_CATEGORIES_XML, MASTER_APPS_XML, user_path['categories_xml_file'], user_path['apps_xml_file'], user_path['includes_xml_file']], dtd_files)
                error = image.unselect_all_apps()
                error = image.unselect_all_categories()
                image.save_includes_to_xml_file()
                menu_categories = image.get_all_categories_dict()
                size = float(image.calculate_size()) / 1000
                web.render ('list_all.html')

        ## Post method. Show the list that it has selected.
        #
        # @param list_mode - The list mode type (0 < list_mode < 3) (don't use it).
        def POST(self, list_mode):
                cookie = web.cookies()
                user_path = get_all_user_path(cookie.nick)
                image =  winsollib.Image([MASTER_CATEGORIES_XML, MASTER_APPS_XML, user_path['categories_xml_file'], user_path['apps_xml_file'], user_path['includes_xml_file']], dtd_files)
                dat = web.input()
                menu_categories = image.get_all_categories_dict()
                size = float(image.calculate_size()) / 1000
                list_mode = dat.mode
                web.render ('list_all.html')


## Class for \em Select \em Category in \em list_all.html page. (\b +)
#
# @author David Barragán Merino <bameda [AT] di.uc3m [DOT] com>
# @author CRISOL-UC3M <htp://crisol.uc3m.es>
class list_all_select_category:

	## Get method. Select a Category.
	#
	# @param list_mode - The list mode type (0 < list_mode < 3)
	# @param cat_label - The Category label.
	def GET(self, list_mode, cat_label):
                cookie = web.cookies()
                user_path = get_all_user_path(cookie.nick)
                image =  winsollib.Image([MASTER_CATEGORIES_XML, MASTER_APPS_XML, user_path['categories_xml_file'], user_path['apps_xml_file'], user_path['includes_xml_file']], dtd_files)
                error = image.select_category(cat_label)
		image.save_includes_to_xml_file()
		menu_categories = image.get_all_categories_dict()
		size = float(image.calculate_size()) / 1000
                web.render ('list_all.html')

        ## Post method. Show the list that it has selected.
        #
	# @param list_mode - The list mode type (0 < list_mode < 3) (don't use it).
        # @param cat_label - The Category label (don't use it).
        def POST(self, list_mode, cat_label):
                cookie = web.cookies()
                user_path = get_all_user_path(cookie.nick)
                image =  winsollib.Image([MASTER_CATEGORIES_XML, MASTER_APPS_XML, user_path['categories_xml_file'], user_path['apps_xml_file'], user_path['includes_xml_file']], dtd_files)
                dat = web.input()
                menu_categories = image.get_all_categories_dict()
		size = float(image.calculate_size()) / 1000
                list_mode = dat.mode
                web.render ('list_all.html')

## Class for \em Unselect \em Category in \em list_all.html page. (\b -)
#
# @author David Barragán Merino <bameda [AT] di.uc3m [DOT] com>
# @author CRISOL-UC3M <htp://crisol.uc3m.es>
class list_all_unselect_category:

        ## Get method. Unselect a Category.
	#
	# @param list_mode - The list mode type (0 < list_mode < 3).
	# @param cat_label - The Category label.
	def GET(self, list_mode, cat_label):
                cookie = web.cookies()
                user_path = get_all_user_path(cookie.nick)
                image =  winsollib.Image([MASTER_CATEGORIES_XML, MASTER_APPS_XML, user_path['categories_xml_file'], user_path['apps_xml_file'], user_path['includes_xml_file']], dtd_files)
                error = image.unselect_category(cat_label)
		image.save_includes_to_xml_file()
                menu_categories = image.get_all_categories_dict()
                size = float(image.calculate_size()) / 1000
		web.render ('list_all.html')
		#web.seeother('/list_all.html')

        ## Post method. Show the list that it has selected.
        #
        # @param list_mode - The list mode type (0 < list_mode < 3) (don't use it).
        # @param cat_label - The Category label (don't use it).
        def POST(self, list_mode, cat_label):
                cookie = web.cookies()
                user_path = get_all_user_path(cookie.nick)
                image =  winsollib.Image([MASTER_CATEGORIES_XML, MASTER_APPS_XML, user_path['categories_xml_file'], user_path['apps_xml_file'], user_path['includes_xml_file']], dtd_files)
                dat = web.input()
		menu_categories = image.get_all_categories_dict()
		size = float(image.calculate_size()) / 1000
		list_mode = dat.mode
                web.render ('list_all.html')

## Class for \em Select \em App in \em list_all.html page. (\b +)
#
# @author David Barragán Merino <bameda [AT] di.uc3m [DOT] com>
# @author CRISOL-UC3M <htp://crisol.uc3m.es>
class list_all_select_application:

	## Get method. Select an App.
        #
        # @param list_mode - The list mode type (0 < list_mode < 3).
	# @param app_name - The App name.
        def GET(self, list_mode, app_name):
                cookie = web.cookies()
                user_path = get_all_user_path(cookie.nick)
                image =  winsollib.Image([MASTER_CATEGORIES_XML, MASTER_APPS_XML, user_path['categories_xml_file'], user_path['apps_xml_file'], user_path['includes_xml_file']], dtd_files)
                error = image.select_app(app_name)
		image.save_includes_to_xml_file()
                menu_categories = image.get_all_categories_dict()
                size = float(image.calculate_size()) / 1000
		web.render ('list_all.html')
                #web.seeother('/list_all.html')

        ## Post method. Show the list that it has selected.
        #
	# @param list_mode - The list mode type (0 < list_mode < 3) (don't use it).
        # @param app_name - The App name (don't use it).
        def POST(self, list_mode, app_name):
                cookie = web.cookies()
                user_path = get_all_user_path(cookie.nick)
                image =  winsollib.Image([MASTER_CATEGORIES_XML, MASTER_APPS_XML, user_path['categories_xml_file'], user_path['apps_xml_file'], user_path['includes_xml_file']], dtd_files)
                dat = web.input()
                menu_categories = image.get_all_categories_dict()
                size = float(image.calculate_size()) / 1000
		list_mode = dat.mode
                web.render ('list_all.html')

## Class for \em Unselect \em App in \em list_all.html page. (\b -)
#
# @author David Barragán Merino <bameda [AT] di.uc3m [DOT] com>
# @author CRISOL-UC3M <htp://crisol.uc3m.es>
class list_all_unselect_application:

	## Get method. Unselect an App.
	#
	# @param list_mode - The list mode type (0 < list_mode < 3).
	# @param app_name - The App name.
        def GET(self, list_mode, app_name):
                cookie = web.cookies()
                user_path = get_all_user_path(cookie.nick)
                image =  winsollib.Image([MASTER_CATEGORIES_XML, MASTER_APPS_XML, user_path['categories_xml_file'], user_path['apps_xml_file'], user_path['includes_xml_file']], dtd_files)
                error = image.unselect_app(app_name)
		image.save_includes_to_xml_file()
                menu_categories = image.get_all_categories_dict()
		size = float(image.calculate_size()) / 1000
                web.render ('list_all.html')
                #web.seeother('/list_all.html')

        ## Post method. Show the list that it has selected.
        #
	# @param list_mode - The list mode type (0 < list_mode < 3) (don't use it).
        # @param app_name - The App name (don't use it).
        def POST(self, list_mode, app_name):
                cookie = web.cookies()
                user_path = get_all_user_path(cookie.nick)
                image =  winsollib.Image([MASTER_CATEGORIES_XML, MASTER_APPS_XML, user_path['categories_xml_file'], user_path['apps_xml_file'], user_path['includes_xml_file']], dtd_files)
                dat = web.input()
                menu_categories = image.get_all_categories_dict()
                list_mode = dat.mode
		size = float(image.calculate_size()) / 1000
                web.render ('list_all.html')

## Class for \em Select \em All \em at \em Category in \em list_all.html page. (\b *)
#
# @author David Barragán Merino <bameda [AT] di.uc3m [DOT] com>
# @author CRISOL-UC3M <htp://crisol.uc3m.es>
class list_all_select_all_by_category:

	## Get method. Select all applications at the Category with the same name as \em cat_label.
	#
        # @param list_mode - The list mode type (0 < list_mode < 3).
	# @param cat_label - The Category label.
	def GET(self, list_mode, cat_label):
		cookie = web.cookies()
		user_path = get_all_user_path(cookie.nick)
		image =  winsollib.Image([MASTER_CATEGORIES_XML, MASTER_APPS_XML, user_path['categories_xml_file'], user_path['apps_xml_file'], user_path['includes_xml_file']], dtd_files)
		error = image.select_category(cat_label)
		error = image.select_apps_by_category(cat_label)
		image.save_includes_to_xml_file()
		menu_categories = image.get_all_categories_dict()
		size = float(image.calculate_size()) / 1000
                web.render ('list_all.html')
                #web.seeother('/list_all.html')

        ## Post method. Show the list that it has selected.
        #
        # @param list_mode - The list mode type (0 < list_mode < 3) (don't use it).
        # @param cat_label - The Category label (don't use it).
        def POST(self, list_mode, cat_label):
                cookie = web.cookies()
                user_path = get_all_user_path(cookie.nick)
                image =  winsollib.Image([MASTER_CATEGORIES_XML, MASTER_APPS_XML, user_path['categories_xml_file'], user_path['apps_xml_file'], user_path['includes_xml_file']], dtd_files)
                dat = web.input()
                menu_categories = image.get_all_categories_dict()
		size = float(image.calculate_size()) / 1000
                list_mode = dat.mode
                web.render ('list_all.html')

## Class for \em Unselect \em All \em at \em Category in \em list_all.html page. (\b =)
#
# @author David Barragán Merino <bameda [AT] di.uc3m [DOT] com>
# @author CRISOL-UC3M <htp://crisol.uc3m.es>
class list_all_unselect_all_by_category:

        ## Get method. Unselect all applications at the Category with the same name as \em cat_label.
	#
        # @param list_mode - The list mode type (0 < list_mode < 3).
	# @param cat_label - The Category label.
	def GET(self, list_mode, cat_label):
		cookie = web.cookies()
		user_path = get_all_user_path(cookie.nick)
		image =  winsollib.Image([MASTER_CATEGORIES_XML, MASTER_APPS_XML, user_path['categories_xml_file'], user_path['apps_xml_file'], user_path['includes_xml_file']], dtd_files)
		error = image.unselect_category(cat_label)
		error = image.unselect_apps_by_category(cat_label)
		image.save_includes_to_xml_file()
		menu_categories = image.get_all_categories_dict()
		size = float(image.calculate_size()) / 1000
                web.render ('list_all.html')
                #web.seeother('/list_all.html')

        ## Post method. Show the list that it has selected.
        #
        # @param list_mode - The list mode type (0 < list_mode < 3) (don't use it).
        # @param cat_label - The Category label (don't use it).
        def POST(self, list_mode, cat_label):
                cookie = web.cookies()
                user_path = get_all_user_path(cookie.nick)
                image =  winsollib.Image([MASTER_CATEGORIES_XML, MASTER_APPS_XML, user_path['categories_xml_file'], user_path['apps_xml_file'], user_path['includes_xml_file']], dtd_files)
                dat = web.input()
                menu_categories = image.get_all_categories_dict()
		size = float(image.calculate_size()) / 1000
                list_mode = dat.mode
                web.render ('list_all.html')

## Class for \em View \em A \em Category process.
#
# @author David Barragán Merino <bameda [AT] di.uc3m [DOT] com>
# @author CRISOL-UC3M <htp://crisol.uc3m.es>
class category:
	
	## Get method. Show the Category information.
	#
	# @param cat_label - The Category label.
	# @param messages - List of ºem 'Ok' messages.
	def GET(self, cat_label, messages = []):
                cookie = web.cookies()
                user_path = get_all_user_path(cookie.nick)
                image =  winsollib.Image([MASTER_CATEGORIES_XML, MASTER_APPS_XML, user_path['categories_xml_file'], user_path['apps_xml_file'], user_path['includes_xml_file']], dtd_files)
		menu_categories = image.get_all_categories_dict()
		size = float(image.calculate_size()) / 1000
		category = image.get_category_dict_by_label(cat_label)
		web.render ('category.html')


## Class for \em Add \em Category process.
#
# @author David Barragán Merino <bameda [AT] di.uc3m [DOT] com>
# @author CRISOL-UC3M <htp://crisol.uc3m.es>
class add_category:

        ## Get method. Show the \em Add \em Category form.
        #
        # @param errors - List of errors messages.
	def GET(self, errors = []):
                cookie = web.cookies()
                user_path = get_all_user_path(cookie.nick)
                image =  winsollib.Image([MASTER_CATEGORIES_XML, MASTER_APPS_XML, user_path['categories_xml_file'], user_path['apps_xml_file'], user_path['includes_xml_file']], dtd_files)
                menu_categories = image.get_all_categories_dict()
		size = float(image.calculate_size()) / 1000
		cat = {'name':"",
                       'label':"",
                       'description':"",
		       'icon':"",
		       'icon_url':""}
		web.render ('add_cat.html')

	## Post method. Add a new Category.
	#
	def POST(self):
		cookie = web.cookies()
                user_path = get_all_user_path(cookie.nick)
                image =  winsollib.Image([MASTER_CATEGORIES_XML, MASTER_APPS_XML, user_path['categories_xml_file'], user_path['apps_xml_file'], user_path['includes_xml_file']], dtd_files)
                category = web.input()
		cat_values = [category.name, 
                              category.label.strip(), 
                              category.description]
		if category.icon.strip() == "" or category.icon == None or category.icon_url.strip() == "" or category.icon_url == None: 
			cat_values.append(CATEGORY_ICON)
			cat_values.append(CATEGORY_ICON_URL)
		else:
			cat_values.append(category.icon.strip())
			cat_values.append(category.icon_url.strip())

		if image.add_category(cat_values):
			# Category added
			image.save_categories_to_xml_file() ## To save to thee xml file
			menu_categories = image.get_all_categories_dict()
			size = float(image.calculate_size()) / 1000
			category = image.get_category_dict_by_label(category.label.strip())
			messages = []
			messages.append("Categoría \"" + category['name'] + "\" añadida con éxito.")
			web.render('/category.html')	
		else:
			# Category did'n add
			menu_categories = image.get_all_categories_dict()
			size = float(image.calculate_size()) / 1000
			cat = {'name':category.name,
                               'label':category.label,
                               'description':category.description,
			       'icon':category.icon,
			       'icon_url':category.icon_url}
			errors = []
			errors.append("Error fatal - Compruebe que la etiqueta de esta categoría no este usada y sea distinta de \"none\".")
			web.render('/add_cat.html')

## Class for \em Delete \em A \em Category process.
#
# @author David Barragán Merino <bameda [AT] di.uc3m [DOT] com>
# @author CRISOL-UC3M <htp://crisol.uc3m.es>
class del_category:

	## Get method. Delete a Category.
	#
	# @param cat_label - The Category label.
	def GET(self, cat_label):
                cookie = web.cookies()
                user_path = get_all_user_path(cookie.nick)
                image =  winsollib.Image([MASTER_CATEGORIES_XML, MASTER_APPS_XML, user_path['categories_xml_file'], user_path['apps_xml_file'], user_path['includes_xml_file']], dtd_files)
		if image.del_category(cat_label):
                        image.save_categories_to_xml_file()
			image.save_applications_to_xml_file()
                        image.save_includes_to_xml_file()

			menu_categories = image.get_all_categories_dict()
			size = float(image.calculate_size()) / 1000
			messages = ["La categoría con la etiqueta \"" + cat_label + "\" ha sido borrada."]
			errors = []
			web.render('/index.html')
                else:
                        # Category didn't delete
			web.redirect('/category/' + cat_label)

## Class for \em Modify \em A \em Category process.
#
# @author David Barragán Merino <bameda [AT] di.uc3m [DOT] com>
# @author CRISOL-UC3M <htp://crisol.uc3m.es>
class modify_category:

	## Get method. Show the \em Modify \em a \em Category form. 
	#
	# @param cat_label - The Category label.
	# @param errors - List of error messages.
	def GET(self, cat_label, errors = []):
                cookie = web.cookies()
                user_path = get_all_user_path(cookie.nick)
                image =  winsollib.Image([MASTER_CATEGORIES_XML, MASTER_APPS_XML, user_path['categories_xml_file'], user_path['apps_xml_file'], user_path['includes_xml_file']], dtd_files)
                menu_categories = image.get_all_categories_dict()
		size = float(image.calculate_size()) / 1000
		category = image.get_category_dict_by_label(cat_label)
		if category != None:
			web.render ('/mod_cat.html')
	
	## Post method. Modify a Category.
	#
	# @param cat_label - The Category label.
	def POST(self, cat_label):
                cookie = web.cookies()
                user_path = get_all_user_path(cookie.nick)
                image =  winsollib.Image([MASTER_CATEGORIES_XML, MASTER_APPS_XML, user_path['categories_xml_file'], user_path['apps_xml_file'], user_path['includes_xml_file']], dtd_files)
                categ = web.input()
		cat_values = [categ.name,
                              categ.description]
		if categ.icon.strip() == "" or categ.icon == None or categ.icon_url.strip() == "" or categ.icon_url == None:
			cat_values.append(CATEGORY_ICON)
			cat_values.append(CATEGORY_ICON_URL)
		else:
			cat_values.append(categ.icon.strip())
			cat_values.append(categ.icon_url.strip())

		if image.modify_category_values(cat_label, cat_values):
			image.save_categories_to_xml_file()
			image.save_applications_to_xml_file()
			menu_categories = image.get_all_categories_dict()
			size = float(image.calculate_size()) / 1000
                        category = image.get_category_dict_by_label(cat_label)
                        messages = []
                        messages.append("Categoría \"" + categ.name + "\" modificada con éxito.")
			web.render('/category.html')
		else:
			# Imposible
			menu_categories = image.get_all_categories_dict()
			size = float(image.calculate_size()) / 1000
			cat = {'name':categ.name,
                               'description':categ.description,
			       'icon':categ.icon,
			       'icon_url':categ.icon_url}
			errors = []
			errors.append("Error fatal - No se ha podido modificar esta categoría.")
			web.render('/mod_cat.html')

## Class for \em Select \em Category in \em category/'cat_name'.html page. 
#
# @author David Barragán Merino <bameda [AT] di.uc3m [DOT] com>
# @author CRISOL-UC3M <htp://crisol.uc3m.es>
class select_category:

	## Get method. Select a Category.
        #
        # @param cat_label - The Category label.
	def GET(self, cat_label):
                cookie = web.cookies()
                user_path = get_all_user_path(cookie.nick)
                image =  winsollib.Image([MASTER_CATEGORIES_XML, MASTER_APPS_XML, user_path['categories_xml_file'], user_path['apps_xml_file'], user_path['includes_xml_file']], dtd_files)
                error = image.select_category(cat_label)
		image.save_includes_to_xml_file()
		web.seeother('/category/' + cat_label)

## Class for \em Select \em App in \em category/'cat_name'.html page.
#
# @author David Barragán Merino <bameda [AT] di.uc3m [DOT] com>
# @author CRISOL-UC3M <htp://crisol.uc3m.es>
class category_select_application:

	## Get method. Select an App in a Category web page.
	#
	# @param cat_label - The Category label.
	# @param app_name - The App name.
	def GET(self, cat_label, app_name):
		cookie = web.cookies()
                user_path = get_all_user_path(cookie.nick)
                image =  winsollib.Image([MASTER_CATEGORIES_XML, MASTER_APPS_XML, user_path['categories_xml_file'], user_path['apps_xml_file'], user_path['includes_xml_file']], dtd_files)
		errors = image.select_app(app_name)
		image.save_includes_to_xml_file()
		web.seeother('/category/' + cat_label)

## Class for \em Unselect \em App in \em category/'cat_name'.html page.
#
# @author David Barragán Merino <bameda [AT] di.uc3m [DOT] com>
# @author CRISOL-UC3M <htp://crisol.uc3m.es>
class category_unselect_application:
	
	## Get method. Unselect an App in a Category web page.
        #
        # @param cat_label - The Category label.
        # @param app_name - The App name.
	def GET(self, cat_label, app_name):
		cookie = web.cookies()
                user_path = get_all_user_path(cookie.nick)
                image =  winsollib.Image([MASTER_CATEGORIES_XML, MASTER_APPS_XML, user_path['categories_xml_file'], user_path['apps_xml_file'], user_path['includes_xml_file']], dtd_files)
		errors = image.unselect_app(app_name)
		image.save_includes_to_xml_file()
		web.seeother('/category/' + cat_label)

## Class for \em Select \em All \em Apps in \em category/'cat_name'.html page.
#
# @author David Barragán Merino <bameda [AT] di.uc3m [DOT] com>
# @author CRISOL-UC3M <htp://crisol.uc3m.es>
class select_all_apps_by_category:

        ## Get method. Select all applications at the Category with the same name as \em cat_label.
        #
        # @param cat_label - The Category label.
        def GET(self, cat_label):
                cookie = web.cookies()
                user_path = get_all_user_path(cookie.nick)
                image =  winsollib.Image([MASTER_CATEGORIES_XML, MASTER_APPS_XML, user_path['categories_xml_file'], user_path['apps_xml_file'], user_path['includes_xml_file']], dtd_files)
                error = image.select_category(cat_label)
		error = image.select_apps_by_category(cat_label)
		image.save_includes_to_xml_file()
		web.seeother('/category/' + cat_label)

## Class for \em Unselect \em Category in \em category/'cat_name'.html page.
#
# @author David Barragán Merino <bameda [AT] di.uc3m [DOT] com>
# @author CRISOL-UC3M <htp://crisol.uc3m.es>
class unselect_category:

	## Get method. Unselect a Category.
	#
	# @param cat_label - The Category label.
        def GET(self, cat_label):
                cookie = web.cookies()
                user_path = get_all_user_path(cookie.nick)
                image =  winsollib.Image([MASTER_CATEGORIES_XML, MASTER_APPS_XML, user_path['categories_xml_file'], user_path['apps_xml_file'], user_path['includes_xml_file']], dtd_files)
                error = image.unselect_category(cat_label)
		image.save_includes_to_xml_file()
		web.seeother('/category/' + cat_label)

## Class for \em Unselect \em All \em Apps in \em category/'cat_name'.html page.
#
# @author David Barragán Merino <bameda [AT] di.uc3m [DOT] com>
# @author CRISOL-UC3M <htp://crisol.uc3m.es>
class unselect_all_apps_by_category:

	## Get method. Unselect all applications at the Category with the same name as \em cat_label.
	#
	# @param cat_label - The Category label.
        def GET(self, cat_label):
                cookie = web.cookies()
                user_path = get_all_user_path(cookie.nick)
                image =  winsollib.Image([MASTER_CATEGORIES_XML, MASTER_APPS_XML, user_path['categories_xml_file'], user_path['apps_xml_file'], user_path['includes_xml_file']], dtd_files)
                error = image.unselect_category(cat_label)
		error = image.unselect_apps_by_category(cat_label)
		image.save_includes_to_xml_file()
		web.seeother('/category/' + cat_label)

## Class for \em View \em An \em App process.
#
# @author David Barragán Merino <bameda [AT] di.uc3m [DOT] com>
# @author CRISOL-UC3M <htp://crisol.uc3m.es>
class app:
	
	## Get method. Show the App information.
	#
	# @param app_name - The App name.
	# @param messages - List of \em 'Ok' messages.
        def GET(self, app_name, messages = []):
                cookie = web.cookies()
                user_path = get_all_user_path(cookie.nick)
                image =  winsollib.Image([MASTER_CATEGORIES_XML, MASTER_APPS_XML, user_path['categories_xml_file'], user_path['apps_xml_file'], user_path['includes_xml_file']], dtd_files)
                menu_categories = image.get_all_categories_dict()
		size = float(image.calculate_size()) / 1000
                app = image.get_app_dict_by_name(app_name)
                web.render ('app.html')

## Class for \em Add \em An \em App process.
#
# @author David Barragán Merino <bameda [AT] di.uc3m [DOT] com>
# @author CRISOL-UC3M <htp://crisol.uc3m.es>
class add_application:

	## Get method. Show the \em Add \em App form.
	#
	# @param errors - List of errors messages.
	def GET(self, errors = []):
                cookie = web.cookies()
                user_path = get_all_user_path(cookie.nick)
                image =  winsollib.Image([MASTER_CATEGORIES_XML, MASTER_APPS_XML, user_path['categories_xml_file'], user_path['apps_xml_file'], user_path['includes_xml_file']], dtd_files)
                menu_categories = image.get_all_categories_dict()
		size = float(image.calculate_size()) / 1000
		app ={'name':"",
                      'version':"",
		      'size':"",
                      'site':"",
                      'plat_win':"",
                      'plat_unix':"",
                      'plat_mac':"",
                      'minidescription':"",
                      'description':"",
                      'file':"",
                      'file_url':"",
                      'icon':"",
                      'icon_url':"",
                      'md5sum':"",
                      'categories':[],
                      'alternatives':""}
		for cat in menu_categories:
			app['categories'].append({'name':cat['name'],'label':cat['label'], 'status':""})
		web.render ('add_app.html')
	
	## Post method. Add a new App.
	#
	def POST(self):
                cookie = web.cookies()
                user_path = get_all_user_path(cookie.nick)
                image =  winsollib.Image([MASTER_CATEGORIES_XML, MASTER_APPS_XML, user_path['categories_xml_file'], user_path['apps_xml_file'], user_path['includes_xml_file']], dtd_files)
		menu_categories = image.get_all_categories_dict()
                application = web.input()
		# Manuals (Not in this form)
		manuals = {}
		manuals['app_man_online'] = []
		manuals['app_man_offline'] = []
		# Plataforms
		plataforms = []
		try:
			if application.plat_win != None:	
				plataforms.append("Windows")
		except Exception:
			pass # You don't select it
		try:
			if application.plat_unix != None:
				plataforms.append("GNU-Linux/UNIX")
		except Exception:
			pass # You don't select it
		try:
			if application.plat_mac != None:
				plataforms.append("Mac OSX")
		except Exception:
			pass # You don't select it
		# Categories
		categories = []
		for cat in menu_categories:
			try:
				if getattr(application, 'cat_' + cat['label']) != None:
					categories.append(cat['label'])
			except Exception:
				pass # You don't select it

		# Alternatives
		alternatives = []
		alternatives = application.alternatives.split(',')
                n = 0;
                for alt in alternatives:
                        alternatives[n] = alt.strip() #to remove leading and trailing whitespace
                        if alternatives[n] == '':
                                alternatives.remove(alternatives[n])
                        else:
                                n +=1

		app_values = [application.name,
                              application.version,
			      application.size,
                              application.site,
                              manuals,
                              plataforms,
                              application.minidescription,
                              application.description,
                              application.file,
                              application.file_url]		
		if application.icon.strip() == "" or application.icon == None or application.icon_url.strip() == "" or application.icon_url == None:
                        app_values.append(APPLICATION_ICON)
                        app_values.append(APPLICATION_ICON_URL)
                else:
                        app_values.append(application.icon.strip())
                        app_values.append(application.icon_url.strip())
		app_values.append(application.md5sum)
                app_values.append(categories)
                app_values.append(alternatives)

		if image.add_app(app_values):
                        # App added 
                        image.save_applications_to_xml_file() ## To save to the xml file
			menu_categories = image.get_all_categories_dict()
			size = float(image.calculate_size()) / 1000
			app = image.get_app_dict_by_name(application.name)
                        messages = []
                        messages.append("Aplicación \"" + application.name + "\" añadida con éxito.")
                        web.render('/app.html')
                else:
                        # App did'n add
			menu_categories = image.get_all_categories_dict() 
			size = float(image.calculate_size()) / 1000
			app ={'name':application.name,
                              'version':application.version,
			      'size':application.size,
                              'site':application.site,
                              'minidescription':application.minidescription,
                              'description':application.description,
                              'file':application.file,
                              'file_url':application.file_url,
                              'icon':application.icon,
                              'icon_url':application.icon_url,
                              'md5sum':application.md5sum,
                              'categories':[],
                              'alternatives':application.alternatives}
			#Plataforms
			app['plat_win'] = "" 
			app['plat_unix'] = ""
			app['plat_mac'] = ""
			for plat in plataforms:
				if plat == "Windows":
					app['plat_win'] = "checked"
				elif plat == "GNU-Linux/UNIX":
					app['plat_unix'] = "checked"
				elif plat == "Mac OSX":
					app['plat_mac'] = "checked"
			#categories
			for cat in menu_categories:
				app['categories'].append({'name':cat['name'],'label':cat['label'], 'status':""})

			for lab in categories:
				for cat in app['categories']:
					if cat['label'] == lab:
						cat['status'] = "checked"

			errors = []
			errors.append("Error fatal - Compruebe que el nombre de esta aplicación no este usada.")
                        web.render('/add_app.html')

## Class for \em Delete \em An \em App process.
#
# @author David Barragán Merino <bameda [AT] di.uc3m [DOT] com>
# @author CRISOL-UC3M <htp://crisol.uc3m.es>
class del_application:
	
	## Get method. Delete an App.
	#
	# @param app_name - The App name.
        def GET(self, app_name):
                cookie = web.cookies()
                user_path = get_all_user_path(cookie.nick)
                image =  winsollib.Image([MASTER_CATEGORIES_XML, MASTER_APPS_XML, user_path['categories_xml_file'], user_path['apps_xml_file'], user_path['includes_xml_file']], dtd_files)
                if image.del_app(app_name):
                        image.save_applications_to_xml_file()
                        image.save_includes_to_xml_file()
			image.save_categories_to_xml_file()

                        menu_categories = image.get_all_categories_dict()
			size = float(image.calculate_size()) / 1000
                        messages = ["La aplicaicón \"" + app_name + "\" ha sido borrada."]
                        errors = []
                        web.render('/index.html')
                else:
                        # Application didn't delete
                        web.redirect('/app/' + app.name)

## Class for \em Modify \em An \em App process.
#
# @author David Barragán Merino <bameda [AT] di.uc3m [DOT] com>
# @author CRISOL-UC3M <htp://crisol.uc3m.es>
class modify_application:
	
	## Get method. Show the \em Modify \em an \em App form
	#
	# @param app_name - The App name.
	# @param errors - List of errors messages.
	def GET(self, app_name, errors = []):
                cookie = web.cookies()
                user_path = get_all_user_path(cookie.nick)
                image =  winsollib.Image([MASTER_CATEGORIES_XML, MASTER_APPS_XML, user_path['categories_xml_file'], user_path['apps_xml_file'], user_path['includes_xml_file']], dtd_files)
                menu_categories = image.get_all_categories_dict()
		size = float(image.calculate_size()) / 1000
		app_dict = image.get_app_dict_by_name(app_name)
		app = {'name':app_dict['name'],
                       'version':app_dict['version'],
		       'size':app_dict['size'],
                       'site':app_dict['site'],
                       'minidescription':app_dict['minidescription'],
                       'description':app_dict['description'],
                       'file':app_dict['file'],
                       'software_url':app_dict['software_url'],
                       'icon':app_dict['icon'],
                       'icon_url':app_dict['icon_url'],
                       'md5sum':app_dict['md5sum']}
		# Plataform
		app['plat_win'] = ''
		app['plat_unix'] = ''
		app['plat_mac'] = ''
		for plat in app_dict['plataforms']:
			if plat == "Windows":
				app['plat_win'] = "checked"
			elif plat == "GNU-Linux/UNIX":
				app['plat_unix'] = "checked"
			elif plat == "Mac OSX":
				app['plat_mac'] = "checked"
		# Categoryes
		app['categories'] = []
		for cat in menu_categories:
			app['categories'].append({'name':cat['name'],'label':cat['label'], 'status':""})
		for lab in app_dict['categories']:
			for cat in app['categories']:
				if cat['label'] == lab:
					cat['status'] = "checked"

		# Alternatives
		n = 0
                alternatives = ""
                for alt in app_dict['alternatives']:
                        n = n + 1
                        alternatives = alternatives + alt
                        if n < len(app_dict['alternatives']):
                                alternatives = alternatives + ","
                app['alternatives'] = alternatives
		web.render ('mod_app.html')

	## Post method. Modify some App.
	#
        # @param app_name - The App name.
	def POST(self, app_name):
                cookie = web.cookies()
                user_path = get_all_user_path(cookie.nick)
                image =  winsollib.Image([MASTER_CATEGORIES_XML, MASTER_APPS_XML, user_path['categories_xml_file'], user_path['apps_xml_file'], user_path['includes_xml_file']], dtd_files)
                menu_categories = image.get_all_categories_dict()
		application = web.input()
                # Manuals (Not in this form)
                manuals = {}
                manuals['app_man_online'] = []
                manuals['app_man_offline'] = []
                # Plataforms
                plataforms = []
                try:
                        if application.plat_win != None:
                                plataforms.append("Windows")
                except Exception, e:
                        pass # You don't select it
                try:
                        if application.plat_unix != None:
                                plataforms.append("GNU-Linux/UNIX")
                except Exception, e:
                        pass # You don't select it
                try:
                        if application.plat_mac != None:
                                plataforms.append("Mac OSX")
                except Exception, e:
                        pass # You don't select it
                # Categories
                categories = []
                for cat in menu_categories:
                        try:
                                if getattr(application, 'cat_' + cat['label']) != None:
                                        categories.append(cat['label'])
                        except Exception:
                                pass # You don't select it
		# Alternatives
                alternatives = []
                alternatives = application.alternatives.split(',')
                n = 0;
                for alt in alternatives:
                        alternatives[n] = alt.strip() #to remove leading and trailing whitespace
                        if alternatives[n] == '':
                                alternatives.remove(alternatives[n])
			else:
				n +=1
		
		app_values = [application.version,
			      application.size,
                              application.site,
                              manuals,
                              plataforms,
                              application.minidescription,
                              application.description,
                              application.file,
                              application.file_url]
		if application.icon.strip() == "" or application.icon == None or application.icon_url.strip() == "" or application.icon_url == None:
		   app_values.append(APPLICATION_ICON)
		   app_values.append(APPLICATION_ICON_URL)
		else:
			app_values.append(application.icon.strip())
			app_values.append(application.icon_url.strip())
		app_values.append(application.md5sum)
		app_values.append(categories)
		app_values.append(alternatives)
	
                if image.modify_app_values(app_name, app_values):
			# App modified
                        image.save_applications_to_xml_file() ## To save to the xml file
                        menu_categories = image.get_all_categories_dict()
			size = float(image.calculate_size()) / 1000
                        app = image.get_app_dict_by_name(app_name)
                        messages = []
                        messages.append("Aplicación \"" + app_name + "\" modificada con éxito.")
                        web.render('/app.html')

		else:
			# App did'n modify
                        menu_categories = image.get_all_categories_dict()
			size = float(image.calculate_size()) / 1000
                        app ={'name':app_name,
                              'version':application.version,
			      'size':application.size,
                              'site':application.site,
                              'minidescription':application.minidescription,
                              'description':application.description,
                              'file':application.file,
                              'file_url':application.file_url,
                              'icon':application.icon,
                              'icon_url':application.icon_url,
                              'md5sum':application.md5sum,
                              'categories':[],
                              'alternatives':application.alternatives}
                        # Plataforms
			app['plat_win'] = ""
                        app['plat_unix'] = ""
                        app['plat_mac'] = ""
                        for plat in plataforms:
                                if plat == "Windows":
                                        app['plat_win'] = "checked"
                                elif plat == "GNU-Linux/UNIX":
                                        app['plat_unix'] = "checked"
                                elif plat == "Mac OSX":
                                        app['plat_mac'] = "checked"
			# Categories
                        for cat in menu_categories:
                                app['categories'].append({'name':cat['name'],'label':cat['label'], 'status':""})

                        for lab in categories:
                                for cat in app['categories']:
                                        if cat['label'] == lab:
                                                cat['status'] = "checked"

                        errors = []
                        errors.append("Error fatal - No se ha podido modificar esta aplicacion.")
			errors.append("            - Compruebe que los valores introducidos son correctos.")
                        web.render('/mod_app.html')

## Class for \em Select \em App in \em app/'app_name'.html page.
#
# @author David Barragán Merino <bameda [AT] di.uc3m [DOT] com>
# @author CRISOL-UC3M <htp://crisol.uc3m.es>
class select_application:

	## Get method. Unselect an App at application web page.
        #
        # @param app_name - The App name.
        def GET(self, app_name):
                cookie = web.cookies()
                user_path = get_all_user_path(cookie.nick)
                image =  winsollib.Image([MASTER_CATEGORIES_XML, MASTER_APPS_XML, user_path['categories_xml_file'], user_path['apps_xml_file'], user_path['includes_xml_file']], dtd_files)
                error = image.select_app(app_name)
		image.save_includes_to_xml_file()
                web.seeother('/app/' + app_name)

## Class for \em Unselect \em App in \em app/'app_name'.html page.
#
# @author David Barragán Merino <bameda [AT] di.uc3m [DOT] com>
# @author CRISOL-UC3M <htp://crisol.uc3m.es>
class unselect_application:

	## Get method. Select an App at application web page.
	#
	# @param app_name - The App name.
        def GET(self, app_name):
                cookie = web.cookies()
                user_path = get_all_user_path(cookie.nick)
                image =  winsollib.Image([MASTER_CATEGORIES_XML, MASTER_APPS_XML, user_path['categories_xml_file'], user_path['apps_xml_file'], user_path['includes_xml_file']], dtd_files)
                error = image.unselect_app(app_name)
		image.save_includes_to_xml_file()
                web.seeother('/app/' + app_name)

## Class for \em Add \em On-Line \em Manual \em to \em An \em App process.
#
# @author David Barragán Merino <bameda [AT] di.uc3m [DOT] com>
# @author CRISOL-UC3M <htp://crisol.uc3m.es>
class add_application_man_online:

        ## Get method. Show the \em Add \em App \em Manual \em Online form.
        #
        # @param app_name - The App name.
        def GET(self, app_name, errors = []):
                cookie = web.cookies()
                user_path = get_all_user_path(cookie.nick)
                image =  winsollib.Image([MASTER_CATEGORIES_XML, MASTER_APPS_XML, user_path['categories_xml_file'], user_path['apps_xml_file'], user_path['includes_xml_file']], dtd_files)
                menu_categories = image.get_all_categories_dict()
		size = float(image.calculate_size()) / 1000
                man_on = {'name':"", 
                          'url':"",
                          'description':"",
                          'lang':""}
                web.render('/add_app_man_online.html')
        
	## Post method. Add an off-line manuals to some application.
	#
	# @param app_name - The App name.
        def POST(self, app_name):
                cookie = web.cookies()
                user_path = get_all_user_path(cookie.nick)
                image =  winsollib.Image([MASTER_CATEGORIES_XML, MASTER_APPS_XML, user_path['categories_xml_file'], user_path['apps_xml_file'], user_path['includes_xml_file']], dtd_files)
                dat = web.input()
                manual = []
                manual.append(dat.man_name)
                manual.append(dat.man_url)
                manual.append(dat.man_description)
                manual.append(dat.man_lang)
                if image.add_manual_online_to_app(app_name, manual):
                        # OK
                        image.save_applications_to_xml_file() ## To save to the xml file
                        menu_categories = image.get_all_categories_dict()
			size = float(image.calculate_size()) / 1000
                        app = image.get_app_dict_by_name(app_name)
                        messages = []
                        messages.append("Manual añadido a la aplicación \"" + app_name + "\" con éxito.")
                        web.render('/app.html')
                else:
                        # ERROR
                        menu_categories = image.get_all_categories_dict()
			size = float(image.calculate_size()) / 1000
                        man_on = {'name':dat.man_name, 
                                  'url':dat.man_url,
                                  'description':dat.man_description,
                                  'lang':dat.man_lang}
                        
                        errors = []
                        errors.append("Errori. No se ha podido añadir el manual a la applicación.")
			errors.append("Compruebe que los valores introducidos son correctos.")

                        web.render('/add_app_man_online.html')

## Class for \em Add \em Off-Line \em Manual \em to \em An \em App process.
#
# @author David Barragán Merino <bameda [AT] di.uc3m [DOT] com>
# @author CRISOL-UC3M <htp://crisol.uc3m.es>
class add_application_man_offline:

	## Get method. Show the \em Add \em App \em Manual \em Offline form.
	#
	# @param app_name - The App name.
        def GET(self, app_name, errors = []):
                cookie = web.cookies()
                user_path = get_all_user_path(cookie.nick)
                image =  winsollib.Image([MASTER_CATEGORIES_XML, MASTER_APPS_XML, user_path['categories_xml_file'], user_path['apps_xml_file'], user_path['includes_xml_file']], dtd_files)
                menu_categories = image.get_all_categories_dict()
		size = float(image.calculate_size()) / 1000
                man_off = {'name':"", 
                          'url':"",
                          'file':"",
			  'size':"",
                          'description':"",
                          'lang':""}
                web.render('/add_app_man_offline.html')
        
	## Post method. Add an on-line manuals to some application.
	#
	# @param app_name - The App name.
        def POST(self, app_name):
                cookie = web.cookies()
                user_path = get_all_user_path(cookie.nick)
                image =  winsollib.Image([MASTER_CATEGORIES_XML, MASTER_APPS_XML, user_path['categories_xml_file'], user_path['apps_xml_file'], user_path['includes_xml_file']], dtd_files)
                dat = web.input()
                manual = []
                manual.append(dat.man_name)
                manual.append(dat.man_url)
                manual.append(dat.man_file)
		manual.append(dat.man_size)
                manual.append(dat.man_description)
                manual.append(dat.man_lang)
                if image.add_manual_offline_to_app(app_name, manual):
                        # OK
                        image.save_applications_to_xml_file() ## To save to the xml file
                        menu_categories = image.get_all_categories_dict()
			size = float(image.calculate_size()) / 1000
                        app = image.get_app_dict_by_name(app_name)
                        messages = []
                        messages.append("Manual añadido a la aplicación \"" + app_name + "\" con éxito.")
                        web.render('/app.html')
                else:
                        # ERROR
                        menu_categories = image.get_all_categories_dict()
			size = float(image.calculate_size()) / 1000
                        man_off = {'name':dat.man_name, 
                                  'url':dat.man_url,
                                  'file':dat.man_file,
				  'size':dat.man_size,
                                  'description':dat.man_description,
                                  'lang':dat.man_lang}
                        
                        errors = []
                        errors.append("Error fatal. No se ha podido añadir el manual a la applicación.")
			errors.append("Compruebe que los valores introducidos son correctos.")

                        web.render('/add_app_man_offline.html')

## Class for \em Make \em ISO process.
#
# @author David Barragán Merino <bameda [AT] di.uc3m [DOT] com>
# @author CRISOL-UC3M <htp://crisol.uc3m.es>
class make_composition:

	## Get method. Show the \em Make \em ISO form.
	#
	# @param errors - List with errors messages.
        def GET(self, errors = []):
                cookie = web.cookies()
                user_path = get_all_user_path(cookie.nick)
                image =  winsollib.Image([MASTER_CATEGORIES_XML, MASTER_APPS_XML, user_path['categories_xml_file'], user_path['apps_xml_file'], user_path['includes_xml_file']], dtd_files)
                menu_categories = image.get_all_categories_dict()
		size = float(image.calculate_size()) / 1000
                template_list = []
                for f in os.listdir(TEMPLATES_DIR):
                        if os.path.isdir(os.path.join(TEMPLATES_DIR, f)) and not f.startswith("."):
				if os.path.exists(MASTER_DIR+"/web/static/images/templates/"+f+".png"):
					template_list.append({'name':f,'image':f+".png"})
				else:
					template_list.append({'name':f,'image':""})

                web.render('/make_composition.html')
	
	## Post method. Create the ISO image file. 
	#
        def POST(self):
                cookie = web.cookies()
                user_path = get_all_user_path(cookie.nick)
                image =  winsollib.Image([MASTER_CATEGORIES_XML, MASTER_APPS_XML, user_path['categories_xml_file'], user_path['apps_xml_file'], user_path['includes_xml_file']], dtd_files)
                iso_options = web.input()
                
		# Download to system directories		
                image.download_software( SOFTWARE_DIR )
		image.download_icons( ICONS_DIR )
		image.download_manuals( MANUALS_DIR )
             	
		# Make Mrproper to users image directory
		mrproper_image(cookie.nick)
		
		# Make html
                image.gen_html(user_path['html_dir'], TEMPLATES_DIR + "/" + iso_options.template )

                # Make symbolic links
		for category in image.get_all_categories():
			if category.is_included():
				if not os.path.exists( user_path['icons_dir'] + "/" + category.get_icon()):
					if  os.path.exists(ICONS_DIR + "/" + category.get_icon()):
						os.symlink(ICONS_DIR + "/" + category.get_icon(), user_path['icons_dir'] + "/" + category.get_icon())

				for app in category.get_all_apps():
					if app.is_included():
						if not os.path.exists( user_path['software_dir'] + "/" + app.get_file_name() ):
							if os.path.exists( SOFTWARE_DIR + "/" + app.get_file_name() ):
								os.symlink( SOFTWARE_DIR + "/" + app.get_file_name(),user_path['software_dir'] + "/" + app.get_file_name() )
						if not os.path.exists( user_path['icons_dir'] + "/" + app.get_icon_name() ):
							if  os.path.exists( ICONS_DIR + "/" + app.get_icon_name() ):
								os.symlink( ICONS_DIR + "/" + app.get_icon_name(), user_path['icons_dir'] + "/" + app.get_icon_name() )
						for manual in app.get_manuals()['app_man_offline']:
							if not os.path.exists( user_path['manuals_dir'] + "/" + manual['app_man_off_file'] ):
								if os.path.exists( MANUALS_DIR + "/" + manual['app_man_off_file'] ):
									os.symlink( MANUALS_DIR + "/" + manual['app_man_off_file'], user_path['manuals_dir'] + "/" + manual['app_man_off_file'] )
		if not os.path.exists( user_path['image_dir'] + "/autorun.inf" ): os.symlink( MASTER_DIR + "/cd-base/autorun.inf", user_path['image_dir'] + "/autorun.inf" )
		if not os.path.exists( user_path['image_dir'] + "/browsercall.exe" ): os.symlink( MASTER_DIR + "/cd-base/browsercall.exe", user_path['image_dir'] + "/browsercall.exe" )
		if not os.path.exists( user_path['image_dir'] + "/logo.ico" ):os.symlink( MASTER_DIR + "/cd-base/logo.ico", user_path['image_dir'] + "/logo.ico" )
                
		# Make composition
                composition_file = ""
		if iso_options.composition == "zip":
			composition_file = "/WinSOL-image_" + cookie.nick + ".zip"
			image.make_zip( user_path['image_dir'], user_path['user_home'] + composition_file)
		else:
			composition_file = "/WinSOL-image_" + cookie.nick + ".iso"
                	image.make_iso( user_path['image_dir'], user_path['user_home'] + composition_file)
                
		# Send the mail
		users = list(web.select(DB_TABLE_USER, where="nick=\'" + cookie.nick + "\'"))
		if len(users) > 0:	
			user = {'name':users[0].name,
				'surname':users[0].surname,
				'nik':cookie.nick,
				'mail':users[0].mail,
				'image_url':HOST + "/users/" + cookie.nick + composition_file}
			
			try:
				send_mail(MAIL_COMPOSITION_SUBJECT, user, "composition_text_mail.txt", "composition_html_mail.txt")
			except Exception:
				menu_categories = image.get_all_categories_dict()
				size = float(image.calculate_size()) / 1000
				errors = []
				errors.append("Error, no se ha podido enviar el E-mail.")
				errors.append("Compruebe que la dirección de su E-mail es correcta en \"Cuenta de Usuario\".")
				template_list = []
				for f in os.listdir(TEMPLATES_DIR):
					if os.path.isdir(os.path.join(TEMPLATES_DIR, f)) and not f.startswith("."):
						if os.path.exists(MASTER_DIR+"/web/static/images/templates/"+f+".png"):
							template_list.append({'name':f,'image':f+".png"})
						else:
							template_list.append({'name':f,'image':""})
				web.render('/make_composition.html')
			else:
				# Generate the application stadistic
				make_applications_stadistic(image)
				# Show the index page.
				menu_categories = image.get_all_categories_dict()
				size = float(image.calculate_size()) / 1000
				messages = ["La composición se creó correctamente", "Se le ha enviado un e-mail a la dirección que nos envió explicando el metodo para obtener su archivo " + iso_options.composition + "."]
				errors = []
				web.render ('index.html')
		else:
			menu_categories = image.get_all_categories_dict()
			size = float(image.calculate_size()) / 1000
			messages = []
			errors = ["Error, no se ha podido enviaar el e-mail"]
			web.render ('index.html')

## Class for View a list of precompile compositions.
#
# @author David Barragán Merino <bameda [AT] di.uc3m [DOT] com>
# @author CRISOL-UC3M <htp://crisol.uc3m.es>
class precompile_composition:

        ## Get method. Show the help page.
	#
	def GET(self):
		cookie = web.cookies()
		user_path = get_all_user_path(cookie.nick)
		image =  winsollib.Image([MASTER_CATEGORIES_XML, MASTER_APPS_XML, user_path['categories_xml_file'], user_path['apps_xml_file'], user_path['includes_xml_file']], dtd_files)
		menu_categories = image.get_all_categories_dict()
		size = float(image.calculate_size()) / 1000
		web.render ('precompile_composition.html')


# View static files (png, jpg, gif, pdf, css,... this files are in ./static/)		

## Class to view static files (png, jpg, gif, pdf, css,... this files are in ./static/)
#
# @author David Barragán Merino <bameda [AT] di.uc3m [DOT] com>
# @author CRISOL-UC3M <htp://crisol.uc3m.es>
class view_static_files:

	## Get method. Load any file (phg, jpg, css,...).
	#
	# @param localpath - The path file.
    	def GET(self, localpath):
        	if '..' in localpath:
        		return web.badrequest()
       		if '/' in localpath or (not localpath in os.listdir('static')):
       			return web.notfound()
        	rpath = os.path.join('static', localpath)
        	st = os.stat(rpath)
        	if (stat.S_ISREG(st.st_mode)):
        		web.header('Content-Type', get_file_type(localpath))
        		web.header('Content-Length', str(st.st_size))
        		web.ctx.output = open(rpath, 'rb') 
	
# View CSS Styles.

## Class to css color style.
#
# @author David Barragán Merino <bameda [AT] di.uc3m [DOT] com>
# @author CRISOL-UC3M <htp://crisol.uc3m.es>
class style_color:

	## Get method
	def GET(self):
		web.header("Content-Type","text/css; charset=utf-8")
                print open('templates/color.css').read()

## Class to css layout style.
#
# @author David Barragán Merino <bameda [AT] di.uc3m [DOT] com>
# @author CRISOL-UC3M <htp://crisol.uc3m.es>
class style_layout:
	
	## Get Method.
	def GET(self):
		web.header("Content-Type","text/css; charset=utf-8")
		print open('templates/layout.css').read()

## Debuger variable to web.py.
#web.internalerror = web.debugerror
## Run FastCGI insted WCGI
#
#Don't tested yet.
#web.runwsgi = web.runfcgi

# Main 
if __name__ == "__main__":
	web.db_parameters = dict(dbn=DB_GS, user=DB_USER, pw=DB_PASSWORD, db=DB_NAME)
	web.run(urls, web.reloader) 
