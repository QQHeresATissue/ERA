__author__ = 'narthollis'


import platform
import os
import os.path

class ClassProperty(property):
    """Subclass property to make classmethod properties possible"""
    def __get__(self, cls, owner):
        return self.fget.__get__(None, owner)()


class EVEDir(object):
    """
        This class provides a consistant way of locating the EVE User directory across multiple platforms.
    """

    @ClassProperty
    @classmethod
    def personal(cls):
        system = platform.system()

        if system == "Linux":
            # Wine default path
            return os.path.expanduser('~/EVE/')

        elif system == "Windows":
            # Try and use pywin32 to make ask windows for the location of My Documents
            try:
                import win32com.client
                import pythoncom
                pythoncom.CoInitialize()
                objShell = win32com.client.Dispatch("WScript.Shell")
                return os.path.join(objShell.SpecialFolders("MyDocuments"), 'EVE')
            except ImportError:
                print "You appear to be running Windows, but do not have the pywin32 package.  You can get it here \nhttp://sourceforge.net/projects/pywin32/files/pywin32/Build%20219/ if you choose.\n"
                # If we can't use pywin32, just fall back to a guess
                return os.path.join(os.path.expanduser('~'), 'Documents', 'EVE')
        elif system == "Darwin":
            return os.path.expanduser('~/Library/Application Support/EVE Online/p_drive/User/My Documents/EVE')

    @ClassProperty
    @classmethod
    def game_logs(cls):
        return os.path.join(cls.personal, "logs", "Gamelogs")

    @ClassProperty
    @classmethod
    def chat_logs(cls):
        return os.path.join(cls.personal, "logs", "Chatlogs")

