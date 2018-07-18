#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import importlib
import logging
from six.moves.configparser import SafeConfigParser

log = logging.getLogger(__name__)


class SettingsWrapper(object):
    def __init__(self, settings_name='settings.py'):
        self.my_settings = {}
        self.settings_name = settings_name
        self._load_settings()

    def __call__(self):
        return self.my_settings

    def settings(self):
        return self.my_settings

    def load_with_file(self, module_name, module_file_path='.'):
        if module_name[-3:] != '.py':
            log.error("module name must be python file, such as : example.py")

        module_spec = importlib.util.spec_from_file_location(
            module_name, module_file_path
        )
        if module_spec is None:
            log.error("Module path: {} not found Module:{}".format(module_file_path, module_name))
            return
        module = importlib.util.module_from_spec(module_spec)
        module_spec.loader.exec_module(module)
        load_settings = self._convert2dict(module)
        self.my_settings.update(load_settings)

    def load_with_dict(self, dict_parms):
        self.my_settings.update(dict_parms)

    def load_from_cfg(self, file_name, file_path='.'):
        base_path = os.path.abspath(file_path)
        cfg = SafeConfigParser()
        path = os.path.join(base_path, file_path)
        cfg.read(self._closest_file(filename=file_name, path=path))

        cfg_dict = {}
        for section in cfg.sections():
            section_dict = {}
            for option in cfg[section]:
                section_dict[option] = cfg.get(section, option)
            cfg_dict.update({section: section_dict})

        self.my_settings.update(cfg_dict)

    def _load_settings(self):
        '''
        Load the default settings
        '''

        try:
            module = self._dynamic_import(self._closest_file(self.settings_name))
            self.my_settings = self._convert2dict(module)
        except ImportError:
            log.warning("No default settings found")

    def _dynamic_import(self, module_path):
        basename = os.path.basename(module_path)

        if basename[-3:] == '.py':
            basename = basename[:-3]

        module_spec = importlib.util.spec_from_file_location(
            basename, module_path
        )

        if module_spec is None:
            log.error("Module path: {} not found Module:{}".format(module_path, basename))
            return
        module = importlib.util.module_from_spec(module_spec)
        module_spec.loader.exec_module(module)
        return module

    def _convert2dict(self, module):
        res = {}
        m = dir(module)
        for key in m:
            if key.startswith('__'):
                continue
            value = getattr(module, key)
            res[key] = value
        return res

    def _closest_file(self, filename='settings.py', path='.', prevpath=None):
        """
        return the path  of the closest settings.py file
        :param filename: default  get file name
        :param path:
        :param prevpath:
        :return:
        """
        if path == prevpath:
            return ''

        path = os.path.abspath(path)
        settings_file = os.path.join(path, filename)
        if os.path.exists(settings_file):
            return settings_file
        return self._closest_file(filename=filename, path=os.path.dirname(path), prevpath=path)

if __name__ == '__main__':
    s = SettingsWrapper()
    print(s.my_settings.keys())
    print(s.my_settings.get('REQUEST_CONFIG', None))