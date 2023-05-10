#!/bin/bash

# Check that exactly two command-line arguments were passed
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 num1 num2"
    exit 1
fi

# Read the two command-line arguments
num1="$1"
num2="$2"

# Add the two numbers together
sum=$((num1 + num2))

# Print the result to standard output
echo "The sum of $num1 and $num2 is $sum"