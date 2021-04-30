# Unimatrix Zero

This is a simple script to generate lottery wheels, both full and abbreviated.

It supports all type of wheels, with a maximum variety of combinations.

## Examples

*Standard wheels*
* 10 6 6 5 - range of 10 numbers, line length of 6, 6 picked numbers, 5 numbers guaranteed
* 10 6 6 4 - range of 20 numbers, line length of 6, 6 picked numbers, 4 numbers guaranteed

*Slightly more complicated wheels*
* 10 7 6 5 - range of 10 numbers, line length of 7, 6 picked numbers, 5 numbers guaranteed
* 10 5 6 5 - range of 10 numbers, line length of 5, 6 picked numbers, 5 numbers guaranteed

*Exotic wheels*
* 10 6 4 4 - range of 10 numbers, line length of 6, 4 picked numbers, 4 numbers guaranteed
* 10 6 8 6 - range of 10 numbers, line length of 6, 8 picked numbers, 6 numbers guaranteed

It also supports extremely large ranges - picked numbers can be as big as you need, but anything over 40 numbers will likely take a long time and will slow your computer down.

## Usage

python generator.py [range] [line length] [picked] [guarantee]
Example: python generator.py 10 6 6 5

## Requirements
Python3 (version 3.9.1 known to work)
