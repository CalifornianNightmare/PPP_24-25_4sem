#!/bin/bash

# Function to calculate Fibonacci numbers
fibonacci() {
    local count=$1
    local a=0
    local b=1

    echo "Fibonacci sequence up to $count terms:"
    for (( i=0; i<count; i++ )); do
        echo -n "$a "
        local temp=$a
        a=$b
        b=$((temp + b))
    done
    echo
}

# Check if the user provided a count
if [ $# -eq 0 ]; then
    echo "Usage: $0 <count>"
    exit 1
fi

# Call the Fibonacci function with the provided count
fibonacci $1
