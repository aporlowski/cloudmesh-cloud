from cloudmesh.common.parameter import Parameter
from cloudmesh.common.variables import Variables
from cloudmesh.shell.command import PluginCommand, map_parameters
from cloudmesh.shell.command import command
from cloudmesh.mongo.CmDatabase import CmDatabase
from cloudmesh.compute.vm.Provider import Provider
import os

class SshCommand(PluginCommand):

    # see https://github.com/cloudmesh/client/blob/master/cloudmesh_client/shell/plugins/SecureShellCommand.py
    # noinspection PyUnusedLocal
    @command
    def do_ssh(self, args, arguments):
        """
        ::

            Usage:
                ssh config list [--output=OUTPUT]
                ssh config add NAME IP [USER] [KEY]
                ssh config delete NAME
                ssh [--name=VMs] [--user=USERs] [COMMAND]

            Arguments:
              NAME        Name or ip of the machine to log in
              list        Lists the machines that are registered and
                          the commands to login to them
              PARAMETERS  Register te resource and add the given
                          parameters to the ssh config file.  if the
                          resource exists, it will be overwritten. The
                          information will be written in /.ssh/config

            Options:
               -v                verbose mode
               --output=OUTPUT   the format in which this list is given
                                 formats includes cat, table, json, yaml,
                                 dict. If cat is used, it is just printed as
                                 is. [default: table]
               --user=USERs      overwrites the username that is
                                 specified in ~/.ssh/config
               --name=CMs        the names of the VMS to execute the
                                 command on

            Description:
                ssh config list
                    lists the hostsnames  that are present in the
                    ~/.ssh/config file

                ssh config add NAME IP [USER] [KEY]
                    registers a host i ~/.ssh/config file
                    Parameters are attribute=value pairs
                    Note: Note yet implemented

                ssh [--name=VMs] [--user=USERs] [COMMAND]
                    executes the command on the named hosts. If user is
                    specified and is greater than 1, it must be specified for
                    each vm. If only one username is specified it is used for
                    all vms. However, as the user is typically specified in the
                    cloudmesh database, you probably do not have to specify
                    it as it is automatically found.

            Examples:


                 ssh config add blue 192.168.1.245 blue

                     Adds the folloewing to the !/.ssh/congig file

                     Host blue
                          HostName 192.168.1.245
                          User blue
                          IdentityFile ~/.ssh/id_rsa.pub



        """

        map_parameters(arguments,
                       "name",
                       "user",
                       "output")

        if arguments.config and arguments.list:
            # ssh config list [--output=OUTPUT]"

            raise NotImplementedError

        elif arguments.config and arguments.add:
            # ssh config add NAME IP [USER] [KEY]

            variables = Variables()

            user = Parameter.find("user",
                                  arguments,
                                  variables.dict())

            key = Parameter.find("key",
                                 arguments,
                                 variables.dict())

            name = arguments.NAME or variables['vm']

            ip = arguments.IP

            print(user, key, name, ip)

            raise NotImplementedError

        elif arguments.config and arguments.delete:
            # ssh config delete NAME

            raise NotImplementedError

        else:
            # ssh [--name=VMs] [--user=USERs] [COMMAND]"

            variables = Variables()

            if arguments.name is None:
                name = arguments.NAME or variables['vm']
                names = [name]
            else:
                names = Parameter.expand(arguments.name)
            users = Parameter.expand(arguments.users)
            command = arguments.COMMAND



            if arguments.command is None and len(names) > 1:
                raise ValueError("For interactive shells the number of vms "
                                 "must be 1")
            elif arguments.command is None and len(names) == 1:
                cm = CmDatabase()
                vm = cm.find_name(names[0], kind="vm")[0]

                cloud = vm['cm']['cloud']

                provider = Provider(name=cloud)
                result = provider.ssh(vm=vm, command=command)
                print(result)
                return ""

            if len(names) > 1 and len(users) == 1:
                users = [users] * len(names)

            if len(names) > 1 and len(users) > 1 and len(names) != len(users):
                raise ValueError("vms and users have different length")


            for name in names:
                cm = CmDatabase()
                vm = cm.find_name(name, kind="vm")
                cloud = vm['cm']['cloud']
                provider = Provider(name=cloud)
                result = provider.ssh(vm=vm, command=command)
                print (result)
