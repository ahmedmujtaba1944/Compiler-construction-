Here is the formatted content for your README file on GitHub:

---

# Custom Programming Language

## Variables
- Variables are not case-sensitive.
- Variables must start with the `$` symbol or an underscore (`_`).
- A variable can only contain alphanumeric characters (`a-z`, `A-Z`, `0-9`).
- The first character of a variable can only be `$`.
- Keywords are not allowed to be used as variables.
- No special characters such as semi-colons (`;`), periods (`.`), whitespaces (` `), slashes (`-`), or commas (`,`) are permitted in or as variables.
- It is preferred to use camelCase if the variable name has more than one word.

## Datatypes
We use the following datatypes in our language:
- `integer`: for positive or negative integers.
- `line`: for string values.
- `decimal`: for floating-point values.
- `single`: for a single character.
- `flag`: for Boolean values.

## Declaration and Initialization
- **Declaration Syntax**: `datatype variableName!`
- **Initialization Syntax**: `datatype variableName = value!`

### Examples
- `integer $my_age = 22!`
- `line $uni_name = “Riphah International University”!`
- `decimal $pi = 3.14!`
- `single $a = ‘a’!`
- `flag $pass = yes!`
- `flag $pass = no!`

Each line must be terminated with `!`.

## Conditional Statements
We use the following for conditional statements:
- `iff`: for `if` statement
- `otherwise`: for `else-if` statement
- `then`: for `else` statement

## Iterative Statements (Loop, Recursion, Jump, Continue)
- **rotate** (while loop):
  ``` 
  rotate (relational expression){      
  @ body of rotate 
  }
  ```
- **repeat** (for loop):
  ```
  repeat (startValue! endValue! Inc/dec){ 
  @ body of repeat
  }
  ```

### Examples
```
integer $i = 0!
rotate ($i <= 10) {
    show($i)!
    $i++!
}

repeat (integer $i = 1! $i > 20! $i++) {
    show($i)!
}
```

## Functions
- **Declaration**
  ```
  blank $displayAge()!
  ```

- **Definition**
  ```
  blank $displayAge() {
      integer $myAge = 22!
      show($myAge)!
  }
  ```

- **Calling**
  ```
  $displayAge()!
  ```

## Keywords
- `integer`, `decimal`, `line`, `flag`, `single`: Datatype keywords.
- `iff`, `otherwise`, `then`: Conditional statement keywords.
- `repeat`, `rotate`, `stop`, `resume`: Loop keywords.
- `!`: Statement terminator.
- `@`: for comment.
- `blank`: for void functions.

---

