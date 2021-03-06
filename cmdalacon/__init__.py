#-*- coding: utf-8 -*-
import ConfigParser
import os
import random
import re
from pipobot.lib.modules import MultiSyncModule, defaultcmd

DEFAULT_CONFIG = os.path.join(os.path.dirname(__file__), "cmdlist.cfg")


def multiwordReplace(text, wordDic):
    """
    take a text and replace words that match a key in a dictionary with
    the associated value, return the changed text
    """
    rc = re.compile('|'.join(map(re.escape, wordDic)))

    def translate(match):
        return wordDic[match.group(0)]
    return rc.sub(translate, text)


class ListConfigParser(ConfigParser.RawConfigParser):
    def get(self, section, option):
        "Redéfinition du get pour gérer les listes"
        value = ConfigParser.RawConfigParser.get(self, section, option)
        if (value[0] == "[") and (value[-1] == "]"):
            return map(lambda s: s.decode("utf-8"), eval(value))
        else:
            return value.decode("utf-8")


class CmdAlacon(MultiSyncModule):
    _config = (("config_path", str, DEFAULT_CONFIG),)

    def __init__(self, bot):
        names = self.readconf(bot)
        MultiSyncModule.__init__(self,
                                 bot,
                                 names=names)

    def extract_to(self, config, cmd, value, backup):
        try:
            v = config.get(cmd, value)
        except ConfigParser.NoOptionError:
            v = config.get(cmd, backup)
        if type(v) != list:
            v = [v]
        self.dico[cmd.decode("utf-8")][value] = v

    def readconf(self, bot):
        #name, description and actions associated to each command
        self.dico = {}
        #To initialize MultiSyncModule
        names = {}

        config = ListConfigParser()
        config.read(self.config_path)
        for c in config.sections():
            command_name = c.decode("utf-8")
            self.dico[command_name] = {}
            self.dico[command_name]['desc'] = config.get(c, 'desc')
            names[command_name] = self.dico[command_name]['desc']
            self.dico[command_name]['toNobody'] = config.get(c, 'toNobody') if type(config.get(c, 'toNobody')) == list else [config.get(c, 'toNobody')]
            self.extract_to(config, c, "toSender", "toNobody")
            self.extract_to(config, c, "toBot", "toNobody")
            self.extract_to(config, c, "toSomebody", "toNobody")
        return names

    @defaultcmd
    def answer(self, cmd, sender, message):
        toall = self.bot.occupants.get_all(" ", [self.bot.name, sender])
        replacement = {"__somebody__": message, "__sender__": sender, "_all_": toall}
        if message.lower() == sender.lower():
            key = "toSender"
        elif message == '':
            key = "toNobody"
        elif message.lower() == self.bot.name.lower():
            key = "toBot"
        else:
            key = "toSomebody"
        return multiwordReplace(multiwordReplace(random.choice(self.dico[cmd][key]), replacement), replacement)
