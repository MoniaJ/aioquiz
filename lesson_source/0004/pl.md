Logika Pythona
==============

Sprawdzanie warunków
--------------------

Porównanie: prawda, czy fałsz?
------------------------------

Porozmawiajmy o porównaniach. Spójrzmy, jak się one zachowują podczas
krótkiej lekcji matematyki:

	>>>  2 > 1 
	True 
	>>> 1 == 2 
	False 
	>>> 1 == 1.0 
	True 
	>>> 10 >= 10 
	True 
	13 <= 1 + 3
	False 
	>>> -1 != 0 
	True

Rezultatem porównania jest zawsze `True` lub `False`. Porównania mogą
być włączone w bardziej złożone wyrażenia przy użyciu słów and i or:

	>>>  x = 5 
	>>>  x < 10 
	True 
	>>>  2*x > x 
	True 
	>>>  (x < 10) and (2*x > x) 
	True 
	>>>  (x != 5) and (x != 4)
	False 
	>>>  (x != 5) and (x != 4) or (x == 5) 
	True

Python Love - ćwiczenie
-----------------------

Porozmawiajmy o miłości z naszym cudownym wężem. Napiszcie to w swoim 
interpreterze.

	>>>  import this 
	>>>  love = this 
	>>>  love is this 
	>>>  love is not True or False 
	>>>  love is love

W Pytonie możemy porównywać używając kilku różnych operatorów:

-   ==
-   is
-   !=
-   not
-   \>=
-   <=
-   in

i łączyć wyrażenia za pomocą:

-   and
-   or

Czy is to to samo co == ?
-------------------------

Przeprowadźmy kilka testów, by sprawdzić, czy 'is' to to samo co '==':

    :::python3
    >>> 1000 is 10**3 
    >>> 1000 == 10**3
    >>> "a" is "a" 
    >>> "aa" is "a" * 2 
    >>> x = "a" 
    >>> "aa" is x * 2 
    >>> "aa" == x * 2
    >>> [1, 2] == [1, 2]
    >>> [1, 2] is [1, 2]

Wniosek: 'is' zwróci True, jeśli dwie zmienne wskazują na ten sam obiekt,
a '==' zwróci True jesli obiekty, do których odnoszą się zmienne są równe.

BMI: Gruby, czy nie? Niechaj Python zadecyduje za Ciebie
--------------------------------------------------------

Przejdźmy do naszego kolejnego problemu. Chcemy aby program wydrukował
właściwą klasyfikację dla obliczonego BMI, przy użyciu poniższej tabeli:

  BMI              Klasyfikacja
  -------------- ----------------
  < 18,5         niedowaga
  18,5 – 24,99   prawidłowa waga
  25,0 – 29,99   nadwaga
  ≥ 30,0         otyłość

Musimy użyć "komendy warunkowej' if. Wykona ona dalszy ciąg programu
zależnie od podanego warunku:

Ćwiczenie - prosty pythonowy kalkulator
---------------------------------------

Napiszcie skrypt stanowiący prosty kalkulator, który pobierze dwie
liczby oraz znak operacji matematycznej (+, -, \*, /) i wyświetli
przyjemny string, który pokaże całe równanie oraz rozwiązanie. 
Pamiętajcie: string + string = nowy string :-)
Przykład:

	>>>  'Wprowadź pierwszą liczbę' 
	10 
	>>>  "Wprowadź znak operacji matematycznej (+, -, \*, /)" 
	+ 
	>>> 'Wprowadź drugą liczbę'
	5
	'10 + 5 = 15'

Indentacja
----------

Rzecz, na którą powinniście zwrócić uwagę w kodzie jest indentacja.
Another thing you should pay attention to is the indentation in the
code. Open the interactive mode and enter a simple condition such as:

    >>> if 2 > 1:
    ...

So far nothing has happened, as evidenced by dots `...` instead of a
prompt `>>>`, which we have seen so far. Python expects us to give
further instructions that are supposed to be executed if the condition
`2 > 1` turns out to be true. Let’s try to make Python print "OK":

    :::python3
    >>> if 2 > 1:
    ... print("OK")
      File "<stdin>", line 2
        print("OK")
            ^
    IndentationError: expected an indented block

Unfortunately, we did not succeed. Python needs to know whether the
instruction we have written is a continuation of if or it is the next
instruction not covered by the condition. To this purpose, we need to
indent our code:

	>>>  if 2 > 1: ... print("OK") ... OK

All you need is one space or `TAB`. However, all the lines that are
supposed to be executed one after another should be indented the same
way:

    :::python3
    >>> if -1 < 0:
    ...  print("A")
    ...   print("B")
      File "<stdin>", line 3
        print("B")
        ^
    IndentationError: unexpected indent

    >>> if -1 < 0:
    ...     print("A")
    ...   print("B")
      File "<stdin>", line 3
        print("B")
                ^
    IndentationError: unindent does not match any outer indentation level

    >>> if -1 < 0:
    ...   print("A")
    ...   print("B")
    ...
    A
    B

To avoid chaos, most Python programmers use four spaces for each level
of indentation. We will do the same:

	>>>  if 2 > 1: ... if 3 > 2: ... print("OK") ... else:
	>>>  ... print("FAIL") ... print("DONE") OK DONE

What if not?
------------

Actually, we could write our program just by using if :

    :::python3
    if bmi < 18.5:
        print("underweight")
    if bmi >= 18.5:
        if bmi < 25.0:
            print("normal weight")
    if bmi >= 25.0:
        print("overweight")

We can also use else and elif to avoid repeating similar conditions and
increase readability. In more complex programs it may not be obvious
from the beginning that a certain condition is the opposite of the
previous one.

Using else , we have the guarantee that the given instructions will be
executed only if the instructions printed under if haven’t been
executed:

    :::python3
    if bmi < 18.5:
        print("underweight")
    else:
        # If your program executes this instruction,
        # for sure bmi >= 18.5 !
        if bmi < 25.0:
            print("normal weight")
        else:
            # now for sure bmi >= 25.0, we don’t have to
            # check it
            print("overweight")

Pay particular attention to the indentations. Every use of else, will
cause an increased indentation of our code. It is very annoying when you
have to check a few or a dozen or so conditions which exclude one
another . Therefore the authors of Python added a little 'improvement'
in the form of elif, instruction, which allows you to check another
condition immediately:

    :::python3
    if n < 1:
        print("one")
    elif n < 2:
        # if it wasn’t n < 1, and now it is n < 2
        print("two")
    elif n < 3:
        # ,if none of the previous condition was true.
        # n >= 1 i n>= 2, ale n < 3
        print("three")
    else:
        # trolls can count only to three
        print("more")

Exercised data:
===============


| BMI          | WOMEN         |
|--------------|---------------|
| < 17,5       | underweight   |
| 17,5 – 22,49 | normal weight |
| 22,5 – 27,49 | overweight    |
| ≥ 27,5       | obesity    |


| BMI          | MEN           |
|--------------|---------------|
| < 19.99      | underweight   |
| 20 – 24,99   | normal weight |
| 25,0 – 29,99 | overweight    |
| ≥ 30,0       | obesity       |

Summary
=======

We now know some basic python logic, and we can use it.

