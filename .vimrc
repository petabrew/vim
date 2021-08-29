set rtp +=~/.vim/bundle/Vundle.vim
call vundle#begin()
Plugin 'VundleVim/Vundle.vim'
Plugin 'The-NERD-tree'
call vundle#end()

syntax on
set autoindent
set cindent
set nu
set ts=4
set shiftwidth=4
set noimd

nmap <F2> :NERDTreeToggle<CR>

