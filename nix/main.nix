let
  n = 100;

  divisibleBy = a: b: (a / b * b) == a;

  fizzBuzzOne =
    i:
    if divisibleBy i 15 then
      "FizzBuzz"
    else if divisibleBy i 5 then
      "Buzz"
    else if divisibleBy i 3 then
      "Fizz"
    else
      toString i;

  numbers = builtins.genList (idx: idx + 1) n;

in
map fizzBuzzOne numbers
