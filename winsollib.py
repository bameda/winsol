#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# WinSOL (https://forja.rediris.es/projects/cd-crisol)
# Copyright (C) 2006-2007 by David Barragán Merino <bameda@di.uc3m.es>
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


import os
import sys
import urllib
import md5
# XML
from elementtree.ElementTree import ElementTree, Element, SubElement, parse
from xml.parsers.xmlproc import xmlproc, xmlval, xmldtd
# HTML Template
from Cheetah.Template import Template 

# The WinSol library.

## Class representing a Category, that owns a set of assigned App Objects.
#
# @author David Barragán Merino <bameda [AT] di.uc3m [DOT] com>
# @author CRISOL-UC3M <htp://crisol.uc3m.es>
class Category:
   
	## Inicialize the Category values. Be carefull with string encoding.
	#
	# @param  values - (list[5]) The Category values.
	def __init__(self,values):
		if values[0] is not None:
			if isinstance(values[0], unicode): self.__name =  values[0].encode('utf8')
			else:self.__name =  values[0]		
		else: self.__name = ""
		
		self.__included = 0
		
		if values[1] is not None: 
			if isinstance(values[1], unicode): self.__label = values[1].encode('utf8')
			else: self.__label = values[1]
		else: self.__label = ""

		if values[2] is not None: 
			if isinstance(values[2], unicode): self.__description = values[2].encode('utf8')
			else: self.__description = values[2]
		else: self.__description = ""
		
		if values[3] is not None:
                        if isinstance(values[3], unicode): self.__icon = values[3].encode('utf8')
                        else: self.__icon = values[3]
                else: self.__icon = ""

		if values[4] is not None:
                        if isinstance(values[4], unicode): self.__icon_url = values[4].encode('utf8')
                        else: self.__icon_url = values[4]
                else: self.__icon_url = ""

		self.__apps = []
		
		self.__to_save = 0
	        
		self.__html_file = self.__label + ".html"
  
  	## Compare this Categpry to other.
	#
	# @param other - (Category |  None) Object to compare with this.
	# @return \b -1 If this < other. \b 0 If this = other. \b 1 If this > other on other = None
	def __cmp__(self, other):
		if other == None:
			return 1
        	if self.__name.lower() > other.get_name().lower():
            		return 1
       		elif self.__name.lower() == other.get_name().lower():
            		return 0
        	else:
            		return -1
        
	## Select this Category.
	#
    	def select_category(self):
        	self.__included = 1
    
    	## Unselect this Category.
	#
    	def unselect_category(self):
        	self.__included = 0
   
	## Select the App in this Category with the name is the same as \em name.
	#
	# @param name - App name
	# @return \b 1 If it's selected. \b 0 If not.
    	def select_application(self, name):
        	for app in self.__apps:
            		if name.lower() == app.get_name().lower():
                		app.select_app()
                		return 1
        	return 0

	## Unselect the App in this Category with the name is the same as \em name.
	#
	# @param name - App name.
	# @return \b 1 If it's unselected. \b 0 If not.
    	def unselect_application(self, name):
        	for app in self.__apps:
            		if name.lower() == app.get_name().lower():
                		app.unselect_app()
            			return 1
        	return 0

        ## Download the Category's icon.
        #
        # If it can't download it. The \em icon_url is going to be delete.
        # @param icon_dir - The icon directory path.
        def download_icon(self, icon_dir):
                try:
                        if not os.path.exists(icon_dir+"/"+self.__icon):
                                if self.__icon_url != None and self.__icon_url != "":
                                        sys.stderr.write("!! Getting " + self.__icon + "... ")
                                        if urllib.urlretrieve(self.__icon_url, icon_dir + "/" + self.__icon):
                                                sys.stderr.write("Done\n")
                except Exception, e:
                        sys.stderr.write("\nEE Error downloading category's icon from \"" + self.__name + "\".\n")
                        sys.stderr.write(str(e) + "\n")
                        self.__icon_url = ""
                        self.__to_save = 1
                        pass

	## Download all the software of selected App Objects in this Category.
	#
	# @param software_dir - Path to the software directory.
    	def download_software(self, software_dir):
        	for app in self.__apps:
            		if app.is_included():
                		app.download_software(software_dir)
	
	## Download all the icons of selected App Objects in this Category.
	#
	# @param icon_dir - Path to the icons directory.
	def download_apps_icons(self, icon_dir):
		for app in self.__apps:
            		if app.is_included():
                		app.download_icon(icon_dir)
    
    	## Download all the manuals of selected App Objects in this Category.
	#
	# @param manual_dir - Path to the manuals directory.
	def download_manuals(self, manual_dir):
		for app in self.__apps:
			if app.is_included():
				app.download_manuals(manual_dir)

	## Delete the App with \em app_name fron this Category.
	#
	# @param app_name - App name.
    	def del_application(self, app_name):
		result_list = []
        	delete  =  0
        	for app in self.__apps:
            		if app.get_name().lower() != app_name.lower():
                		result_list.append(app)
            		else:
				app.del_category(self.__label)
                		delete = 1
                self.__apps = result_list
		self.__apps.sort()
        	return delete
       
       	## Add a new App to this category.
	#
	# @param app - (App) App Object
	def add_application(self, app):
		self.__apps.append(app)	
        
	## Get all App Objects.
	#
    	def get_all_apps(self):
        	return self.__apps

	## Get the Category label.
	#
    	def get_label(self):
        	return self.__label
	
	## Get the Category name.
	#
    	def get_name(self): 
        	return self.__name
	
	## Get the Category html file name.
	#
	def get_html_file(self):
		return self.__html_file

	## Get the Category description.
	#
	def get_description(self): 
		return self.__description

	## Get the Category icon file name.
	#
	def get_icon(self):
		return self.__icon

        ## Get the Category icon file url.
	#
	def get_icon_url(self):
		return self.__icon_url

	## Find an App with 'app_name' and return it.
	#
	# @param app_name - App name.
	# @return an App Object or None if it isn't here.
    	def find_app(self, app_name):
		return App.find_app(self.__apps, app_name )
	
	## Return a Category dictionary with all App Objects dictionaries in it.
	#
	# @return The Category Dictionary.
    	def get_category_dict(self):
		apps = []
        	for app in self.__apps:
			apps.append( app.get_app_dict() )
		return {'name':self.__name,
        		'included':self.__included,
        		'label':self.__label,
			'description':self.__description,
			'icon':self.__icon,
			'icon_url':self.__icon_url,
			'html_file':self.__html_file,
			'apps':apps}

	## Return the \em included value.
	#
	# @return \b True/1 If it is include. \b False/0 If it isn't include.
    	def is_included(self):
        	return self.__included
	
	## Return the 'to_save' value.
	#
	# If this Category \em to_save value is \b True/1, it means that this Category has been modified or added by the user.
	# @return \b True/1 If it is a Category create/modified by the user. \b False/0 If it isn't.
	def is_to_save(self):
		return self.__to_save
	
	## Generate the Category XML element.
	#
	# @return Category XML \em Element.
    	def gen_xml_element(self):
        	category= Element("CATEGORY")
        	name = SubElement(category,"CAT_NAME")
		name.text = self.__name.decode('utf8')
        	label = SubElement(category,"CAT_LABEL")
        	label.text = self.__label.decode('utf8')
		description = SubElement(category,"CAT_DESCRIPTION")
		description.text = self.__description.decode('utf8')
		icon = SubElement(category,"CAT_ICON")
                icon.text = self.__icon.decode('utf8')
		icon_url = SubElement(category,"CAT_ICON_URL")
                icon_url.text = self.__icon_url.decode('utf8')
        	return category
	
	## Set the Category name.
	#
	# @param category_name - New Category name.
	def set_name(self, category_name):
		if category_name is not None: 
			if isinstance(category_name, unicode): self.__name = category_name.encode('utf8')
			else: self.__name = category_name
		else: self.__name = ""

	## Set the Category label.
	#
	# @param category_label - New Category label.
	def set_label(self, category_label):
		if category_label is not None: 
			if isinstance(category_label, unicode): self.__label = category_label.encode('utf8')
			else: self.__label = category_label
		self.__html_file = self.__label + ".html"
	
	## Set the Category description.
	#
	# @param category_description - New Category description.
	def set_description(self, category_description):
		if category_description is not None: 
			if isinstance(category_description, unicode): self.__description = category_description.encode('utf8') 
			else: self.__description = category_description
		else: self.__description = ""

        ## Set the Category icon file name.
        #
        # @param category_icon - New Category icon file name.
        def set_icon(self, category_icon):
                if category_icon is not None:
                        if isinstance(category_icon, unicode): self.__icon = category_icon.encode('utf8')
                        else: self.__icon = category_icon
                else: self.__icon = ""

        ## Set the Category icon file url.
        #
        # @param category_icon - New Category icon file url.
        def set_icon_url(self, category_icon_url):
                if category_icon_url is not None:
                        if isinstance(category_icon_url, unicode): self.__icon_url = category_icon_url.encode('utf8')
                        else: self.__icon_url = category_icon_url
                else: self.__icon_url = ""

	## Set \em to_save value.
	#
	# @param category_to_save - \b 0 if it is a system Category or \b 1 if it is a user Category.
	def set_to_save(self, category_to_save):
		self.__to_save = category_to_save
   	
	## Static method. Find a Category with some label in a Category List.
	#
	# @param cat_list - (list[]) Category list.
	# @param cat_label - Category Label.
	# @return \c Category Object or None.
	def find_category(self, cat_list, cat_label):
		#TODO: Optimize this method
		if cat_label is not None:
                        if isinstance(cat_label, unicode): c_label = cat_label.encode('utf8')
			else: c_label = cat_label
		else: c_label = ""
		
		cat_list.sort()
		for cat in cat_list:
			if cat.get_label().lower() == c_label.lower():
				return cat
		return None

	find_category = classmethod( find_category )

	## @var __name
	# The Category name.
	
	## @var __label
	# The Category label. It's the category id.
	
	## @var __description
	# The Category description.

	## @var __icon
	# The Category icon file name.

	## @var __icon_url
	# The Category icon file url.
	
	## @var __included
	# The Category included value: yes or no.
	
	## @var __to_save
	# The Category to_save value: yes or no.
	
	## @var __html_file
	# The Category html file name.

	## @var __apps
	# List of all App Objects that They are included in this Category

## Class representing an application.
#
# @author David Barragán Merino <bameda [AT] di.uc3m [DOT] com>
# @author CRISOL-UC3M <htp://crisol.uc3m.es>
class App:
 	
	
	## Inicialize the App values. Be carefull with string encoding.
	#
	# @param values - (list[14]) List of all App values.
    	def __init__(self,values):
		if values[0] is not None: 
			if isinstance(values[0], unicode): self.__name =  values[0].encode('utf8')
			else: self.__name =  values[0]
		else: self.__name = ""
		
		if values[1] is not None: 
			if isinstance(values[1], unicode): self.__version = values[1].encode('utf8')
			else: self.__version = values[1]
		else: self.__version = ""
		
		self.__size = 0
		if values[2] is not None:
			if isinstance(values[2], unicode): 
				if values[2].encode('utf8').isdigit(): self.__size = int(values[2].encode('utf8'))
			else: 
				if values[2].isdigit(): self.__size = int(values[2])
		
		if values[3] is not None: 
			if isinstance(values[3], unicode): self.__site = values[3].encode('utf8')
			else: self.__site = values[3]
		else: self.__site =  ""
		
		manuals = {'app_man_online':[], 
			   'app_man_offline':[]}
		for man in values[4]['app_man_online']:
			manu = {}
			if isinstance(man['app_man_on_name'], unicode): manu['app_man_on_name'] = man['app_man_on_name'].encode('utf8')
			else: manu['app_man_on_name'] = man['app_man_on_name']
			if isinstance(man['app_man_on_url'], unicode): manu['app_man_on_url'] = man['app_man_on_url'].encode('utf8')
			else: manu['app_man_on_url'] = man['app_man_on_url']
			if isinstance(man['app_man_on_description'], unicode): manu['app_man_on_description'] = man['app_man_on_description'].encode('utf8')
			else: manu['app_man_on_description'] = man['app_man_on_description']
			if isinstance(man['app_man_on_lang'], unicode): manu['app_man_on_lang'] = man['app_man_on_lang'].encode('utf8')
			else: manu['app_man_on_lang'] = man['app_man_on_lang']			
			manuals['app_man_online'].append(manu)
		for man in values[4]['app_man_offline']:
			manu = {}
			if isinstance(man['app_man_off_name'], unicode): manu['app_man_off_name'] = man['app_man_off_name'].encode('utf8')
			else: manu['app_man_off_name'] = man['app_man_off_name']
			if isinstance(man['app_man_off_url'], unicode): manu['app_man_off_url'] = man['app_man_off_url'].encode('utf8')
			else: manu['app_man_off_url'] = man['app_man_off_url']
			if isinstance(man['app_man_off_file'], unicode): manu['app_man_off_file'] = man['app_man_off_file'].encode('utf8')
			else: manu['app_man_off_file'] = man['app_man_off_file']
			manu['app_man_off_size'] = 0
			if man['app_man_off_size'] != None:
				if isinstance(man['app_man_off_size'], unicode): 
					if man['app_man_off_size'].encode('utf8').isdigit(): manu['app_man_off_size'] = int(man['app_man_off_size'].encode('utf8'))
				else: 
					if man['app_man_off_size'].isdigit(): manu['app_man_off_size'] = int(man['app_man_off_size'])
			if isinstance(man['app_man_off_description'], unicode): manu['app_man_off_description'] = man['app_man_off_description'].encode('utf8')
			else: manu['app_man_off_description'] = man['app_man_off_description']
			if isinstance(man['app_man_off_lang'], unicode): manu['app_man_off_lang'] = man['app_man_off_lang'].encode('utf8')
			else: manu['app_man_off_lang'] = man['app_man_off_lang']
			manuals['app_man_offline'].append(manu)
		self.__manuals = manuals
		
		plataforms = []
		for plat in values[5]:
			if isinstance(plat, unicode): plataforms.append(plat.encode('utf8'))
			else: plataforms.append(plat)
        	self.__plataforms = plataforms
		
		if values[6] != None: 
			if isinstance(values[6], unicode): self.__minidescription = values[6].encode('utf8')
			else: self.__minidescription = values[6]
		else: self.__minidescription = ""
		
		if values[7] != None: 
			if isinstance(values[7], unicode): self.__description = values[7].encode('utf8')
			else: self.__description = values[7]
		else: self.__description = ""
		
		if values[8] != None: 
			if isinstance(values[8], unicode): self.__file = values[8].encode('utf8')
			else: self.__file = values[8]
		else: self.__file = ""
		
		if values[9] != None: 
			if isinstance(values[9], unicode): self.__software_url = values[9].encode('utf8')
			else: self.__software_url = values[9]
		else: self.__software_url = ""
		
		if values[10] != None: 
			if isinstance(values[10], unicode): self.__icon = values[10].encode('utf8')
			else: self.__icon = values[10]
		else: self.__icon = ""
		
		if values[11] != None: 
			if isinstance(values[11], unicode): self.__icon_url = values[11].encode('utf8')
			else: self.__icon_url = values[11]
		else: self.__icon_url = ""

		if values[12] != None:
			if isinstance(values[12], unicode): self.__md5sum = values[12].encode('utf8')
			else: self.__md5sum = values[12]
		else: self.__md5sum = ""

		categories = []
		for cat in values[13]:
			if isinstance(cat, unicode): categories.append(cat.encode('utf8'))
			else: categories.append(cat)
        	self.__categories = categories
		
		alternatives = []
		for alt in values[14]:
			if isinstance(alt, unicode): alternatives.append(alt.encode('utf8'))
			else: alternatives.append(alt)
		self.__alternatives = alternatives
        	
		self.__included = 0
        	
		self.__to_save = 0
		
		self.__html_file = self.__name + ".html"

	## Compare this App to other.
	#
	# @param other - Object.
	# @return \b -1 - If this < other.\b 0 - If this = other.\b 1 - If this > other on other = None.
    	def __cmp__(self,other):
		if other == None:
			return 1
        	if self.__name.lower() > other.get_name().lower():
            		return 1
        	elif self.__name.lower() == other.get_name().lower():
            		return 0
        	else:
            	
			return -1


	## Compare this App to other.
	#
	# @return The App length in KB. 
	def __len__(self):
		size = self.__size
		for man in self.__manuals['app_man_offline']:
			size += man['app_man_off_size']
		return size

	## Select this App.
	#
    	def select_app(self):
        	self.__included = 1

	## Unselect this App.
	#
    	def unselect_app(self):
        	self.__included = 0
        
	## Return the \em included value.
	#
	# @return \b true/1 if it's include or \b false/0 if it isn't.
    	def is_included(self):
        	return self.__included
   	
	## Return the \em to_save value.
	#
	# If this App \em to_save value is \b true/1, it means that this App has been modified or added by the user.
	# @return \b true/1 that it must be save or \b false/0 that it dosen't have to be save. 
	def is_to_save(self):
		return self.__to_save  

	## Download the App's icon.
	#
	# If it can't download it. The \em icon_url is going to be delete.
	# @param icon_dir - The icon directory path.
    	def download_icon(self, icon_dir):
		try:
        		if not os.path.exists(icon_dir+"/"+self.__icon):
            			if self.__icon_url != None and self.__icon_url != "":
                			sys.stderr.write("!! Getting " + self.__icon + "... ")
					if urllib.urlretrieve(self.__icon_url, icon_dir + "/" + self.__icon):
                    				sys.stderr.write("Done\n")
		except Exception, e:
			sys.stderr.write("\nEE Error downloading application's icon from \"" + self.__name + "\".\n")
			sys.stderr.write(str(e) + "\n")	
			self.__icon_url = "" 
			self.__to_save = 1
			pass
	
	## Download the application's offline manuals. 
	#
	# If any manual don't download correctly, it information is going to be delete.
	# @param manual_dir - The manual directory path.
	def download_manuals(self, manual_dir):
		for manual in self.__manuals['app_man_offline']:
			try:
				if not os.path.exists(manual_dir+"/"+manual['app_man_off_file']):
                                	if manual['app_man_off_url'] != None:
                                        	sys.stderr.write("!! Getting " + manual['app_man_off_file'] + "... ")
						if urllib.urlretrieve(manual['app_man_off_url'], manual_dir+"/"+manual['app_man_off_file']):
                                                	sys.stderr.write("Done\n")
			except Exception, e:
				sys.stderr.write( "\nEE Error downloading application's manual (\"" + manual['app_man_off_file']+ "\")from \"" + self.__name + "\".\n")
                        	sys.stderr.write(str(e) + "\n") 
				
				self.__manuals['app_man_offline'].remove( manual )
				self.__to_save = 1
                        	pass

	## Download the application's software.
	#
	# If any software don't download correctly, it App is going to be unselect.
	# @param software_dir - The softwares path.
    	def download_software(self,software_dir):
	        try:
			if not os.path.exists(software_dir+"/"+self.__file):
        	    		sys.stderr.write("!! Getting " + self.__file + "... ") 
				if urllib.urlretrieve(self.__software_url, software_dir + "/" + self.__file):
        	        		sys.stderr.write("Done\n")
        	        		self.__md5sum = self.__get_md5_hash(software_dir + "/" + self.__file)
        	    		while self.__get_md5_hash(software_dir + "/" + self.__file) != self.__md5sum:
        	        		sys.stderr.write("\nEE md5 signatures don't match.\n")
					sys.stderr.write( "Getting " + self.__file + "... ")
					os.remove(software_dir+"/"+self.__file)
        	        		if urllib.urlretrieve(self.__software_url, software_dir + "/" + self.__file):
						sys.stderr.write("Done\n")
        	            			self.__md5sum = self.__get_md5_hash(software_dir + "/" + self.__file)
					
    		except Exception, e:
			sys.stderr.write("\nEE Error downloading application's software from \"" + self.__name + "\".\n")
			sys.stderr.write(str(e) + "\n")
			sys.stdout.write("\nERROR: \"" +  self.__name + "\" will not be including.\n")
			self.__included = 0

	## Add a new online manual to this App.
	#
	# @param values - (list[4]) List of all on-line manual values.
	#
	# @see App.__manuals
        def add_manual_online(self, values):
		manu = {}
		if isinstance(values[0], unicode): manu['app_man_on_name'] = values[0].encode('utf8')
		else: manu['app_man_on_name'] = values[0]
		if isinstance(values[1], unicode): manu['app_man_on_url'] = values[1].encode('utf8')
		else: manu['app_man_on_url'] = values[1]
		if isinstance(values[2], unicode): manu['app_man_on_description'] = values[2].encode('utf8')
		else: manu['app_man_on_description'] = values[2]
		if isinstance(values[3], unicode): manu['app_man_on_lang'] = values[3].encode('utf8')
		else: manu['app_man_on_lang'] = values[3]
            
		self.__manuals['app_man_online'].append(manu)	
		self.__to_save = 1

	## Add a new offline manual to this App.
	#
	# @param values - (list[6]) List of all off-line manual values.
	# 
	# @see App.__manuals
        def add_manual_offline(self, values):
		manu = {}
		if isinstance(values[0], unicode): manu['app_man_off_name'] = values[0].encode('utf8')
		else: manu['app_man_off_name'] = values[0]
		if isinstance(values[1], unicode): manu['app_man_off_url'] = values[0].encode('utf8')
		else: manu['app_man_off_url'] = values[1]
		if isinstance(values[2], unicode): manu['app_man_off_file'] = values[2].encode('utf8')
		else: manu['app_man_off_file'] = values[2]
		manu['app_man_off_size'] = 0
		if values[3] != None:
			if isinstance(values[3], unicode): 
				if values[3].encode('utf8').isdigit(): manu['app_man_off_size'] = int(values[3].encode('utf8'))
			else: 
				if values[3].isdigit(): manu['app_man_off_size'] = int(values[3])
		if isinstance(values[4], unicode): manu['app_man_off_description'] = values[4].encode('utf8')
		else: manu['app_man_off_description'] = values[4]
                if isinstance(values[5], unicode): manu['app_man_off_lang'] = values[5].encode('utf8')
                else: manu['app_man_off_lang'] = values[5]
                
		self.__manuals['app_man_offline'].append(manu)
		self.__to_save = 1
	
	## Calculate the md5 hash.
	#
	# @param filename - The path to the file we want the md5 hash.
	# @return md5 hash.
    	def __get_md5_hash(self,filename):
        	f = open(filename,'rb')
        	hsh = md5.new()
        	hsh.update(f.read())
        	f.close()
        	return hsh.hexdigest()

	## Create a dictionary with all App information.
	#
	# @return A dictionary with all App information
    	def get_app_dict(self):
		dict = {}
        	dict['name'] = self.__name
        	dict['version'] = self.__version
		dict['size'] = self.__size
        	dict['site'] = self.__site 
		dict['manuals'] = self.__manuals
		dict['plataforms'] = self.__plataforms
		dict['minidescription'] = self.__minidescription
		dict['description'] = self.__description
        	dict['file'] = self.__file
        	dict['software_url'] = self.__software_url
        	dict['icon'] = self.__icon
        	dict['icon_url'] = self.__icon_url
        	dict['md5sum'] = self.__md5sum
		dict['included'] = self.__included
		dict['html_file'] = self.__html_file
		if len(self.__categories) == 0: dict['categories'] = ["none"]
		else: dict['categories'] = self.__categories
        	dict['alternatives'] = self.__alternatives
		return dict;

	## Generate the App XML Element.
	#
	# @return App XML Element.
    	def gen_xml_element(self):
		app = Element("APP")
        	
		name = SubElement(app,"APP_NAME")
        	name.text = self.__name.decode('utf8')

        	version = SubElement(app,"APP_VERSION")
        	version.text = self.__version.decode('utf8')

		size = SubElement(app,"APP_SIZE")
		size.text = str(self.__size).decode('utf8')

        	site = SubElement(app,"APP_SITE")
        	site.text = self.__site.decode('utf8')

        	manuals = SubElement(app,"APP_MANUALS")
		for man in self.__manuals['app_man_online']:
			man_on = SubElement(manuals, "APP_MAN_ONLINE")
			m_name = SubElement(man_on, "APP_MAN_ONLINE_NAME")
			m_name.text = man['app_man_on_name'].decode('utf8')
			m_url = SubElement(man_on, "APP_MAN_ONLINE_URL")
			m_url.text = man['app_man_on_url'].decode('utf8')
			m_description = SubElement(man_on, "APP_MAN_ONLINE_DESCRIPTION")
			m_description.text = man['app_man_on_description'].decode('utf8')
			m_lang = SubElement(man_on, "APP_MAN_ONLINE_LANG")
			m_lang.text = man['app_man_on_lang'].decode('utf8')
		for man in self.__manuals['app_man_offline']:
			man_off = SubElement(manuals, "APP_MAN_OFFLINE")
			m_name = SubElement(man_off, "APP_MAN_OFFLINE_NAME")
                        m_name.text = man['app_man_off_name'].decode('utf8')
                        m_url = SubElement(man_off, "APP_MAN_OFFLINE_URL")
                        m_url.text = man['app_man_off_url'].decode('utf8')
			m_file = SubElement(man_off, "APP_MAN_OFFLINE_FILE")
			m_file.text = man['app_man_off_file'].decode('utf8')
			m_size = SubElement(man_off, "APP_MAN_OFFLINE_SIZE")
			m_size.text = str(man['app_man_off_size']).decode('utf8')
                        m_description = SubElement(man_off, "APP_MAN_OFFLINE_DESCRIPTION")
                        m_description.text = man['app_man_off_description'].decode('utf8')
                        m_lang = SubElement(man_off, "APP_MAN_OFFLINE_LANG")
                        m_lang.text = man['app_man_off_lang'].decode('utf8')
		
		plataforms = SubElement(app,"APP_PLATAFORMS")
                plats = []
                for plataform in self.__plataforms:
                        plats.append(SubElement(plataforms,"APP_PLAT"))
                        plats[-1].text = plataform.decode('utf8')

		minidescription = SubElement(app,"APP_MINIDESCRIPTION")
                minidescription.text = self.__minidescription.decode('utf8')

        	description = SubElement(app,"APP_DESCRIPTION")
        	description.text = self.__description.decode('utf8')

        	file = SubElement(app,"APP_FILE")
        	file.text = self.__file.decode('utf8')

        	download_url = SubElement(app,"APP_DOWNLOAD_URL")
        	download_url.text = self.__software_url.decode('utf8')

        	icon = SubElement(app,"APP_ICON")
        	icon.text = self.__icon.decode('utf8')

        	icon_url = SubElement(app,"APP_ICON_URL")
        	icon_url.text = self.__icon_url.decode('utf8')

        	md5sum = SubElement(app,"APP_MD5SUM")
        	md5sum.text = self.__md5sum.decode('utf8')

        	categories = SubElement(app,"APP_CATEGORIES")
        	cats = []
        	for category in self.__categories:
            		cats.append(SubElement(categories,"APP_CATEGORY"))
            		cats[-1].text = category.decode('utf8')

        	alternatives = SubElement(app,"APP_ALTERNATIVES")
        	alts = []
        	for alternative in self.__alternatives:
            		alts.append(SubElement(alternatives,"APP_ALT"))
            		alts[-1].text = alternative.decode('utf8')

        	return app
   	
	## Get the App name value.
	#
	# @return The App name.
	def get_name(self):
	        return self.__name
	
	## Get the App html file name value.
	#
	# @return The App html file name.
	def get_html_file(self):
		return self.__html_file
	
	## Get the App version value.
	#
	# @return The App version.
	def get_version(self):
		return self.__version	
   
	## Get the App software size value.
	#
	# @return The App software size value (in KB).
	def get_size(self):
		return str(self.__size)

    	## Return the App Web Site url value.
	#
	# @return The App site.
	def get_site(self):
		return self.__site
    
    	## Get the App manual dictionary value.
	#
	# @return The App manuals dictionary.
	#
	# @see App.__manuals
	def get_manuals(self):
		return self.__manuals
    	
	## Get the App plateforms List.
	#
	# @return The App platform List.
	def get_plataforms(self):
		return self.__plataforms
	
	## Get the App minidescription value.
	#
	# @return The App minidescription.
	def get_minidescription(self):
		return self.__minidescription

	## Get the App description value.
	#
	# @return The App description.
	def get_description(self):
		return self.__description
    	
	## Get the App software file name value.
	#
	# @return The App file name software.
	def get_file_name(self):
		return self.__file
    
    	## Get the App software url value.
	#
	# @return The App software url.
	def get_software_url(self):
		return self.__software_url
    	
	## Get the App icon file name value.
	#
	# @return The App file name icon.
	def get_icon_name(self):
		return self.__icon
    
    	## Get the App icon url value.
	#
	# @return The App icon url.
	def get_icon_url(self):
		return self.__icon_url

	## Get the App software md5um value.
	#
	# @return The App software md5sum.
	def get_md5sum(self):
		return self.__md5sum
	
	## Get the App Category List.
	#
	# @return The App Category List.
	def get_categories(self):
		return self.__categories

	## Get the App software alternatives List.
	#
	# @return The App software alternatives List.
	def get_alternatives(self):
		return self.__alternatives
        
	## Set the App name value.
	#
	# @param name - New App name.
	def set_name(self, name):
		if name is not None: 
                        if isinstance(name, unicode): self.__name = name.encode('utf8')
			else: self.__name = name
		self.__html_file = self.__name + ".html"
    
    	## Set the App version value.
	#
	# @param version - New App version.
	def set_version(self, version):
		if version is not None: 
			if isinstance(version, unicode): self.__version = version.encode('utf8')
			else: self.__version = version
		else: self.__version = ""

	## Set the App version value.
	#
	# @param size - New App size (in KB).
	def set_size(self, size):
		if size is not None:
			if isinstance(size, unicode): 
				if size.encode('utf8').isdigit(): self.__size = int(size.encode('utf8'))
			else: 
				if size.isdigit(): self.__size = int(size)
				

	## Set the App Web Site url value.
	#
	# @param site - New App site.
	def set_site(self, site):
		if site is not None: 
			if isinstance(site, unicode): self.__site = site.encode('utf8')
		    	else: self.__site = site
		else: self.__site = ""

	## Set the App manual List Dictionary.
	#
	# @param mans - New App manual Dictionary.
	#
	# @see App.__manuals 
	def set_manuals(self, mans):
		manuals = {'app_man_online':[],
		           'app_man_offline':[]}

		for man in mans['app_man_online']:
			manu = {}
			if isinstance(man['app_man_on_name'], unicode): manu['app_man_on_name'] = man['app_man_on_name'].encode('utf8')
			else: manu['app_man_on_name'] = man['app_man_on_name']
			if isinstance(man['app_man_on_url'], unicode): manu['app_man_on_url'] = man['app_man_on_url'].encode('utf8')
			else: manu['app_man_on_url'] = man['app_man_on_url']
			if isinstance(man['app_man_on_description'], unicode): manu['app_man_on_description'] = man['app_man_on_description'].encode('utf8')
			else: manu['app_man_on_description'] = man['app_man_on_description']
			if isinstance(man['app_man_on_lang'], unicode): manu['app_man_on_lang'] = man['app_man_on_lang'].encode('utf8')
			else: manu['app_man_on_lang'] = man['app_man_on_lang']
			manuals['app_man_online'].append(manu)

		for man in mans['app_man_offline']:
			manu = {}
			if isinstance(man['app_man_off_name'], unicode): manu['app_man_off_name'] = man['app_man_off_name'].encode('utf8')
			else: manu['app_man_off_name'] = man['app_man_off_name']
			if isinstance(man['app_man_off_url'], unicode): manu['app_man_off_url'] = man['app_man_off_url'].encode('utf8')
			else: manu['app_man_off_url'] = man['app_man_off_url']
			if isinstance(man['app_man_off_file'], unicode): manu['app_man_off_file'] = man['app_man_off_file'].encode('utf8')
			else: manu['app_man_off_file'] = man['app_man_off_file']
			manu['app_man_off_size'] = 0
			if man['app_man_off_size'] != None:
				if isinstance(man['app_man_off_size'], unicode): 
					if man['app_man_off_size'].encode('utf8').isdigit(): manu['app_man_off_size'] = int(man['app_man_off_size'].encode('utf8'))
				else: 
					if man['app_man_off_size'].isdigit(): manu['app_man_off_size'] = int(man['app_man_off_size'])
			if isinstance(man['app_man_off_description'], unicode): manu['app_man_off_description'] = man['app_man_off_description'].encode('utf8')
			else: manu['app_man_off_description'] = man['app_man_off_description']
			if isinstance(man['app_man_off_lang'], unicode): manu['app_man_off_lang'] = man['app_man_off_lang'].encode('utf8')
			else: manu['app_man_off_lang'] = man['app_man_off_lang']
			manuals['app_man_offline'].append(manu)

	        self.__manuals = manuals
	
	## Set the App plataform List value.
	#
	# @param plataforms - New App plataform List.
	def set_plataforms(self, plataforms):
		plataf = []
		for plat in plataforms:
			if isinstance(plat, unicode): plataf.append(plat.encode('utf8'))
			else: plataf.append(plat)
		self.__plataforms = plataf
    
    	##  Set the App minidescription value.
	#
	# @param minidescription - New App minidescription.
	def set_minidescription(self, minidescription):
		if minidescription is not None: 
			if isinstance(minidescription, unicode): self.__minidescription = minidescription.encode('utf8')
			else: self.__minidescription = minidescription
		else: self.__minidescription = ""

	## Set the App description value.
	#
	# @param description - New App description.
	def set_description(self, description):
		if description is not None: 
			if isinstance(description, unicode): self.__description = description.encode('utf8')
			else: self.__description = description
		else: self.__description = ""

	## Set the App software file name value.
	#
	# @param file - New App software file name.
	def set_file_name(self, file):
		if file is not None: 
			if isinstance(file, unicode): self.__file = file.encode('utf8')
			else: self.__file = file
		else: self.__file = ""

	## Set the App software url value.
	#
	# @param surl - New App software url.
	def set_software_url(self, surl):
		if surl is not None: 
			if isinstance(surl, unicode): self.__software_url = surl.encode('utf8')
			else: self.__software_url = surl
		else: self.__software_url = ""    

    	## Set the App icon file name value.
	#
	# @param icon - New App icon file name.
	def set_icon_name(self, icon):
		if icon is not None: 
			if isinstance(icon, unicode): self.__icon = icon.encode('utf8')
			else: self.__icon = icon
		else: self.__icon = ""
    	
	##  Set the App icon url value.
	#
	# @param icon_url - New App icon url.
	def set_icon_url(self, icon_url):
		if icon_url is not None: 
			if isinstance(icon_url, unicode): self.__icon_url = icon_url.encode('utf8')
			else: self.__icon_url = icon_url
		else: self.__icon_url = ""
	
	## Set the App software md5sum value.
	#
	# @param md5 - New App md5sum.
	def set_md5sum(self, md5):
	        if md5 is not None: 
			if isinstance(md5, unicode): self.__md5sum = md5.encode('utf8')
			else: self.__md5sum = md5
		else: self.__md5sum = ""
	
	## Set the App Category List values.
	#
	# @param categories - New App category List.
	def set_categories(self, categories):
		categ = []
		for cat in categories:
			if isinstance(cat, unicode): categ.append(cat.encode('utf8'))
			else: categ.append(cat)
	    	self.__categories = categ
    	
	## Delete a Category from the Categoy list.
	#
	# @param category_label - The Category name it has been delete.
	# @return \b true/1 if it's delete or \b false/0 if it isn't.
	def del_category(self, category_label):
		try:
			self.__categories.remove(category_label)
			return 1
		except Exception:
			return 0

	## Change a Category from Category list. 
	#
	# @param old_category - The label of th Category it has been change.
	# @param new_category - The new label.
	# @return \b true/1 if it's correctly or \b false/0 if it isn't.
	def change_category(self, old_category, new_category):
		try:
			n = self.__categories.index(old_category)
			if isinstance(new_category, unicode): self.__categories[n] = new_category.encode('utf8')
			else: self.__categories[n] = new_category
			return 1
		except Exception:
			return 0 

	## Set the application alterbatives list.
	#
	# @param alternatives - New App alternatives list.
	def set_alternatives(self, alternatives):
		alter = []
		for alt in alternatives:
			if isinstance(alt, unicode): alter.append(alt.encode('utf8'))
			else: alter.append(alt)
	        self.__alternatives = alter
	
	## Set application tu save.
	#
	# @param app_to_save - Value \b true/1 (to save) or \b false/0 (don't save).
	def set_to_save(self, app_to_save):
		self.__to_save = app_to_save

	## Find an App with the same name as \em name param in a App list.
	#
	# @param app_list - (list[]) App list.
	# @param app_name - App name.
	# @return App Object or None.
	def find_app( self, app_list, app_name):
		#TODO: Optimize this method
                if app_name is not None:
			if isinstance(app_name, unicode): a_name = app_name.encode('utf8')
			else: a_name = app_name
		else: a_name = ""
										
		app_list.sort()
		for app in app_list:
			if app.get_name().lower() == a_name.lower():
				return app
		return None
	
	find_app = classmethod( find_app )	
	
	## @var __name
	# The App name.

	## @var __version
	# The App version.

	## @var __size
	# The App software size (in KB).
	
	## @var __site
	# The App Web Site url.
	
	## @var __manuals
	# The App manuals Dictionary:
	#
	#    	\li \em app_man_online  - List of On-Line Manuals dictionaries.
	#    	\li \em app_man_online/app_man_on_name - On-Line manual name.
	#	\li \em app_man_online/app_man_on_url - On-Line manual url.
	#	\li \em app_man_online/app_man_on_description - On-Line manual description.
	#       \li \em app_man_online/app_man_on_lang - On-Line mnuals languages.
	#	
	#    	\li \em app_man_offline - List of Off-Line Manuals dictionaries.
	#       \li \em app_man_offline/app_man_off_name - Off-Line manual name.
	#       \li \em app_man_offline/app_man_off_url - Off-Line manual url.
	#	\li \em app_man_offline/app_man_off_file - Off-Line manual file name. 
	#       \li \em app_man_offline/app_man_off_size - Off-Line manual file size.
	#       \li \em app_man_offline/app_man_off_description - Off-Line manual description.
	#       \li \em app_man_offline/app_man_off_lang - Off-Line manual languages. 
	
	## @var __plataforms
	# The App plataform List.
	
	## @var __minidescription
	# The App minidescription. 
	
	## @var __description
	# The App description
	
	## @var __file
	# The App software file name.
	
	## @var __software_url
	# The App software url.
	
	## @var __icon
	# The App icon file name.
	
	## @var __icon_url
	# The App icon url.
	
	## @var __md5sum
	# The App md5sum.
	
	## @var __categories
	# The App Category label List.
	
	## @var __alternatives
	# The App alternatives List.
	
	## @var __included
	# The App include value (\em true/1 or \em false/0).
	
	## @var __to_save
	# The App to_save value (\em true/1 or \em false/0).
	
	## @var __html_file
	# The App html file name.

## Class repreesent a WinSOL image, with the Categories and applications list.
#
# @author David Barragán Merino <bameda [AT] di.uc3m [DOT] com>
# @author CRISOL-UC3M <htp://crisol.uc3m.es>
class Image:

	## Inicialice the Image atrivutes.
	#
	# @param xml_files - (list[5]) list of xml path files (sys_cat, sys_app, user_cat, user_app, user_includes)
	# @param dtd_files - (list[2]) list of dtd path files (cat_dtd, app_dtd, includes_dtd)
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
	
	## Privated method that insert all application in its categories.
	#
	def __insert_apps_into_category(self):
		for app in self.__apps:
			# Add apps without category
			if len(app.get_categories()) == 0:
				cat = Category.find_category(self.__categories, "none")
                                if cat != None:
                                        cat.add_application(app)
				else:
					cat = Category(["Sin Categoría", "none", "Aplicaiones sin una categoría asignada.","",""])
					self.__categories.append(cat)
					cat.add_application(app)
			# Add apps with category
			else:
				for cat_label in app.get_categories():
					cat = Category.find_category(self.__categories, cat_label)
					if cat != None:
						cat.add_application(app)
					

	## Calculate the image size in KB.
	#
	def calculate_size(self):
		size = 0
		for app in self.__apps:
			if app.is_included():
				for cat_label in app.get_categories():
					cat = Category.find_category(self.__categories, cat_label)
					if cat != None and cat.is_included():
						size += len(app)
						break
		return size

	## Add a new Category to the Category List. If there is a Category with the same name, it don't insert it.
	# 
	# @param category_values - List of the values to the new Category. 
	# @return \b true/1 it's ok or \b false/0 it's failed, this Category exist.
	#
	# @see Category.__init__()
	def add_category(self, category_values):
		if category_values[0] == None or category_values[0] == "": return 0
		if category_values[1] == None or category_values[1] == "": return 0
		
		cat = Category(category_values)
		if Category.find_category(self.__categories, cat.get_label()) == None:
			self.__categories.append(cat)
			self.__categories.sort()
			cat.set_to_save(1)
			return 1
		# There is one category with the same label"	
		return 0
	
	## Modify the Category, that it has the same label as \em category_label, with the new values.
        #
	# @param category_label - The label of the Category to be modifie.
        # @param category_value - A List of the new Category values.
        # return \b true/1 if it's ok, this Category has been modifie, or \b false/0 if it's failed, this Category don't exist.
        #
	# @see Category.set_name()
	# @see Category.set_description()
	def modify_category_values(self, category_label, category_value):
		if category_value[0] == None or category_value[0] == "": return 0
		
		cat = Category.find_category(self.__categories, category_label)
		if cat == None:
			return 0
		else:	
                       	cat.set_name(category_value[0])
			cat.set_description(category_value[1])
			cat.set_icon(category_value[2])
			cat.set_icon_url(category_value[3])
			cat.set_to_save(1)
			return 1

	## Delete the Category that it has the same label as \em category_label.
	#
	# @param category_label - The label of the Category to be delete.
	# @return \b true/1 if it's ok, the Category has been delete, or \b false/0 if it's failed. The Category don't exist or it's from the system XML file.
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
            		if cat.get_label().lower() != category_label.lower():
                		result_list.append(cat)
            		else:
                		delete = 1
				# Delete to app.categories
				#if cat.is_to_save():
				for app in cat.get_all_apps():
					app.del_category(category_label)
					app.set_to_save( 1 )
                self.__categories = result_list
		self.__categories.sort()
        	return delete

	## Add a new App to the App List. If there is one with the same name. It don't include.
	#
	# @param app_values - The new App values.
	# @return \b true/1 if it's ok or \b false/0 if it's failed. This App exist.
	#
	# @see App.__init__()
	def add_app(self, app_values):
		if app_values[0] == None or app_values[0] == "": return 0
		if app_values[1] == None or app_values[1] == "": return 0
		if app_values[8] == None or app_values[0] == "": return 0
		if app_values[9] == None or app_values[0] == "": return 0

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
					cat = Category(["Sin Categoría", "none", "Aplicaiones sin una categoría asignada.","",""])
					cat.set_to_save(1)
					self.__categories.append(cat)
					cat.add_application(app)
			else:
				# The app is from any category
				for cat_label in app.get_categories():
					cat = Category.find_category(self.__categories, cat_label)
					if cat != None:
						cat.add_application(app)
					else:
						app.del_category(cat_label)
			return 1
		# There is a App with the same name"
		return 0
	
	## Modify the App, that it has the same name as \em app_name, with the new values.
        #
        # @param app_name - The name of the App to be modifie.
        # @param app_values - A List of the new App values.
        # return \b true/1 if it's ok, this App has been modifie, or \b false/0 if it's failed, this App don't exist.
        #
        # @see App.set_version()
	# @see App.set_size()
        # @see App.set_site()
        # @see App.set_manuals()
        # @see App.set_plataforms()
        # @see App.set_minidescription()
        # @see App.set_description()
        # @see App.set_file_name()
        # @see App.set_software_url()
        # @see App.set_icon_name()
        # @see App.set_icon_url()
        # @see App.set_md5sum()
	# @see App.set_categories()
	# @see App.set_alternatives()
	def modify_app_values(self, app_name, app_values):
                if app_values[0] == None or app_values[0] == "": return 0
		if app_values[7] == None or app_values[7] == "": return 0
		if app_values[8] == None or app_values[8] == "": return 0

		app = App.find_app(self.__apps, app_name)
		if app == None:
			return 0
		else:
			app.set_version(app_values[0])
			app.set_size(app_values[1])
			app.set_site(app_values[2])
			app.set_manuals(app_values[3])
			app.set_plataforms(app_values[4])
			app.set_minidescription(app_values[5])
			app.set_description(app_values[6])
			app.set_file_name(app_values[7])
			app.set_software_url(app_values[8])
			app.set_icon_name(app_values[9])
			app.set_icon_url(app_values[10])
			app.set_md5sum(app_values[11])

			oldcats = app.get_categories()
			if len(oldcats) == 0:
				cat = Category.find_category(self.__categories, "none")
				cat.del_application(app.get_name())
				if len(cat.get_all_apps()) == 0: # Delete "None" category if it isn't any app
					self.__categories.remove(cat)
			else:
				for cat_label in oldcats:
					cat = Category.find_category(self.__categories, cat_label)
					if cat != None:
						cat.del_application(app.get_name())
			
			newcats = app_values[12]
			app.set_categories(newcats)
			if len(newcats) == 0:
				cat = Category.find_category(self.__categories, "none")
				if cat != None:
					cat.add_application(app)
				else:
					cat = Category(["Sin Categoría", "none", "Aplicaiones sin una categoría asignada.","",""])
					self.__categories.append(cat)
					cat.add_application(app)
			else:
				for cat_label in newcats:
					cat = Category.find_category(self.__categories, cat_label)
					if cat != None:
						cat.add_application(app)
					else:
						app.del_category(cat_label)

			app.set_alternatives(app_values[13])
			app.set_to_save(1)
			return 1

        ## Delete the App that it has the same name as \em app_name.
        #
        # @param app_name - The name of the App to be delete.
        # @return \b true/1 if it's ok, the App has been delete, or \b false/0 if it's failed. The App don't exist or it's from the system XML file.
	def del_app(self, app_name):
		result_list = []
		delete = 0
		for app in self.__apps:
			if app.get_name().lower() != app_name.lower():
				result_list.append(app)
			else:
				# The App is delete
				delete = 1
				if len(app.get_categories()) == 0:
					cat = Category.find_category(self.__categories, "none")
					if cat != None:
						cat.del_application(app_name)
						# Delete None Category.
						# if don't have applications.
						if len(cat.get_all_apps()) == 0:
							cat_list = []
							for categ in self.__categories:
                        					if categ != cat:
                                					cat_list.append(categ)
                					self.__categories = cat_list
                					self.__categories.sort()

				else:
					for cat_label in app.get_categories():
                                        	cat = Category.find_category(self.__categories, cat_label)
                                		if cat != None:
							cat.del_application(app_name)
		self.__apps = result_list
		self.__apps.sort()
		return delete
	
	
        ## Add a new On-Line manual to a specific App.
        #
	# @param app_name - The App name.
        # @param manual - The List of manual values.
        # @return \b true/1 if it's ok or \b false/0 if it's failed. There isn't any App with this name or the manual values are incomplete.
	#
	# @see App.add_manual_online()
        def add_manual_online_to_app(self, app_name, manual):
                app = App.find_app(self.__apps, app_name)
               	if app == None:
			return 0
		else:
                        if len(manual) != 4:
                                return 0
                        else:
                                app.add_manual_online(manual)
                                return 1

        ## Add a new Off-Line manual to a specific App.
        #
        # @param app_name - The App name.
        # @param manual - The List of manual values.
        # @return \b true/1 if it's ok or \b false/0 if it's failed. There isn't any App with this name or the manual values are incomplete.
        #
        # @see App.add_manual_offline()
        def add_manual_offline_to_app(self, app_name, manual):
                app = App.find_app(self.__apps, app_name)
               	if app == None:
			return 0
                else:
                        if len(manual) != 6:
                                return 0
                        else:
                                app.add_manual_offline(manual)
                                return 1

	## Select the Category with its label is the same as \em category_label.
	# 
	# @param category_label - The Category label.
	# @return \b true/1 if it has been selected or \b false/0 if it hasn't been selected.		
	def select_category(self, category_label):
		cat = Category.find_category(self.__categories, category_label)
                if cat != None:
                       	cat.select_category()
			return 1
		return 0

        ## 'Unselect' the Category with its label is the same as \em category_label.
        #
        # @param category_label - The Category label.
        # @return \b true/1 if it has been unselected or \b false/0 if it hasn't been unselected.
	def unselect_category(self, category_label):
		cat = Category.find_category(self.__categories, category_label)
                if cat != None:
                       	cat.unselect_category()
			return 1
		return 0

	## Select all categories.		
	#
	def select_all_categories(self):
		for cat in self.__categories:
			cat.select_category()
		return 1	

	## 'Unselect' all categories.
	#
	def unselect_all_categories(self):
		for cat in self.__categories:
			cat.unselect_category()
		return 1	
	
        ## Select the App with its name is the same as \em app_name.
        #
        # @param app_name - The App name.
        # @return \b true/1 if it has been selected or \b false/0 if it hasn't been selected.	
	def select_app(self, app_name):
		app = App.find_app(self.__apps, app_name)
		if app != None:
                        app.select_app()
			for cat_label in app.get_categories():
				cat = Category.find_category(self.__categories, cat_label)
				if cat != None:
					cat.select_category()
			return 1
		return 0
	
        ## Select all applications that they're included in a Category with its label is the same as \em category_label.
        #
        # @param category_label - The Category label.
        # @return \b true/1 if they have been selected or \b false/0 if they haven't been selected.
	def select_apps_by_category(self, category_label):
		cat = Category.find_category(self.__categories, category_label)
                if cat != None:
			for app in cat.get_all_apps():
                		app.select_app()
			return 1
		return 0

	## Select all aplications.
	#
	def select_all_apps(self):
		for app in self.__apps:
			app.select_app()			
		return 1

        ## 'Unselect' the App with its name is the same as \em app_name.
        #
        # @param app_name - The App name.
        # @return \b true/1 if it has been unselected or \b false/0 if it hasn't been unselected.
	def unselect_app(self, app_name):
		app = App.find_app(self.__apps, app_name)
                if app != None:
                        app.unselect_app()
                        return 1
                return 0

	## 'Unselect' all applications that they're included in a Category with its label is the same as \em category_label.
        #
        # @param category_label - The Category label.
        # @return \b true/1 if they have been unselected or \b false/0 if they haven't been unselected.
        def unselect_apps_by_category(self, category_label):
                cat = Category.find_category(self.__categories, category_label)
                if cat != None:
                        for app in cat.get_all_apps():
                                app.unselect_app()
                        return 1
                return 0

	## 'Unselect' all applications.
	#
        def unselect_all_apps(self):
		for app in self.__apps:
			app.unselect_app()
		return 1
	
	## Download the software from all selected applications.
	#
	# @param soft_dir - Path to download the software files.
	def download_software(self, soft_dir):
		for cat in self.__categories:
			cat.download_software(soft_dir)
		self.save_categories_to_xml_file()
		self.save_applications_to_xml_file()
		self.save_includes_to_xml_file()

        ## Download the software from some applications.
	#
	# @param app_name - The App name.
	# @param soft_dir - Path to download the software files.
	def download_app_software(self, app_name, soft_dir):
		app = App.find_app(self.__apps, app_name)
		if app != None:
			app.download_software(soft_dir)

	## Download the icons from all selected applications.
	#
	# @param icon_dir - Path to download the icons files.
	def download_icons(self, icon_dir):
		for cat in self.__categories:
			cat.download_apps_icons(icon_dir)
			cat.download_icon(icon_dir)
		self.save_categories_to_xml_file()
		self.save_applications_to_xml_file()
	
	## Download the icon from some applications.
	#
	# @param app_name - The App name.
	# @param icon_dir - Path to download the icons files.
	def download_app_icon(self, app_name, icon_dir):
		app = App.find_app(self.__apps, app_name)
		if app != None:
			app.download_icon(icon_dir)

	## Download the icon from some category.
	#
	# @param category_label - The Category label.
	# @param icon_dir - Path to download the icons files.
	def download_category_icon(self, category_label, icon_dir):
		cat = Category.find_category(self.__categories, category_label)
		if cat != None:
			cat.download_icon(icon_dir)

	## Download the manuals from all selected applications.
	#
	# @param manual_dir - Path to download the manuals files.
	def download_manuals(self, manual_dir):
		for cat in self.__categories:
                        cat.download_manuals(manual_dir)
		self.save_applications_to_xml_file()
	
	## Download the manuals from some applications.
	#
	# @param app_name - The App name.
	# @param manual_dir - Path to download the manuals files.
	def download_app_manual(self, app_name, manual_dir):
		app = App.find_app(self.__apps, app_name)
		if app != None:
			app.download_manuals(manual_dir)

	
	## Unselect all categories that there isn't any selected apps.
	#
	def __unselect_categories_without_selected_apps(self):
		for cat in self.__categories:
			if cat.is_included():
				empty = 1
				for app in cat.get_all_apps():
					if app.is_included(): 
						empty = 0
						break
				if empty: cat.unselect_category()
		self.save_includes_to_xml_file()

	## Generate the image html files from all selected categories and applications.
	#
	# @param html_dir - Path to generate the html structure.
	# @param template_dir - Path to html template directory.
	def gen_html(self, html_dir, template_dir):
		if not os.path.exists(html_dir): return 0
		if not os.path.exists(template_dir + "/category.tmpl"): return 0
		if not os.path.exists(template_dir + "/application.tmpl"): return 0
		if not os.path.exists(template_dir + "/index.tmpl"): return 0
		
		if not os.path.exists(html_dir + "/apps"): 
			os.mkdir(html_dir + "/apps")
		if not os.path.exists(html_dir + "/categories"): 
			os.mkdir(html_dir + "/categories")

		self.__unselect_categories_without_selected_apps()

		# Adding aditional images
		if os.path.exists(template_dir + "/mis"):
			if os.path.exists(html_dir + "/mis"):
				os.system( "rm -rf '"+ html_dir +"/mis" +"'" )
			os.system( "cp -rf "+ template_dir + "/mis " + "'" + html_dir +"/mis" +"'" )
		categories = []
		for cat in self.__categories:
			if cat.is_included():
				categories.append(cat.get_category_dict())
		
		index = Template( file = template_dir + "/index.tmpl",  searchList = [ {'categories' : categories} ] )	
		f = open( html_dir + "/index.html", 'w')
		f.write( "" + str(index) )
		f.close()
		
		for cat in categories:
			category = Template( file = template_dir + "/category.tmpl",  searchList = [ {'category' : cat, 'categories' : categories} ]  )
			f = open( html_dir + "/categories/" + cat['html_file'], 'w')
                        f.write( str(category))
			f.close()

			for app in cat['apps']:
				if app['included']:
					if not os.path.exists(html_dir +"/apps/" + app['html_file']):
						application = Template( file = template_dir + "/application.tmpl",  searchList = [ {'application' : app, 'categories': categories} ] )
                                                
						f = open( html_dir + "/apps/" + app['html_file'], 'w')
                                                f.write( "" + str(application) )
						f.close()
	
		return 1
	
	## Make the iso image from \em image_dir path to \em iso_file path.
	#
	# @param image_dir - Path of image directory.
	# @param iso_file - Path of iso file.
	# @return \b true/1 if it has been created or \b false/0 if it hasn't been created.
	def make_iso(self, image_dir, iso_file):
		if not os.path.exists(image_dir): 
			return 0
		else:
			os.system( "mkisofs -J -R -f -o '" + iso_file + "' '" + image_dir + "'" )
			return 1
	
	## Make the zip file from \em image_dir path to \em zip_file path.
	#
	# @param image_dir - Path of image directory.
	# @param zip_file - Path of zip file.
	# @return \b true/1 if it has been created or \b false/0 if it hasn't been created.
	def make_zip(self, image_dir, zip_file):
		if not os.path.exists(image_dir):
			return 0
		else:
			cwd = os.getcwd()
			os.chdir(image_dir)
			os.system( "zip -r0 " + zip_file + " " + "*" )
			os.chdir(cwd)
                        return 1

	## Get the Category List from this Image..
	#
	# @return A Category List.
	def get_all_categories(self):
		return self.__categories

	## Get a List with all categories name.
	#
	# @return A Category name List.
	def get_all_categories_name(self):
		result = []
		for cat in self.__categories:
			result.append( cat.get_name() )
		return result 
	
	## Get a List with all categories Dictionaries. 
	#
	# @return A Category Dictionary List.
	def get_all_categories_dict(self):
		result = []
		for cat in self.__categories:
			result.append( cat.get_category_dict() )
		return result 

	## Get a List with all categories label.
	#
	# @return A Category label List.
	def get_all_categories_label(self):
		result = []
		for cat in self.__categories:
			result.append( cat.get_label() )
		return result 

	## Get the Category with the same label as \em category_label or return \b None if it dosen't exist.
	#
	# @param category_label - The Category label.
	# @return A Category Object.
	#
	# @see Category.find_category()
	def get_category_by_label(self, category_label):
		return Category.find_category(self.__categories, category_label)

	## Get the Category Dictionary from the Category with the same label as \em category_label or return \b None if it dosen't exist.
	#
	# @param category_label - The Category label.
	# @return A Category Object.
	#
	# @see Category.find_category()
	def get_category_dict_by_label(self, category_label):
		cat = Category.find_category(self.__categories, category_label)
		if cat == None:
			return None
		else:
			return cat.get_category_dict()
	
	## Get a list with all applications.
	#
	# @return The App List.
	def get_all_apps(self):
		return self.__apps

	## Get a list of all applications names.
	#
	# @return A App name List.
	def get_all_apps_name(self):
		result = []
		for app in self.__apps:
			result.append( app.get_name() )
		return result

	## Get a list of all applications dictionaries.
	#
	# @return A App dictionary List.
	def get_all_apps_dict(self):
		result = []
		for app in self.__apps:
			result.append( app.get_dict() )
		return result

	## Get a list of all applications that they have been included in a Category with the same label of \em category_label.
	#
	# @param category_label - The Category label.
	# @return An App List.
	def get_apps_by_category(self, category_label):
		cat = Category.find_category(self.__categories, category_label)
		if cat == None: 
			return [] 
		else:
			return cat.get_all_apps()		

	## Get a list of all applications name that they have been included in a Category with the same label of \em category_label.
	#
	# @param category_label - The Category label.
	# @return An App name List.
	def get_apps_name_by_category(self, category_label):
		result = []
		for app in Category.find_category(self.__categories, category_label).get_applications():
			result.append( app.get_name() )
		return result

	## Get a list of all applications dictionaries that they have been included in a Category with the same label of \em category_label.
	#
	# @param category_label - The Category label.
	# @return An App dictionary List.
	def get_apps_dict_by_category(slef, category_label):
		result = []
		for app in Category.find_category(self.__categories, category_label).get_applications():
			result.append( app.get_dict() )
		return result

	## Get a App  with the same name of \em app_name or return \b None if it dosen't exist.
	#
	# @param app_name - The App name.
	# @return An App Object.
	#
	# @see App.find_app()
	def get_app_by_name(self, app_name):
		return App.find_app(self.__apps, app_name)

	## Get a App Dictionary with the same name of \em app_name or return \b None if it dosen't exist.
	#
	# @param app_name - The App name.
	# @return An App Dictionary.
	#
	# @see App.find_app()           
	def get_app_dict_by_name(self, app_name):
		app =  App.find_app(self.__apps, app_name)
		if (app == None):
			return None
		else:
			return app.get_app_dict()

	## Save the categories list to a file.
	#
	def save_categories_to_xml_file(self):
		self.__user_category_file.write_to_XML_file( self.__categories )

	## Save the applications list to a file.
	#
	def save_applications_to_xml_file(self):
		self.__user_app_file.write_to_XML_file( self.__apps )

	## Save include information to a file.
	#
	def save_includes_to_xml_file(self):
		self.__user_include_file.write_to_XML_file( self.__categories, self.__apps )
	
## Superclass to control the XML file imput/output.
#
# @author David Barragán Merino <bameda [AT] di.uc3m [DOT] com>
# @author CRISOL-UC3M <htp://crisol.uc3m.es>
class DataFile:

	## Inicialice the DataFile values.
	#
	# @param xml_file - XML file path.
	# @param dtd_file - DTD file path.
	def __init__(self, xml_file, dtd_file ):
		self.__xml_file = xml_file
		self.__dtd_file = dtd_file
		self.__check = 0

	## Check the XML integrity, with the DTD, and parser it.
	#
	# @return \em true/1 if it has been cheked or \em false/0 if it hasn't.
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
			sys.stderr.write("EE Error in XML-File \"" + self.__xml_file + "\" validation\n")
			self.__check = 0
		return self.__check

	## Returnthe check value.
	#
	# @return \em true/1 if it has been cheked or \em false/0 if it hasn't.
	def is_cheked(self):
		return self.__check

	## Write the applications_list to the XML file with the applications DTD structure.
	#
	# @param app_list - Application list.
	def write_apps_to_XML_file(self, app_list):
		root = Element("APPLICATIONS")
                for app in app_list:
                        if app.is_to_save():
                                root.append(app.gen_xml_element())
                self.__tree = ElementTree(root)
                self.__tree.write(self.__xml_file)

	## Write the categories list to the XML file with the categories DTD structure.
	#
	# @param category_list - Categories list.
	def write_categories_to_XML_file(self, category_list):
		root = Element("CATEGORIES")
                for category in category_list:
			if category.is_to_save():
                        	root.append(category.gen_xml_element())
                self.__tree = ElementTree(root)
                self.__tree.write(self.__xml_file)

	## Write the includes list of category and applications with the includes DTD structure.
	#
	# @param category_list - Categories list.
	# @param app_list - Application list.
	def write_includes_to_XML_file(self, category_list, app_list):
		root = Element("INCLUDES")
		categories = SubElement(root,"CATEGORIES")
		for cat in category_list:
			if cat.is_included():
				label = SubElement(categories,"CAT_LABEL")
                		label.text = cat.get_label().decode('utf8')
		applications = SubElement(root,"APPLICATIONS")
		for app in app_list:	
			if app.is_included():
				name = SubElement(applications,"APP_NAME")
				name.text = app.get_name().decode('utf8')
		self.__tree = ElementTree(root)
		self.__tree.write(self.__xml_file)
	
	## Get the XML path file.
	#
	# @return The XML path  file value.
	def get_XML_file(self):
		return self.__xml_file

	## Get the DTD path file.
	#
	# @return The DTD path file value.
	def get_DTD_file(self):
		return self.__dtd_file

	## Get the Tree structure.
	#
	# @return The ElementTree structure.
	def get_tree(self):
		return self.__tree
	
	## Set the XML path file.
	#
	# @param xml_file - New XML path file.
	def set_XML_file(self, xml_file):
		self.__xml_file = xml_file
		self.__check = 0

	## Set the DTD path file. 
	#
	# @param dtd_file - New DTD path file.
	def set_DTD_file(self, dtd_file):
		self.__dtd_file = dtd_file
		self.__check = 0

	## @var __dtd_file
	# The DTD file path.

	## @var __xml_file
	# the XML file path.

	## @var __check
	# Check value (\em true/1 or \em false/0)

	## @var __tree
	# The ElementTree Object from the XML file process.

## Class represent the Application XML file input/output.
#
# @author David Barragán Merino <bameda [AT] di.uc3m [DOT] com>
# @author CRISOL-UC3M <htp://crisol.uc3m.es>
class AppsDataFile(DataFile):

	## Inicialice AppsDataFile.
	#
	# @param xml_file - XML path file.
	# @param dtd_file - DTD path file.
	#
	# @see DataFile.__init_()
	def __init__(self, xml_file, dtd_file ):
        	DataFile.__init__(self, xml_file, dtd_file)
	
	## Add all applications from XML file to the App List.
	#
	# @param app_list - The application list.
	# @param save - The save value (0 to System App 1 to User App).
	# @return \em true/1 if it is correct or \em false/0 if isn't correct.
	def get_Apps(self, app_list, save = 0):
		if( DataFile.is_cheked(self) == 0):
			sys.stderr.write("EE The XML-File \"" + DataFile.get_XML_file(self) + "\" is not checked\n")
			return 0 
		else:
                	for application in DataFile.get_tree(self).findall("/./APP"):
                        	name = application.findall("./APP_NAME")[0].text
				
				version = application.findall("./APP_VERSION")[0].text

				size = application.findall("./APP_SIZE")[0].text

                        	site = application.findall("./APP_SITE")[0].text
				
				manuals = {}
				man_on = []
                        	for manual in application.findall("./APP_MANUALS/APP_MAN_ONLINE"):
					m_on = {}
					m_on['app_man_on_name'] = manual.findall("./APP_MAN_ONLINE_NAME")[0].text
					m_on['app_man_on_url'] = manual.findall("./APP_MAN_ONLINE_URL")[0].text
					m_on['app_man_on_description'] = manual.findall("./APP_MAN_ONLINE_DESCRIPTION")[0].text
					m_on['app_man_on_lang'] = manual.findall("./APP_MAN_ONLINE_LANG")[0].text
					man_on.append(m_on)
				manuals['app_man_online'] = man_on
				man_off = []
				for manual in application.findall("./APP_MANUALS/APP_MAN_OFFLINE"):
					m_off = {}
                                        m_off['app_man_off_name'] = manual.findall("./APP_MAN_OFFLINE_NAME")[0].text
                                        m_off['app_man_off_url'] = manual.findall("./APP_MAN_OFFLINE_URL")[0].text
					m_off['app_man_off_file'] = manual.findall("./APP_MAN_OFFLINE_FILE")[0].text
					m_off['app_man_off_size'] = manual.findall("./APP_MAN_OFFLINE_SIZE")[0].text
                                        m_off['app_man_off_description'] = manual.findall("./APP_MAN_OFFLINE_DESCRIPTION")[0].text
                                        m_off['app_man_off_lang'] = manual.findall("./APP_MAN_OFFLINE_LANG")[0].text
                                        man_off.append(m_off)
                                manuals['app_man_offline'] = man_off

				plataforms =[]
                                for app_plataform in application.findall("./APP_PLATAFORMS/APP_PLAT"):
                                        plataforms.append(app_plataform.text)

				minidescription = application.findall("./APP_MINIDESCRIPTION")[0].text
				
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
					app = App( [name, version, size, site, manuals, plataforms, minidescription, description, file, download_url, icon, icon_url, md5sum, categories, alternatives] )
					app.set_to_save(save)
					app_list.append(app)
				else:
					applicat.set_version(version)
					applicat.set_size(size)
					applicat.set_site(site)
					applicat.set_manuals(manuals)
					applicat.set_plataforms(plataforms)
					applicat.set_minidescription(minidescription)
					applicat.set_description(description)
					applicat.set_file_name(file)
					applicat.set_software_url(download_url)
					applicat.set_icon_name(icon)
					applicat.set_icon_url(icon_url)
					applicat.set_md5sum(md5sum)
					applicat.set_categories(categories)
					applicat.set_alternatives(alternatives)
					applicat.set_to_save(1)
                	app_list.sort()
                	return 1

	## Write the applications list to XML file.
	#
	# @param app_list - Applications list.
	#
	# @see DataFile.write_apps_to_XML_file()
	def write_to_XML_file(self, app_list ):
		DataFile.write_apps_to_XML_file( self, app_list )

## Class represent the Categories XML file input/output.
#
# @author David Barragán Merino <bameda [AT] di.uc3m [DOT] com>
# @author CRISOL-UC3M <htp://crisol.uc3m.es>
class CategoriesDataFile(DataFile):

	## Inicialice CategoriesDataFile.
	#
	# @param xml_file - XML path file.
	# @param dtd_file - DTD path file.
	#
	# @see DataFile.__init__()
	def __init__(self, xml_file, dtd_file ):
		DataFile.__init__(self, xml_file, dtd_file)
	
	## Add all categories from XML file to the categories list.
	#
	# @param category_list - The categories list.
	# @param save - The save value (0 to System Category 1 to User Category).
	# @return \em true/1 if it is correct or \em false/0 if isn't correct.
	def get_Categories(self, category_list, save =  0):
		if( DataFile.is_cheked(self) == 0):
			sys.stdout.write("EE The XML-File \"" + DataFile.get_XML_file(self) + "\" is not checked")
			return 0
		else:
			for category in DataFile.get_tree(self).findall("/./CATEGORY"):
				name = category.findall("./CAT_NAME")[0].text

				label = category.findall("./CAT_LABEL")[0].text

				description = category.findall("./CAT_DESCRIPTION")[0].text
				
				icon = category.findall("./CAT_ICON")[0].text

				icon_url = category.findall("./CAT_ICON_URL")[0].text

				categ =  Category.find_category(category_list, label)	
				if categ == None:
					cat = Category( [name, label, description, icon, icon_url] )
					cat.set_to_save(save)
					category_list.append(cat)
				else:
					categ.set_name(name)
					categ.set_description(description)
					categ.set_icon(icon)
					categ.set_icon_url(icon_url)
					categ.set_to_save(save)
                	return 1
	
	## Write the categories list to XML file.
	#
	# @param category_list - Categories list.
	#
	# @see DataFile.write_categories_to_XML_file()
	def write_to_XML_file(self, category_list ):
		DataFile.write_categories_to_XML_file(self, category_list )

## Class represent the Includes XML file input/output.
#
# @author David Barragán Merino <bameda [AT] di.uc3m [DOT] com>
# @author CRISOL-UC3M <htp://crisol.uc3m.es>
class IncludesDataFile(DataFile):
	
	## nicialice IncludesDataFile.
	#
	# @param xml_file - XML path file.
	# @param dtd_file - DTD path file.
	#
	# @see DataFile.__init__()
        def __init__(self, xml_file, dtd_file ):
                DataFile.__init__(self, xml_file, dtd_file)

	## Set the included status to all categories and applications from XML file to the categories list and applications list.
	#
	# @param category_list - The categories list.
	# @param app_list - The application list.
	# @return \em true/1 if it is correct or \em false/0 if isn't correct.
	def set_includes(self, category_list, app_list):	
		if( DataFile.is_cheked(self) == 0):
			sys.stderr.write("EE The XML-File \"" + DataFile.get_XML_file(self) + "\" is not checked")
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
	
	## Write the includes values to XML file.
	#
	# @param category_list - Categories list.
	# @param app_list - Applications list.
	#
	# @see DataFile.write_includes_to_XML_file()
	def write_to_XML_file(self, category_list, app_list ):
		DataFile.write_includes_to_XML_file( self, category_list, app_list )

if __name__=='__main__':
        pass
	
