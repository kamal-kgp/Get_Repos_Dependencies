import requests
import ParseXML

def get_path_contents(user, headers,path):
    selected_repo = input('enter repo name containing pom.xml: ') 
    url = f'https://api.github.com/repos/{user}/{selected_repo}/contents/{path}' 

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            pathContents = response.json() 
            # print(pathContents) 

            print(f"\nDependencies in '{selected_repo}' repository:") 

            pom_url = pathContents['download_url']
            # print(f'pom url: {pom_url}') 

            parsed_dependencies = ParseXML.parse_dependencies(pom_url)
            # print('parsing pom.xml....') 

            if parsed_dependencies:
                # print(f"Total number of dependencies: {len(parsed_dependencies)}")
                sno = 1
                for key, dependency in parsed_dependencies.items():
                    print(f"{sno} Dependency: {key} - Version: {dependency['version']}")
                    sno += 1

            showAnotherRepo = input(f"show another repo's dependencies (y/n)")
            if(showAnotherRepo.lower() == 'y'):
                get_path_contents(user, headers, path)  
            else:
                exit() 
        else:
            print(f'Error: {response.status_code}, {response.text}')
    except Exception as e:
        print(f'Error while getting pom.xml contents: {e}') 


def getRepoList(access_token):
    user = input('enter your github user name: ') 
    print(f'List of repos for user: {user}')

    repo_url = 'https://api.github.com/user/repos' 
    headers = {
        'Accept': 'application/vnd.github+json',
        'X-GitHub-Api-Version': '2022-11-28', 
        'User-Agent': 'cloudD', 
        'Authorization': f'Bearer {access_token}'  
    }  
    try:
        response = requests.get(repo_url, headers=headers) 
        if response.status_code == 200:
            repos = response.json()
            sno = 1 
            for repo in repos:
                print (sno, repo['name']) 
                sno += 1 
            
            get_path_contents(user, headers, 'pom.xml')
        else:
            print(f'Error: {response.status_code}, {response.text}')
    except Exception as e:
        print(f'Error while getting repos list: {e}')
        exit()

