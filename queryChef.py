import subprocess
import os
import time
import sys
import getpass

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
    print(len(chefServerList)-1)
    print('Would you like to see a list of servers? (yes or no)')
    answer = input().lower()
    if answer.startswith('y'):
        for i in range(len(chefServerList)-1):
            print("Server[" + str(i + 1) + "]: " + chefServerList[i].lower())
        pause()
    chefServers.close()

# List Cookbooks on the Chef Server
def cookbookList():
    subprocess.call('knife cookbook list', shell=True)
    pause()

# Search the list for the server
# TODO: split domain name from server when searching
def searchList():
    while True:
        print('please enter [server name] or [q] to quit? ')
        serverName = input().lower()
        print(serverName)
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

# Add recipe to all servers
def multiRecipe():
    chefServers = open(os.path.join(_location_, 'chefservers2.txt'))
    chefServersContent = chefServers.read()
    chefServerList = chefServersContent.split('\n')
    recipes = open('recipes.txt', 'a')
    print('Which recipe would you like to add to all servers?')
    answer = input()
    recipes = open('recipes.txt', 'a')
    for i in range(len(chefServerList)):
        recipes.write('knife node run_list add ' + chefServerList[i] + ' \'recipe[%s]\' \n' % (answer))
    print('Would you like to run the recipe? ')
    runRecipeAnswer = input()
    runRecipe3 = open(os.path.join(_location_, 'recipes.txt'))
    runRecipe3Content = runRecipe3.read()
    runRecipe3List = runRecipe3Content.split('\n')
    if runRecipeAnswer.lower().startswith('y'):
        for addRecipe in runRecipe3List:
            runRecipe = subprocess.call(addRecipe, shell=True)
            print(runRecipe)
    recipes.close()
    chefServers.close()

def addRecipe():
    recipe = input('Which recipe would you like to add \n')
    server = input('Which Server? \n')
    recipeServer = 'knife node run_list add %s \'recipe[%s]\'' % (server, recipe)
    oneAdd = subprocess.call(recipeServer, shell=True)
    print(oneAdd)
    pause()

# This function is for bootstrapping windows and linux servers
def bootstrapping():
    while True:
        option = input('Press [1] for Windows and [2] for Linux\n')
        ipaddress = input('What is the ip address?(In AD leave blank)\n ')
        server = input('What is the name of the server?\n ')
        admin = input('What is the admin name?\n ')
        password = input('Please enter password?\n ')
        # password = getpass.getpass('Please enter password?\n')
        recipes = recipes1()
        if ipaddress == '':
            if option == '1':
                print('You choose windows')
                installchef = open('bootstrapping.txt', 'a')
                installchef.write('knife bootstrap windows winrm %s -N %s --winrm-user %s --winrm-password %s --run-list \'%s\' \n' % (server, server, admin, password, recipes))
                print('Would you like to add another server? (yes, no) ')
                anotherServer = input().lower()
                if anotherServer.startswith('n'):
                    installchef.close()
                    break
            else:
                print('You choose linux')
                installchef = open('bootstrapping.txt', 'a')
                installchef.write('knife bootstrap %s -N %s -x %s --ssh-password %s --run-list \'%s\' --sudo \n' % (server, server, admin, password, recipes))
                print('Would you like to add another server? (yes, no) ')
                anotherServer = input().lower()
                if anotherServer.startswith('n'):
                    installchef.close()
                    break
        else:
            if option == '1':
                print('You choose windows')
                installchef = open('bootstrapping.txt', 'a')
                installchef.write('knife bootstrap windows winrm %s -N %s --winrm-user %s --winrm-password %s --run-list \'%s\' \n' % (ipaddress, server, admin, password, recipes))
                print('Would you like to add another server? (yes, no) ')
                anotherServer = input().lower()
                if anotherServer.startswith('n'):
                    installchef.close()
                    break
            else:
                print('You choose linux')
                installchef = open('bootstrapping.txt', 'a')
                installchef.write('knife bootstrap %s -N %s -x %s --ssh-password %s --run-list \'%s\' --sudo \n' % (ipaddress, server, admin, password, recipes))
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

# Remove Old Servers From Chef Server
def list5hourOld():
	print ('This will list all servers that have not communicated with the chef server in 24 hours')
	# subprocess.call("knife search node \"ohai_time:[* TO $(date +\%s -d \'5 hours ago\')]\"", shell=True)
	oldServer = "knife search node \"ohai_time:[* TO $(date +\%s -d \'5 hours ago\')]\" -i"
	for node in oldServer:
		print(node)

def removeServers():
        answer = input('Which server would you like to remove?')
        try:
        	removeServerText = open('RemoveServers.txt', 'a')
        except IOError:
        	print("File not found or path is incorrect")
        finally:
	        removeServerText.write('knife node list | grep -i %s' % (answer))
	        textfile = open(os.path.join(_location_, 'RemoveServers.txt'))
	        textfileContent = textfile.read()
	        textfileList = textfileContent.split('\n')
	        for serverName in textfileList:
	            runtextfile = subprocess.call(serverName, shell=True)
	            print(runtextfile)
	        removeServerText.close()

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
    os.remove(f)

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
print('Welcome to Chef.... Please Wait')
subprocess.call('knife node list | sort > chefservers.txt', shell=True)
while True:
    print('\n' * 75)
    print('----------------')
    print('Welcome to Chef')
    print('WARNING -- You need to be in your chef-repo')
    print('What would you like to do?')    
    print('[1] List of servers \n[2] Cookbooks \n[3] Search \n[4] Bootstrapping \n[5] Bulk Add \n[6] Add Recipe \n[7] Remove Old Servers \n[q] Quit')
    answer = input('\n>> ')
    if answer == '1':
        listServers()
    elif answer == '2':
        cookbookList()
    elif answer == '3':
        searchList()
    elif answer == '4':
        bootstrapping()
    elif answer == '5':
        multiRecipe()
    elif answer == '6':
        addRecipe()
    elif answer == '7':
    	list5hourOld()
    elif answer == '8':
        removeServers()
    else:


        break
print('Remove all cached files? (yes or no)')
removeFiles = input().lower()
if removeFiles.startswith('y'):
    removeFile()
    removebootstrapping()
    removeRecipe()