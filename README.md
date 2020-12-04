<!-- mode: markdown -->

# ansiesc-colors

Some functions and examples to use ANSI escape codes to color the output in Python

Some functions and examples to use ANSI escape codes to color the output in Python

this is  a simple package  (and obviously not  perfect) that implements the  use of ANSI  Escape Codes to  print colored
strings to the console

<!-- [Github-flavored Markdown](https://guides.github.com/features/mastering-markdown/) -->

After installing the  package in the ways, I  think well known, the imports  sufficient to perform a first  test are the
following:

```python
from ansiesc_colors import co
from ansiesc_colors import cf
from ansiesc_colors import printColorTable
from ansiesc_colors import stripAnsiEscSeq
```

`printColorTable()` print the color table and some test lines

`co(str, *args)` it is a single instance (singleton) that allows you to color single strings, see the example below

`cf(str="")` similar  to 'co'  but generate an  instance with  an interface  of type 'fluent'  and allows  formatting of
multiple strings, see examples below

`stripAnsiEscSeq(str)` it is simply used to remove ANSI sequences from a string

## examples

```python
printColorTable()
```

```python
cf().test()
```

```python
print(co("---", co.normal))
print(co(" blue ", co.normal, co.blue, co, co.normal))
print(co(" blue and bold ", co.normal, co.blue, co.bold, co, co.normal))
print(co(" blue and bold and reverse ", co.normal, co.blue, co.bold, co.reverse, co, co.normal))
print(co(" white on blue ", co.normal, co.c255, co.b12, co, co.normal))
print(co(" white on blue and bold ", co.normal, co.c255, co.b12, co.bold, co, co.normal))
print(co(" white on blue and italic ", co.normal, co.c255, co.b12, co.italic, co, co.normal))
```

```python
print(co("---", co.normal))
print(cf().a(" blue ").h(co.normal).h(co.blue).t(co.normal).r())
print(cf().a(" blue and bold ").h(co.normal).h(co.blue).h(co.bold).t(co.normal).r())
print(cf().a(" blue and bold and reverse ").h(co.normal).h(co.blue).h(co.bold).h(co.reverse).t(co.normal).r())
print(cf().a(" white on blue ").h(co.normal).h(co.c255).h(co.b12).t(co.normal).r())
print(cf().a(" white on blue and bold ").h(co.normal).h(co.c255).h(co.b12).h(co.bold).t(co.normal).r())
print(cf().a(" white on blue and italic ").h(co.normal).h(co.c255).h(co.b12).h(co.italic).t(co.normal).r())
```

```python
coloredString = (cf(" " * 4).h(co.normal).a("test strip ANSI Escape Sequences ... ")
                 .a("test in bold blue ......").h(co.normal).h(co.blue).h(co.bold).t(co.normal)
                 .a(" and in reverse bold red ....").h(co.normal).h(co.red).h(co.bold).h(co.reverse).t(co.normal)
                 .r())
print(coloredString)
print(stripAnsiEscSeq(coloredString))
```

the end ... :)
