import subprocess
import os
import time
import sys

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
    chefServers = open(os.path.join(_location_, 'chefservers.txt'))
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

# TODO: Add subprocess to run the file
# This function is for bootstrapping windows and linux servers
def bootstrapping():
    while True:
        print('Press [1] for Windows and [2] for Linux')
        option = input()
        print('What is the ip address?(In AD leave blank) ')
        ipaddress = input()
        print('What is the name of the server? ')
        server = input()
        print('What is the admin name? ')
        admin = input()
        print('Please enter password? ')
        password = input()
        print('Please enter recipes? ')
        recipes = input()
        if ipaddress == '':
            if option == '1':
                print('You choose windows')
                installchef = open('bootstrapping.txt', 'a')
                installchef.write('knife bootstrap windows winrm %s -N %s --winrm-user %s --winrm-password %s --run-list \'recipe[%s]\' \n' % (server, server, admin, password, recipes))
                print('Would you like to add another server? (yes, no) ')
                anotherServer = input().lower()
                if anotherServer.startswith('n'):
                    installchef.close()
                    break
            else:
                print('You choose linux')
                installchef = open('bootstrapping.txt', 'a')
                installchef.write('knife bootstrap %s -N %s -x %s --ssh-password %s --run-list \'recipe[%s]\' --sudo \n' % (server, server, admin, password, recipes))
                print('Would you like to add another server? (yes, no) ')
                anotherServer = input().lower()
                if anotherServer.startswith('n'):
                    installchef.close()
                    break
        else:
            if option == '1':
                print('You choose windows')
                installchef = open('bootstrapping.txt', 'a')
                installchef.write('knife bootstrap windows winrm %s -N %s --winrm-user %s --winrm-password %s --run-list \'recipe[%s]\' \n' % (ipaddress, server, admin, password, recipes))
                print('Would you like to add another server? (yes, no) ')
                anotherServer = input().lower()
                if anotherServer.startswith('n'):
                    installchef.close()
                    break
            else:
                print('You choose linux')
                installchef = open('bootstrapping.txt', 'a')
                installchef.write('knife bootstrap %s -N %s -x %s --ssh-password %s --run-list \'recipe[%s]\' --sudo \n' % (ipaddress, server, admin, password, recipes))
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

# Start of Program
print('Welcome to Chef.... Please Wait')
subprocess.call('knife node list | sort > chefservers.txt', shell=True)
while True:
    print('\n' * 75)
    print('----------------')
    print('Welcome to Chef')
    print('WARNING -- You need to be in your chef-repo')
    print('What would you like to do?')    
    print('[1] for list of servers \n[2] for cookbooks \n[3] for search \n[4] for bootstrapping or \n[q] for quit')
    answer = input()
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
    else:
        break
print('Remove all cached files? (yes or no)')
removeFiles = input().lower()
if removeFiles.startswith('y'):
    removeFile()
    removebootstrapping()
    removeRecipe()