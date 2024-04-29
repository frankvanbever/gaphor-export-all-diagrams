#   Copyright 2024 KION Group AG
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
#   This plugin uses code from the upstream Gaphor project, licensed under the
#   Apache License, Version 2.0, Copyright The Gaphor Development Team


import logging
from pathlib import Path

from gaphor.abc import ActionProvider, Service
from gaphor.action import action
from gaphor.i18n import gettext
from gaphor.diagram.export import save_png, escape_filename
from gaphor.core.modeling import Diagram
from gaphor.plugins.diagramexport import exportcli

from gi.repository import Gtk

log = logging.getLogger(__name__)


class ExportAllPlugin(Service, ActionProvider):

    def __init__(self, main_window=None, export_menu=None, element_factory=None):
        self.main_window = main_window
        self.export_menu = export_menu
        self.factory = element_factory
        if export_menu:
            export_menu.add_actions(self)

    def shutdown(self):
        pass

    # Adapted from the upstream DiagramExport plugin
    def export_pngs_handler(self, path):
        log.info(f"Outputting diagrams to {path}")
        for diagram in self.factory.select(Diagram):
            odir = f"{path}/{exportcli.pkg2dir(diagram.owner)}"

            # just diagram name
            dname = escape_filename(diagram.name)
            # full diagram name including package path
            pname = f"{odir}/{dname}"

            odir = odir.replace(" ", "_")
            dname = dname.replace(" ", "_")

            outfilename = f"{odir}/{dname}.png"

            if not Path(odir).exists():
                log.debug("creating dir %s", odir)
                Path(odir).mkdir(parents=True)

            log.debug("rendering: %s -> %s...", pname, outfilename)

            save_png(outfilename, diagram)

    @action(
        name="export-all-diagrams",
        label=gettext("Export all diagrams"),
        tooltip=gettext("Export all diagrams as PNG diagrams in a specified directory"),
    )
    def export_all_action(self):
        dialog = Gtk.FileDialog.new()
        dialog.set_title(gettext("Export all diagrams"))

        def response(dialog, result):
            if result.had_error():
                return

            folder = dialog.select_folder_finish(result).get_path()
            self.export_pngs_handler(folder)

        dialog.select_folder(callback=response)
