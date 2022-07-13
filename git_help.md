# Frequently used Git tips

## Fix last commit message
```
git commit --amend
```

## Undo last commit
```
git reset HEAD^
```

## Checkout one file
```
git checkout <branch> <file>
```

## Copy changes without commit
```
git pull --no-commit --squash origin remote-branch-name
```

## Edit (squash) last two commits
```
git rebase -i HEAD~2
```

## Show unresolved conflicts
```
git diff --check
```

## Flag for staged changes (git diff, for example)
```
--staged
```

## Show diff without whitespace changes
```
git diff -w
```

