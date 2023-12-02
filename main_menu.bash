function goto {
  echo -e "\033[$1;${2:-1}H"
}

function display_menu {
  clear
  echo -e "\e[1;32m╔════════════════════════════╗\e[0m"
  echo -e "\e[1;32m║        Menu Options        ║\e[0m"
  echo -e "\e[1;32m╠════════════════════════════╝\e[0m"

  option_count=0
  for option_text in "Open Editor" "Open Game" "Exit"; do
    option_count=$((option_count + 1))
    if [ $option_count -eq $selected_option ]; then
      echo -e "\e[1;33m║  \e[0m\e[1;36m$option_count. $option_text\e[0m\e[1;33m\e[0m"
    else
      echo -e "\e[1;32m║  \e[0m\e[1;37m$option_count. $option_text\e[0m\e[1;32m\e[0m"
    fi
  done

  echo -e "\e[1;32m╚═════════════════════════════\e[0m"
  echo "Press Enter to select an option."
}

function handle_option {
  case $selected_option in
    1) echo -e "\e[1;36mOpen Editor\e[0m"; python main.py editor; clear;;
    2) echo -e "\e[1;36mOpen Game\e[0m"; python main.py game; clear;;
    3) echo -e "\e[1;36mExit\e[0m"; exit;;
  esac
  sleep 1
}

function read_option {
  read -s -n 1 option
  case $option in
    [0-9])
      selected_option=$option
      ;;
    "") # Enter key
      handle_option
      ;;
    *)
      ;;
  esac
}

trap 'goto 12 1; exit' SIGINT SIGTERM

selected_option=1

while true; do
  display_menu
  goto $((selected_option + 6))
  read_option
  goto 12 1
done

