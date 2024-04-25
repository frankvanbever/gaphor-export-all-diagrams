import logging
import gi

from gaphor.abc import ActionProvider, Service
from gaphor.action import action
from gaphor.i18n import gettext

from gi.repository import Adw

log = logging.getLogger(__name__)


class ExportAllPlugin(Service, ActionProvider):

    def __init__(self, main_window, tools_menu):
        self.main_window = main_window
        tools_menu.add_actions(self)

    def shutdown(self):
        pass

    @action(
        name="export-all-diagrams",
        label=gettext("Export all diagrams"),
        tooltip=gettext("Export all diagrams as PNG diagrams in a specified directory"),
    )
    def export_all_action(self):
        window = self.main_window.window

        dialog = Adw.MessageDialog.new(window, gettext("Export all diagrams"))
        dialog.set_body(gettext("This is a test"))
        dialog.add_response("close", gettext("Close"))
        dialog.set_close_response("close")

        dialog.set_visible(True)

