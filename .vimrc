filetype plugin indent on
" show existing tab with 4 spaces width
set tabstop=4
" when indenting with '>', use 4 spaces width
set shiftwidth=4
" On pressing tab, insert 4 spaces
set expandtab
" Delete 4 spaces by backspace
set softtabstop=4
set nu
set mouse=a
syntax on
" cut trailing spaces
autocmd BufWritePre * :%s/\s\+$//e
" highlight line tail that is greater than 80 characters
match ErrorMsg '\%>80v.\+'
