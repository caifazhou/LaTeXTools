from base_viewer import BaseViewer

from latextools_utils import get_setting

import subprocess
import sys
import time


class OkularViewer(BaseViewer):

    def _run_okular(self, locator=None, **kwargs):
        keep_focus = kwargs.pop('keep_focus', True)
        command = ['okular', '--unique']
        if keep_focus:
            command.append('--noraise')
        if locator is not None:
            command.append(locator)

        subprocess.Popen(command)

    def _is_okular_running(self):
        stdout = subprocess.Popen(
            ['ps', 'xw'], stdout=subprocess.PIPE
        ).communicate()[0]

        running_apps = stdout.decode(sys.getdefaultencoding(), 'ignore')
        for app in running_apps.splitlines():
            if 'okular' not in app:
                continue
            if '--unique' in app:
                return True
        return False

    def _ensure_okular(self, **kwargs):
        if not self._is_okular_running():
            self._run_okular(**kwargs)
            time.sleep(get_setting('linux', {}).get('sync_wait') or 1.0)

    def forward_sync(self, pdf_file, tex_file, line, col, **kwargs):
        self._ensure_okular()
        self._run_okular(
            '{pdf_file}#src:{line}{tex_file}'.format(**locals()),
            **kwargs
        )

    def view_file(self, pdf_file, **kwargs):
        self._ensure_okular()
        self._run_okular(
            pdf_file,
            **kwargs
        )

    def supports_keep_focus(self):
        return True

    def supports_platform(self, platform):
        return platform == 'linux'
