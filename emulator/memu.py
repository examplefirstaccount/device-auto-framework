"""A wrapper for memuc.exe"""

import re
import subprocess as sp

from ._constants import EMU_CONSOLE
from ._exceptions import MemucIndexException, MemucRunException


class Memuc:
    """A class to interact with the memuc.exe command line tool.

    :param memuc_path: Path to memuc.exe. Set to None for autodetect.
    :type memuc_path: str, optional
    """

    def __init__(self, memuc_path: str = None) -> None:

        if memuc_path is not None:
            self.memuc_path: str = memuc_path
        else:
            self.memuc_path: str = EMU_CONSOLE

    def __memuc_run(self, args: list, non_blocking=False) -> tuple[int, str]:

        args.insert(0, self.memuc_path)
        if non_blocking:
            args += "-t"
        proc = sp.run(args, capture_output=True, shell=True)
        return proc.returncode, proc.stdout.decode('utf-8')

    def create_emu(self, vm_version: str = "76") -> int:

        status, output = self.__memuc_run(['create', vm_version])

        success = status == 0 and output is not None and "SUCCESS" in output
        if not success:
            raise MemucRunException(f'Failed to create VM: {output}')

        indices = re.search(r"index:(\w)", output)
        if indices is not None:
            return int(indices[1])
        else:
            return -1

    def delete_emu(self, vm_index: int = None, vm_name: str = None) -> bool:

        if vm_index is not None:
            status, output = self.__memuc_run(['remove', '-i', str(vm_index)])
        elif vm_name is not None:
            status, output = self.__memuc_run(['remove', '-n', vm_name])
        else:
            raise MemucIndexException("Please specify either a vm index or a vm name")

        success = status == 0 and output is not None and "SUCCESS" in output
        if not success:
            raise MemucRunException(f"Failed to delete VM: {output}")
        return True

    def clone_emu(
            self,
            vm_index: int = None,
            vm_name: str = None,
            new_name: str = None
    ) -> bool:

        new_name_cmd = ["-r", new_name] if new_name is not None else []
        if vm_index is not None:
            status, output = self.__memuc_run(['clone', '-i', str(vm_index), *new_name_cmd])
        elif vm_name is not None:
            status, output = self.__memuc_run(['clone', '-n', vm_name, *new_name_cmd])
        else:
            raise MemucIndexException("Please specify either a vm index or a vm name")

        success = status == 0 and output is not None and "SUCCESS" in output
        if not success:
            raise MemucRunException(f"Failed to clone VM: {output}")
        return True

    def start_emu(
            self,
            vm_index: int = None,
            vm_name: str = None,
            non_blocking=False
    ) -> bool:

        if vm_index is not None:
            status, output = self.__memuc_run(['start', '-i', str(vm_index)], non_blocking)
        elif vm_name is not None:
            status, output = self.__memuc_run(['start', '-n', vm_name], non_blocking)
        else:
            raise MemucIndexException("Please specify either a vm index or a vm name")

        success = status == 0 and output is not None and "SUCCESS" in output
        if not success:
            raise MemucRunException(f"Failed to start VM: {output}")
        return True

    def stop_emu(
            self,
            vm_index: int = None,
            vm_name: str = None,
            non_blocking=False
    ) -> bool:

        if vm_index is not None:
            status, output = self.__memuc_run(['stop', '-i', str(vm_index)], non_blocking)
        elif vm_name is not None:
            status, output = self.__memuc_run(['stop', '-n', vm_name], non_blocking)
        else:
            raise MemucIndexException("Please specify either a vm index or a vm name")

        success = status == 0 and output is not None and "SUCCESS" in output
        if not success:
            raise MemucRunException(f"Failed to stop VM: {output}")
        return True

    def reboot_emu(
            self,
            vm_index: int = None,
            vm_name: str = None,
            non_blocking=False
    ) -> bool:

        if vm_index is not None:
            status, output = self.__memuc_run(['reboot', '-i', str(vm_index)], non_blocking)
        elif vm_name is not None:
            status, output = self.__memuc_run(['reboot', '-n', vm_name], non_blocking)
        else:
            raise MemucIndexException("Please specify either a vm index or a vm name")

        success = status == 0 and output is not None and "SUCCESS" in output
        if not success:
            raise MemucRunException(f"Failed to reboot VM: {output}")
        return True

    def set_config(
            self,
            key: str,
            value: str,
            vm_index: int = None,
            vm_name: str = None
    ) -> bool:

        if vm_index is not None:
            status, output = self.__memuc_run(['setconfigex', '-i', str(vm_index), key, value])
        elif vm_name is not None:
            status, output = self.__memuc_run(['setconfigex', '-n', vm_name, key, value])
        else:
            raise MemucIndexException("Please specify either a vm index or a vm name")

        success = status == 0 and output is not None and "SUCCESS" in output
        if not success:
            raise MemucRunException(f"Failed to set VM config: {output}")
        return True

    def get_config(
            self,
            key: str,
            vm_index: int = None,
            vm_name: str = None
    ) -> str:

        if vm_index is not None:
            status, output = self.__memuc_run(['getconfigex', '-i', str(vm_index), key])
        elif vm_name is not None:
            status, output = self.__memuc_run(['getconfigex', '-n', vm_name, key])
        else:
            raise MemucIndexException("Please specify either a vm index or a vm name")

        success = status == 0 and output is not None
        if not success:
            raise MemucRunException(f"Failed to get VM config: {output}")
        return output.strip().split()[1]

    def exec_android_cmd(
            self,
            command,
            vm_index: int = None,
            vm_name: str = None
    ) -> str:

        if vm_index is not None:
            status, output = self.__memuc_run(['-i', str(vm_index), 'execcmd', command])
        elif vm_name is not None:
            status, output = self.__memuc_run(['-n', vm_name, 'execcmd', command])
        else:
            raise MemucIndexException("Please specify either a vm index or a vm name")

        success = status == 0 and output is not None
        if not success:
            raise MemucRunException(f"Failed to execute android command: {output}")
        return output.strip()

    def adb_cmd(
            self,
            command,
            vm_index: int = None,
            vm_name: str = None
    ) -> str:

        if vm_index is not None:
            status, output = self.__memuc_run(['-i', str(vm_index), 'adb', command])
        elif vm_name is not None:
            status, output = self.__memuc_run(['-n', vm_name, 'adb', command])
        else:
            raise MemucIndexException("Please specify either a vm index or a vm name")

        success = status == 0 and output is not None
        if not success:
            raise MemucRunException(f"Failed to execute adb command: {output}")
        return output.strip()

# https://hack.technoherder.com/adb-shell/
# https://www.memuplay.com/blog/memucommand-reference-manual.html
# https://www.memuplay.com/blog/how-to-manipulate-memu-thru-command-line.html

# api for lang/time settings
# https://ipinfo.io/developers#authentication

# locale == lang_COUNTRYCODE ( en_US )
