[![CI](https://github.com/meeshkan/introduction-to-property-based-testing/workflows/CI/badge.svg)](https://github.com/meeshkan/introduction-to-property-based-testing/actions?query=branch%3Amaster)

# Introduction to property-based testing
This repository contains this README article introducing property-based testing with code samples in python.

# Example based testing
Normally software testing is done through **example based testing**. A human writes one or several sample inputs to the function or system under test, runs the function or system, and then asserts on the result of that.

Let's start with a toy example - a python `bubble_sort` function to sort a list of numbers (note: this is a toy example, use [list.sort()](https://docs.python.org/3/library/stdtypes.html#list.sort) in production):

```python
def bubble_sort(nums):
    swapped = True
    while swapped:
        swapped = False
        for i in range(len(nums) - 1):
            if nums[i] > nums[i + 1]:
                nums[i], nums[i + 1] = nums[i + 1], nums[i]
                swapped = True

def test_bubble_sort_example():
    # Test using two manually worked out examples:
    assert [1, 2, 3, 4, 5] == bubble_sort([5, 3, 1, 4, 2])
    assert [1, 1, 3, 3, 5] == bubble_sort([1, 3, 1, 3, 5])
```

# Property based testing
While great and simple, testing examples does just that: test examples that we have come up with! What if we want to test hundreds of test cases, possibly ones we could never dream of coming up with ourselves? 

**Property based testing** is a different approach here to help with that. You yourself don't generate the exact input - that is done by by a computer automatically. What you as a developer do is:

- You specify what input to generate.
- You assert on properties which are true regardless of exact input.

Let's see an example using the [Hypothesis](https://hypothesis.readthedocs.io/en/latest/) test library

```python
import hypothesis.strategies as some

# Guide the framework in what input we need:
@given(some.tuples(some.text(), some.text()))
def test_concatenate(input_strings):
    result = concatenate(input_strings[0], input_strings[1])
    
    # Assert on postconditions:
    assert result.startswith(j[0])
    assert result.endswith(input_strings[1])
```

Here we specify that we want two strings (currently unspecified, but we could for example specify that we want them to be of a specific length, or contain specific characters), and **asserts on properties that are true regardless of the exact input**.

While different, a property based test shares a lot with how an example based test is written.

| Example based                          | Property based                              |
| -------------------------------------- | ------------------------------------------- |
| 1. Set up some data                    | 1. For all data matching some specification |
| 2. Perform some operations on the data | 2. Perform some operations on the data      |
| 3. Assert something about the result   | 3. Assert something about the result        |

# Why use property based testing?
- A computer can generate a lot more input than a human can.
- It forces you to reason and express at a higher level than individual examples. 

# Why use example based testing?
- Specific test 

# Vocabulary
- **Example-based testing** The traditional way of writing tests using examples.
- **Property-based testing** 
- **Preconditions**
- **Postconditions**
- [...]





# Running the tests
Execute `make` to run the tests (it will setup a `venv` folder and install dependencies there). It will also format the code using [black](https://black.readthedocs.io/en/stable/) and [isort](https://timothycrosley.github.io/isort/) automatically.

# Resources
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
