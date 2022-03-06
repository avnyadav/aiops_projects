Clonning source code from repo

```
git clone <https://github.com/Avnish327030/aiops_projects.git>
```

TO add files into staging or to allow file to be tracked by git
```
git add <file_name>
```
Replace "you@example.com" with github email id
```
 git config --global user.email "you@example.com"
```

Replace "Your Name" with user name of github
```
git config --global user.name "Your Name"
```

To perform commit
```
git commit -m "Write your message about your changes"
```

Rename current branch to main branch
```
git branch -M main
```

To list the branch name
```
git branch
```

To check remote branch url and variable name
```
git remote -v
```


To send changes to remote branch
``
git push <remote_branch_variable> <branch_name>
```



To remove file from staging area
```
git rm --cached <file_name>
```