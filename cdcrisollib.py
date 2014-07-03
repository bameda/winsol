#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

# CD-Crisol v. 0.1 (https://forja.rediris.es/projects/cd-crisol)
# Devel by: David Barragán Merino (d.barragan.alumnos.uc3m.es)
# CRISOL-UC3M (http://crisol.uc3m.es)

import os
import sys
import urllib
import md5
# XML
from elementtree.ElementTree import ElementTree, Element, SubElement, parse
from xml.parsers.xmlproc import xmlproc
from xml.parsers.xmlproc import xmlval
from xml.parsers.xmlproc import xmldtd
# HTML Template
from Cheetah.Template import Template 

class Category:
	"Clase que representa una categoria, la cual posee una serie de aplicaciones asignadas."
    
    	def __init__(self,values):
	        self.__name = values[0]
	        self.__included = 0
	        self.__label = values[1]
	        self.__apps = []
		self.__to_save = 0
	        self.__html_file = self.__label + ".html"
   
	def __cmp__(self,other):
		if other == None:
			return 1
        	if self.__name > other.get_name():
            		return 1
       		elif self.__name == other.get_name():
            		return 0
        	else:
            		return -1
            
    	def select_category(self):
        	self.__included = 1
    
    	def unselect_category(self):
        	self.__included = 0
    
    	def select_application(self,name):
        	for app in self.__apps:
            		if name == app.get_name():
                		app.select_app()
                		return 1
        	return 0

    	def unselect_application(self,name):
        	for app in self.__apps:
            		if name == app.get_name():
                		app.unselect_app()
            			return 1
        	return 0

    	def download_software(self,software_dir):
        	for app in self.__apps:
            		if app.is_included():
                		app.download_software(software_dir)
	
	def download_icons(self,icon_dir):
        	for app in self.__apps:
            		if app.is_included():
                		app.download_icon(icon_dir)
    	
    	def del_application(self,app_name):
        	result_list = []
        	delete  =  0
        	for app in self.__apps:
            		if app.get_name() != app_name:
                		result_list.append(app)
            		else:
				app.del_category(self.__label)
                		delete = 1
                self.__apps = result_list
		self.__apps.sort()
        	return delete
        
	def add_application(self,app):
        	self.__apps.append(app)
		self.__apps.sort()
          
    	def get_all_apps(self):
        	return self.__apps

    	def get_label(self):
        	return self.__label

    	def get_name(self):
        	return self.__name

	def get_html_file(self):
		return self.__html_file

    	def find_app(self, app_name):
		return App.find_app(self.__apps, app_name )

    	def get_category_dict(self):
		apps = []
        	for app in self.__apps:
			apps.append( app.get_app_dict() )
		return {'name':self.__name,
        		'included':self.__included,
        		'label':self.__label,
			'html_file':self.__html_file,
			'apps':apps}
    
    	def is_included(self):
        	return self.__included
	
	def is_to_save(self):
		return self.__to_save
	
    	def gen_xml_element(self):
        	category= Element("CATEGORY")
        	name = SubElement(category,"CAT_NAME")
        	name.text = self.__name
        	label = SubElement(category,"CAT_LABEL")
        	label.text = self.__label
        	return category

	def set_name(self, category_name):
		self.__name = category_name

	def set_label(self, category_label):
		self.__label = category_label
		self.__html_file = self.__label + ".html"

	def set_to_save(self, category_to_save):
		self.__to_save = category_to_save
   		
	def find_category(self, cat_list, cat_label):
		""" TODO: Optimize this method"""
		cat_list.sort()
		for cat in cat_list:
			if cat.get_label() == cat_label:
				return cat
		return None
	find_category = classmethod( find_category )

class App:
    	"Clase que representa una aplicación."
  
    	def __init__(self,values):
        	self.__name = values[0]
        	self.__version = values[1]
        	self.__site = values[2]
        	self.__manual = values[3]
        	self.__description = values[4]
        	self.__file = values[5]
        	self.__software_url = values[6]
        	self.__icon = values[7]
        	self.__icon_url = values[8]
        	self.__md5sum = values[9]
        	self.__categories = values[10]
		self.__alternatives = values[11]
        	self.__included = 0
        	self.__to_save = 0
		self.__html_file = self.__name + ".html"

    	def __cmp__(self,other):
		if other == None:
			return 1
        	if self.__name > other.get_name():
            		return 1
        	elif self.__name == other.get_name():
            		return 0
        	else:
            		return -1
    
    	def select_app(self):
        	self.__included = 1

    	def unselect_app(self):
        	self.__included = 0
                
    	def is_included(self):
        	return self.__included
   	
	def is_to_save(self):
		return self.__to_save  
	 
    	def download_icon(self,icon_dir):
        	if not os.path.exists(icon_dir+"/"+self.__icon):
            		if self.__icon_url != None:
                		sys.stdout.write("Getting " + self.__icon + "...")
                		if urllib.urlretrieve(self.__icon_url, icon_dir + "/" + self.__icon):
                    			print "Done\n"

    	def download_software(self,software_dir):
        	if not os.path.exists(software_dir+"/"+self.__file):
            		sys.stdout.write("Getting " + self.__file + "...")
            		if urllib.urlretrieve(self.__software_url, software_dir + "/" + self.__file):
                		print "Done\n"
                		self.__md5sum = self.__get_md5_hash(software_dir + "/" + self.__file)
            		while self.__get_md5_hash(software_dir + "/" + self.__file) != self.__md5sum:
                		print "The md5 isn't equals.\n"
                		sys.stdout.write("Getting " + self.__file + "...")
                		os.remove(software_dir+"/"+self.__file)
                		if urllib.urlretrieve(self.__software_url, software_dir + "/" + self.__file):
					print "Done\n"
                    			self.__md5sum = self.__get_md5_hash(software_dir + "/" + self.__file)
    
    	def __get_md5_hash(self,filename):
        	""" Return md5 hash """
        	f = open(filename,'rb')
        	hsh = md5.new()
        	hsh.update(f.read())
        	f.close()
        	return hsh.hexdigest()

    	def get_app_dict(self):
        	return {'name':self.__name,
        	'version':self.__version,
        	'site':self.__site,
        	'manual':self.__manual,
        	'description':self.__description.encode("iso-8859-1"),
        	'file':self.__file,
        	'software_url':self.__software_url,
        	'icon':self.__icon,
        	'icon_url':self.__icon_url,
        	'md5sum':self.__md5sum,
		'included':self.__included,
		'html_file':self.__html_file,
        	'categories':self.__categories,
        	'alternatives':self.__alternatives}

    	def gen_html(self):
        	print "Funcion no implementada"

    	def gen_xml_element(self):
        	app = Element("APP")
        	name = SubElement(app,"APP_NAME")
        	name.text = self.__name
        	version = SubElement(app,"APP_VERSION")
        	version.text = self.__version
        	site = SubElement(app,"APP_SITE")
        	site.text = self.__site
        	manual = SubElement(app,"APP_MANUAL")
        	manual.text = self.__manual
        	description = SubElement(app,"APP_DESCRIPTION")
        	description.text = self.__description
        	file = SubElement(app,"APP_FILE")
        	file.text = self.__file
        	download_url = SubElement(app,"APP_DOWNLOAD_URL")
        	download_url.text = self.__software_url
        	icon = SubElement(app,"APP_ICON")
        	icon.text = self.__icon
        	icon_url = SubElement(app,"APP_ICON_URL")
        	icon_url.text = self.__icon_url
        	md5sum = SubElement(app,"APP_MD5SUM")
        	md5sum.text = self.__md5sum
        	categories = SubElement(app,"APP_CATEGORIES")
        	cats = []
        	for category in self.__categories:
            		cats.append(SubElement(categories,"APP_CATEGORY"))
            		cats[-1].text = category
        	alternatives = SubElement(app,"APP_ALTERNATIVES")
        	alts = []
        	for alternative in self.__alternatives:
            		alts.append(SubElement(alternatives,"APP_ALT"))
            		alts[-1].text = alternative
        	return app
    
	def get_name(self):
	        return self.__name
	
	def get_html_file(self):
		return self.__html_file

	def get_version(self):
		return self.__version	
    
	def get_site(self):
	        return self.__site
    
	def get_manual(self):
	        return self.__manuel
    
	def get_description(self):
	        return self.__description
    
	def get_file_name(self):
		return self.__file
    
	def get_software_url(self):
	        return self.__software_url
    
	def get_icon_name(self):
	        return self.__icon
    
	def get_icon_url(self):
	        return self.__icon_url

	def get_md5sum(self):
	        return self.__md5sum
	
	def get_categories(self):
	    	return self.__categories
    
	def get_alternatives(self):
	        return self.__alternatives
        
	def set_name(self, name):
	        self.__name = name
		self.__html_file = self.__name + ".html"
    
	def set_version(self, version):
		self.__version = version

	def set_site(self, size):
	        self.__size = size
    
	def set_manual(self, manual):
	        self.__manuel = manual
    
	def set_description(self, description):
	        self.__description = description
	    
	def set_file_name(self, file):
	        self.__file = file
    
	def set_software_url(self, surl):
	        self.__software_url = surl
    
	def set_icon_name(self, icon):
	        self.__icon = icon
    
	def set_icon_url(self, icon_url):
	        self.__icon_url = icon_url
	    
	def set_md5sum(self, md5):
	        self.__md5sum = md5
	
	def set_categories(self, categories):
	    	self.__categories = categories
    
	def del_category(self, category_label):
		try:
			self.__categories.remove(category_label)
			return 1
		except Exception:
			return 0
	
	def change_category(self, old_category, new_category):
		try:
			n = self.__categories.index(old_category)
			self.__categories[n] = new_category
			return 1
		except Exception:
			return 0 

	def set_alternatives(self, alternatives):
	        self.__alternatives = alternatives
	   
	def set_to_save(self, app_to_save):
		self.__to_save = app_to_save

	def find_app( self, app_list, app_name):
		""" TODO: Optimize this method"""
		app_list.sort()
		for app in app_list:
			if app.get_name() == app_name:
				return app
		return None
	
	find_app = classmethod( find_app )	

class Image:

    	def __init__(self, xml_files, dtd_files):
    		self.__categories = []
   		self.__apps = []
		self.__sys_category_file = CategoriesDataFile( xml_files[0], dtd_files[0]  )
		self.__sys_app_file  = AppsDataFile( xml_files[1], dtd_files[1] )
 		self.__user_category_file = CategoriesDataFile( xml_files[2], dtd_files[0] )
		self.__user_app_file = AppsDataFile( xml_files[3], dtd_files[1] )
		self.__user_include_file = IncludesDataFile( xml_files[4], dtd_files[2] )
   	
		# Verify the XML file
		
		do = 1

		if( not self.__sys_category_file.check_XML_file() ): 
			do = 0
		if( not self.__sys_app_file.check_XML_file() ): 
			do = 0
		if( not self.__user_category_file.check_XML_file() ): 
			do = 0
		if( not self.__user_app_file.check_XML_file() ): 
			do = 0
		if( not self.__user_include_file.check_XML_file() ): 
			do = 0 
		
		# get applications and categories
		
		if do == 1:
			self.__sys_app_file.get_Apps(self.__apps)
			self.__user_app_file.get_Apps(self.__apps, 1)
			self.__apps.sort()
			self.__sys_category_file.get_Categories(self.__categories)
			self.__user_category_file.get_Categories(self.__categories, 1)
			self.__categories.sort()
			self.__insert_apps_into_category()
			self.__user_include_file.set_includes(self.__categories, self.__apps)

	def __insert_apps_into_category(self):
		for app in self.__apps:
			# Add apps without category
			if len(app.get_categories()) == 0:
				cat = Category.find_category(self.__categories, "none")
                                if cat != None:
                                        cat.add_application(app)
				else:
					cat = Category(["Sin Categoria", "none"])
					self.__categories.append(cat)
					cat.add_application(app)
			# Add apps with category
			else:
				for cat_label in app.get_categories():
					cat = Category.find_category(self.__categories, cat_label)
					if cat != None:
						cat.add_application(app)
					
			
	def add_category(self, category_values):
		cat = Category(category_values)
		if Category.find_category(self.__categories, cat.get_label()) == None:
			self.__categories.append(cat)
			self.__categories.sort()
			cat.set_to_save(1)
			return 1
		# There is one category with the same label"	
		return 0

	def modify_category_values(self, category_label, category_value):
		cat = Category.find_category(self.__categories, category_label)
		if cat == None:
			return 0
		else:	
                       	cat.set_name(category_value[0])
			cat.set_to_save(1)
			return 1
	
	def del_category(self, category_label):
        	c = Category.find_category(self.__categories, category_label)
		if c != None:
			if not c.is_to_save():
				# The category is from the system XML file
				return 0 
		else:
			# there isn't any category with this label
			return 0
 
		result_list = []
        	delete  =  0
        	for cat in self.__categories:
            		if cat.get_label() != category_label:
                		result_list.append(cat)
            		else:
                		delete = 1
				# Delete to app.categories
				if cat.is_to_save():
					for app in cat.get_all_apps():
						if app.is_to_save(): 
							# this "if" sentence isn't necesary
							app.del_category(category_label)
							app.set_to_save( 1 )
                self.__categories = result_list
		self.__categories.sort()
        	return delete

	def add_app(self, app_values):
		app = App(app_values)
		if App.find_app(self.__apps, app.get_name()) == None:
			self.__apps.append(app)
                	self.__apps.sort()
			app.set_to_save( 1 )
			if len(app.get_categories()) == 0:
				# The app isn't from any category
				cat = Category.find_category(self.__categories, "none")
                                if cat != None:
                                        cat.add_application(app)
				else:
					cat = Category(["Sin Categoria", "none"])
					self.__categories.append(cat)
					cat.add_application(app)
			else:
				# The app is from any category
				for cat_label in app.get_categories():
					cat = Category.find_category(self.__categories, cat_label)
					if cat != None:
						cat.add_application(app)
			return 1
		# There is a App with the same name"
		return 0
		
	def modify_app_values(self, app_name, app_values):	
		app = App.find_app(self.__apps, app_name)
		if app == None:
			return 0
		else:
			app.set_version(app_values[0])
			app.set_site(app_values[1])
			app.set_manual(app_values[2])
			app.set_description(app_values[3])
			app.set_file_name(app_values[4])
			app.set_software_url(app_values[5])
			app.set_icon_name(app_values[6])
			app.set_icon_url(app_values[7])
			app.set_md5sum(app_values[8])

			oldcats = app.get_categories()
			if len(oldcats) == 0:
				cat = Category.find_category(self.__categories, "none")
				cat.del_application(app.get_name())
			else:
				for cat_label in oldcats:
					cat = Category.find_category(self.__categories, cat_label)
					if cat != None:
						cat.del_application(app.get_name())
			
			newcats = app_values[9]	
			if len(newcats) == 0:
				cat = Category.find_category(self.__categories, "none")
				if cat != None:
					cat.add_application(app.get_name())
				else:
					cat = Category(["Sin Categoria", "none"])
					self.__categories.append(cat)
					cat.add_application(app)
			else:
				for cat_label in newcats:
					cat = Category.find_category(self.__categories, cat_label)
					if cat != None:
						cat.add_application(app.get_name())

			app.set_categories(newcats)
			app.set_alternatives(app_values[10])
			app.set_to_save(1)
			return 1

	def del_app(self, app_name):
		result_list = []
		delete = 0
		for app in self.__apps:
			if app.get_name != app_name:
				result_list.append(app)
			else:
				# The App is delete"
				delete = 1
				if len(app.get_categories()) == 0:
					cat = Category.find_category(self.__categories, "none")
					if cat != None:
						cat.del_application(app_name)
				else:
					for cat_label in app.get_categories():
                                        	cat = Category.find_category(self.__categories, cat_label)
                                		if cat != None:
							cat.del_application(app_name)
		self.__apps = result_list
		self.__apps.sort()
		return delete
					
	def select_category(self, category_label):
		cat = Category.find_category(self.__categories, category_label)
                if cat != None:
                       	cat.select_category()
			return 1
		return 0

	def unselect_category(self, category_label):
		cat = Category.find_category(self.__categories, category_label)
                if cat != None:
                       	cat.unselect_category()
			return 1
		return 0
		
	def select_all_categories(self):
		for cat in self.__categories:
			cat.select_category()
		return 1	

	def unselect_all_categories(self):
		for cat in self.__categories:
			cat.unselect_category()
		return 1	
	
	def select_app(self, app_name):
		app = App.find_app(self.__apps, app_name)
		if app != None:
                        app.select_app()
			return 1
		return 0

	def select_app_by_category(self, category_label):
		cat = Category.find_category(self.__categories, category_label)
                if cat != None:
			for app in cat.get_all_apps():
                		app.select_app()
			return 1
		return 0

	def select_all_apps(self):		
		for app in self.__apps:
			app.select_app()			
		return 1

	def unselct_app(self, app_name):
		app = App.find_app(self.__apps, app_name)
                if app != None:
                        app.unselect_app()
                        return 1
                return 0

        def unselect_app_by_category(self, category_label):
                cat = Category.find_category(self.__categories, category_label)
                if cat != None:
                        for app in cat.get_all_apps():
                                app.unselect_app()
                        return 1
                return 0

        def unselect_all_apps(self):
		for app in self.__apps:
			app.unselect_app()
		return 1

	def download_software(self, soft_dir):
		for cat in self.__categories:
			cat.download_software(soft_dir)

	def download_icons(self, icon_dir):
		for cat in self.__categories:
			cat.download_icons(icon_dir)		
	
	def gen_html(self, html_dir, template_dir):
		if not os.path.exists(html_dir): return 0
		if not os.path.exists(template_dir + "/category.tmpl"): return 0
		if not os.path.exists(template_dir + "/application.tmpl"): return 0
		if not os.path.exists(template_dir + "/index.tmpl"): return 0
		
		if not os.path.exists(html_dir +"/apps"): 
			os.mkdir(html_dir +"/apps")
		if not os.path.exists(html_dir +"/categories"): 
			os.mkdir(html_dir +"/categories")

		categories = []
		for cat in self.__categories:
			if cat.is_included():
				categories.append(cat.get_category_dict())
		
		index = Template( file = template_dir + "/index.tmpl",  searchList = [ {'categories' : categories} ] )	
		
		f = open( html_dir + "/index.html", 'w')
		f.write( repr(index) )
		f.close()
		
		for cat in categories:
			category = Template( file = template_dir + "/category.tmpl",  searchList = [ {'category' : cat} ] )

			f = open( html_dir + "/categories/" + cat['html_file'], 'w')
			f.write( repr(category) )
			f.close()

			for app in cat['apps']:
				if app['included']:
					if not os.path.exists(html_dir +"/apps/" + app['html_file']):
						application = Template( file = template_dir + "/application.tmpl",  searchList = [ {'application' : app} ] )
						
						f = open( html_dir + "/apps/" + app['html_file'], 'w')
						f.write( repr(application) )
						f.close()
	
		return 1
		
	
	def make_iso(self, image_dir, iso_file):
		if not os.path.exists(image_dir): 
			return 0
		else:
			os.system( "mkisofs -J -R -f -o '" + iso_file + "' '" + image_dir + "'" )
			return 1
	
	def get_all_categories(self):
		return self.__categories

	def get_all_categories_name(self):
		result = []
		for cat in self.__categories:
			result.append( cat.get_name() )
		return result 

	def get_all_categories_dict(self):
		result = []
		for cat in self.__categories:
			result.append( cat.get_dict() )
		return result 

	def get_all_categories_label(self):
		result = []
		for cat in self.__categories:
			result.append( cat.get_label() )
		return result 

	def get_category_by_label(self, category_label):
		return Category.find_category(self.__categories, category_label)

	def get_category_dict_by_label(self, category_label):
		cat = Category.find_category(self.__categories, category_label)
		if cat == None:
			return None
		else:
			return cat.get_category_dict()

	def get_all_apps(self):
		return self.__apps

	def get_all_apps_name(self):
		result = []
		for app in self.__apps:
			result.append( app.get_name() )
		return result

	def get_all_apps_dict(self):
		result = []
		for app in self.__apps:
			result.append( app.get_dict() )
		return result

	def get_apps_by_category(self, category_label):
		cat = Category.find_category(self.__categories, category_label)
		if cat == None: 
			return [] 
		else:
			return cat.get_all_apps()		

	def get_appss_name_by_category(self, category_label):
		result = []
		for app in Category.find_category(self.__categories, category_label).get_applications():
			result.append( app.get_name() )
		return result

	def get_apps_dict_by_category(slef, category_label):
		result = []
		for app in Category.find_category(self.__categories, category_label).get_applications():
			result.append( app.get_dict() )
		return result

	def get_app_by_name(self, app_name):
		return App.find_app(self.__apps, app_name)

	def get_app_dict_by_name(self, app_name):
		app =  App.find_app(self.__apps, app_name)
		if (app == None):
			return None
		else:
			return app.get_app_dict()

	def save_categories_to_xml_file(self):
		self.__user_category_file.write_to_XML_file( self.__categories )

	def save_applications_to_xml_file(self):
		self.__user_app_file.write_to_XML_file( self.__apps )

	def save_includes_to_xml_file(self):
		self.__user_include_file.write_to_XML_file( self.__categories, self.__apps )
	


class DataFile:
	
	def __init__(self, xml_file, dtd_file ):
		self.__xml_file = xml_file
		self.__dtd_file = dtd_file
		self.__check = 0
	
	def check_XML_file(self):
    		dtd = xmldtd.load_dtd( self.__dtd_file)
    		parser = xmlproc.XMLProcessor()
    		parser.set_application(xmlval.ValidatingApp(dtd, parser))
    		parser.dtd = dtd
    		parser.ent = dtd
    		try:
			parser.parse_resource(self.__xml_file)
			self.__check = 1
			self.__tree = parse( self.__xml_file )
		except Exception, e:
			print "EE Error in XML-File \"" + self.__xml_file + "\" validation"
			self.__check = 0
		return self.__check

	def is_cheked(self):
		return self.__check

	def write_apps_to_XML_file(self, app_list):
		""" Implement to AppsDataFile child"""	
		root = Element("APPLICATIONS")
                for app in app_list:
                        if app.is_to_save():
                                root.append(app.gen_xml_element())
                self.__tree = ElementTree(root)
                self.__tree.write(self.__xml_file)
	

	def write_categories_to_XML_file(self, category_list):
		""" Implement to CategoriesDataFile child """
		root = Element("CATEGORIES")
                for category in category_list:
			if category.is_to_save():
                        	root.append(category.gen_xml_element())
                self.__tree = ElementTree(root)
                self.__tree.write(self.__xml_file)


	def write_includes_to_XML_file(self, category_list, app_list):
		""" Implement to IncludesDataFile child """
		root = Element("INCLUDES")
		categories = SubElement(root,"CATEGORIES")
		for cat in category_list:
			if cat.is_included():
				label = SubElement(categories,"CAT_LABEL")
                		label.text = cat.get_label()
		applications = SubElement(root,"APPLICATIONS")
		for app in app_list:	
			if app.is_included():
				name = SubElement(applications,"APP_NAME")
				name.text = app.get_name()
		self.__tree = ElementTree(root)
		self.__tree.write(self.__xml_file)
	

	def get_XML_file(self):
		return self.__xml_file

	def get_DTD_file(self):
		return self.__dtd_file

	def get_tree(self):
		return self.__tree
	
	def set_XML_file(self, xml_file):
		self.__xml_file = xml_file
		self.__check = 0

	def set_DTD_file(self, dtd_file):
		self.__dtd_file = dtd_file
		self.__check = 0
		
class AppsDataFile(DataFile):
	
	def __init__(self, xml_file, dtd_file ):
        	DataFile.__init__(self, xml_file, dtd_file)

	def get_Apps(self, app_list, save = 0):
		if( DataFile.is_cheked(self) == 0):
			print "EE The XML-File \"" + DataFile.get_XML_file(self) + "\" is not cheked"
			return 0 
		else:
                	for application in DataFile.get_tree(self).findall("/./APP"):
                        	name = application.findall("./APP_NAME")[0].text
				version = application.findall("./APP_VERSION")[0].text
                        	site = application.findall("./APP_SITE")[0].text
                        	manual = application.findall("./APP_MANUAL")[0].text
                        	description = application.findall("./APP_DESCRIPTION")[0].text
                        	file = application.findall("./APP_FILE")[0].text
                        	download_url = application.findall("./APP_DOWNLOAD_URL")[0].text
                        	icon = application.findall("./APP_ICON")[0].text
                        	icon_url = application.findall("./APP_ICON_URL")[0].text
                        	md5sum = application.findall("./APP_MD5SUM")[0].text
                        	categories =[]
                        	for app_category in application.findall("./APP_CATEGORIES/APP_CATEGORY"):
                                	categories.append(app_category.text)
                        	alternatives = []
                        	for app_alternative in application.findall("./APP_ALTERNATIVES/APP_ALT"):
                                	alternatives.append(app_alternative.text)
				
				applicat = App.find_app(app_list, name)
				if applicat == None:
					app = App( [name, version, site, manual, description, file, download_url, icon, icon_url, md5sum, categories, alternatives] )
					app.set_to_save(save)
					app_list.append(app)
				else:
					applicat.set_version( version )
					applicat.set_site( site )
					applicat.set_manual( manual )
					applicat.set_description( description )
					applicat.set_file_name( file )
					applicat.set_software_url( download_url )
					applicat.set_icon_name( icon )
					applicat.set_icon_url( icon_url )
					applicat.set_md5sum( md5sum )
					applicat.set_categories( categories )
					applicat.set_alternatives( alternatives )
					applicat.set_to_save( 1 )
                	app_list.sort()
                	return 1
	
	def write_to_XML_file(self, app_list ):
		return DataFile.write_apps_to_XML_file( self, app_list )

class CategoriesDataFile(DataFile):

	def __init__(self, xml_file, dtd_file ):
		DataFile.__init__(self, xml_file, dtd_file)

	def get_Categories(self, category_list, save =  0):
		if( DataFile.is_cheked(self) == 0):
			print "EE The XML-File \"" + DataFile.get_XML_file(self) + "\" is not cheked"
			return 0
		else:
			for category in DataFile.get_tree(self).findall("/./CATEGORY"):
				name = category.findall("./CAT_NAME")[0].text
				label = category.findall("./CAT_LABEL")[0].text
				
				categ =  Category.find_category(category_list, label)	
				if categ == None:
					cat = Category( [name, label] )
					cat.set_to_save(save)
					category_list.append(cat)
				else:
					categ.set_name(name)
					categ.set_to_save(save)
                	return 1

	def write_to_XML_file(self, category_list ):
		return DataFile.write_categories_to_XML_file( self, category_list )

class IncludesDataFile(DataFile):

        def __init__(self, xml_file, dtd_file ):
                DataFile.__init__(self, xml_file, dtd_file)

	def set_includes(self, category_list, app_list):	
		if( DataFile.is_cheked(self) == 0):
			print "EE The XML-File \"" + DataFile.get_XML_file(self) + "\" is not cheked"
			return 0
		else:
			for cat_label in DataFile.get_tree(self).findall("/./CATEGORIES/CAT_LABEL"):
				cat = Category.find_category(category_list, cat_label.text)
				if cat != None:
					cat.select_category()
			for  app_name in DataFile.get_tree(self).findall("/./APPLICATIONS/APP_NAME"):
				app = App.find_app(app_list, app_name.text)
				if app != None:
					app.select_app()
			return 1
	

	def write_to_XML_file(self, category_list, app_list ):
		return DataFile.write_includes_to_XML_file( self, category_list, app_list )

if __name__=='__main__':
        pass
	