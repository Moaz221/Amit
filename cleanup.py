import os

# Delete .gitkeep files
for folder in ['src/Data-ananlysis', 'src/ML', 'src/Python_Sessions']:
    gitkeep = os.path.join(folder, '.gitkeep')
    if os.path.exists(gitkeep):
        os.remove(gitkeep)
        print(f'Deleted {gitkeep}')

# Create .notebook folder
os.makedirs('src/.notebook', exist_ok=True)
print('Created src/.notebook')

# Create .vscode folder
os.makedirs('src/.vscode', exist_ok=True)
print('Created src/.vscode')

print('Done!')