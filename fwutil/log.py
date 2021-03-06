#!/usr/bin/env python
#
# log.py
#
# Logging library for command-line interface for interacting with platform components within SONiC
#

try:
    import click
    from sonic_py_common import logger
except ImportError as e:
    raise ImportError("Required module not found: {}".format(str(e)))

# ========================= Constants ==========================================

SYSLOG_IDENTIFIER = "fwutil"

# Global logger instance
log = logger.Logger(SYSLOG_IDENTIFIER)


# ========================= Helper classes =====================================

class LogHelper(object):
    """
    LogHelper
    """
    FW_ACTION_DOWNLOAD = "download"
    FW_ACTION_INSTALL = "install"
    FW_ACTION_UPDATE = "update"

    STATUS_SUCCESS = "success"
    STATUS_FAILURE = "failure"

    def __log_fw_action_start(self, action, component, firmware):
        caption = "Firmware {} started".format(action)
        template = "{}: component={}, firmware={}"

        log.log_info(
            template.format(
                caption,
                component,
                firmware
            )
        )

    def __log_fw_action_end(self, action, component, firmware, status, exception=None):
        caption = "Firmware {} ended".format(action)

        status_template = "{}: component={}, firmware={}, status={}"
        exception_template = "{}: component={}, firmware={}, status={}, exception={}"

        if status:
            log.log_info(
                status_template.format(
                    caption,
                    component,
                    firmware,
                    self.STATUS_SUCCESS
                )
            )
        else:
            if exception is None:
                log.log_error(
                    status_template.format(
                        caption,
                        component,
                        firmware,
                        self.STATUS_FAILURE
                    )
                )
            else:
                log.log_error(
                    exception_template.format(
                        caption,
                        component,
                        firmware,
                        self.STATUS_FAILURE,
                        str(exception)
                    )
                )

    def log_fw_download_start(self, component, firmware):
        self.__log_fw_action_start(self.FW_ACTION_DOWNLOAD, component, firmware)

    def log_fw_download_end(self, component, firmware, status, exception=None):
        self.__log_fw_action_end(self.FW_ACTION_DOWNLOAD, component, firmware, status, exception)

    def log_fw_install_start(self, component, firmware):
        self.__log_fw_action_start(self.FW_ACTION_INSTALL, component, firmware)

    def log_fw_install_end(self, component, firmware, status, exception=None):
        self.__log_fw_action_end(self.FW_ACTION_INSTALL, component, firmware, status, exception)

    def log_fw_update_start(self, component, firmware):
        self.__log_fw_action_start(self.FW_ACTION_UPDATE, component, firmware)

    def log_fw_update_end(self, component, firmware, status, exception=None):
        self.__log_fw_action_end(self.FW_ACTION_UPDATE, component, firmware, status, exception)

    def print_error(self, msg):
        click.echo("Error: {}.".format(msg))

    def print_warning(self, msg):
        click.echo("Warning: {}.".format(msg))

    def print_info(self, msg):
        click.echo("Info: {}.".format(msg))
