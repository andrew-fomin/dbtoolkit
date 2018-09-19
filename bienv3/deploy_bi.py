#!usr/bin/env python

# Standard Python distribution libraries
import os
import sys
import argparse

# Custom python libraries:
import rm_sys

try:
    rm_sys.os.chdir(rm_sys.SCRIPT_DIR)  # Change to script directory

    # ArgumentParser to parse arguments and options
    parser = argparse.ArgumentParser(description="Test Deployment Script")
    parser.add_argument("-r", "--rpd_only", action="store_true", default=False, help="Only deploys the RPD.")
    parser.add_argument("-w", "--webcat_only", action="store_true", default=False, help="Only deploys the Webcat.")
    #parser.add_argument("-a", "--webcat_deploy_all", action="store_true", default=False, help="Deploy all Webcat content from source folder.")
    #parser.add_argument('-b', '--git_branch', action="store", default="master",
    #                    help="Specify the Git branch from which the repo should be downloaded.")
    parser.add_argument('-c', '--config', default='config.ini', help='Config file to be used. Default: "config.ini"')
    parser.add_argument("-d", "--debug", action="store_true", default=False,
                        help="Enables debugging mode, with enhanced error messages.")
    parser.add_argument('-n', '--name', default='default', help='Release name to deploy')
    #parser.add_argument("-f", "--deploy_from_folder", action="store_true", default=False,
    #                    help="Deploys from a folder instead from Git. "
    #                         "WEBCAT_DEPLOY_FROM_FOLDER and RPD_DEPLOY_FROM_FOLDER parameters are required in the config.ini file under [OBIEE].")


    args = parser.parse_args()
    CONFIG_FILE = args.config

    rm_sys.parse_config(CONFIG_FILE, ['Git', 'OBIEE'])
    if args.debug:
        rm_sys.DEBUG = True
    RPD_ONLY = False
    WEBCAT_ONLY = False
    WEBCAT_DEPLOY_ALL = False
    GIT_BRANCH = 'master'

    DEPLOY_FROM_FOLDER = False

    release_name=args.name

    script_path = os.path.dirname(os.path.abspath(__file__))
    print(script_path)


    print(rm_sys.CONNECTION_POOLS)

except Exception as err:
    print '\n\nException caught:\n\n%s ' % err
    print '\n\tError: Failed to get command line arguments. Exiting.'
    sys.exit(1)


def exit_on_error(out):
    if out[1]:
        if 'Already on ' not in out[1]:
            print('Error %s' % out[1])
            sys.exit(1)

def get_txt_file_content(folder_root, file_name):
    try:
        with open(os.path.join(folder_root, file_name), 'r') as path_file:
            content = path_file.read()
        return str(content).strip()
    except Exception as err:
        return 'N/A'

def main():

    with open(os.path.join(script_path, 'Releases','manifest-release-'+release_name+'.txt')) as release_manifest:
        rm_sys.ws.connect()
        for obj in release_manifest.readlines():
            if len(obj)>1:
                obj=obj.strip('\n')
                if len(os.path.relpath(obj,'./RPD'))<len(obj):
                    print '\nDeploying RPD...'
                    rpd_path = os.path.abspath(obj)
                    print(rpd_path)
                    temp_rpd_path = os.path.join(rm_sys.SCRIPT_DIR, rm_sys.GIT_RPD)
                    print(temp_rpd_path)
                    print '\nUpdating the RPD %s with the credentials from %s...\nThis will take several minutes...' % (rpd_path, rm_sys.CONNECTION_POOLS)
                    update_rpd_command_input = ['python', os.path.join(rm_sys.SCRIPT_DIR, 'update_rpd.py'), rpd_path,
                                                rm_sys.CONNECTION_POOLS, '-o', temp_rpd_path]
                    print(update_rpd_command_input)
                    out = rm_sys.run_os_cmd(update_rpd_command_input)
                    # print 'RPD update output: %s' % str(out)
                    exit_on_error(out)

                    print 'Updating the RPD with the saved credentials done!'

                    # deploy RPD to OBIEE via WLST
                    print('\nDeploying the RPD to OBIEE via WLST...')
                    rm_sys.obi.deploy_rpd(temp_rpd_path)
                    print '\nDeleting the temporary rpd (%s)...' % temp_rpd_path
                    rm_sys.delete_file(temp_rpd_path)
                    print('\nCompleted RPD deployment!')

                elif len(os.path.relpath(obj,'./WebCat'))<len(obj):

                        content = rm_sys.read_file(os.path.abspath(obj))
                        import_root = '/'+os.path.dirname(os.path.relpath(obj, os.path.join(rm_sys.SCRIPT_DIR,'WebCat'))).replace('.base64','').replace('\\','/')
                        print(import_root)
                        print ('Deploying %s to %s' % (obj, import_root))
                        rm_sys.ws.unarchive_wc_dir(content, import_root, overwrite=True, inc_security=True)
        rm_sys.ws.disconnect()

    '''
    if DEPLOY_FROM_FOLDER or True: # from folder
        print '\nStarting OBIEE repository deployment from local folders...'

        if os.path.isdir(rm_sys.WEBCAT_DEPLOY_FROM_FOLDER):
            print 'Web Catalog source folder %s exists.' % rm_sys.WEBCAT_DEPLOY_FROM_FOLDER
        else:
            print 'Error: Web Catalog source folder %s DOES NOT EXIST.' % rm_sys.WEBCAT_DEPLOY_FROM_FOLDER
            sys.exit(1)

        if os.path.exists(rm_sys.RPD_DEPLOY_FROM_FOLDER):
            print 'RPD source file %s exists.' % rm_sys.RPD_DEPLOY_FROM_FOLDER
        else:
            print 'Error: RPD source folder %s DOES NOT EXIST.' % rm_sys.RPD_DEPLOY_FROM_FOLDER
            sys.exit(1)

    if not WEBCAT_ONLY:
        print '\nDeploying RPD...'

        # create temp.rpd with the user credentials
        if DEPLOY_FROM_FOLDER:
            rpd_path = rm_sys.RPD_DEPLOY_FROM_FOLDER
        else:
            rpd_path = os.path.abspath(os.path.join(rm_sys.GIT_REPO, rm_sys.GIT_SUBFOLDER, rm_sys.GIT_RPD))

        temp_rpd_path = os.path.join(rm_sys.SCRIPT_DIR, rm_sys.GIT_RPD)

        print '\nUpdating the RPD %s with the credentials from %s...\nThis will take several minutes...' % (rpd_path, rm_sys.CONNECTION_POOLS)
        update_rpd_command_input = ['python', os.path.join(rm_sys.SCRIPT_DIR, 'update_rpd.py'), rpd_path,
                                 rm_sys.CONNECTION_POOLS, '-o', temp_rpd_path]

        print 'update_rpd command input: %s' % update_rpd_command_input

        out = rm_sys.run_os_cmd(update_rpd_command_input)
        #print 'RPD update output: %s' % str(out)
        exit_on_error(out)

        print 'Updating the RPD with the saved credentials done!'

        # deploy RPD to OBIEE via WLST
        print('\nDeploying the RPD to OBIEE via WLST...')
        rm_sys.obi.deploy_rpd(temp_rpd_path)
        print '\nDeleting the temporary rpd (%s)...' % temp_rpd_path
        rm_sys.delete_file(temp_rpd_path)
        print('\nCompleted RPD deployment!')

    if not RPD_ONLY:

        if DEPLOY_FROM_FOLDER:
            webcat_root = rm_sys.WEBCAT_DEPLOY_FROM_FOLDER
        else:
            webcat_root = rm_sys.WEBCAT_ARCHIVE

        if WEBCAT_DEPLOY_ALL:
            print 'Deploying all WebCat archives from folder %s' % webcat_root
            wc_archive_list_1 = [f.replace('.base64','') for f in os.listdir(webcat_root)
                               if os.path.isfile(os.path.join(webcat_root, f)) and f[-6:] == 'base64']

            wc_archive_list_2 = [[f, get_txt_file_content(webcat_root, f+'.path')] for f in wc_archive_list_1]

            wc_archive_list = [f for f in wc_archive_list_2 if f[1] != 'N/A']
            wc_archive_list_failed = [f for f in wc_archive_list_2 if f[1] == 'N/A']

            if len(wc_archive_list) == 0 and len(wc_archive_list_failed) > 0:
                print 'All archive file are missing the accompanying .path file where the full Web Catalog path should be stored: %s' % str(wc_archive_list_failed)
            elif len(wc_archive_list) > 0 and len(wc_archive_list_failed) > 0:
                print 'Some archive file are missing the accompanying .path file where the full Web Catalog path should be stored: %s' % str(wc_archive_list_failed)
                print 'The archive files that do have an accompanying .path file: %s' % str(wc_archive_list)

            #for file_name in wc_archive_list:
            #print 'archives: %s' % str(wc_archive_list)
        else:
            print 'Deploying all WebCat archives as defined in the file %s' % rm_sys.WEBCAT_IDX
            wc_archive_list = rm_sys.ws.parse_wc_list()

        rm_sys.ws.connect()
        for archive in wc_archive_list: #rm_sys.ws.parse_wc_list():
            print 'Deploying %s to %s' % ('%s.base64' % archive[0], archive[1])
            content = rm_sys.read_file(os.path.join(webcat_root, '%s.base64' % archive[0]))
            rm_sys.ws.unarchive_wc_dir(content, os.path.dirname(archive[1]), overwrite=True, inc_security=True)
        rm_sys.ws.disconnect()
        print('Completed Webcat deployment.')
    '''

if __name__ == "__main__":
    main()
