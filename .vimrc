set rtp +=~/.vim/bundle/Vundle.vim
call vundle#begin()
Plugin 'VundleVim/Vundle.vim'
Plugin 'The-NERD-tree'
call vundle#end()

syntax on
set nu
set autoindent
set cindent
set noimd

set smartindent
set tabstop=4
set expandtab
set shiftwidth=4


nmap <F2> :NERDTreeToggle<CR>

