[![CI](https://github.com/meeshkan/introduction-to-property-based-testing/workflows/CI/badge.svg)](https://github.com/meeshkan/introduction-to-property-based-testing/actions?query=branch%3Amaster)

# Introduction to property-based testing
This repository contains this README article introducing property-based testing with code samples in python.

## Example based testing
Normally software testing is done through **example based testing**. A human writes one or several sample inputs to the function or system under test, runs the function or system, and then asserts on the result of that.

Let's start with a toy example - a python `bubble_sort` function to sort a list of numbers (note: this is a toy example, use [list.sort()](https://docs.python.org/3/library/stdtypes.html#list.sort) in production):

```python
def bubble_sort(nums):
    result = nums.copy()
    swapped = True
    while swapped:
        swapped = False
        for i in range(len(result) - 1):
            if result[i] > result[i + 1]:
                result[i], result[i + 1] = result[i + 1], result[i]
                swapped = True
    return result

def test_bubble_sort_example():
    # Test using two manually worked out examples:
    assert [1, 2, 3, 4, 5] == bubble_sort([5, 3, 1, 4, 2])
    assert [1, 1, 3, 3, 5] == bubble_sort([1, 3, 1, 3, 5])
```

## Property based testing
While great and simple, testing examples does just that: test examples that we have come up with! What if we want to test hundreds of test cases, possibly ones we could never dream of coming up with ourselves? How could we have saved the student records in the below example?

![Bobby tables](https://imgs.xkcd.com/comics/exploits_of_a_mom.png)

**Property based testing** is a different approach here to help with that. You yourself don't generate the exact input - that is done by by a computer automatically. What you as a developer do is:

- You specify what input to generate.
- You assert on guarantees (here after called **properties**) which are true regardless of exact input.

Let's see an example using the [Hypothesis](https://hypothesis.readthedocs.io/en/latest/) test library:

```python
import hypothesis.strategies as some

# Guide the framework in what input we need:
@given(input_list=some.lists(some.integers()))
def test_bubble_sort_properties(input_list):
    input_list_copy = input_list.copy()
    sorted_list = bubble_sort(input_list)

    # Regardless of input, sorting should never change the original list:
    assert input_list_copy == input_list

    # Regardless of input, sorting should never change the size:
    assert len(sorted_list) == len(input_list)

    # Regardless of input, sorting should never change the set of distinct elements:
    assert set(sorted_list) == set(input_list)

    # Regardless of input, each element in the sorted list should be
    # lower or equal to the value that comes after it:
    for i in range(len(sorted_list) - 1):
        assert sorted_list[i] <= sorted_list[i + 1]
```

Here we specify that we want lists of integers as input (using the [@given](https://hypothesis.readthedocs.io/en/latest/details.html#hypothesis.given) function decorator) and **asserts on properties that are true regardless of the exact input**.

If we peek on what input is generated by adding a `print(input_list)` statement, we can see 100 different generated input values (the number of runs and specifics can be configured, more on that later on):

```
[]
[92]
[66, 24, -25219, 94, -28953, 31131]
[-16316, -367479896]
[-7336253322929551029, -7336253322929551029, 27974, -24308, -64]
...
```

While different, a property based test shares a lot with how an example based test is written.

| Example based                          | Property based                              |
| -------------------------------------- | ------------------------------------------- |
| 1. Set up some data                    | 1. For all data matching some specification |
| 2. Perform some operations on the data | 2. Perform some operations on the data      |
| 3. Assert something about the result   | 3. Assert something about the result        |


## Property: Unexpected exceptions should never be thrown
One thing we got tested "for free" in the above `test_bubble_sort_properties` function, was that the code did not throw any exception. This property, that the code does not throw any exception (or more generally, only expected and documented exceptions), can be a convenient one to test, especially if the code has a lot of internal assertions.

Let's test that the property that the [json.loads](https://docs.python.org/3/library/json.html#json.loads) function in the python standard library never throws any exception other than `json.JSONDecodeError` regardless of input:

```python
@given(some.text())
@example("[")
def test_json_loads(input_string):
    try:
        json.loads(input_string)
    except json.JSONDecodeError:
        return
```

Running the test passes, so what we believe held up under test! Note here that we have used a [@example](https://hypothesis.readthedocs.io/en/latest/reproducing.html#hypothesis.example) decorator to make sure that a specific value is always tested - it's easy to mix a specific example into a property-based test.

## Property: Symmetry, such as decoding an encoding value always brings back original
Symmetry of certain operations, such the property that decoding an encoded value always brings back the original value, can sometimes be used. Let's apply it to [base32-crockford](https://github.com/jbittel/base32-crockford), a python library for the [Base 32](https://www.crockford.com/base32.html) 

```python
@given(some.integers(min_value=0))
def test_base32_crockford(input_int):
      assert base32_crockford.decode(base32_crockford.encode(input_int)) == input_int
```

Since this decoding scheme only works for non-negative integers, we specify to the **generator** of input data to only generate integers with a minium value of zero: `some.integers(min_value=0)`.

## Comparing with a correct value obtained through an inefficient or otherwise naive way
Sometimes we can get the desired solution through a way that is not acceptable to use in production code: That might be due to execution time being to slow, memory consumption too high or requiring special dependencies that are not acceptable to install in production.

For an example, consider counting the number of bits in an (arbitrary sized) integer, where we have an optimized solution from the [pygmp2](https://gmpy2.readthedocs.io/en/latest/) library, which we compare with a slow solution that converts the integer to a binary string and counting the occurences of the string "1" inside it, using the [bin](https://docs.python.org/3/library/functions.html#bin) function in the standard python library:

```python
def count_bits_slow(input_int):
    return bin(input_int).count("1")

@pytest.mark.skip(reason="Avoid forcing to install gmpy2")
@given(some.integers(min_value=0))
def test_gmpy2_popcount(input_int):
    assert count_bits_slow(input_int) == gmpy2.popcount(input_int)
```


## Why use property based testing?
- A computer can generate a lot more input than a human can.
- It forces you to reason and express at a higher level than individual examples. 

## Why use example based testing?
- Test cases using specific examples may in many cases be more readable.
- Regression tests of specific bugs to prevent them from ever happening again.

## Vocabulary
- **Example-based testing** The traditional way of writing tests using examples.
- **Property-based testing** 
- **Preconditions**
- **Postconditions**
- **Generators**: The thing that generates input data, such as `some.lists(some.integers())`.
- [...]


## Libraries
- [QuickCheck](https://hackage.haskell.org/package/QuickCheck): Haskell
- [fast-check](https://github.com/dubzzz/fast-check): TypeScript
- [Hypothesis](https://hypothesis.readthedocs.io/en/latest/): Python (covered in this article)
- Includes NumPy and Pandas tools!
- [PropEr](https://proper-testing.github.io/): Erlang
- [PropCheck](https://github.com/alfert/propcheck): Elixir
- [FsCheck](https://fscheck.github.io/FsCheck/): .NET


## Meta: Running the tests
Execute `make` to run the tests (it will setup a `venv` folder and install dependencies there). It will also format the code using [black](https://black.readthedocs.io/en/stable/) and [isort](https://timothycrosley.github.io/isort/) automatically.

# Meta: Where to announce (and possibly ask for feedback):
- https://hypothesis.readthedocs.io/en/latest/community.html mentions their IRC channel and mailing list.
- https://reddit.com/r/programming and https://reddit.com/r/python perhaps?
- https://twitter.com/meeshkanml
- TODO



# Meta: Various resources
- https://hackage.haskell.org/package/QuickCheck
  - Early (1999) Haskell library.
  - https://jqwik.net/property-based-testing.html mentions it as "Quickcheck is the original tool for writing property tests."
  - Also https://en.wikipedia.org/wiki/QuickCheck: "QuickCheck is a software library, specifically a combinator library, originally written in the programming language Haskell, designed to assist in software testing by generating test cases for test suites. It is compatible with the compiler, Glasgow Haskell Compiler (GHC) and the interpreter, Haskell User's Gofer System (Hugs). It is free and open-source software released under a BSD-style license. In QuickCheck, assertions are written about logical properties that a function should fulfill. Then QuickCheck attempts to generate a test case that falsifies such assertions. Once such a test case is found, QuickCheck tries to reduce it to a minimal failing subset by removing or simplifying input data that are unneeded to make the test fail. The project began in 1999. Besides being used to test regular programs, QuickCheck is also useful for building up a functional specification, for documenting what functions should be doing, and for testing compiler implementations."
- https://hypothesis.works/
  - "This sort of testing is often called 'property-based testing', and the most widely known implementation of the concept is the Haskell library QuickCheck, but Hypothesis differs significantly from QuickCheck and is designed to fit idiomatically and easily into existing styles of testing that you are used to, with absolutely no familiarity with Haskell or functional programming needed."
  - https://hypothesis.works/articles/what-is-property-based-testing/
- https://github.com/ksaaskil/introduction-to-property-based-testing
- https://medium.com/criteo-labs/introduction-to-property-based-testing-f5236229d237
- https://jqwik.net/property-based-testing.html
- https://blog.ssanj.net/posts/2016-06-26-property-based-testing-patterns.html
  - 
