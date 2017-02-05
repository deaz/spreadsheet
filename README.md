# Spreadsheet

Command line application for calculating simple Excel-like spreadsheets.

## Requirements

- Python 3.6 installed

## How to run

Assuming your current directory is project directory:

`./bin/spreadsheet`

## Error Messages

- `#ERROR!` - syntax error in cell
- `#VALUE!` - wrong argument for operation
(for example: division by cell with string value)
- `#REF!` - circular dependency in cell expression
- `#DIV/0!` - division by zero
- `#NONEXIST!` - referenced cell is not exists in current spreadsheet
