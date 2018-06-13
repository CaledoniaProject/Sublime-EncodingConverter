import re
import subprocess
import sublime
import sublime_plugin

class BaseCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        if self.view.is_scratch():
            sublime.error_message('File is scratch')
            return

        try:
            region = sublime.Region(0, self.view.size())
            data   = self.convert()

            self.view.replace(edit, region, data)
        except Exception as e:
            sublime.error_message('Exception: ' + str(e))
            raise

    def convert(self):
        result = subprocess.check_output([
            'iconv', '-f', self.from_e, '-t', 'utf8//ignore', self.view.file_name()
        ])

        result = result.decode('utf8')
        result = re.sub(r'[\r]+', '', result)
        return result

class ReopenAsGbkCommand(BaseCommand):
    def run(self, edit):
        self.from_e = 'gbk'
        return super(ReopenAsGbkCommand, self).run(edit)

class ReopenAsBig5Command(BaseCommand):
    def run(self, edit):
        self.from_e = 'big5'
        return super(ReopenAsBig5Command, self).run(edit)


