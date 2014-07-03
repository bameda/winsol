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
os.chdir("/usr/share/winsol/")
import sys
import shutil
import winsollib

#
# WinSOL Configuration
#
#   see ./baseconfig/config
#       ~/.winsol/config
#

## WinSOL master directory path.
MASTER_DIR = "/usr/share/winsol"
## User config directory path.
CONFIG_DIR = os.getenv("HOME")+"/.winsol"

# DTD's

## System categories DTD file path.
CATEGORIES_DTD = MASTER_DIR + "/categories.dtd"
## System applications DTD file path.
APPS_DTD = MASTER_DIR + "/apps.dtd"
## System includes DTD file path.
INCLUDES_DTD = MASTER_DIR + "/includes.dtd"

# System's XML files

## System categories XML file path.
MASTER_CATEGORIES_XML = MASTER_DIR + "/categories.xml"
## System applications XML file path.
MASTER_APPS_XML = MASTER_DIR + "/apps.xml"

# User's XML files

## User categories XML file path.
USER_CATEGORIES_XML = CONFIG_DIR + "/categories.xml"
## User applications XML file path.
USER_APPS_XML = CONFIG_DIR + "/apps.xml"
## User includes XML file path.
USER_INCLUDES_XML = CONFIG_DIR + "/includes.xml"

# User's config variables

## User source image directory path.
IMAGE_DIR = CONFIG_DIR + "/image"
## User software directory path.
SOFTWARE_DIR = CONFIG_DIR + "/software"
## User icon directory path.
ICONS_DIR = CONFIG_DIR + "/icons"
## User manuals directory path.
MANUALS_DIR = CONFIG_DIR + "/manuals"
## User template html directory path.
TEMPLATE_DIR = MASTER_DIR+"/baseconfig/templates/default" 
## Coposition type.
IMAGE_TYPE = "iso"	# "zip" or "iso"
## User ISO file path.
ISO_FILE = CONFIG_DIR + "/WinSOL.iso"
## User ZIP file path.
ZIP_FILE = CONFIG_DIR + "/WinSOL.zip"
## User html directory path. 
HTML_DIR = IMAGE_DIR + "/html"


if not os.path.exists(CONFIG_DIR):
	os.mkdir(CONFIG_DIR)
	shutil.copy(MASTER_DIR+"/baseconfig/config",CONFIG_DIR+"/config")
	shutil.copy(MASTER_DIR+"/baseconfig/categories.xml",CONFIG_DIR+"/categories.xml")
	shutil.copy(MASTER_DIR+"/baseconfig/apps.xml",CONFIG_DIR+"/apps.xml")
	shutil.copy(MASTER_DIR+"/baseconfig/includes.xml",CONFIG_DIR+"/includes.xml")
	execfile(CONFIG_DIR+"/config")
else:
	if os.path.exists(CONFIG_DIR+"/config"): 
		execfile(CONFIG_DIR+"/config")
	else:
		shutil.copy(MASTER_DIR+"/baseconfig/config",CONFIG_DIR+"/config")
		execfile(CONFIG_DIR+"/config")

if not os.path.exists(CONFIG_DIR+"/categories.xml"):
	shutil.copy(MASTER_DIR+"/baseconfig/categories.xml",CONFIG_DIR+"/categories.xml")

if not os.path.exists(CONFIG_DIR+"/apps.xml"):
	shutil.copy(MASTER_DIR+"/baseconfig/apps.xml",CONFIG_DIR+"/apps.xml")

if not os.path.exists(CONFIG_DIR+"/includes.xml"):
	shutil.copy(MASTER_DIR+"/baseconfig/includes.xml",CONFIG_DIR+"/includes.xml")

## WinSOL Command Interface class.
#
# @author David Barragán Merino <bameda [AT] di.uc3m [DOT] com>
# @author CRISOL-UC3M <htp://crisol.uc3m.es>
class WinSOL:
	
	## Inicialiced tthe new image object.
	#
	# @param xml_files  (\c list[5]) The XML files path (sys_categories, sys_apps, user_categories, user_apps, user_includes).
	# @param dtd_files  (\c list[3]) The DTD files path (categories, apps, includes)
	def __init__(self, xml_files, dtd_files):
		self.__xml_files = []
		self.__xml_files = xml_files
		self.__dtd_files = []
		self.__dtd_files = dtd_files
		self.__image = winsollib.Image(self.__xml_files, self.__dtd_files)

	## Generate the image html files.
	#
	# @param image_dir - The image directory path.
	# @param template_dir  The templates directory path.
	def html(self, image_dir, template_dir):
		if not os.path.exists( image_dir ): 
			os.mkdir( image_dir )
                if not os.path.exists( image_dir + "/html" ): 
			os.mkdir( image_dir + "/html" )
		else:
			os.system( "rm -rf '" + image_dir + "/html"  + "'" )
			os.mkdir( image_dir+"/html" )

		self.__image.gen_html(image_dir+"/html", template_dir )

	## List all categories and applications.
	#
	def list(self):
		for category in self.__image.get_all_categories():
        		if category.is_included(): 
				print "\t+ " + category.get_name() +" (" + category.get_label() + ")" 
                        elif not category.is_included(): 
				print "\t- " + category.get_name() +" (" + category.get_label() + ")"
			for app in self.__image.get_apps_by_category( category.get_label() ):
        	        	if app.is_included(): 
					print "\t  + " + app.get_name()
                        	elif not app.is_included():
					print "\t  - " + app.get_name()

	## List all applications with its versions.
	#
	# This method is only for development. 
	def list_apps(self):
		for app in self.__image.get_all_apps():
			print "\t\t" + app.get_name() + " " + app.get_version()

	## Add a new Category.
	#
	def add_category(self):
	        print "Write the \"Category Name\": ",
                name = raw_input()
                print "Write the \"Category Label\": ",
                label = raw_input()
		print "Write the \"Category Description\": ",
                description = raw_input()
                print "Write the \"Category Icon file name\": ",
		icon = raw_input()
		print "Write the \"Category Icon file URL\": ",
		icon_url = raw_input()

                if ( self.__image.add_category( [name, label, description, icon, icon_url] )):
			print "!! Adding \"" + name + "\" category." 
			self.__image.save_categories_to_xml_file()
		else:
			print "EE Unable to add the new category, it's possible that there is another one with the same label."

	## Delete the Category with the same label as \em label param.
	#
	# @param label - Label of any Category.
	def del_category(self, label = ""):
		if self.__image.del_category(label):
			print "!! Deleting category \"" + label + "\""
			self.__image.save_categories_to_xml_file()
			self.__image.save_includes_to_xml_file()
		else:
			print "EE Unable to delete the category. It's possible that there isn't any category with this label or this category is protected"	

	## Modify the Category with the same label as \em label param.
	#
	# @param label - Label of any category.
	def modify_category(self, label):
		if self.__image.get_category_by_label(label) == None:
			print "EE There isn't any category with that label"
		else:
			dict = self.__image.get_category_dict_by_label(label)
			values = []
			
			print "Write the \"Category Name\" (default: \"" + dict['name'] + "\"): ",
			name = raw_input()
			if name == "": name = dict['name']
			values.append(name)
			
			print "Write the \"Category Description\" (default: \"" + dict['description'] + "\"): ",
                        description = raw_input()
                        if description == "": description = dict['description']
                        values.append(description)

			print "Write the \"Category Icon file name\" (default: \"" + dict['icon'] + "\"): ",
                        icon = raw_input()
			if icon == "": icon = dict['icon']
			values.append(icon)
									
                        print "Write the \"Category Icon file URL\" (default: \"" + dict['icon_url'] + "\"): ",
			icon_url = raw_input()
			if icon_url == "": icon = dict['icon_url']
			values.append(icon_url)

			if self.__image.modify_category_values(label, values):
				print "!! Modify \"" + name + "\" category." 
				self.__image.save_categories_to_xml_file()
				self.__image.save_applications_to_xml_file()
			else:
				# Imposible
				print "EE There is already a category with that label."

	## Select the Category with the same label as \em label param.
	#
	# @param label - Label of any Category.
	def select_category(self, label):
		if self.__image.select_category(label):
			print "!! The category is selected"
			self.__image.save_includes_to_xml_file()
		else:
			print "EE There isn't any category with that label"

	## Select all categories.
	#
	def select_all_categories(self):
		if self.__image.select_all_categories():	
			print "!! All categories are selected"
			self.__image.save_includes_to_xml_file()
		else:
			print "EE Unable to selected all categories"

	## Unselect the Category with the same label as \em label param.
	#
	# @param label - Label of any Category.
	def unselect_category(self, label):
		if self.__image.unselect_category(label):
			print "!! The category is unselected"
			self.__image.save_includes_to_xml_file()
		else:
			print "EE There isn't any category with that label"

	## Unselect all categories.
	#
	def unselect_all_categories(self):
		if self.__image.unselect_all_categories():	
			print "!! All categories are unselected"
			self.__image.save_includes_to_xml_file()
		else:
			print "EE Unable to unselected all categories"

	## View the information from a Category with the same label as \em label param.
	#
	# @param label - Label of any Category.
	def view_category(self, label):
		if self.__image.get_category_by_label(label) == None:
			print "EE There isn't any category with that label"
		else:
			dict = self.__image.get_category_dict_by_label(label)
			print " CATEGORY DETAILS:"
			print ""
			print "   NAME:\t\t" + dict['name']
			print "   LABEL:\t\t" + dict['label']
			print "   DESCRIPTION:\t\t" + dict['description']
			print "   ICON:\t\t" + dict['icon']
			print "   ICON URL:\t\t" + dict['icon_url']
			if dict["included"]: print "   INCLUDED:\t\tyes"
			else: print "   INCLUDED:\t\tno"
			if len( dict['apps'] ) > 0:
				print "   APLICATIONS:"
				for app in dict['apps']:
					print "         \t\t- " + app['name']
			print""
	
	## Add a new App.
	#
	def add_application(self):
		print "Name: ",
                name = raw_input()
		print "Version: ",
		version = raw_input()
		print "Size: ",
		size = raw_input()
                print "Site: ",
                site = raw_input()
		manuals = {}
		manuals['app_man_online'] = []
		manuals['app_man_offline'] = []
		man_on = "-"
		while man_on != None:
			man_on = {}
			print "Online Manual Name (press ENTER to finish): ",
			man_on['app_man_on_name'] = raw_input()
			if (man_on['app_man_on_name'] != ""):
				print "Online Manual URL: ",
	                        man_on['app_man_on_url'] = raw_input()
				print "Online Manual Description: ",
                	        man_on['app_man_on_description'] = raw_input()
				print "Online Manual Language: ",
                        	man_on['app_man_on_lang'] = raw_input()
				manuals['app_man_online'].append(man_on)
			else:
				man_on = None
		man_off = "-"
                while man_off != None:
                        man_off = {}
                        print "Offline Manual Name (press ENTER to finish): ",
                        man_off['app_man_off_name'] = raw_input()
                        if (man_off['app_man_off_name'] != ""):
                                print "Offline Manual URL: ",
                                man_off['app_man_off_url'] = raw_input()
				print "Offline Manual File Name: ",
                                man_off['app_man_off_file'] = raw_input()
				print "Offline Manual File Size: ",
				man_off['app_man_off_size'] = raw_input()
                    	        print "Offline Manual Description: ",
                                man_off['app_man_off_description'] = raw_input()
                                print "Offline Manual Language: ",
                                man_off['app_man_off_lang'] = raw_input()
                                manuals['app_man_offline'].append(man_off)
                        else:
                                man_off = None                
		plataforms = []
                plat = None
                while plat != "":
                        if plat != None:
                                plataforms.append(plat)
                        print "Platforms (press ENTER to finish): ",
                        plat = raw_input()
                print "Mini-Description: ",
		minidescription = raw_input()
		print "Description: ",
                description = raw_input()
                print "File: ",
                file = raw_input()
                print "Software URL: ",
                software_url = raw_input()
                print "Icon: ",
                icon = raw_input()
                print "Icono URL (press ENTER to ignore): ",
                icon_url = raw_input()
                print "MD5Sum (press ENTER to ignore): ",
                md5sum = raw_input()
                categories = []
                category = None
                while category != "":
                        if category != None:
                                categories.append(category)
                        print "Categories (press ENTER to finish): ",
                        category = raw_input()
                alternatives = []
                alt = None
                while alt != "":
                        if alt != None:
                                alternatives.append(alt)
                        print "Alternatives (press ENTER to finish): ",
                        alt = raw_input()
		
		if self.__image.add_app( [name, version, size, site, manuals, plataforms, minidescription, description, file, software_url, icon, icon_url, md5sum, categories, alternatives ] ):
			print "!! Adding \"" + name + "\" application."
			self.__image.save_applications_to_xml_file()
		else:
			print "EE Unable to add the new application, it's possible that there is another one with the same name."

	## Delete the App with the same name as \em name param.
	#
	# @param name - Name of any App.
	def del_application(self, name):
		if self.__image.del_app(name):
			print "!! Deleting application \"" + name + "\""
			self.__image.save_applications_to_xml_file()
			self.__image.save_includes_to_xml_file()
		else:
			print "EE Unable to delete the application. It's possible that there isn't any application with that name or the application is protected"
	
	## Modify the App with the same name as \em name param.
	#
	# @param name - Name of any application.
	def modify_application(self, name):
		if self.__image.get_app_by_name(name) == None:
			print "EE There isn't any category with this label"
		else:
			dict = self.__image.get_app_dict_by_name(name)
			values = []

			print "Write the \"App Version\" (default: \"" + dict['version'] + "\"): ",
			version = raw_input()
			if version == "": version = dict['version']
			values.append(version)

			print "Write the \"App Size\" (default: \"" + str(dict['size']) + "\"): ",
			size = raw_input()
			if size == "": size = dict['size']
			values.append(size)

			print "Write the \"App Site\" (default: \"" + dict['site'] + "\"): ",
			site = raw_input()
			if site == "": site = dict['site']
			values.append(site)
			
			manuals = {}
			manuals['app_man_online'] = []
			manuals['app_man_offline'] = []
			man_on = ""
			for manual in dict['manuals']['app_man_online']:
				if (man_on != ""): man_on = man_on + "\n         "
				man_on = man_on  + "=>" + manual['app_man_on_name'] + "\", \"" + manual['app_man_on_url'] + "\", \"" + manual['app_man_on_description'] + "\", \"" + manual['app_man_on_lang'] + "\""  
			print "Write \"default\" to get the default \"App Online Manuals\" or press ENTER to add new ones"
			print "default: " + man_on + ": ",
			man_on  = raw_input()
			if man_on == "default":
                                manuals['app_man_online'] = dict['manuals']['app_man_online']
			else:
				man_on = "-"
                		while man_on != None:
                        		man_on = {}
                        		print "Online Manual Name (press ENTER to finish): ",
                        		man_on['app_man_on_name'] = raw_input()
                        		if (man_on['app_man_on_name'] != ""):
                                		print "Online Manual URL: ",
                                		man_on['app_man_on_url'] = raw_input()
                                		print "Online Manual Description: ",
                                		man_on['app_man_on_description'] = raw_input()
                                		print "Online Manual Language: ",
                                		man_on['app_man_on_lang'] = raw_input()
                                		manuals['app_man_online'].append(man_on)
                        		else:
                                		man_on = None
			man_off = ""
                        for manual in dict['manuals']['app_man_offline']:
                                if (man_off != ""): man_off = man_off + "\n         "
                                man_off = man_off  + "=>" + manual['app_man_off_name'] + "\", \"" + manual['app_man_off_url'] + "\", \"" + manual['app_man_off_file'] + "\", \"" + str(manual['app_man_off_size']) + "\"KB, \"" + manual['app_man_off_description'] + "\", \"" + manual['app_man_off_lang'] + "\""
                        print "Write \"default\" to get the default \"App Offline Manuals\" or press ENTER to add new ones"
			print "default: " + man_off + ": ",
                        man_off  = raw_input()
                        if man_off == "default":
                                manuals['app_man_offline'] = dict['manuals']['app_man_offline']
                        else:
				man_off = "-"
		                while man_off != None:
	        	                man_off = {}
                		        print "Offline Manual Name (press ENTER to finish): ",
                		        man_off['app_man_off_name'] = raw_input()
		                        if (man_off['app_man_off_name'] != ""):
		                                print "Offline Manual URL: ",
		                                man_off['app_man_off_url'] = raw_input()
        		                        print "Offline Manual File Name: ",
        		                        man_off['app_man_off_file'] = raw_input()
						print "Offline Manual Size: ",
						man_off['app_man_off_size'] = raw_input()
        		                        print "Offline Manual Description: ",
        		                        man_off['app_man_off_description'] = raw_input()
        		                        print "Offline Manual Language: ",
        		                        man_off['app_man_off_lang'] = raw_input()
        		                        manuals['app_man_offline'].append(man_off)
        		                else:
        		                        man_off = None	
			values.append(manuals)	

			p = ""
                        for ptf in dict['plataforms']:
                                if ptf != None:
                                        p =  p + ", " + ptf
                        print "Write \"default\" to get the default \"App Platforms\" or press ENTER to add new ones (default: \"" + p + "\"): ",
                        plat = raw_input()
                        plataforms = []
                        if plat == "default":
                                plataforms = dict['plataforms']
                        else:
                                plat = "-"
                                while plat != "":
                                        print "Platforms (press ENTER to finish): ",
                                        plat = raw_input()
                                        if plat != "":
                                                plataforms.append(plat)
                        values.append(plataforms)

			print "Write the \"App Mini-Description\" (default: \"" + dict['minidescription'] + "\"): ",
                        minidescription = raw_input()
                        if minidescription == "": minidescription = dict['minidescription']
                        values.append(minidescription)

			print "Write the \"App Description\" (default: \"" + dict['description'] + "\"): ",
			description = raw_input()
			if description == "": description = dict['description']
			values.append(description)

			print "Write the \"App File\" (default: \"" + dict['file'] + "\"): ",
			file = raw_input()
			if file == "": file = dict['file']
			values.append(file)

			print "Write the \"App Software URL\" (default: \"" + dict['software_url'] + "\"): ",
			software_url = raw_input()
			if software_url == "": software_url = dict['software_url']
			values.append(software_url)
			
			print "Write the \"App Icon\" (default: \"" + dict['icon'] + "\"): ",
			icon = raw_input()
			if icon == "": icon = dict['icon']
			values.append(icon)

			if dict['icon_url'] == None:
					print "Write the \"App Icon URL\" (default: \"\"): ",
					icon_url = raw_input()
			else:
				print "Write the \"App Icon URL\" (default: \"" + dict['icon_url'] + "\"): ",
				icon_url = raw_input()
				if icon_url == "": icon_url = dict['icon_url']
			values.append(icon_url)

			print "Write the \"App MD5Sum\" (default: \"" + dict['md5sum'] + "\"): ",
			md5sum = raw_input()
			if md5sum == "": md5sum = dict['md5sum']
			values.append(md5sum)

			c = ""
			for ctg in dict['categories']:
				if ctg != None: 
					c =  c + ", " + ctg 
			print "Write \"default\" to get the default \"App Categories\" or press ENTER to add new ones (default: \"" + c + "\"): ",
			cat = raw_input()
			categories = []
			if cat == "default": 
				categories = dict['categories']
			else:
				cat = "-"
				while cat != "":
					print "Categories (press ENTER to finish): ",
					cat = raw_input()
					if cat != "":
                          	      		categories.append(cat)
			values.append(categories)

			a = ""
			for atn in dict['alternatives']:
				if atn != None: 
					a = a + ", " + atn 
			print "Write the \"App Alternatives\" (default: \"" + a + "\"): ",
			alt = raw_input()
			alternatives = []
			if alt == "": 
				alternatives = dict['alternatives']
			else:
				while alt != "":
					if alt != None:
                          	      		alternatives.append(alt)
					print "Alternatives (press ENTER to finish): ",
					alt = raw_input()
			values.append(alternatives)

			if self.__image.modify_app_values(name, values):
				print "!! Modify \"" + name + "\" application." 
				self.__image.save_applications_to_xml_file()
			else: 
				print "EE There is already an application with that name."
	
	## Select the App with the same name as \em name param.
	#
	# @param name - Name of any App.
	def select_application(self, name):
		if self.__image.select_app(name):
			print "!! The application is selected"
			self.__image.save_includes_to_xml_file()
		else:
			print "EE There isn't any application with that name"
	
	## Select all aplications.
	#
	def select_all_applications(self):
		if self.__image.select_all_apps():
			print "!! All the applications are selected"
			self.__image.save_includes_to_xml_file()
		else:
			print "EE Unable to select all applications"
        
	## Select all aplications include in a Category with the same label as \em category_label param.
	#
	# @param category_label - Label of any Category.
	def select_all_applications_by_category(self, category_label):
		if self.__image.select_apps_by_category(category_label):
			print "!! All applications from \"" + category_label + "\" category are selected"
			self.__image.save_includes_to_xml_file()
		else:
			print "EE There isn't any category with that name"

	## Unselect the App with the same name as \em name param.
	#
	# @param name - Name of any App.
	def unselect_application(self, name):
		if self.__image.unselect_app(name):
                        print "!! The application is unselected"
                        self.__image.save_includes_to_xml_file()
                else:
                        print "EE There isn't any application with that name"

	## Unselect all applications.
	#
	def unselect_all_applications(self):
		if self.__image.unselect_all_apps():
			print "!! All the applications are unselected"
			self.__image.save_includes_to_xml_file()
		else:
			print "EE Unable to unselect all applications"
        
	## Unselect all aplications include in a Category with the same label as \em category_label param.
	#
	# @param category_label - Label of any Category.
	def unselect_all_applications_by_category(self, category_label):
		if self.__image.unselect_apps_by_category(category_label):
			print "!! All applications from \"" + category_label + "\" category are unselected"
			self.__image.save_includes_to_xml_file()
		else:
			print "EE There isn't any category with that name"
	
	## View the information from an App with the same name as \em name param.
	#
	# @param name - Name of any App.
	def view_application(self, name):
		if self.__image.get_app_by_name(name) == None:
			print "EE There isn't any application with that name"
		else:
			dict = self.__image.get_app_dict_by_name(name)
			print " APPLICATION DETAILS:"
			print ""
			print "   NAME:\t\t" + dict['name']
			print "   VERSION:\t\t" + dict['version']
			print "   SIZE (KB):\t\t" + str(dict['size'])
			print "   SITE:\t\t" + dict['site']
			if ( (len(dict['manuals']['app_man_online']) > 0) or (len(dict['manuals']['app_man_offline']) > 0) ): print "   MANUALS"
			if ( len(dict['manuals']['app_man_online']) > 0 ):
				print "     ONLINE MANUALS:"
				for man in dict['manuals']['app_man_online']:
					print "     \t=> NAME:\t\t" + man['app_man_on_name']
					print "     \t   URL:\t\t\t" + man['app_man_on_url']
					print "     \t   LANGUAGE:\t\t" + man['app_man_on_lang']
					print "     \t   DESCRIPTION:\t\t" + man['app_man_on_description']
					
			if ( len(dict['manuals']['app_man_offline']) > 0 ):
                        	print "     OFFLINE MANUALS:"
                                for man in dict['manuals']['app_man_offline']:
                                        print "     \t=> NAME:\t\t" + man['app_man_off_name']
                                        print "     \t   URL:\t\t\t" + man['app_man_off_url']
					print "     \t   FILE NAME:\t\t" + man['app_man_off_file']
					print "     \t   SIZE (KB):\t\t" + str(man['app_man_off_size'])
                                        print "     \t   LANGUAGE:\t\t" + man['app_man_off_lang']
                                        print "     \t   DESCRIPTION:\t\t" + man['app_man_off_description']
			if len( dict['plataforms'] ) > 0:
                                print "   PLATFORMS:"
                                for plat in dict['plataforms']:
                                        print "         \t\t" + plat
			print "   FILE:\t\t" + dict['file']
			print "   SOFTWARE URL:\t" + dict['software_url']
			print "   ICON:\t\t" + dict['icon']
			if dict['icon_url'] != None:print "   ICON URL:\t\t" + dict['icon_url']
			print "   MD5SUM:\t\t" + dict['md5sum']
			if dict['included']: print "   INCLUDED:\t\tyes"
			else: print "   INCLUDED:\t\tno"
			if len( dict['categories'] ) > 0:
				print "   CATEGORIES:"
				for cat in dict['categories']:
					print "         \t\t" + cat	
			if len( dict['alternatives'] ) > 0:
				print "   ALTERNATIVES:"
				for alt in dict['alternatives']:
					if alt != None:
						print "         \t\t" + alt
			print "   MINI-DESCRIPTION:\t" + dict['minidescription']
			print "   DESCRIPTION:\t\t" + dict['description']
			print""

	## Remove the \em imagen_dir source directory.
	#
	# @param image_dir - User image source directory path.
	def clean(self, image_dir):
                os.system( "rm -rf '"+ image_dir +"'" )

	## Remove the user 'config_dir' directory.
	#
	# @param config_dir - User configuration directory path.
	def mrproper(self, config_dir):
                os.system( "rm -rf '"+ config_dir +"'" )
	
	## Make an Iso image from the imagen source directory.
	#
	# @param image_dir - User image source directory path.
	# @param iso_file - User iso file path.
	def iso(self, image_dir, iso_file):
		self.__image.make_iso( image_dir, iso_file )

	## Make an Zip file from the imagen source directory.
	#
	# @param image_dir - User image source directory path.
	# @param zip_file - User zip file path.
	def zip(self, image_dir, zip_file):
		self.__image.make_zip( image_dir, zip_file )

	## Show the Image Size
	#
	def size(self):
		print "\t- The Actual Image size is %d KB." % (self.__image.calculate_size())

	## Download all files (software, manuals and icons) to make an iso file.
	#
	# @param software_dir - User software directory path.
	# @param icon_dir - User icon directory path.
	# @param manual_dir - User manuals directory path.
	def download(self, software_dir, icon_dir, manual_dir):
		if not os.path.exists( software_dir ): os.mkdir( software_dir )
		if not os.path.exists( icon_dir ): os.mkdir( icon_dir )
		if not os.path.exists( manual_dir ): os.mkdir( manual_dir )
		
		self.__image.download_software( software_dir )
	 	self.__image.download_icons( icon_dir )
		self.__image.download_manuals( manual_dir)

		self.__image.save_applications_to_xml_file()
                self.__image.save_includes_to_xml_file()

	## Create the user source image directory.
	#
	# \li Cretae the structure.
	# \li Create links to all selected aplications software, icons and manuals.
	# \li Create links to cd-base files (cd icon, autoeun,...i).
	#
	# @param image_dir - The image directory path.
	# @param software_dir - The software directory path.
	# @param icons_dir - The icons directory path.
	# @param manual_dir - The manuals directory path.
	# @param master_dir - The WinSOL master directory path.
	def copy( self, image_dir, software_dir, icons_dir, manual_dir, master_dir ):
		""" Create the user source image directory: 

		\li Cretae the structure.
		\li Create links to all selected aplications software, icons and manuals.
		\li Create links to cd-base files (cd icon, autoeun,...)
		"""
		if not os.path.exists( image_dir ): os.mkdir( image_dir )
		if not os.path.exists( image_dir + "/software" ): os.mkdir(image_dir + "/software" )
		if not os.path.exists( image_dir + "/html" ): os.mkdir(image_dir + "/html" )
		if not os.path.exists( image_dir + "/html/icons" ): os.mkdir( image_dir + "/html/icons" )
		if not os.path.exists( image_dir + "/manuals" ): os.mkdir(image_dir + "/manuals" )
		for category in self.__image.get_all_categories():
			if category.is_included():
				if not os.path.exists(image_dir + "/html/icons/" + category.get_icon()):
					if os.path.exists(icons_dir + "/" + category.get_icon()):
						os.symlink( icons_dir + "/" + category.get_icon(), image_dir + "/html/icons/" + category.get_icon() )

				for app in category.get_all_apps():
					if app.is_included():
						if not os.path.exists( image_dir + "/software/" + app.get_file_name() ):
							if os.path.exists( software_dir + "/" + app.get_file_name() ):
								os.symlink( software_dir + "/" + app.get_file_name(), image_dir + "/software/" + app.get_file_name() )
						if not os.path.exists( image_dir + "/html/icons/" + app.get_icon_name() ):
							if  os.path.exists( icons_dir + "/" + app.get_icon_name() ):
								os.symlink( icons_dir + "/" + app.get_icon_name(), image_dir + "/html/icons/" + app.get_icon_name() )
						for manual in app.get_manuals()['app_man_offline']:
							if not os.path.exists( image_dir + "/manuals/" + manual['app_man_off_file'] ):
								if os.path.exists( manual_dir + "/" + manual['app_man_off_file'] ):
									os.symlink( manual_dir + "/" + manual['app_man_off_file'], image_dir + "/manuals/" + manual['app_man_off_file'] )

		if not os.path.exists( image_dir + "/autorun.inf" ): os.symlink( master_dir + "/cd-base/autorun.inf", image_dir + "/autorun.inf" )
		if not os.path.exists( image_dir + "/browsercall.exe" ): os.symlink( master_dir + "/cd-base/browsercall.exe", image_dir + "/browsercall.exe" )
		if not os.path.exists( image_dir + "/logo.ico" ):os.symlink( master_dir + "/cd-base/logo.ico", image_dir + "/logo.ico" )

	## @var __dtd_files
	# A DTD file path List.

	## @var __xml_files
	# A XML file path List. 

	## @var __image
	# Image Object.
	# @see winsollib.Image


"""------------------------------------"""

## Function that print the WinSOL help.
#
def print_help():
	print "Usage: " + sys.argv[0] + " <option> [parameter]\n"
	print "Options:"
	print ""
	print "  Operations over applications:"
	print "    add_app\t\t\t\t\t  Add an application."
	print "    del_app <app-name>\t\t\t\t  Remove an application."
	print "    mod_app <app-name>\t\t\t\t  Modify an application."
	print "    select_app <app-name>\t\t\t  Select applications to include."
	print "    select_all_apps\t\t\t\t  Select all applications."
	print "    select_all_apps_by_categ <categ-label>\t  Select all applications by category."
	print "    unselect_app <app-name>\t\t\t  Unselect applications to include."
	print "    unselect_all_apps\t\t\t\t  Unselect all applications."
        print "    unselect_all_apps_by_categ <categ-label>\t  Unselect all applications by category."
	print "    view_app <app-name>\t\t\t\t  View an application details,"
	print ""
	print "  Operations over categories:"
	print "    add_categ\t\t\t\t\t  Add a category."
	print "    del_categ <categ-label>\t\t\t  Remove a category."
	print "    mod_categ <categ-label>\t\t\t  Modify a category,"
	print "    select_categ <categ-label>\t\t\t  Select categories to include."
	print "    select_all_categ\t\t\t\t  Select all categories,"   
	print "    unselect_categ <categ-label>\t\t  Unselect categories to include."
	print "    unselect_all_categ\t\t\t\t  Select all categories,"
	print "    view_categ <categ-label>\t\t\t  View a category details,"
	print ""
	print "    select_all\t\t\t\t\t  Select all applications and categories."
	print "    unselect_all\t\t\t\t  Unselect all applications and categories."
	print ""
	print ""
	print "  Image options:"	
	print "    all\t\t\t\t\t\t  Execute html, copy and zip/iso actions."
	print "    clean\t\t\t\t\t  Clean the image directory."
	print "    copy\t\t\t\t\t  Copy base files, software and icons."
	print "    download\t\t\t\t\t  Download the necessary software."
	print "    html\t\t\t\t\t  Generate html files into the image."
	print "    iso\t\t\t\t\t\t  Generate an iso image from image directory."
	print "    zip\t\t\t\t\t\t  Generate an zip file from image directory."
	print "    size\t\t\t\t\t  Show the Imagen Size (in KB)."
	print "    list\t\t\t\t\t  List all applications and the status."
	print "    mrproper\t\t\t\t\t  Clean the user config dir."
	print ""
	print "  EXAMPLE:"
	print "    To make a Iso image with all categories and applications do:"
	print "         winsol select_all"
	print "         winsol download"
	print "         winsol copy"
	print "         winsol html"
	print "         winsol iso"
	print "    or"
	print "        winsol select_all"
	print "        winsol all" 

if len( sys.argv ) < 2 or len ( sys.argv ) > 3:
	print_help()
else:
	
	xml_files = [ MASTER_CATEGORIES_XML, MASTER_APPS_XML, USER_CATEGORIES_XML, USER_APPS_XML, USER_INCLUDES_XML ]
	dtd_files = [ CATEGORIES_DTD, APPS_DTD, INCLUDES_DTD]

#	try:
 	winsol = WinSOL( xml_files, dtd_files )
#	except Exception, e:	
#		print"EE Error. the program finish."
	
	if sys.argv[1] == "html":
		winsol.html( IMAGE_DIR, TEMPLATE_DIR )
        elif sys.argv[1] == "clean":
		winsol.clean(IMAGE_DIR)
	elif sys.argv[1] == "mrproper":
		winsol.mrproper(CONFIG_DIR)
	elif sys.argv[1] == "iso":
		winsol.iso(IMAGE_DIR, ISO_FILE)
	elif sys.argv[1] == "zip":
		winsol.zip(IMAGE_DIR, ZIP_FILE)
	elif sys.argv[1] == "download":
		winsol.download(SOFTWARE_DIR, ICONS_DIR, MANUALS_DIR)
	elif sys.argv[1] == "copy":
		winsol.copy(IMAGE_DIR, SOFTWARE_DIR, ICONS_DIR, MANUALS_DIR, MASTER_DIR)
	elif sys.argv[1] == "size":
		winsol.size()
	elif sys.argv[1] == "all":
		winsol.clean(IMAGE_DIR)
		winsol.download(SOFTWARE_DIR, ICONS_DIR, MANUALS_DIR)
		winsol.html(IMAGE_DIR, TEMPLATE_DIR)
		winsol.copy(IMAGE_DIR, SOFTWARE_DIR, ICONS_DIR, MANUALS_DIR, MASTER_DIR)
		if IMAGE_TYPE == "zip": winsol.zip(IMAGE_DIR, ZIP_FILE)
		else: winsol.iso(IMAGE_DIR, ISO_FILE)
		
	elif sys.argv[1] == "list":
		winsol.list()
	elif sys.argv[1] == "list_apps":
		winsol.list_apps()
	# Categories functions
	elif sys.argv[1] == "add_categ":
		winsol.add_category()
	elif sys.argv[1] == "del_categ":
		winsol.del_category(sys.argv[2])
	elif sys.argv[1] == "mod_categ":
		winsol.modify_category(sys.argv[2])
	elif sys.argv[1] == "select_categ":
		winsol.select_category(sys.argv[2])
	elif sys.argv[1] == "select_all_categ":
		winsol.select_all_categories()
	elif sys.argv[1] == "unselect_categ":
		winsol.unselect_category(sys.argv[2])
	elif sys.argv[1] == "unselect_all_categ":
		winsol.unselect_all_categories()
	elif sys.argv[1] == "view_categ":
		winsol.view_category(sys.argv[2])
	# Applications fuction
	elif sys.argv[1] == "add_app":
		winsol.add_application()
	elif sys.argv[1] == "del_app":
		winsol.del_application(sys.argv[2])
	elif sys.argv[1] == "mod_app":
		winsol.modify_application(sys.argv[2])
	elif sys.argv[1] == "select_app":
		winsol.select_application(sys.argv[2])
	elif sys.argv[1] == "select_all_apps":
                winsol.select_all_applications()
	elif sys.argv[1] == "select_all_apps_by_categ":
                winsol.select_all_applications_by_category(sys.argv[2])
	elif sys.argv[1] == "unselect_app":
		winsol.unselect_application(sys.argv[2])
	elif sys.argv[1] == "unselect_all_apps":
                winsol.unselect_all_applications()
        elif sys.argv[1] == "unselect_all_apps_by_categ":
                winsol.unselect_all_applications_by_category(sys.argv[2])
	elif sys.argv[1] == "view_app":
		winsol.view_application(sys.argv[2])
	elif sys.argv[1] == "select_all":
                winsol.select_all_categories()
		winsol.select_all_applications()
	elif sys.argv[1] == "unselect_all":
                winsol.unselect_all_categories()
                winsol.unselect_all_applications()
	else:
		print_help()

	## @var xml_files
	# A XML file path List.

	## @var dtd_files
	# A DTD file path List.

	## @var winsol
	# A WinSol Object.
	# @see WinSOL

