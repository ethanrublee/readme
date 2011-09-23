#!/usr/bin/env python
'''
Given a nicely formatted, in reStructuredText, readme file, attempt to build what
it describes.

 Assumes the user has put a little bit of semantic markup into
the file, so that this script can use it properly ;)
'''

import docutils
from docutils.parsers import rst

def parse_args(args=None):
    import argparse
    parser = argparse.ArgumentParser(description='''Parses a reStructuredText file in order to _parse_build a project.''')
    parser.add_argument('--workspace', metavar='WORKSPACE', type=str, default='workspace',
                        help='The workspace, will be created if necessary. All commands in the readme happen relative to this.')

    parser.add_argument('readme', metavar='README_RST', type=argparse.FileType('r'), nargs=1,
                   help='A readme file to parse.')
    args = parser.parse_args()
    return args

class Buildable(object):
    '''This is little stateful readme follower, that given a docutils parsed document
    will attempt to follow the instructions.
    
    It expects sections with names:
    - source
    - dependencies
    - build
    - test
    - install
    
    All of these sections are assumed to have literal blocks which may be directly
    copy pasted into a terminal, with the exception begin dependencies.
    
    Dependencies should contain a bulleted list, where each item is a definition list
    e.g::
        - Boost
            Where to get boost...
        - OpenCV
            You should use version 2.3 or greater
    
    Literal blocks will be run in a shell session and should only contain valid
    shell code.
    
    TODO support lines prefixed with $ or % or > as commands and others as non
    commands.
    '''
    #little template for running the commands, with echo and exit on error
    script_str = """#!/bin/sh
set -x
set -o errexit
(
cd %s
export INSTALL_PREFIX=`pwd`/installed
#other env stuff here? TODO figure out how to set the env dynamically
%s
)
touch %s.success"""

    def __init__(self, document):
        ''' Initialize the Buildable, should pass in a pre parsed document.
        This will not build it.
        '''
        self.document = document
        self._source = ""
        self._build = ""
        self._test = ""
        self.dep_list = []
        self._parse_source()
        self._parse_dependencies()
        self._parse_build()
        self._parse_test()
        self._parse_install()


    def _parse_literal_blocks(self, section):
        try:
            document = self.document
            l_section = document.ids[section]
            #TODO do a few more robust things here
            literal_blocks = [str(x[0]) for x in l_section.traverse() if isinstance(x, docutils.nodes.literal_block)]
            if literal_blocks and len(literal_blocks) > 0:
                return '\n'.join(literal_blocks)
            else:
                return None # there was no literal block.
        except KeyError, e:
            if section in str(e): return None
            else: raise e

    def _parse_source(self):
        self._source = self._parse_literal_blocks('source')

    def _parse_build(self):
        self._build = self._parse_literal_blocks('build')

    def _parse_test(self):
        self._test = self._parse_literal_blocks('test')

    def _parse_install(self):
        self._install = self._parse_literal_blocks('install')

    def _parse_dependencies(self):
        document = self.document
        dep_idx = document.ids['dependencies'].first_child_matching_class(docutils.nodes.bullet_list)
        if dep_idx:
            dependencies = document.ids['dependencies'][dep_idx]
            for x in dependencies:
                self.dep_list.append(str(x[0][0][0][0])) #Assumes that this is a definition list TODO FIXME

    def _execute_script(self, path, script_name, text):
        if text is None: return
        import os, subprocess
        if not os.path.exists(path):
            os.makedirs(path)
        script_path = os.path.join(path, script_name)
        if os.path.exists(script_path):
            os.remove(script_path)
        with open(script_path, 'w') as f:
            f.write(Buildable.script_str % (path, text, script_path))
        try:
            subprocess.check_call(['sh', script_path])
        except subprocess.CalledProcessError, e:
            print str(e)

    def doit(self, path):
        ''' Execute the readme in some workspace given by path.
        '''
        self._execute_script(path, '_source.sh', self._source)
        self._execute_script(path, '_build.sh', self._build)
        self._execute_script(path, '_test.sh', self._test)
        self._execute_script(path, '_install.sh', self._install)

if __name__ == '__main__':
    args = parse_args()
    readme = args.readme[0] #select the first arg
    parser = rst.Parser()
    document = docutils.utils.new_document(readme.name)
    document.settings.tab_width = 2
    document.settings.pep_references = None
    document.settings.rfc_references = None
    parser.parse(''.join(readme), document)
    buildable = Buildable(document)
    buildable.doit(args.workspace)
