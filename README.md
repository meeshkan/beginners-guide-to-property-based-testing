[![CI](https://github.com/meeshkan/introduction-to-property-based-testing/workflows/CI/badge.svg)](https://github.com/meeshkan/introduction-to-property-based-testing/actions?query=branch%3Amaster)

# Introduction to property-based testing
This repository contains this README article introducing property-based testing with code samples in python.




# What is property based testing?
Normally software testing is done through **example-based testing**. A human writes one or several sample inputs to the function or system under test, runs the function or system, and then asserts on the result of that.

TODO: Mention that it's silly and unrealistic, but we'll come to more realistic uses cases later.

```python
def concatenate(a, b):
    return a + " " + b

def test_concatenate():
    assert "hello world" == concatenate("hello", "world")
    assert "1 2" == concatenate("1", "2")
```

**Property based testing** is using a different approach. You yourself don't write the exact input - a testing framework does that for you. What you as a developer do is:

- You guide test testing framework in what kind of input you want to use.
  - This is in order to not get any random input. TODO: Clarify
- You assert on properties which are true regardless of exact input.

Let's see an example:

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

Here [...]

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
