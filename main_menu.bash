# We do this using bash cause of the arbitrary command amount we have to hit for each language. Trust me, I would much rather do this in python.
./verify.bash

db_file="players.db"

create_character() {
    read -p "Enter the name for the new character: " name
    x=5
    y=5
    mapname="maps/quad.json"
    inventory=""
    sqlite3 "$db_file" "INSERT INTO players (name, x, y, inventory, mapname) VALUES ('$name', $x, $y, '$inventory', '$mapname');"
    echo "Character created successfully!"
    python main.py game "$name" $x $y "$mapname" "$inventory"
}

select_character() {
    clear
    echo "Available characters:"
    echo
    sqlite3 -header -column "$db_file" "SELECT id, name FROM players;"

    read -p "Enter the ID of the character you want to select (or 0 to create a new character): " character_id

    if [ "$character_id" -eq 0 ]; then
        create_character
    else
        # Retrieve character details from the database
        mapfile -t character_details < <(sqlite3 -separator "|" "$db_file" "SELECT name, x, y, inventory, mapname FROM players WHERE id = $character_id;")

        if [ "${#character_details[@]}" -eq 0 ]; then
            echo "Invalid character ID."
            read
        else
            # Assign values to variables
            IFS='|' read -r name x y inventory mapname <<< "${character_details[0]}"
            echo "Character selected:"
            echo "Name: $name"
            echo "Coordinates: ($x, $y)"
            echo "Inventory: $inventory"
            echo "Map: $mapname"
            echo "Press ENTER to start!"
            python main.py game "$name" $x $y "$mapname" "$inventory"
        fi
    fi
}

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
    1) clear; echo -e "\e[1;36mOpen Editor\e[0m";
        echo "0. ==New Map=="
        ls maps/*.json | awk -F/ '{print $2}' | awk -F. '{print NR ". " $1}'
        read -p "Enter the number of the map: " choice
        selected_map=""
        if [ "$choice" == "0" ]; then
            selected_map="new"
        else
            selected_map=$(ls maps/*.json | awk -F/ '{print $2}' | awk -F. '{print $1}' | sed -n "${choice}p")
        fi

        python main.py editor "$selected_map"
        clear;;
    2) echo -e "\e[1;36mOpen Game\e[0m"; select_character; clear;;
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

