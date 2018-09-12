import subprocess
import os
import time
import sys
import getpass
import re

_location_ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

# To pause the screen
def pause():
    print('Press Enter when done')
    pressEnter = input()

# Total Servers and List All Servers on the Chef Server
def listServers():
    chefServers = open(os.path.join(_location_, 'chefservers.txt'))
    chefServersContent = chefServers.read()
    chefServerList = chefServersContent.split('\n')
    print("There are a total of: %s" %(len(chefServerList)-1))
    print('Would you like to see a list of servers? (yes or no)')
    answer = input().lower()
    if answer.startswith('y'):
        for i in range(len(chefServerList)-1):
            print("Server[" + str(i + 1) + "]: " + chefServerList[i])
        pause()
    chefServers.close()

# List Cookbooks on the Chef Server
def cookbookList():
    subprocess.call('knife cookbook list', shell=True)
    pause()

# Search the list for the server
# Replace by searchList_regex
def searchList():
    while True:
        print('please enter [server name] or [q] to quit? ')
        serverName = input().lower()
        if serverName == 'q':
            break
        else:
            chefServers = open(os.path.join(_location_, 'chefservers.txt'))
            chefServersContent = chefServers.read()
            chefServerList = chefServersContent.split('\n')
            chefServerListLower = [x.lower() for x in chefServerList]
            if serverName in chefServerListLower:
                print('Server: ' + serverName + ' Exists')
                time.sleep(3)
            else:
                print('Server: ' + serverName + ' is not present')
                time.sleep(3)
            chefServers.close()

def searchList_regex():
    while True:
        print('please enter [server name] or [q] to quit? ')
        serverName = input()
        if serverName == 'q':
            break
        else:
            chefServers = open(os.path.join(_location_, 'chefservers.txt'))
            chefServersContent = chefServers.read()
            chefServerList = chefServersContent.split('\n')
            for i in chefServerList:
                if re.search(r"^" + serverName,i,re.IGNORECASE):
                    print('Server: ' + i)
            chefServers.close()
            pause()

# Add recipe to specified instance
def addRecipe():
    recipe = input('Which recipe would you like to add \n')
    server = input('Which Server? \n')
    chefServers = open(os.path.join(_location_, 'chefservers.txt'))
    chefServersContent = chefServers.read()
    chefServerList = chefServersContent.split('\n')
    for i in chefServerList:
        if server.lower() == i.lower():
            recipeServer = 'knife node run_list add %s \'recipe[%s]\'' % (i, recipe)
            add_recipe = input("Are you sure you want to add %s to this recipe %s (y or no)\n>> " % (i, recipe))
            if add_recipe.startswith('y'):
                oneAdd = subprocess.call(recipeServer, shell=True)
                print(oneAdd)
    chefServers.close()
    pause()

# Add role to specified instance
def addRole():
    recipe = input('Which role would you like to add \n')
    chefServers = open(os.path.join(_location_, 'roleservers.txt'))
    chefServersContent = chefServers.read()
    chefServerList = chefServersContent.split('\n')
    for i in chefServerList:
            recipeServer = 'knife node run_list add %s \'role[%s]\'' % (i, recipe)
            add_recipe = input("Are you sure you want to add %s to this recipe %s (y or no)\n>> " % (i, recipe))
            if add_recipe.startswith('y'):
                oneAdd = subprocess.call(recipeServer, shell=True)
                print(oneAdd)
    chefServers.close()
    pause()

# This function is for bootstrapping windows and linux servers
def bootstrapping():
    while True:
        option = input('Press [1] for Windows and [2] for Linux\n')
        ipaddress = input('What is the ip address?(In AD leave blank)\n ')
        server = input('What is the name of the server?\n ')
        admin = input('What is the admin name?\n ')
        #password = input('Please enter password or pem for linux?\n ')
        password = getpass.getpass(prompt='Please enter password? ')
        print(password)
        recipes = recipes1()
        if ipaddress == '':
            if option == '1':
                print('You choose windows')
                installchef = open('bootstrapping.txt', 'a')
                installchef.write('knife bootstrap windows winrm %s -N %s --winrm-user "%s" --winrm-password "%s" --run-list \'%s\' \n' % (server, server, admin, password, recipes))
                print('Would you like to add another server? (yes, no) ')
                anotherServer = input().lower()
                if anotherServer.startswith('n'):
                    installchef.close()
                    break
            else:
                print('You choose linux')
                installchef = open('bootstrapping.txt', 'a')
                installchef.write('knife bootstrap %s -N %s -x %s --identity-file %s --run-list \'%s\' --sudo \n' % (server, server, admin, password, recipes))
                print('Would you like to add another server? (yes, no) ')
                anotherServer = input().lower()
                if anotherServer.startswith('n'):
                    installchef.close()
                    break
        else:
            if option == '1':
                print('You choose windows')
                installchef = open('bootstrapping.txt', 'a')
                installchef.write('knife bootstrap windows winrm %s -N %s --winrm-user "%s" --winrm-password "%s" --run-list \'%s\' \n' % (ipaddress, server, admin, password, recipes))
                print('Would you like to add another server? (yes, no) ')
                anotherServer = input().lower()
                if anotherServer.startswith('n'):
                    installchef.close()
                    break
            else:
                print('You choose linux')
                installchef = open('bootstrapping.txt', 'a')
                installchef.write('knife bootstrap %s -N %s -x %s --identity-file %s --run-list \'%s\' --sudo \n' % (ipaddress, server, admin, password, recipes))
                print('Would you like to add another server? (yes, no) ')
                anotherServer = input().lower()
                if anotherServer.startswith('n'):
                    installchef.close()
                    break
    bootstrapping = open(os.path.join(_location_, 'bootstrapping.txt'))
    bootstrappingContent = bootstrapping.read()
    bootstrappingList = bootstrappingContent.split('\n')
    for serverName in bootstrappingList:
        runBootstrapping = subprocess.call(serverName, shell=True)
        print(runBootstrapping)
    bootstrapping.close()
    removebootstrapping()

# Remove Servers from ChefServer
def removeServers():
    removeServer = []
    chefServers = open(os.path.join(_location_, 'chefservers.txt'))
    chefServersContent = chefServers.read()
    chefServerList = chefServersContent.split('\n')
    while True:
        r_server = input("Enter Server you want to remove type r to run\n>> ")
        if r_server != 'r':
            removeServer.append(r_server)
            print(removeServer)
        else:
            break
    for i in range(len(chefServerList)-1):
        for k in range(len(removeServer)):
            if chefServerList[i].lower() == removeServer[k].lower():
                print("Server[" + str(i + 1) + "]: " + chefServerList[i])
                r_node = ("knife node delete %s -y" % (chefServerList[i]))
                r_client = ("knife client delete %s -y" % (chefServerList[i]))
                r_node_sub = subprocess.call(r_node, shell=True)
                r_client_sub = subprocess.call(r_client, shell=True)
                print(r_node_sub)
                print(r_client_sub)
            else:
                continue
    chefServers.close()
    pause()

# Add recipes to list and format for bootstapping
run_list = []
def recipes1():
    run_list_modified = ""
    while True:
        recipes = input('Please enter recipes? or q to quit\n ')
        if recipes != 'q':
            run_list.append(recipes)
            print(run_list)
        else:
            break
    for i in run_list:
        run_list_modified += "recipe[%s]," %(i)
    print(run_list_modified)
    run_list_modified = run_list_modified.rstrip(',')
    return run_list_modified
        
# Deletes File when done
def removeFile():
    f = os.path.join(_location_, 'chefservers.txt')
    try:
        os.remove(f)
    except OSError:
        pass

# Delete bootstrapping file if it exists.
def removebootstrapping():
    f = os.path.join(_location_, 'bootstrapping.txt')
    try:
        os.remove(f)
    except OSError:
        pass

# Delete recipe file if it exists.
def removeRecipe():
    f = os.path.join(_location_, 'recipes.txt')
    try:
        os.remove(f)
    except OSError:
        pass

# Start of Program
removeFile()
removebootstrapping()
removeRecipe()
print('Welcome to Chef.... Please Wait')
subprocess.call('knife node list | sort > chefservers.txt', shell=True)
while True:
    print('\n' * 75)
    print('----------------')
    print('Welcome to Chef')
    print('WARNING -- You need to be in your chef-repo')
    print('What would you like to do?')    
    print('[1] List of servers \n[2] Cookbooks \n[3] Search \n[4] Bootstrapping \n[5] Remove Servers From Chef \n[6] Add Recipe \n[q] Quit')
    answer = input('\n>> ')
    if answer == '1':
        listServers()
    elif answer == '2':
        cookbookList()
    elif answer == '3':
        searchList_regex()
    elif answer == '4':
        bootstrapping()
    elif answer == '5':
        removeServers()
    elif answer == '6':
        addRecipe()
    elif answer == '7':
        # Not working yet
    	list5hourOld()
    elif answer == '8':
        addRole()
    else:
        break
removeFile()
removebootstrapping()
removeRecipe()