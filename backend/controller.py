import importlib.util
import sys
import os


file_path = os.getenv('CONTROLLER_PATH')
module_name = "controller"
spec = importlib.util.spec_from_file_location(module_name, file_path)
controller = importlib.util.module_from_spec(spec)
sys.modules[module_name] = controller
spec.loader.exec_module(controller)
