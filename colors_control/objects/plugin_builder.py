import zipfile as _zipfile
import json as _json
import typing as _T
import types as _types
import linecache as _linecache
import traceback as _traceback
import threading as _threading
import hashlib as _hashlib

from .device_scanner import *
from .provider_scanner import *
from .provider_assignator import *

from .plugin_error import PluginError
from .plugin import Plugin

class PluginBuilder():
    def __init__(self, pathname: str, environment: dict) -> None:
        self.__path = pathname
        self.__environment = environment

        self.__plugins: dict[str, tuple[list[str], dict[str, dict]]] = {}
        self.__loaded_plugins: dict[str, Plugin] = {}

        _threading.excepthook = self._except_hook

    def get_pathname(self) -> str:
        return self.__path

    def load_file(self, plugin_pathname:str, plugin_name: str, file_content: str, filename:str, zip: _zipfile.ZipFile) -> dict:
        if filename in self.__plugins[plugin_pathname][1]:
            return self.__plugins[plugin_pathname][1][filename]

        _linecache.cache[plugin_name + ":" + filename] = (
            len(file_content),
            None,
            [line + '\n' for line in file_content.splitlines()],
            plugin_name + ":" + filename,
        )

        namespace = self.__environment.copy()
        namespace["__name__"] = "plugin"

        i = 1
        for line in file_content.splitlines():
            if line.startswith("#color-plugin:"):
                instruction = line[line.index(":") + 1:].split(" ")

                if instruction[0] == "require":
                    if len(instruction) == 2:
                        module_name = instruction[1]
                    elif len(instruction) == 4 and instruction[2] == 'as':
                        module_name = instruction[3]
                    else:
                        raise SyntaxError("invalid syntax at line " + repr(line))
                    
                    try:
                        file_data = zip.read(instruction[1] + ".py").decode()
                    except Exception as exc:
                        raise PluginError(plugin_name + ":" + filename, i, "<module>", line, ImportError("could not find import " + instruction[1] + " in plugin " + plugin_name)) from None

                    module = _types.ModuleType(module_name)
                    try:
                        module.__dict__.update(self.load_file(plugin_pathname, plugin_name, file_data, plugin_name + ":" + instruction[1] + ".py", zip))
                    except Exception as exc:
                        raise PluginError(plugin_name + ":" + instruction[1], i, "<module>", line, exc.with_traceback(exc.__traceback__.tb_next)) from None #type:ignore because there is a call
                
                    namespace[module_name] = module
                
                elif instruction[0] == "include":
                    if len(instruction) == 2:
                        try:
                            file_data = zip.read(instruction[1] + ".py").decode()
                        except Exception as exc:
                            raise PluginError(plugin_name + ":" + filename, i, "<module>", line, ImportError("could not find import " + instruction[1] + " in plugin " + plugin_name)) from None

                        try:
                            namespace.update(self.load_file(plugin_pathname, plugin_name, file_data, instruction[1] + ".py", zip))
                        except Exception as exc:
                            raise PluginError(plugin_name + ":" + filename, i, "<module>", line, exc.with_traceback(exc.__traceback__.tb_next)) from None #type:ignore because there is a call

                    else:
                        raise SyntaxError("invalid syntax at line " + repr(line))
                
                elif instruction[:2] == "refers to".split():
                    if len(instruction) == 3:
                        module = _types.ModuleType(instruction[2])

                        try:
                            module.__dict__.update(self.load_plugin(instruction[2] + ".crp").namespace)
                        except Exception as exc:
                            raise PluginError(plugin_name + ":" + filename, i, "<module>", line, exc.with_traceback(exc.__traceback__.tb_next)) from None #type:ignore because there is a call
                    
                        namespace[instruction[2]] = module
                        self.__plugins[plugin_pathname][0].append(instruction[2])

                    else:
                        raise SyntaxError("invalid syntax at line " + repr(line))
 
                else:
                    raise NameError("unknown command: " + " ".join(instruction))
            
            i += 1

        exec(compile(file_content, plugin_name + ":" + filename, mode="exec"), namespace)

        return namespace
    
    def _except_hook(self, args: _threading.ExceptHookArgs) -> None:
        if args.thread is not None:
            print(f"Exception in thread {args.thread.name}:") 

        _linecache.checkcache()
        _traceback.print_exception(args.exc_type, args.exc_value, args.exc_traceback)
    
    def get_object_type[Type](self, metadata: _T.Any, name: str, required_type: _T.Type[Type], plugin_content: dict) -> list[Type]:
        objects: list[Type] = []

        if not name in metadata:
            return []

        objects_names = metadata[name]

        if type(objects_names) != list or not all(type(i) is str for i in objects_names):
            raise ValueError(name + " must be an array of string")
        
        for object in objects_names:
            try:
                real_object = eval(object, plugin_content)

                if not isinstance(real_object, required_type):
                    raise TypeError(repr(object) + " is not a valid " + repr(name) + "( required " + required_type.__name__ + ")")
                
                objects.append(real_object)

            except:
                raise ReferenceError("Couldn't find scanner " + repr(object)) from None
    
        return objects
    
    def get_current_hash(self, plugin_name: str) -> str:
        sha256 = _hashlib.sha256()

        with open(self.__path + "/" + plugin_name, "rb") as f:
            for bloc in iter(lambda: f.read(4096), b""):
                sha256.update(bloc)
    
        return sha256.hexdigest()
    
    def execute(self, pathname: str, plugin_zipfile: _zipfile.ZipFile, import_stack: list[str] = []) -> Plugin:
        zip_names = plugin_zipfile.namelist()

        if not "META.conf" in zip_names:
            raise TypeError("missing META configuration")
        
        metadata = _json.loads(plugin_zipfile.read("META.conf"))

        if type(metadata) != dict:
            raise TypeError("metadata file must be a json dict")
        
        if not "name" in metadata:
            raise KeyError("missing name in metadata")
        
        if not type(metadata["name"]) is str:
            raise TypeError("name must be a string")
        
        if not "main.py" in zip_names:
            raise TypeError("missing main file")
        
        data = plugin_zipfile.read("main.py").decode()

        plugin_content = self.load_file(pathname, metadata["name"], data, "main.py", plugin_zipfile)

        device_scanners: list[DevicesScanner] = self.get_object_type(metadata, "device_scanners", DevicesScanner, plugin_content)
        provider_scanners: list[ProvidersScanner] = self.get_object_type(metadata, "provider_scanners", ProvidersScanner, plugin_content)
        assignators: list[DeviceProviderAssignator] = self.get_object_type(metadata, "assignators", DeviceProviderAssignator, plugin_content)

        return Plugin(self.get_current_hash(pathname), metadata["name"], pathname, device_scanners, provider_scanners, assignators, [], plugin_content)
    
    def load_plugin(self, plugin_name:str) -> Plugin:
        if plugin_name in self.__loaded_plugins:
            return self.__loaded_plugins[plugin_name]
    
        self.__plugins[plugin_name] = ([], {})

        with _zipfile.ZipFile(self.__path + "/" + plugin_name) as zipFile:
            try:
                plugin = self.execute(plugin_name, zipFile)
            except PluginError as err:
                print("Could not load plugin at " + self.__path + "/" + plugin_name+ ":")
                err.print_traceback()

                plugin = Plugin(self.get_current_hash(plugin_name), "<error>", plugin_name, [], [], [], [], {})
            except Exception:
                print("Could not load plugin at " + self.__path + "/" + plugin_name+ ":")
                _traceback.print_exc()
            
                plugin = Plugin(self.get_current_hash(plugin_name), "<error>", plugin_name, [], [], [], [], {})

        self.__loaded_plugins[plugin_name] = plugin

        return self.__loaded_plugins[plugin_name]
    
    def reload_plugin(self, plugin_name: str) -> list[Plugin]:
        dependent_plugins: list[str] = []

        for plugin in self.__plugins:
            if plugin_name in self.__plugins[plugin][0]:
                dependent_plugins.append(plugin)
        
        for plugin in dependent_plugins:
            del self.__plugins[plugin]
            del self.__loaded_plugins[plugin]
        
        del self.__plugins[plugin_name]
        del self.__loaded_plugins[plugin_name]

        new_plugins: list[Plugin] = []
        new_plugins.append(self.load_plugin(plugin_name))

        for dependent_plugin in dependent_plugins:
            new_plugins.append(self.load_plugin(dependent_plugin))
        
        return new_plugins
        

