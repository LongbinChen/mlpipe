from django.core.management.base import BaseCommand, CommandError
import imp
import  argparse
import yaml

class Command(BaseCommand):
    help = 'create yaml files '
    
    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('python_code_path', type=str, default=None)
        parser.add_argument('--dry_run', action = 'store_true',  default=False)

    def get_app_module_name(self, code_path):
        ''' 
           get the app name and module name from the code path
            assumming the code path is like .../../[app_name]/module/[module_name].py
        '''
        paths = code_path.split("/")
        module_name = paths[-1]
        if module_name.endswith('.py'):
            module_name = module_name[:-3]
        if len(paths) >= 3:
            app_name = paths[-3]
        return app_name, module_name


    def create_dict(self, runpy, code_path):
        if not 'create_parser' in dir(runpy):
            print   "Can not find create_parser in your python script." \
                    "You need to refactorize your code, put the argparser" \
                    "config in a function called create_parser"
            return {}
        parser = runpy.create_parser()
        result = {'input':{}, 'output':{}, 'parameters':{}, 'cmd':""}
        app_name, module_name = self.get_app_module_name(code_path)
        cmd = "python -m %s.module.%s " % (app_name, module_name)
        for s in getattr(parser, '_actions'):
            print vars(s)
            key_name = s.dest
            if key_name == 'help': continue
            info = {}
            print key_name

            if s.option_strings != None and len(s.option_strings) > 0:
                print s.option_strings
                cmd += " " +  s.option_strings[0] + " "
            cmd += " " + s.dest + " "

            if s.type != None:
                info['type'] = str(s.type)
            else:
                info['type'] = 'string'
            if s.default != None:
                info['default'] = str(s.default)
            info['datafile'] = True
            if 'input' in s.help:
                result['input'][key_name] = info
            elif 'output' in s.help:
                result['output'][key_name] = info
            elif 'param' in s.help:
                result['parameters'][key_name] = info
            else:
                print "Can not process argument %s, please include 'input', 'output', 'param' in the help message'. " % key_name
        result['cmd'] = cmd
        return result

        

    def handle(self, *args, **options):
        dry_run = options.get("dry_run", False)
        try:
            code_path = options.get('python_code_path')
            runpy = imp.load_source('my_module', code_path)
            result = self.create_dict(runpy, code_path)
            print result
            with open('data.yml', 'w') as outfile:
                yaml.dump(result, outfile, default_flow_style=False)
        except SystemExit:
            print "catch system exit error"
        except Exception, e:
            print "caught exception"
            print str(e)

