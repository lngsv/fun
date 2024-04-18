ZSH_THEME="candy-patched"

# zsh 5.0.2

__get_jump_box() {
  declare -A jump_boxes
  jump_boxes=( ldz ldzls105i nyz nyzls105i sgz sgzls105i )
  local site="$(hostname | cut -c1-3)"
  local jump_box=${jump_boxes[${site}]}
  echo "${jump_box}"
}
__get_deploy_box() {
  declare -A deploy_boxes
  deploy_boxes=( ldz ldzls160i nyz nyzls160i sgz sgzls160i )
  local site="$(hostname | cut -c1-3)"
  local deploy_box=${deploy_boxes[${site}]}
  echo "${deploy_box}"
}
function __sudosh {
  if [[ -z ${1:-} ]]; then
      echo "No username given"
      return
  fi
  local jump_box=$(__get_jump_box)
  local user="${1}"
  print ${jump_box}
  ssh -t "${jump_box}" "sudo -u "${user}" /usr/bin/sudosh"
}
alias sudosh=__sudosh
alias jmp_ro='sudosh sys_sp_prod_ro'
alias jmp_dev='sudosh sp_dev'
alias jmp_risk='sudosh sp_risk'
alias jmp_riskp='sudosh sp_risk_prd'
alias jmp_prod='sudosh sp_prod'
alias jmp_stage='sudosh sp_stage'
alias jmp_qa='sudosh sp_qa'
alias jmp_me="ssh $(__get_jump_box)"
alias dpl_me="ssh $(__get_deploy_box)"
alias dev_me="ssh ldzls580d"

sqpc_deploy() {
  if [ -z "$1" ]; then
    echo "No username given"
    return 1
  fi
  
  ssh -t "$(__get_deploy_box)" "sudo -u "$1" /apps/hft/bin/sqpc_deploy ${@:2}"
}