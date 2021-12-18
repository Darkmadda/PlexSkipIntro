# -*- coding: utf-8 -*-

'''
    TvSkipIntro Add-on
    Copyright (C) 2018 aenema

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''
import threading

import xbmc,xbmcaddon,xbmcgui, time
from plexapi.server import PlexServer
import asyncio
from threading import Timer

KODI_VERSION = int(xbmc.getInfoLabel("System.BuildVersion").split(".")[0])
addonInfo = xbmcaddon.Addon().getAddonInfo
settings = xbmcaddon.Addon().getSetting
addonPath = xbmc.translatePath(addonInfo('path'))
introFound = True
introStartTime = 0
introEndTime = 0
chosen = False
Dialog = None
running = False
Ran = False
def closeDialog():
    global Dialog
    global timer
    global running
    global Ran
    Dialog.close()
    timer.cancel()
    Ran = True
    running = False
    timer = threading.Timer(5, closeDialog)

def timerStart():
    global timer
    global running
    global Ran
    if not running and not Ran:
        timer.start()
        Dialog.show()
        running = True


timer = threading.Timer(5, closeDialog)

class Service(xbmc.Monitor):

    WINDOW = xbmcgui.Window(10000)

    def __init__(self, *args):
        addonName = 'Plex TV Skip'


    def onNotification(self, sender, method, data):
            global Ran
            if method in ["Player.OnSeek"]:
                Ran = False
            if method in ["Player.OnPlay"]:
                global introFound
                global introStartTime
                global introEndTime
                global chosen
                Ran = False
                chosen = False
                introFound = False
                myPlayer = xbmc.Player()  # make Player() a single call.
                if myPlayer.isPlayingVideo():
                    season_number = myPlayer.getVideoInfoTag().getSeason()
                    episode_number = myPlayer.getVideoInfoTag().getEpisode()
                    show = myPlayer.getVideoInfoTag().getTVShowTitle()
                    if str(show) == '':
                        xbmc.log("empty", xbmc.LOGINFO)
                        return None
                    xbmc.log(show+"show",xbmc.LOGINFO)
                    baseurl = xbmcaddon.Addon().getSettingString("plex_base_url")
                    token = xbmcaddon.Addon().getSettingString("auth_token")
                    xbmc.log(baseurl,xbmc.LOGINFO)
                    xbmc.log(token,xbmc.LOGINFO)
                    plex = PlexServer(baseurl, token)
                    shows = plex.library.section('TV Shows')
                    show = shows.search(show)[0]
                    episode = show.episode(None, season_number, episode_number)
                    for marker in episode.markers:
                        if (marker.type == "intro"):
                            introFound = True
                            introStartTime = marker.start / 1000
                            introEndTime = marker.end / 1000


    def ServiceEntryPoint(self):
        monitor = xbmc.Monitor()
        global introFound
        global introStartTime
        global introEndTime
        global Ran
        global Dialog
        Dialog = CustomDialog('script-dialog.xml', addonPath)
        while not monitor.abortRequested():
            # check every 5 sec
            if monitor.waitForAbort(3):
                # Abort was requested while waiting. We should exit
                break

            if xbmc.Player().isPlaying():
                if introFound:
                    if xbmc.Player().getTime() > introStartTime and xbmc.Player().getTime() < introEndTime:
                        timerStart()
OK_BUTTON = 201
NEW_BUTTON = 202
DISABLE_BUTTON = 210
ACTION_PREVIOUS_MENU = 10
ACTION_BACK = 92
class CustomDialog(xbmcgui.WindowXMLDialog):

    def __init__(self, xmlFile, resourcePath):
        None

    def onInit(self):
        instuction = ''
        
    def onAction(self, action):
        if action == ACTION_PREVIOUS_MENU or action == ACTION_BACK:
            self.close()

    def onControl(self, control):
        pass

    def onFocus(self, control):
        pass

    def onClick(self, control):
        global chosen
        global introEndTime
        if control == OK_BUTTON:
            xbmc.Player().seekTime(int(introEndTime))

        if control in [OK_BUTTON, NEW_BUTTON, DISABLE_BUTTON]:
            self.close()

Service().ServiceEntryPoint()