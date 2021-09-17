set rtp +=~/.vim/bundle/Vundle.vim
call vundle#begin()
Plugin 'VundleVim/Vundle.vim'
Plugin 'The-NERD-tree'
call vundle#end()

syntax on
set nu
set autoindent
set cindent
set ts=4
set shiftwidth=4
set noimd
set smartindent
set expandtab
set et


nmap <F2> :NERDTreeToggle<CR>

