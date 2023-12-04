#!/usr/bin/perl
use strict;
use warnings;
use Term::ReadKey;

# Game settings
my $width  = 20;
my $height = 10;
my $snake  = [{x => 5, y => 5}];
my $direction = 'right';
my $food      = generate_food();

# Main game loop
while (1) {
    system('clear'); # Clear the terminal (Unix) or use 'cls' for Windows
    
    # Draw the game board
    draw_board();

    # Get user input
    my $key = ReadKey(-1);
    if (defined $key) {
        $direction = change_direction($key);
    }

    # Move the snake
    move_snake();

    # Check for collisions
    if (check_collision()) {
        print "Game Over!\n";
        last;
    }

    # Check if the snake ate the food
    if ($snake->[0]{x} == $food->{x} && $snake->[0]{y} == $food->{y}) {
        push @{$snake}, {}; # Add a new segment to the snake
        $food = generate_food();
    }

    # Sleep for a short duration to control the game speed
    sleep(0.1);
}

# Subroutine to draw the game board
sub draw_board {
    # Draw the snake
    foreach my $segment (@$snake) {
        print "O ";
    }

    # Draw the food
    print "\n" . (' ' x ($food->{x} * 2)) . 'X' . (' ' x (($width - $food->{x} - 1) * 2)) . "\n";

    # Draw the bottom border
    print '-' x ($width * 2) . "\n";
}

# Subroutine to move the snake
sub move_snake {
    # Move each segment of the snake
    for my $i (reverse 1..$#{$snake}) {
        $snake->[$i]{x} = $snake->[$i-1]{x};
        $snake->[$i]{y} = $snake->[$i-1]{y};
    }

    # Move the head of the snake based on the current direction
    if ($direction eq 'up') {
        $snake->[0]{y}--;
    } elsif ($direction eq 'down') {
        $snake->[0]{y}++;
    } elsif ($direction eq 'left') {
        $snake->[0]{x}--;
    } elsif ($direction eq 'right') {
        $snake->[0]{x}++;
    }

    # Wrap around the screen edges
    $snake->[0]{x} = 0 if $snake->[0]{x} >= $width;
    $snake->[0]{x} = $width - 1 if $snake->[0]{x} < 0;
    $snake->[0]{y} = 0 if $snake->[0]{y} >= $height;
    $snake->[0]{y} = $height - 1 if $snake->[0]{y} < 0;
}

# Subroutine to check for collisions (with walls or itself)
sub check_collision {
    # Check for collision with walls
    return 1 if $snake->[0]{x} >= $width || $snake->[0]{x} < 0 || $snake->[0]{y} >= $height || $snake->[0]{y} < 0;

    # Check for collision with itself
    for my $i (1..$#{$snake}) {
        return 1 if $snake->[0]{x} == $snake->[$i]{x} && $snake->[0]{y} == $snake->[$i]{y};
    }

    return 0;
}

# Subroutine to generate random food coordinates
sub generate_food {
    return { x => int(rand($width)), y => int(rand($height)) };
}

# Subroutine to change the direction based on user input
sub change_direction {
    my $key = shift;

    if ($key eq 'w') {
        return 'up';
    } elsif ($key eq 's') {
        return 'down';
    } elsif ($key eq 'a') {
        return 'left';
    } elsif ($key eq 'd') {
        return 'right';
    }

    return $direction; # If an invalid key is pressed, maintain the current direction
}

