scale=1
xsize=16*$scale
ysize=9*$scale

username="kyle"
playerxloc=$((xsize / 2))
playeryloc=$((ysize / 2))

locked=1

chestxloc=$((xsize / 2))
chestyloc=1
chestopened=0

enemycount=0

declare -A room

build_room() {
    locked=1
    chestopened=0

    for ((y = 0; y < ysize; y++)); do
        for ((x = 0; x < xsize; x++)); do
            if [ "$x" -eq 0 ]; then
                room[$x,$y]=1
            elif [ "$y" -eq 0 ]; then
                room[$x,$y]=1
            elif [ "$x" -eq $(($xsize - 1)) ]; then
                room[$x,$y]=1
            elif [ "$y" -eq $(($ysize - 1)) ]; then
                room[$x,$y]=1
            else
                room[$x,$y]=0
            fi
        done
    done

    room[0,$((ysize/2))]=3
    room[0,$(($((ysize/2))-1))]=3


    room[$((xsize-1)),$((ysize/2))]=3
    room[$((xsize-1)),$(($((ysize/2))-1))]=3

    room[$((xsize / 2)),1]=4

    enemycount=0
    for ((y = 0; y < ysize; y++)); do
        for ((x = 0; x < xsize; x++)); do
            if [ ${room[$x,$y]} -eq 0 ]; then
                random_number=$(( (RANDOM % (xsize*ysize)) / ((xsize*ysize) / 24) ))
                if [ $random_number -eq 2 ]; then
                    if [ $enemycount -lt 3 ]; then
                        enemycount=$(($enemycount+1))
                        room[$x,$y]=5
                    fi
                fi
            fi
        done
    done
}

declare -A overlay

build_overlay() {
    for ((y = 0; y < ysize; y++)); do
        for ((x = 0; x < xsize; x++)); do
            overlay[$x,$y]=0
        done
    done
    overlay[$playerxloc,$playeryloc]=1
}

draw_screen() {
    for ((y = 0; y < ysize; y++)); do
        renderstring=""
        for ((x = 0; x < xsize; x++)); do
            object=${room[$x,$y]}
            overlay_object=${overlay[$x,$y]}
            cchar=""
            if [ $overlay_object -eq 0 ]; then
                if [ "$object" -eq 1 ]; then
                    cchar="██"
                elif [ "$object" -eq 0 ]; then
                    cchar="  "
                elif [ "$object" -eq 3 ]; then
                    if [ "$locked" -eq 1 ]; then
                        cchar="▣▣"
                    else
                        cchar="□□"
                    fi
                elif [ "$object" -eq 4 ]; then
                    if [ $chestopened -eq 0 ]; then
                        cchar="⍐⍐"
                    else
                        cchar="⍞⍞"
                    fi
                elif [ "$object" -eq 5 ]; then
                    cchar="⋐⋑"
                else
                    cchar="╳╳"
                fi
            else
                if [ $overlay_object -eq 1 ]; then
                    cchar="${username:0:2}"
                fi
            fi
            renderstring="$renderstring$cchar"
        done
        echo "$renderstring"
    done
}

build_room

valid_movement() {
    object=${room[$1,$2]}

    if [ "$object" -eq 1 ]; then
        return 0
    elif [ "$object" -eq 3 ]; then
        if [ $locked -eq 1 ]; then
            return 0
        else
            if [ $playerxloc -eq 1 ]; then
                playerxloc=$((xsize-2))
            elif [ $playerxloc -eq $((xsize-2)) ]; then
                playerxloc=1
            fi
            build_room
            return 0
        fi
    elif [ "$object" -eq 4 ]; then
        chestopened=1
        locked=0
        return 0
    else
        return 1
    fi
}

move() {
    valid_movement $1 $2
    if [ $? -eq 1 ]; then
        playerxloc=$1
        playeryloc=$2
    fi
}

while true; do
    clear
    build_overlay
    draw_screen
    read -n 1 keypress
    if [ "$keypress" = "d" ]; then
        move $(($playerxloc+1)) $playeryloc
    elif [ "$keypress" = "a" ]; then
        move $(($playerxloc-1)) $playeryloc
    elif [ "$keypress" = "s" ]; then
        move $playerxloc $(($playeryloc+1))
    elif [ "$keypress" = "w" ]; then
        move $playerxloc $(($playeryloc-1))
    fi
done

