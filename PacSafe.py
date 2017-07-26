# -*- coding: utf-8 -*-
"""
/***************************************************************************
 PacSafe
                                 A QGIS plugin
 PacSAFE produces realistic natural hazard impact scenarios for better planning, preparedness and response activities for Pacific Countries
                              -------------------
        begin                : 2015-03-29
        git sha              : $Format:%H$
        copyright            : (C) 2015 by Secretariat of the Pacific Community
        email                : sachindras@spc.int
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from PyQt4.QtCore import QSettings, QTranslator, qVersion, QCoreApplication
from PyQt4.QtGui import QAction, QIcon, QMessageBox
from PyQt4.QtGui import *
import resources
#import resources_rc
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import os, sys
import urllib2


# Initialize Qt resources from file resources.py

# Import the code for the dialog
from PacSafe_dialog import PacSafeDialog
import os.path
import os
#import safe.gui.widgets.dock
import time

def injectionTest(dock):
        #time.sleep(10)
        print dock.inasafe_version
        print "PacSafe Init ***************"
        
        #QMessageBox.about(self.dlg, "Test", "Success")

def my_accept_begin_hook(dock):
    #print dock.inasafe_version
    print "Marco's Hook - my new accept_begin_hook()"


class PacSafe:
    """QGIS Plugin Implementation."""
    
    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """



        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'PacSafe_{}.qm'.format(locale))
        
        splash_pix = QPixmap('splash.png')
        splash = QSplashScreen(splash_pix, Qt.WindowStaysOnTopHint)
        splash.setMask(splash_pix.mask())
        QApplication.processEvents()
        QCoreApplication.instance().processEvents()
        splash.show()
        QApplication.processEvents()
        QCoreApplication.instance().processEvents()

        QApplication.processEvents()

        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("Loading PacSafe...")
        msg.setInformativeText("Tonga Profile")
        msg.setWindowTitle("PacSafe")
        msg.setStandardButtons(QMessageBox.Ok) # | QMessageBox.Cancel)
        # retval = msg.exec_()
        QApplication.processEvents()
        QCoreApplication.instance().processEvents()
        time.sleep(5)
        QApplication.processEvents()
        QCoreApplication.instance().processEvents()
        #QApplication.processEvents()

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # Create the dialog (after translation) and keep reference
        self.dlg = PacSafeDialog()

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&PacSafe')
        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(u'PacSafe')
        self.toolbar.setObjectName(u'PacSafe')
        
        btn = self.dlg.btn
        btn.clicked.connect(self.openProject)
        
        # Load projects dynamically:
        self.path = os.getcwd() + "/data/"

        # Set a globally-accessible list of countries for which we have
        # projects & data available. The two-letter abbreviation must match 
        # the name of the sub-directory in the project/data folders.
        self.countryList = {"Fiji":"FJ", 
                            "Tonga":"TO"}

        for c in sorted(self.countryList.keys()):
            self.dlg.countryListWidget.addItem(c)

        cl = self.dlg.countryListWidget
        self.updateProjectList(0)
        cl.currentIndexChanged.connect(self.updateProjectList)


        btnRemote = self.dlg.btnRemote
        btnRemote.clicked.connect(self.openRemote)

    def updateProjectList(self, i):
        """
        Update the list of locally-available projects based on the selected
        country.
        """

        cl = self.dlg.countryListWidget
        self.cv = cl.currentText()
        prjPath = os.path.join(self.path, self.countryList[self.cv])
        self.dlg.listWidget.clear()
        for f in os.listdir(prjPath):
            if f.endswith(".qgs"):
                f = f.replace(".qgs", "")
                f = f.replace("_", " ")
                f = f.title()
                item = QListWidgetItem(f)
                self.dlg.listWidget.addItem(item)

        
    def openRemote(self):
        try:
            #QMessageBox.about(self.dlg, "Remote Projects", "Open Remote Projects...")
            local = []
            remote =[]
            #build list of remote index
            url = "https://raw.githubusercontent.com/sopac/pacsafe-projects/master/{0}/index.txt".format(self.countryList[self.cv].lower())
            response = urllib2.urlopen(url) 
            for l in response:
                if l.strip().endswith(".qgs"):
                    #print l.strip()
                    remote.append(l.strip())

            #build local list
            path = os.path.join(os.getcwd(), "/data/", self.countryList[self.cv].lower())
            for f in os.listdir(path):
                if f.endswith(".qgs"):
                    local.append(f.strip())

            #compare list
            flist = local + remote
            flist = list(set(flist))
            #print flist
            getlist = []
            for f in flist:
                if f not in local:
                    getlist.append(f)

            msg = "There are no new remote projects available for {0}.".format(self.cv)
            sync = False
            
            if len(getlist) > 0:
                sync = True
                diff = len(getlist)            
                msg = "There are " + str(diff) + " new project(s) available for {0}.\r\nClick Ok To Synchronise.".format(self.cv)

            QMessageBox.about(self.dlg, "Remote Projects", msg)

            if sync == True:
                #sync/download new layers                    
                for n in getlist:
                    print n
                    tf = urllib2.urlopen("https://raw.githubusercontent.com/sopac/pacsafe-projects/master/{0}".format(self.countryList[self.cv]) + n)
                    with open(path + n, "wb") as lf:
                        lf.write(tf.read())

                #refresh project listing
                self.dlg.listWidget.clear()
                for f in os.listdir(path):
                    if f.endswith(".qgs"):
                        f = f.replace(".qgs", "")
                        f = f.replace("_", " ")
                        f = f.title()
                        item = QListWidgetItem(f)
                        self.dlg.listWidget.addItem(item)
                QMessageBox.about(self.dlg, "Remote Projects", 
                                  ("Remote Projects Synchronised.\r\n"
                                   "Please Reopen PacSAFE Project Opener.")
                self.dlg.close()

        except:
            e = sys.exc_info()[0]
            #QMessageBox.about(self.dlg, "Error", "Error Occurred, Ensure Internet Connectivity.\r\n"  + str(e))
            QMessageBox.critical(None, 'Error!', "Error Occurred, Ensure Internet Connectivity.\r\n"  + str(e), QMessageBox.Abort)

    def openProject(self):
        lw = self.dlg.listWidget
        #QMessageBox.about(self.dlg, "sds", lw.currentItem().text()) 
        if lw.currentItem().text().startswith("---"):
            QMessageBox.about(self.dlg, "Sorry", "Remote Repository Is Not Available!")
            return

        pn = self.dlg.listWidget.currentItem().text()

        proj = pn.replace(" ", "_").lower() + ".qgs"
        path = os.path.join(os.getcwd(), "data", self.countryList[self.cv], proj)

        self.iface.addProject(path)
        self.dlg.hide()
    

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('PacSafe', message)


    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/PacSafe/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'PacSafe'),
            callback=self.run,
            parent=self.iface.mainWindow())



    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&PacSafe'),
                action)
            self.iface.removeToolBarIcon(action)
        # remove the toolbar
        del self.toolbar


    def run(self):
        """Run method that performs all the real work"""
        # show the dialog
        self.dlg.show()
        # Run the dialog event loop
        result = self.dlg.exec_()
        # See if OK was pressed
        if result:
            # Do something useful here - delete the line containing pass and
            # substitute with your code.
            pass
