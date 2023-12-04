use strict;
use warnings;

my @snake = ( [2, 2], [2, 1] );
my $snake_length = 2;
my $food_x = int(rand(5));
my $food_y = int(rand(5));
my $direction = 'right';
sub is_snake_position {
    my ($x, $y) = @_;

    return grep { $_->[0] == $x && $_->[1] == $y } @snake;
}

while (1) {
    system("clear");
    print "!PERL 🐍 ARCADE!\n";
    for my $row (0..4) {
        for my $col (0..4) {
            if ($row == $food_y && $col == $food_x) {
                print "* ";
            } elsif (is_snake_position($col, $row)) {
                print "O ";
            } else {
                print ". ";
            }
        }
        print "\n";
    }

    system("stty -icanon -echo");
    my $key = getc(STDIN);
    system("stty icanon echo");

    last if $key eq 'q';

    if ($key eq 'w' && $direction ne 'down') {
        $direction = 'up';
    } elsif ($key eq 'a' && $direction ne 'right') {
        $direction = 'left';
    } elsif ($key eq 's' && $direction ne 'up') {
        $direction = 'down';
    } elsif ($key eq 'd' && $direction ne 'left') {
        $direction = 'right';
    }

    my ($head_x, $head_y) = @{$snake[0]};
    if ($direction eq 'up') {
        $head_y--;
    } elsif ($direction eq 'down') {
        $head_y++;
    } elsif ($direction eq 'left') {
        $head_x--;
    } elsif ($direction eq 'right') {
        $head_x++;
    }

    if ($head_x < 0 || $head_x >= 5 || $head_y < 0 || $head_y >= 5 || is_snake_position($head_x, $head_y)) {
        print "Game Over!\n";
        last;
    }

    if ($head_x == $food_x && $head_y == $food_y) {
        $snake_length++;
        do {
            $food_x = int(rand(5));
            $food_y = int(rand(5));
        } while (is_snake_position($food_x, $food_y));
    }

    unshift @snake, [$head_x, $head_y];

    if (scalar @snake > $snake_length) {
        pop @snake;
    }

    # sleep(1);
}

