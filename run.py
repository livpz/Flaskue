from os import walk, path
from main import App

App.build_app()
app = App.get_app()

for root, folders, files in walk('./BluePrint/'):
    for folder in folders:
        if folder[-3:] == '_bp':
            print(
                'root:', root, '\n',
                'folder:', folder
            )
            root = root.replace('/','')
            root = root.replace('.','')
            path = '.'.join([root, folder,'setup'])
            print('Joined_path: ', path)
            __import__(path)


if __name__ == '__main__':
    App.run_app()