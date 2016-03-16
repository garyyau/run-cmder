import os
import sublime
import sublime_plugin
import subprocess


def print_sublime_error(error):
    sublime.error_message('RunCmder\n%s' % error)


class RunCmderBaseCommand(sublime_plugin.TextCommand):

    def get_current_file_directory(self):
        file = self.view.file_name()
        directory = os.path.dirname(file)
        return directory

    def get_setting(self, key):
        settings = sublime.load_settings('RunCmder.sublime-settings')
        return settings.get(key)

    def get_cmder_path(self):
        cmder_path = self.get_setting('cmder_installation_path')

        if not cmder_path:
            print_sublime_error(
                'Missing Package Setting: cmder_installation_path'
            )
            return

        if not os.path.exists(cmder_path):
            print_sublime_error('Invalid Path: ' + cmder_path)
            return

        if os.path.basename(cmder_path) != 'Cmder.exe':
            print_sublime_error('Cannot find Cmder.exe in ' + cmder_path)

        return cmder_path

    def open_cmder(self, args=None):
        cmder_path = self.get_cmder_path()

        if not cmder_path:
            return

        command_args = [
            cmder_path,
            '/START',
            self.get_current_file_directory()
        ]
        if args:
            command_args = command_args + args

        print(command_args)

        subprocess.call(command_args)


class RunCmderRun(RunCmderBaseCommand):

    def run(self, edit):
        self.open_cmder()
