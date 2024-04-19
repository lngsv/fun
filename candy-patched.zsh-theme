ZSH_THEME_GIT_PROMPT_PREFIX="%{$fg[green]%}["
ZSH_THEME_GIT_PROMPT_SUFFIX="]%{$reset_color%}"
ZSH_THEME_GIT_PROMPT_DIRTY=" %{$fg[red]%}*%{$fg[green]%}"
ZSH_THEME_GIT_PROMPT_CLEAN=""

function parse_git_dirty {
    [[ -n "$(git status --porcelain 2>/dev/null)" ]] && echo $ZSH_THEME_GIT_PROMPT_DIRTY
}
function get_current_git_branch {
    { git symbolic-ref --short -q HEAD || git describe --tags --exact-match || git rev-parse --short HEAD; } 2>/dev/null
}
function my_git_prompt {
    local current_branch="$(get_current_git_branch)"
    [[ -n $current_branch ]] && echo "$ZSH_THEME_GIT_PROMPT_PREFIX$current_branch$(parse_git_dirty)$ZSH_THEME_GIT_PROMPT_SUFFIX"
}

PROMPT=$'%{$fg_bold[green]%}%n@%m %{$fg[blue]%}%D{[%X]} %{$reset_color%}%{$fg[white]%}[%~]%{$reset_color%} $(my_git_prompt)\
%{$fg[blue]%}->%{$fg_bold[blue]%} %#%{$reset_color%} '
